# Alfiyah Backend API

Ini adalah backend API untuk sistem booking Alfiyah, dibangun menggunakan FastAPI dan SQLAlchemy.

## Requirements
- Python 3.11+ (disarankan)
- MySQL database server. Konfigurasi default diasumsikan berjalan di `localhost` dengan database bernama `alfiyah_db`. Anda bisa menggunakan Laragon atau Docker untuk setup cepat.

## Setup

1.  **Buat dan Aktifkan Virtual Environment:**
    ```bash
    python -m venv .venv
    # Untuk Windows:
    .venv\Scripts\activate
    # Untuk macOS/Linux:
    source .venv/bin/activate
    ```

2.  **Install Dependencies:**
    Instal semua library Python yang dibutuhkan, termasuk FastAPI, SQLAlchemy, scikit-learn, dan pandas.
    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Konfigurasi koneksi database default diatur untuk lingkungan pengembangan lokal (misalnya Laragon):

```
DATABASE_URL="mysql+pymysql://root@localhost/alfiyah_db"
SECRET_KEY="your-secret-key-for-jwt"
```

Untuk menimpa pengaturan default atau untuk lingkungan produksi, atur variabel lingkungan berikut:

```bash
# Contoh untuk Windows (Command Prompt):
set DATABASE_URL=mysql+pymysql://user:password@host:port/your_db_name
set SECRET_KEY=super-secret-jwt-key
set ACCESS_TOKEN_EXPIRE_MINUTES=1440 # Contoh: token berlaku 24 jam

# Contoh untuk macOS/Linux (Bash):
export DATABASE_URL="mysql+pymysql://user:password@host:port/your_db_name"
export SECRET_KEY="super-secret-jwt-key"
export ACCESS_TOKEN_EXPIRE_MINUTES=1440
```
Pastikan `SECRET_KEY` adalah string yang kuat dan unik untuk keamanan JWT Anda.

## Run the API

Untuk menjalankan aplikasi API (dalam mode pengembangan dengan reload otomatis):

```bash
uvicorn app.main:app --reload
```

Anda dapat mengakses dokumentasi API interaktif (Swagger UI) di: `http://localhost:8000/docs`

## Seed Initial Data & Setup

Jalankan script ini **setidaknya satu kali** untuk:
1.  Menerapkan skema database (membuat tabel jika belum ada).
2.  **Menambahkan kolom-kolom baru** (seperti `priority_score`, `phone_number`) ke tabel yang sudah ada jika belum ada.
3.  **Melatih dan menyimpan model K-means** untuk perhitungan prioritas booking (`priority_model.pkl`).
4.  Mengisi data awal untuk `Package` dan `ServiceType`.
5.  Membuat pengguna `admin` dengan kredensial: `email: admin@example.com`, `password: adminpassword`.

```bash
python seed_data.py
```

## Key API Endpoints & Features

Berikut adalah beberapa endpoint dan fitur penting yang tersedia:

*   **`GET /health`**: Memeriksa status kesehatan API.
*   **`/auth` (Authentication)**:
    *   `POST /auth/register`: Mendaftarkan pengguna baru.
    *   `POST /auth/login`: Login pengguna, mengembalikan JWT `access_token`.
    *   `GET /auth/me`: Mengambil informasi profil pengguna yang sedang login.
    *   `PATCH /auth/me`: Memperbarui informasi profil pengguna yang sedang login.
*   **`/services` (Service Management)**:
    *   `GET /services/packages`: Mengambil daftar semua paket layanan.
    *   `POST /services/packages`: Membuat paket layanan baru (Admin).
    *   `POST /services/types`: Membuat jenis layanan baru (Admin).
*   **`/bookings` (Booking Management)**:
    *   `POST /bookings/`: Membuat booking baru dengan perhitungan prioritas otomatis.
    *   `GET /bookings/me`: Mengambil daftar booking pengguna yang sedang login, dengan opsi filter/urut berdasarkan prioritas.
    *   `GET /bookings/`: Mengambil semua daftar booking (Admin), dengan opsi filter/urut berdasarkan prioritas.
    *   `PATCH /bookings/{booking_id}`: Memperbarui status booking, dengan perhitungan ulang prioritas (Admin).
    *   **Fitur Perhitungan Prioritas Booking**: Setiap booking kini memiliki `priority_score`, `priority_segment`, `urgency_level`, dan `monetary_level` yang dihitung menggunakan model K-means.
*   **`/segments` (Customer Segmentation)**:
    *   `GET /segments/`: Mengambil data segmentasi pelanggan berdasarkan analisis RFM dan clustering K-means, mengembalikan segmen seperti "Loyal", "Aktif", "Potensial", "Pasif" (Admin).

---