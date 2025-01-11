# API Documentation

## Base URL
All APIs are prefixed with `https://yadra-backend.vercel.app/api`

## Authentication
Most endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Reviews
Base path: `/reviews`

#### POST `/reviews/submit`
Submit a new review.

**Authentication Required:** Yes

**Request Body**
```json
{
    "branch_id": string,
    "title": string,
    "content": string,
    "rating": {
        "staff_satisfaction": number,
        "reliability": number,
        "speed_satisfaction": number
    },
    "is_anonymous": boolean,
    "tags": string[],
    "media": File[] // Optional
}
```

**Response 201**
```json
{
    "review_id": string,
    "status": "published"
}
```

**Response 400**
```json
{
    "msg": "Validation failed",
    "errors": object
}
```

#### POST `/reviews/flag`
Flag a review for moderation.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1) or Company Manager (role=3) for their company

**Request Body**
```json
{
    "review_id": string,
    "description": string // 10-500 characters
}
```

**Response 201**
```json
{
    "message": "Review flagged successfully",
    "flag_id": string,
    "flagged_at": datetime
}
```

#### GET `/reviews/get_flagged`
Get all flagged reviews.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "flagged_reviews": [FlaggedReview]
}
```

#### POST `/reviews/flag/validate`
Validate or reject a flagged review.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "flag_id": string,
    "validated": boolean
}
```

**Response 200**
```json
{
    "message": string,
    "flag_id": string,
    "validated": boolean
}
```

#### POST `/reviews/like`
Like a review.

**Authentication Required:** Yes

**Request Body**
```json
{
    "review_id": string
}
```

**Response 201**
```json
{
    "message": "Review liked successfully",
    "review_id": string,
    "user_id": string
}
```

#### DELETE `/reviews/delete`
Delete (hide) a review.

**Authentication Required:** Yes  
**Required Role:** Review owner or Admin (role=1)

**Request Body**
```json
{
    "review_id": string
}
```

**Response 200**
```json
{
    "message": "Review deleted successfully",
    "review_id": string
}
```

#### GET `/reviews/likes_status`
Get likes status for a review.

**Authentication Required:** Yes

**Request Body**
```json
{
    "review_id": string
}
```

**Response 200**
```json
{
    "likes_count": integer,
    "user_liked": boolean
}
```



### Categories
Base path: `/categories`

#### GET `/categories/get_categories`
Get all categories.

**Authentication Required:** No

**Response 201**
```json
{
    "companies": [Category]
}
```

#### POST `/categories/add_category`
Add a new category.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "name": string
}
```

**Response 201**
Success response (category added)

**Response 300**
```json
{
    "msg": "category already exists" | "User not authorized" | "User does not exist"
}
```





### Response Management
Base path: `/response`

#### GET `/response/get_responses`
Get all responses that aren't hidden.

**Authentication Required:** No

**Response 201**
```json
{
    "companies": [Response]
}
```

#### POST `/response/add_response`
Add a response to a review.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3) for their company's reviews, or Branch Manager (role=4) for their branch's reviews

**Request Body**
```json
{
    "description": string,
    "review_id": integer
}
```

**Response 201**
```json
{
    "msg": "Response added successfully",
    "response_id": integer
}
```

**Response 300**
```json
{
    "msg": "User not authorized or review no longer exists"
}
```
or
```json
{
    "msg": "User does not exist"
}
```

#### POST `/response/delete_response`
Soft delete (hide) a response.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3) for their company's responses, or Branch Manager (role=4) for their branch's responses

**Request Body**
```json
{
    "response_id": integer
}
```

**Response 201**
```json
{
    "msg": "Response deleted successfully"
}
```

**Response 300**
```json
{
    "msg": "User not authorized or review no longer exists"
}
```
or
```json
{
    "msg": "User/response does not exist"
}
```



### Companies
Base path: `/companies`

#### Company Verification

##### POST `/companies/verify`
Verify a company.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "company_id": integer
}
```

**Response 200**
```json
{
    "msg": "verified company",
    "company_id": integer,
    "verified": integer
}
```

