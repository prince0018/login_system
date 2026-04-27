# Login System API

A minimal FastAPI-based user authentication system using JWT (JSON Web Tokens) and PostgreSQL.

## Features

- **User Registration** — Create new user accounts with email and password
- **JWT Authentication** — Secure login with JWT tokens
- **Password Hashing** — bcrypt-based password hashing
- **Protected Endpoints** — Access current user info with token
- **PostgreSQL** — Persistent user data storage

## Project Structure

```
login_system/
├── main.py              # FastAPI app entrypoint
├── .env                 # Environment config (secrets)
├── requirements.txt     # Python dependencies
├── readme.md            # This file
└── src/
    ├── auth/
    │   ├── __init__.py
    │   ├── routes.py        # Auth endpoints (register, login, me)
    │   ├── jwt_handler.py   # JWT token creation/validation
    │   └── hashing.py       # Password hashing utilities
    └── db/
        ├── __init__.py
        ├── connection.py    # PostgreSQL connection
        └── users.py         # User DB helpers
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Step 1: Install Dependencies

```bash
cd /Users/prince/dev/projects/genAI/python_projects/login_system
pip install -r requirements.txt
```

### Step 2: Configure Environment

Update `.env` with your PostgreSQL credentials:

```env
DB_NAME=login_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
```

### Step 3: Run the Server

```bash
uvicorn main:app --reload
```

Server will start at `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

## API Endpoints

### Authentication

#### 1. Register New User
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure123",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

#### 2. Login (Get JWT Token)
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure123
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get Current User
```bash
GET /auth/me
Authorization: Bearer {access_token}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

#### 4. Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

## Usage Example

### 1. Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "password123",
    "full_name": "Alice"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=password123"
```

Copy the `access_token` from response.

### 3. Get Current User (with token)
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/auth/me
```

## Database Schema

### users table
```sql
id         SERIAL PRIMARY KEY
email      TEXT UNIQUE NOT NULL
full_name  TEXT
hashed_password TEXT NOT NULL
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

The table is created automatically on app startup.

## Key Files Explained

### src/auth/routes.py
- `/auth/register` — Create new user
- `/auth/token` — Login (returns JWT)
- `/auth/me` — Get current user (requires JWT)
- `get_current_user()` — Dependency to extract user from token

### src/auth/jwt_handler.py
- `create_token(user_id)` — Generate JWT token
- `decode_token(token)` — Validate and decode JWT token

### src/auth/hashing.py
- `hash_password(password)` — Hash password with bcrypt
- `verify_password(plain, hashed)` — Verify password

### src/db/users.py
- `create_users_table()` — Initialize users table
- `create_user()` — Insert new user
- `get_user_by_email()` — Fetch user by email
- `get_user_by_id()` — Fetch user by id

### src/db/connection.py
- `get_connection()` — PostgreSQL connection helper

## Security Notes

- Keep `SECRET_KEY` secret in `.env` (not in version control)
- Use strong passwords (add validation if needed)
- Tokens expire after 24 hours (configurable in jwt_handler.py)
- Use HTTPS in production
- Add rate limiting for login endpoint to prevent brute-force

## Troubleshooting

### Import Errors
```bash
uvicorn main:app --reload
```

### Database Connection Error
- Check PostgreSQL is running
- Verify .env credentials match your Postgres setup
- Ensure database exists: `createdb login_db`

### Token Not Working
- Check token is not expired (24 hour expiry)
- Token must be in header as: `Authorization: Bearer <TOKEN>`

## Next Steps

- Add email verification on registration
- Add refresh tokens for longer sessions
- Add user profile update endpoint
- Add password reset flow
- Add rate limiting on login
- Add unit tests (pytest)
- Deploy to production with gunicorn + nginx

## License

MIT — Feel free to use and modify.
