"""Login system FastAPI application with JWT authentication."""

import os
import sys
from fastapi import FastAPI

# Add src to path for imports
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def create_app() -> FastAPI:
    """Create and configure FastAPI app."""
    app = FastAPI(
        title="Login System API",
        description="User registration and JWT login system",
        version="1.0.0"
    )

    # Import auth router
    from src.auth.routes import router as auth_router
    from src.db.users import create_users_table

    # Create users table on startup
    @app.on_event("startup")
    def startup():
        create_users_table()

    # Include auth router
    app.include_router(auth_router, prefix="", tags=["auth"])

    # Health check endpoint
    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