##### POST `/companies/unverify`
Remove verification from a company.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "company_id": integer
}
```

**Response 200**
```json
{
    "msg": "unverified successfully",
    "company_id": integer,
    "verified": integer
}
```

#### Company Registration

##### POST `/companies/company_register/register`
Register a new company request.

**Authentication Required:** No

**Request Body**
```json
{
    "name": string,
    "logo": string,
    "category": string,
    "address": string,
    "email": string,
    "admin_email": string,
    "website": string,
    "description": string,
    "phone": string,
    "business_registration": string,
    "social_links": string
}
```

**Response 201**
```json
{
    "company_id": integer
}
```

##### GET `/companies/get_company_register`
Get all company registration requests.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 201**
```json
{
    "companies": [Company]
}
```

##### POST `/companies/company_register/validate`
Validate a company registration request.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "validated": boolean,
    "company_id": integer
}
```

**Response 201**
```json
{
    "msg": "company validated and admin account created",
    "company": {
        "id": integer,
        "account_email": string,
        "account_password": string
    }
}
```

#### Branch Management

##### POST `/companies/company/add_branch`
Add a new branch to a company.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3)

**Request Body**
```json
{
    "name": string,
    "account_email": string,
    "category": string,
    "address": string,
    "email": string,
    "phone": string
}
```

**Response 201**
```json
{
    "msg": "Branch added successfully.",
    "branch_id": integer,
    "account_password": string
}
```

#### Company/Branch Editing

##### POST `/companies/edit_company/edit`
Edit company details.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3) or Admin (role=1)

**Request Body**
```json
{
    "company_id": integer,
    "name": string (optional),
    "description": string (optional),
    "website": string (optional),
    "social_links": string (optional),
    "address": string (optional),
    "email": string (optional),
    "phone": string (optional),
    "logo": string (optional)
}
```

**Response 201**
```json
{
    "msg": "company modified successfully"
}
```

##### POST `/companies/edit_branch/edit`
Edit branch details.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3), Branch Manager (role=4), or Admin (role=1)

**Request Body**
```json
{
    "branch_id": integer,
    "name": string (optional),
    "address": string (optional),
    "email": string (optional),
    "phone": string (optional)
}
```

**Response 201**
```json
{
    "msg": "branch modified successfully"
}
```

#### Retrieval Endpoints

##### GET `/companies/get_branches`
Get all branches.

**Authentication Required:** No

**Response 201**
```json
{
    "branches": [Branch]
}
```

##### GET `/companies/get_branch`
Get specific branch details.

**Authentication Required:** Yes

**Query Parameters**
- `branch_id`: integer

**Response 201**
```json
{
    "name": string,
    "email": string,
    "phone": string,
    "address": string,
    "visits": integer,
    "logo": string,
    "website": string,
    "category": string,
    "verified": boolean,
    "rating": number,
    "staff_satisfaction": number,
    "speed_satisfaction": number,
    "reliability": number,
    "reviews_responses": [Review],
    "repartition": [number]
}
```

##### GET `/companies/get_company`
Get specific company details.

**Authentication Required:** Yes

**Query Parameters**
- `company_id`: integer

**Response 201**
```json
{
    "name": string,
    "email": string,
    "phone": string,
    "address": string,
    "visits": integer,
    "logo": string,
    "website": string,
    "category": string,
    "verified": boolean,
    "branches": [Branch],
    "rating": number
}
```

##### GET `/companies/get_companies`
Get all companies.

**Authentication Required:** No

**Response 201**
```json
{
    "companies": [Company]
}
```

#### Deletion Endpoints

##### POST `/companies/company/delete_company`
Delete (hide) a company.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3) or Admin (role=1)

**Request Body**
```json
{
    "company_id": integer
}
```

**Response 200**
```json
{
    "message": "branch deleted"
}
```

##### POST `/companies/company/delete_branch`
Delete (hide) a branch.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3) or Admin (role=1)

**Request Body**
```json
{
    "branch_id": integer
}
```

**Response 200**
```json
{
    "message": "branch deleted"
}
```

### Authentication
Base path: `/auth`

#### POST `/auth/register`
Register a new user.

**Authentication Required:** No

**Request Body**
```json
{
    "email": string,
    "password": string,
    "name": string,
    "phone": string (optional),
    "role": integer (optional),
    "avatar": string (optional)
}
```

**Response 201**
```json
{
    "user_id": integer,
    "token": string,
    "expires_in": 3600
}
```

