# Alfiyah Booking API Documentation

This document outlines the available API endpoints for the Alfiyah Booking system.

## Base URL
The base URL for all API endpoints is typically `http://localhost:8000` or your deployed domain.

---

## Health Check

### `GET /health`

Checks the health status of the API.

- **Description:** Returns a simple status message to indicate the API is running.
- **Authentication:** None required.
- **Response:**
  ```json
  {
    "status": "ok"
  }
  ```

---

## Authentication Endpoints (`/auth`)

These endpoints handle user registration and login.

### `POST /auth/register`

Registers a new user in the system.

- **Description:** Creates a new user account with the provided details.
- **Authentication:** None required.
  **Request Body (application/json):**
  ```json
  {
    "name": "string",
    "email": "user@example.com",
    "password": "string",
    "address": "string | null",
    "phone_number": "string | null"
  }
  ```
  **Schema: `UserCreate`**
  - `name` (string, max_length=100, required)
  - `email` (EmailStr, required)
  - `password` (string, min_length=6, required)
  - `address` (string | null, max_length=255, optional)
  - `phone_number` (string | null, max_length=20, optional)
- **Response (201 Created) (application/json):**
  ```json
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "address": "string | null",
    "phone_number": "string | null",
    "role": "customer"
  }
  ```
  **Schema: `UserRead`**
  - `id` (integer)
  - `name` (string)
  - `email` (EmailStr)
  - `address` (string | null)
  - `phone_number` (string | null)
  - `role` (string)
- **Error Responses:**
  - `400 Bad Request`: If email is already registered.

### `POST /auth/login`

Authenticates a user and returns an access token.

- **Description:** Verifies user credentials and issues a JWT access token for subsequent authenticated requests.
- **Authentication:** None required.
- **Request Body (application/x-www-form-urlencoded or application/json for Swagger UI):**
  ```
  username: user@example.com
  password: string
  ```
  *Note: When using a tool like `curl` or `Postman`, use `application/x-www-form-urlencoded` with `username` and `password` as form fields. For Swagger UI, it often accepts `application/json` with `username` and `password` keys.*
- **Response (application/json):**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
  **Schema: `Token`**
  - `access_token` (string)
  - `token_type` (string, default="bearer")
- **Error Responses:**
  - `401 Unauthorized`: If invalid credentials are provided.

### `GET /auth/me`

Retrieves information about the current authenticated user.

- **Description:** Returns the details of the user associated with the provided JWT access token.
- **Authentication:** User token required (`Bearer <access_token>`).
- **Response (application/json):**
  ```json
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "address": "string | null",
    "phone_number": "string | null",
    "role": "customer"
  }
  ```
  **Schema: `UserRead`**
  - `id` (integer)
  - `name` (string)
  - `email` (EmailStr)
  - `address` (string | null)
  - `phone_number` (string | null)
  - `role` (string)
- **Error Responses:**
  - `401 Unauthorized`: If no token or an invalid token is provided.

### `PATCH /auth/me`

Updates information for the current authenticated user.

- **Description:** Allows an authenticated user to update their own profile information. Fields that are not provided in the request body will not be updated.
- **Authentication:** User token required (`Bearer <access_token>`).
- **Request Body (application/json):**
  ```json
  {
    "name": "string | null",
    "email": "user@example.com | null",
    "address": "string | null",
    "phone_number": "string | null"
  }
  ```
  **Schema: `UserUpdate`**
  - `name` (string | null, max_length=100, optional)
  - `email` (EmailStr | null, optional)
  - `address` (string | null, max_length=255, optional)
  - `phone_number` (string | null, max_length=20, optional)
- **Response (application/json):**
  ```json
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "address": "string | null",
    "phone_number": "string | null",
    "role": "customer"
  }
  ```
  **Schema: `UserRead`** (returns the updated user object)
- **Error Responses:**
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `400 Bad Request`: If the provided email is already registered by another user.

---

## Service Endpoints (`/services`)

These endpoints manage service packages and service types.

### `GET /services/packages`

Retrieves a list of all available service packages.

