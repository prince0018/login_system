from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from src.auth.jwt_handler import create_token, decode_token
from src.auth.hashing import hash_password, verify_password
from src.db.users import get_user_by_email, create_user, get_user_by_id

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str = None


@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(req: RegisterRequest):
    """Register a new user with email and password."""
    user = get_user_by_email(req.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(req.password)
    user_id = create_user(req.email, hashed_password, req.full_name)
    
    if not user_id:
        raise HTTPException(status_code=500, detail="Could not create user")
    
    return {"id": user_id, "email": req.email, "full_name": req.full_name}


@router.post("/auth/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password, return JWT access token."""
    user = get_user_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_token(user["id"])
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency: Extract and validate user from JWT token."""
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id = payload.get("user_id")
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    """Get current logged-in user details."""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"]
    }
