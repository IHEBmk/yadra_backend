# Analytics API Documentation

## Authentication
All endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### 1. Get Number of Companies
Retrieves the total count of companies in the system.

**Endpoint:** `GET /api/analytics/charts/get_number_of_companies`

**Authorization:** Admin only (role=1)

**Response:**
```json
{
    "message": "succesfully calculated",
    "number of companies": <integer>
}
```

**Status Codes:**
- 200: Success
- 404: User not found or unauthorized

### 2. Increment Visit Count
Increments the visitor counter.

**Endpoint:** `POST /api/analytics/increment_visit_count`

**Authorization:** JWT required

**Response:**
```json
{
    "message": "visit count incremented"
}
```

**Status Codes:**
- 200: Success

### 3. Get Visits Over Time
Retrieves visit statistics over a specified time period.

**Endpoint:** `POST /api/analytics/charts/visits_over_time`

**Authorization:** Admin only (role=1)

**Request Body:**
```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "group_by": "day|month|year"  // optional, defaults to "day"
}
```

**Response:**
```json
[
    {
        "time_period": "YYYY-MM-DD",
        "visit_count": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 400: Invalid request body or date format
- 403: Unauthorized (non-admin user)

### 4. Get Companies Over Time
Retrieves company registration statistics over a specified time period.

**Endpoint:** `POST /api/analytics/charts/companies_over_time`

**Authorization:** Admin only (role=1)

**Request Body:**
```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "group_by": "day|month|year"  // optional, defaults to "day"
}
```

**Response:**
```json
[
    {
        "time_period": "YYYY-MM-DD",
        "company_count": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 400: Invalid request body or date format
- 403: Unauthorized (non-admin user)

### 5. Get Visits Heatmap
Retrieves visit data for the last 7 days in a heatmap format.

**Endpoint:** `GET /api/analytics/charts/visits_heatmap`

**Authorization:** Admin only (role=1)

**Response:**
```json
[
    {
        "interval_start": "YYYY-MM-DD HH:MM:SS",
        "interval_end": "YYYY-MM-DD HH:MM:SS",
        "total_visits": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 403: Unauthorized (non-admin user)

### 6. Get Reviews
Retrieves all reviews for a specific company and its branches.

**Endpoint:** `POST /api/analytics/get_reviews`

**Authorization:** Admin only (role=1)

**Request Body:**
```json
{
    "company_id": "<string>"
}
```

**Response:**
```json
{
    "reviews": [
        {
            "id": "<string>",
            "user_id": "<string>",
            "company_id": "<string>",
            "branch_id": "<string>",
            "title": "<string>",
            "description": "<string>",
            "rating": <float>,
            "product_quality": <float>,
            "price": <float>,
            "delivery_speed": <float>,
            "ease_of_use": <float>,
            "customer_service": <float>,
            "created_at": "<string>",
            "tags": "<string>",
            "is_anonymous": <boolean>,
            "is_hidden": <boolean>
        }
    ]
}
```

**Status Codes:**
- 200: Success
- 403: Unauthorized (non-admin user)

### 7. Get Users
Retrieves all active users and their review counts.

**Endpoint:** `GET /api/analytics/get_users`

**Authorization:** Admin only (role=1)

**Response:**
```json
[
    {
        "name": "<string>",
        "email": "<string>",
        "role": <integer>,
        "last_login": "<string>",
        "state": <integer>,
        "nb_reviews": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 403: Unauthorized (non-admin user)


### 8. Get Reviews Over Time
Retrieves review statistics over a specified time period for a specific branch.

**Endpoint:** `POST /api/analytics/charts/reviews_over_time`

**Authorization:** Admin only (role=1)

**Request Body:**
```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "branch_id": "<string>",
    "group_by": "day|month|year"  // optional, defaults to "day"
}
```

**Response:**
```json
[
    {
        "time_period": "<string>",
        "review_count": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 400: Invalid request body or date format
- 403: Unauthorized (non-admin user)

### 9. Get Number of Reviews per Company
Retrieves the top 5 companies by number of reviews.

**Endpoint:** `GET /api/analytics/charts/nb_reviews_per_company`

**Authorization:** Admin only (role=1)

**Response:**
```json
[
    {
        "company": "<string>",
        "number_of_reviews": <integer>
    }
]
```

**Status Codes:**
- 200: Success
- 403: Unauthorized (non-admin user)



## Error Handling
All endpoints follow a consistent error response format:
```json
{
    "message": "<error_description>"
}
```

## Notes
- All timestamps are in ISO format
- Role=1 represents admin access
- Date formats must be in YYYY-MM-DD format
- Time periods can be grouped by day, month, or year