- **Description:** Fetches all packages, each including its associated service types.
- **Authentication:** None required.
- **Response (application/json):**
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "description": "string | null",
      "service_types": [
        {
          "id": 0,
          "name": "string",
          "description": "string | null",
          "price": 0.00
        }
      ]
    }
  ]
  ```
  **Schema: `PackageRead`**
  - `id` (integer)
  - `name` (string)
  - `description` (string | null)
  - `service_types` (List[`ServiceTypeRead`])
    - `ServiceTypeRead`:
      - `id` (integer)
      - `name` (string)
      - `description` (string | null)
      - `price` (decimal)

### `POST /services/packages`

Creates a new service package.

- **Description:** Adds a new package to the system. Requires administrator privileges.
- **Authentication:** Admin token required (`Bearer <access_token>`).
- **Request Body (application/json):**
  ```json
  {
    "name": "string",
    "description": "string | null"
  }
  ```
  **Schema: `PackageCreate`**
  - `name` (string, max_length=120, required)
  - `description` (string | null, optional)
- **Response (201 Created) (application/json):**
  ```json
  {
    "id": 0,
    "name": "string",
    "description": "string | null",
    "service_types": []
  }
  ```
  **Schema: `PackageRead`** (as above, but `service_types` list will be empty on creation)
- **Error Responses:**
  - `400 Bad Request`: If a package with the same name already exists.
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `403 Forbidden`: If the authenticated user is not an admin.

### `POST /services/types`

Creates a new service type within an existing package.

- **Description:** Adds a new service type (e.g., specific photography package) linked to a package. Requires administrator privileges.
- **Authentication:** Admin token required (`Bearer <access_token>`).
- **Request Body (application/json):**
  ```json
  {
    "package_id": 0,
    "name": "string",
    "description": "string | null",
    "price": 0.00
  }
  ```
  **Schema: `ServiceTypeCreate`**
  - `package_id` (integer, required)
  - `name` (string, max_length=120, required)
  - `description` (string | null, optional)
  - `price` (decimal, required)
- **Response (201 Created) (application/json):**
  ```json
  {
    "id": 0,
    "name": "string",
    "description": "string | null",
    "service_types": [
      {
        "id": 0,
        "name": "string",
        "description": "string | null",
        "price": 0.00
      }
    ]
  }
  ```
  **Schema: `PackageRead`** (returns the updated package including the new service type)
- **Error Responses:**
  - `404 Not Found`: If the `package_id` does not correspond to an existing package.
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `403 Forbidden`: If the authenticated user is not an admin.

---

## Booking Endpoints (`/bookings`)

These endpoints handle user bookings and admin management of bookings.

### `POST /bookings/`

Creates a new booking.

- **Description:** Allows an authenticated user to create a new booking for a specific service type. The system automatically calculates and assigns priority scores and segments upon creation.
- **Authentication:** User token required (`Bearer <access_token>`).
- **Request Body (application/json):**
  ```json
  {
    "service_type_id": 0,
    "tanggal_acara": "2026-02-11T12:00:00Z",
    "jumlah_client": 0
  }
  ```
  **Schema: `BookingCreate`**
  - `service_type_id` (integer, required)
  - `tanggal_acara` (datetime, required)
  - `jumlah_client` (integer, required)
- **Response (201 Created) (application/json):**
  ```json
  {
    "id": 0,
    "user_id": 0,
    "service_type_id": 0,
    "price_locked": 0.00,
    "status": "pending",
    "tanggal_booking": "2026-02-11T12:00:00Z",
    "tanggal_acara": "2026-02-11T12:00:00Z",
    "jumlah_client": 0,
    "priority_score": 0,
    "priority_segment": "low",
    "urgency_level": "upcoming",
    "monetary_level": "regular",
    "updated_priority_at": "2026-02-11T12:00:00Z",
    "user": {
      "id": 0,
      "name": "string",
      "email": "user@example.com",
      "address": "string | null",
      "phone_number": "string | null",
      "role": "customer"
    }
  }
  ```
  **Schema: `BookingRead`**
  - `id` (integer)
  - `user_id` (integer)
  - `service_type_id` (integer)
  - `price_locked` (decimal)
  - `status` (string, default="pending")
  - `tanggal_booking` (datetime)
  - `tanggal_acara` (datetime)
  - `jumlah_client` (integer)
  - `priority_score` (integer): Calculated priority score for the booking.
  - `priority_segment` (string): Segment (e.g., "low", "medium", "high") based on `priority_score`.
  - `urgency_level` (string, optional): Urgency level (e.g., "urgent", "soon", "upcoming") based on `tanggal_acara`.
  - `monetary_level` (string, optional): Monetary level (e.g., "regular", "premium", "vip") based on `price_locked`.
  - `updated_priority_at` (datetime, optional): Timestamp of the last priority calculation.
  - `user` (object): Nested user details.
    - `id` (integer)
    - `name` (string)
    - `email` (EmailStr)
    - `address` (string | null)
    - `phone_number` (string | null)
    - `role` (string)
- **Error Responses:**
  - `404 Not Found`: If the `service_type_id` does not exist.
  - `401 Unauthorized`: If no token or an invalid token is provided.

- **Response (application/json):**
  ```json
  [
    {
      "id": 0,
      "user_id": 0,
      "service_type_id": 0,
      "price_locked": 0.00,
      "status": "pending",
      "tanggal_booking": "2026-02-11T12:00:00Z",
      "tanggal_acara": "2026-02-11T12:00:00Z",
      "jumlah_client": 0,
      "priority_score": 0,
      "priority_segment": "low",
      "urgency_level": "upcoming",
      "monetary_level": "regular",
      "updated_priority_at": "2026-02-11T12:00:00Z",
      "user": {
        "id": 0,
        "name": "string",
        "email": "user@example.com",
        "address": "string | null",
        "phone_number": "string | null",
        "role": "customer"
      }
    }
  ]
  ```
  **Schema: `BookingRead`** (List of objects, as defined above)
- **Error Responses:**
  - `401 Unauthorized`: If no token or an invalid token is provided.

### `GET /bookings/`

Retrieves a list of all bookings.

- **Description:** Fetches all booking records. Requires administrator privileges. Can be filtered by priority segment and ordered by priority score.
- **Authentication:** Admin token required (`Bearer <access_token>`).
- **Query Parameters:**
  - `order_by` (string, optional): How to order the results. Currently supports `priority_score_desc` for descending priority score.
  - `segment` (string, optional): Filter bookings by priority segment (e.g., `low`, `medium`, `high`).
- **Response (application/json):**
  ```json
  [
    {
      "id": 0,
      "user_id": 0,
      "service_type_id": 0,
      "price_locked": 0.00,
      "status": "pending",
      "tanggal_booking": "2026-02-11T12:00:00Z",
      "tanggal_acara": "2026-02-11T12:00:00Z",
      "jumlah_client": 0,
      "priority_score": 0,
      "priority_segment": "low",
      "urgency_level": "upcoming",
      "monetary_level": "regular",
      "updated_priority_at": "2026-02-11T12:00:00Z",
      "user": {
        "id": 0,
        "name": "string",
        "email": "user@example.com",
        "address": "string | null",
        "phone_number": "string | null",
        "role": "customer"
      }
    }
  ]
  ```
  **Schema: `BookingRead`** (List of objects, as defined above)
- **Error Responses:**
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `403 Forbidden`: If the authenticated user is not an admin.

### `PATCH /bookings/{booking_id}`

Updates the status of a specific booking.

- **Description:** Allows an administrator to change the status of a booking (e.g., from "pending" to "confirmed"). This action also triggers a recalculation of the booking's priority.
- **Authentication:** Admin token required (`Bearer <access_token>`).
- **Path Parameters:**
  - `booking_id` (integer, required): The ID of the booking to update.
- **Request Body (application/json):**
  ```json
  {
    "status": "string"
  }
  ```
  **Schema: `BookingStatusUpdate`**
  - `status` (string, required): The new status for the booking.
- **Response (application/json):**
  ```json
  {
    "id": 0,
    "user_id": 0,
    "service_type_id": 0,
    "price_locked": 0.00,
    "status": "string",
    "tanggal_booking": "2026-02-11T12:00:00Z",
    "tanggal_acara": "2026-02-11T12:00:00Z",
    "jumlah_client": 0,
    "priority_score": 0,
    "priority_segment": "low",
    "urgency_level": "upcoming",
    "monetary_level": "regular",
    "updated_priority_at": "2026-02-11T12:00:00Z",
    "user": {
      "id": 0,
      "name": "string",
      "email": "user@example.com",
      "address": "string | null",
      "phone_number": "string | null",
      "role": "customer"
    }
  }
  ```
  **Schema: `BookingRead`** (returns the updated booking object with recalculated priority)
- **Error Responses:**
  - `404 Not Found`: If the `booking_id` does not exist.
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `403 Forbidden`: If the authenticated user is not an admin.

---

## Segmentation Endpoints (`/segments`)

These endpoints provide customer segmentation analysis.

### `GET /segments/`

Retrieves customer segmentation data.

- **Description:** Generates and returns customer segmentation based on RFM (Recency, Frequency, Monetary) analysis. Requires administrator privileges. Uses K-means clustering with `k=4`.
- **Authentication:** Admin token required (`Bearer <access_token>`).
- **Response (application/json):**
  ```json
  [
    {
      "user_id": 0,
      "name": "string",
      "recency": 0,
      "frequency": 0,
      "monetary": 0.00,
      "cluster": 0,
      "customer_segment": "Loyal"
    }
  ]
  ```
  **Schema: `SegmentItem`**
  - `user_id` (integer)
  - `name` (string)
  - `recency` (integer): Days since last booking.
  - `frequency` (integer): Total number of bookings.
  - `monetary` (decimal): Total money spent.
  - `cluster` (integer): The assigned cluster ID.
  - `customer_segment` (string): The derived customer segment (e.g., "Loyal", "Aktif", "Potensial", "Pasif").
- **Error Responses:**
  - `400 Bad Request`: If segmentation fails (e.g., not enough data).
  - `401 Unauthorized`: If no token or an invalid token is provided.
  - `403 Forbidden`: If the authenticated user is not an admin.
