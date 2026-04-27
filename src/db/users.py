from src.db.connection import get_connection


def create_users_table():
    """Create users table if it doesn't exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT,
                    hashed_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                conn.commit()
        print("✅ Users table created/verified")
    except Exception as e:
        print(f"❌ Error creating users table: {e}")


def create_user(email: str, hashed_password: str, full_name: str = None):
    """Create a new user and return user_id."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (email, full_name, hashed_password) VALUES (%s, %s, %s) RETURNING id;",
                    (email, full_name, hashed_password)
                )
                result = cur.fetchone()
                conn.commit()
                return result[0] if result else None
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None


def get_user_by_email(email: str):
    """Get user by email."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, email, full_name, hashed_password, created_at FROM users WHERE email = %s;",
                    (email,)
                )
                row = cur.fetchone()
                if not row:
                    return None
                return {
                    "id": row[0],
                    "email": row[1],
                    "full_name": row[2],
                    "hashed_password": row[3],
                    "created_at": row[4]
                }
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return None


def get_user_by_id(user_id: int):
    """Get user by user_id."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, email, full_name, created_at FROM users WHERE id = %s;",
                    (user_id,)
                )
                row = cur.fetchone()
                if not row:
                    return None
                return {
                    "id": row[0],
                    "email": row[1],
                    "full_name": row[2],
                    "created_at": row[3]
                }
    except Exception as e:
        print(f"❌ Error getting user by id: {e}")
        return None
