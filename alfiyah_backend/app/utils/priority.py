import pickle
import os
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Model storage path
MODEL_PATH = "priority_model.pkl"

# Global variables for the loaded model components
loaded_model = None
loaded_preprocessor = None
cluster_to_priority_map = {}

def _generate_synthetic_data(num_samples=1000):
    """Generates synthetic data for training the K-means model."""
    data = {
        'diff_days': np.random.randint(0, 90, num_samples), # 0 to 90 days out
        'status': np.random.choice(['pending', 'dp', 'paid'], num_samples),
        'price_locked': np.random.randint(100000, 5000000, num_samples), # 100k to 5M
        'jumlah_client': np.random.randint(1, 5, num_samples) # 1 to 4 clients
    }
    return data

def train_and_save_model():
    """Trains the K-means model and saves it along with the preprocessor."""
    print("Training K-means model for booking priority...")
    synthetic_data = _generate_synthetic_data()
    df = pd.DataFrame(synthetic_data)

    # Define preprocessing steps
    numeric_features = ['diff_days', 'price_locked', 'jumlah_client']
    categorical_features = ['status']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough' # Keep other columns if any, though not strictly needed here
    )

    # Create a pipeline with preprocessor and KMeans
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('kmeans', KMeans(n_clusters=3, random_state=42, n_init=10))])

    pipeline.fit(df)

    kmeans_model = pipeline.named_steps['kmeans']
    preprocessor_model = pipeline.named_steps['preprocessor']
    
    # Get centroids in the transformed space
    centroids_transformed = kmeans_model.cluster_centers_

    # Get the StandardScaler and OneHotEncoder components
    scaler = preprocessor_model.named_transformers_['num']
    onehot_encoder = preprocessor_model.named_transformers_['cat']

    # Determine the number of features created by the one-hot encoder
    num_onehot_features = len(onehot_encoder.get_feature_names_out(categorical_features))
    num_numeric_features = len(numeric_features)

    # To score clusters, we'll evaluate their centroids
    # Extract only the numeric parts of the centroids and inverse transform them
    numeric_centroids_transformed = centroids_transformed[:, :num_numeric_features]
    numeric_centroids_original = scaler.inverse_transform(numeric_centroids_transformed)

    # Calculate a composite score for each cluster based on its original-scale numeric features
    # Lower diff_days is better (higher urgency), higher price_locked and jumlah_client are better
    cluster_scores = []
    for i, centroid_numeric in enumerate(numeric_centroids_original):
        diff_days, price_locked, jumlah_client = centroid_numeric
        # Adjust weights as needed
        score = (price_locked * 0.5) - (diff_days * 1000) + (jumlah_client * 50000) 
        cluster_scores.append({'cluster_id': i, 'score': score})

    # Sort clusters by their score in descending order
    cluster_scores.sort(key=lambda x: x['score'], reverse=True)

    # Assign priority segments based on sorted scores
    global cluster_to_priority_map
    cluster_to_priority_map = {}
    
    # Assuming n_clusters=3 for 'high', 'medium', 'low'
    priority_labels = ['high', 'medium', 'low']
    urgency_labels = ['urgent', 'soon', 'upcoming']
    monetary_labels = ['vip', 'premium', 'regular']
    priority_scores = [90, 60, 20]

    for i, cluster_info in enumerate(cluster_scores):
        cluster_id = cluster_info['cluster_id']
        if i < len(priority_labels):
            cluster_to_priority_map[cluster_id] = {
                "priority_score": priority_scores[i],
                "priority_segment": priority_labels[i],
                "urgency_level": urgency_labels[i],
                "monetary_level": monetary_labels[i],
            }
        else:
            # Fallback for more clusters than defined labels
            cluster_to_priority_map[cluster_id] = {
                "priority_score": 0, "priority_segment": "low", "urgency_level": "upcoming", "monetary_level": "regular"
            }
    
    # Save the pipeline and cluster_to_priority_map
    try:
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump((pipeline, cluster_to_priority_map), f)
        print(f"K-means model and cluster map saved to {MODEL_PATH}")
    except Exception as e:
        print(f"Error saving model to disk: {e}")


def _load_model():
    """Loads the trained model and preprocessor from MODEL_PATH."""
    global loaded_model, loaded_preprocessor, cluster_to_priority_map
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                pipeline_loaded, cluster_map_loaded = pickle.load(f)
            loaded_model = pipeline_loaded.named_steps['kmeans']
            loaded_preprocessor = pipeline_loaded.named_steps['preprocessor']
            cluster_to_priority_map = cluster_map_loaded
            print("K-means model and cluster map loaded from disk.")
            return True
        except Exception as e:
            print(f"Error loading model from disk: {e}")
            return False
    return False


def calculate_priority(transaction) -> dict:
    """
    Calculates the priority of a booking based on a pre-trained K-means model.
    """
    global loaded_model, loaded_preprocessor, cluster_to_priority_map

    # Try to load the model if not already loaded
    if loaded_model is None or loaded_preprocessor is None or not cluster_to_priority_map:
        if not _load_model(): # Attempt to load from disk
            # If loading fails or model file doesn't exist, train and save
            train_and_save_model()
            # After training, the global variables should be populated.
            # If _load_model() was called and failed, then train_and_save_model() will populate them.
            # If train_and_save_model() was called directly (e.g., from seed_data.py), they are already populated.

    # Prepare data for prediction
    now = datetime.utcnow()
    # Use transaction.tanggal_booking if available, otherwise use now.
    # This is important for both historical data (seeding) and new transactions.
    base_date_for_diff = transaction.tanggal_booking if transaction.tanggal_booking else now
    diff_days = (transaction.tanggal_acara - base_date_for_diff).days

    # Ensure diff_days is not negative
    if diff_days < 0:
        diff_days = 0

    # The model was trained with 'pending', 'dp', 'paid'. Ensure consistency.
    status = transaction.status if transaction.status in ['pending', 'dp', 'paid'] else 'pending'

    data = {
        'diff_days': [diff_days],
        'status': [status],
        'price_locked': [float(transaction.price_locked)], # Convert Decimal to float
        'jumlah_client': [transaction.jumlah_client]
    }
    df = pd.DataFrame(data)

    # Preprocess the new data
    processed_data = loaded_preprocessor.transform(df)

    # Predict the cluster
    cluster_id = loaded_model.predict(processed_data)[0]

    # Retrieve priority details from the map
    return cluster_to_priority_map.get(cluster_id, {
        "priority_score": 0,
        "priority_segment": "low",
        "urgency_level": "upcoming",
        "monetary_level": "regular",
    })