**Response 400 (Validation Error)**
```json
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Invalid input",
        "details": object
    }
}
```

**Response 400 (Email Exists)**
```json
{
    "error": {
        "code": "EMAIL_EXISTS",
        "message": "Email already registered",
        "details": {
            "field": "email"
        }
    }
}
```

#### POST `/auth/login`
Authenticate a user and get access token.

**Authentication Required:** No

**Request Body**
```json
{
    "email": string,
    "password": string,
    "remember_me": boolean (optional)
}
```

**Response 200**
```json
{
    "token": string,
    "expires_in": integer,
    "user": {
        "id": integer,
        "name": string,
        "email": string,
        "role": integer,
        "company_id": integer,
        "branch_id": integer
    }
}
```

**Response 400**
```json
{
    "msg": "Missing email or password"
}
```

**Response 401**
```json
{
    "msg": "Invalid email or password"
}
```

**Response 401 (Banned User)**
```json
{
    "msg": "user is banned"
}
```

#### POST `/auth/Delete`
Hide/delete the current user's account.

**Authentication Required:** Yes

**Response 200**
```json
{
    "msg": "user is hidden"
}
```

**Response 404**
```json
{
    "msg": "user not found"
}
```

### Analytics
Base path: `/analytics`

#### Charts

##### GET `/analytics/charts/get_categories_distribution`
Get distribution of companies across categories.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "data": [
        {
            "name": string,
            "distribution": integer
        }
    ]
}
```

##### GET `/analytics/charts/get_reviews_distribution`
Get distribution of reviews across companies.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "data": {
        "company_name": number_of_reviews
    }
}
```

##### GET `/analytics/charts/users_over_time`
Get user growth over time.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "group_by": "day|month|year" // optional, defaults to "day"
}
```

**Response 200**
```json
[
    {
        "time_period": string,
        "user_count": integer
    }
]
```

##### GET `/analytics/charts/reviews_over_time`
Get review counts over time for a specific branch.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "branch_id": integer,
    "group_by": "day|month|year" // optional, defaults to "day"
}
```

**Response 200**
```json
[
    {
        "time_period": string,
        "review_count": integer
    }
]
```

#### Blocks

##### GET `/analytics/blocks/get_num_users`
Get total number of active normal users.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number of users": integer
}
```

##### GET `/analytics/blocks/get_num_companies`
Get total number of visible companies.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number of companies": integer
}
```

##### GET `/analytics/blocks/get_num_of_active_users`
Get number of users active in last 24 hours.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number_of_new_users": integer
}
```

##### GET `/analytics/blocks/get_num_new_users`
Get number of users created today.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number_of_new_users": integer
}
```

##### GET `/analytics/blocks/churn_rate`
Get user churn rate (percentage of users inactive for >31 days).

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "churn_rate": float
}
```

##### GET `/analytics/blocks/get_num_branches`
Get total number of branches.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number of branches": integer
}
```

##### GET `/analytics/blocks/get_num_reviews`
Get total number of reviews.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "number of reviews": integer
}
```

##### GET `/analytics/blocks/get_average_rating`
Get average rating across all visible reviews.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "avg_rating": float
}
```

##### GET `/analytics/blocks/num_flagged`
Get number of flagged reviews.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "message": "successfully calculated",
    "Num_of_flagged": integer
}
```

##### GET `/analytics/blocks/reviews_for_company`
Get number of reviews for the authenticated company manager's company.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3)

**Response 200**
```json
{
    "message": "successfully calculated",
    "Num_of_reviews": integer
}
```

##### GET `/analytics/blocks/avg_rating_for_company`
Get average rating for the authenticated company manager's company.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3)

**Response 200**
```json
{
    "message": "successfully calculated",
    "Avg_rating": float
}
```

##### GET `/analytics/blocks/review_trends`
Get review trends filtered by time period.

**Authentication Required:** Yes  
**Required Role:** Company Manager (role=3)

**Request Body**
```json
{
    "filter": "daily|weekly|monthly" // optional, defaults to "daily"
}
```

**Response 200**
```json
{
    "message": "successfully calculated",
    "num_of_reviews": integer
}
```

##### GET `/analytics/blocks/user_growth`
Get user growth comparison between current and previous month.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 200**
```json
{
    "current_month_users": integer,
    "previous_month_users": integer,
    "growth_percentage": float
}
```

##### GET `/analytics/blocks/company_response_avg`
Get company's review response statistics.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "company_id": integer
}
```

**Response 200**
```json
{
    "company_id": integer,
    "company_name": string,
    "total_reviews": integer,
    "responded_reviews": integer
}
```

##### GET `/analytics/blocks/company_response_rate`
Get company's average response time to reviews.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "company_id": integer
}
```

**Response 200**
```json
{
    "company_id": integer,
    "company_name": string,
    "total_reviews": integer,
    "average_response_time_minutes": float
}
```

### User Management

#### GET `/user/profile`
Get the profile of the currently authenticated user.

**Authentication Required:** Yes

**Response 200**
```json
{
    "id": integer,
    "email": string,
    "name": string,
    "phone": string,
    "role": integer,
    "company_id": integer,
    "branch_id": integer,
    "created_at": datetime,
    "avatar": string,
    "state": integer,
    "last_login": datetime
}
```

**Response 404**
```json
{
    "message": "User not found"
}
```

### Account Management

#### POST `/add/company`
Add a new company account.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1) or Company Manager (role=3)

**Request Body**
```json
{
    "company_id": integer,
    "email": string,
    "password": string,
    "name": string,
    "phone": string (optional),
    "avatar": string (optional)
}
```

**Response 201**
```json
{
    "user_id": integer,
    "token": string,
    "expires_in": 3600
}
```

**Response 404**
```json
{
    "msg": "unauthorized" | "Company doesn't exist"
}
```

#### POST `/add/branch`
Add a new branch account.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1) or Company Manager (role=3) or Branch Manager (role=4)

**Request Body**
```json
{
    "branch_id": integer,
    "email": string,
    "password": string,
    "name": string,
    "phone": string (optional),
    "avatar": string (optional)
}
```

**Response 201**
```json
{
    "user_id": integer,
    "token": string,
    "expires_in": 3600
}
```

**Response 404**
```json
{
    "msg": "unauthorized" | "Branch does not exist"
}
```

#### POST `/edit/account`
Edit user account details.

**Authentication Required:** Yes

**Request Body**
```json
{
    "name": string (optional),
    "password": string (optional),
    "email": string (optional),
    "phone": string (optional),
    "avatar": string (optional)
}
```

**Response 201**
```json
{
    "msg": "user modified successfully"
}
```

**Response 404**
```json
{
    "msg": "user doesn't exist"
}
```

#### POST `/edit/ban`
Ban a user account.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "user_id": integer
}
```

**Response 201**
```json
{
    "msg": "user banned successfully"
}
```

**Response 404**
```json
{
    "msg": "user doesn't exist"
}
```

#### POST `/edit/unban`
Unban a user account.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Request Body**
```json
{
    "user_id": integer
}
```

**Response 201**
```json
{
    "msg": "user unbanned successfully"
}
```

**Response 404**
```json
{
    "msg": "user does not exist"
}
```

#### GET `/edit/getbanned`
Get list of banned users.

**Authentication Required:** Yes  
**Required Role:** Admin (role=1)

**Response 201**
```json
{
    "users": [User]
}
```

**Response 404**
```json
{
    "msg": "user doesn't exist"
}
```



## User Roles
- 1: Admin
- 2: Regular User
- 3: Company Manager
- 4: Branch Manager

## Notes
- All successful creation operations return status code 201
- Most error responses return status code 404
- JWT tokens expire in 7 days
- The system maintains user states (0: active, 1: banned)
- Most endpoints require the user account to have `is_hidden=False` and `state=0`
- User roles:
  - 1: Admin
  - 2: Regular User
  - 3: Company Manager
  - 4: Branch Manager
- User states:
  - 0: Active
  - 1: Banned
- `is_hidden` flag is used for soft deletion 
- Company verification is handled through the `verified` flag (0: unverified, 1: verified)
- Visit counts are automatically incremented for normal users viewing company/branch details
- Ratings are calculated as averages across all visible reviews



## Error Responses
Most endpoints return these error responses when applicable:

**404 Not Found**
```json
{
    "message": "User not found"
}
```

**404 Unauthorized**
```json
{
    "message": "Unauthorized User"
}
```









