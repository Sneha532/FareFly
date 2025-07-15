from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Any
from datetime import timedelta
import uuid

from src.app.api import deps
from src.app import crud, models
from src.app.models.user import User
from src.app.schemas import user as schemas
from src.app.core.security import get_password_hash, verify_password, create_access_token
from src.app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.Token)
def register(
    user_in: schemas.UserRegister,
    db: Session = Depends(deps.get_db)
):
    """
    Register a new user and return access token.
    """
    # Check if user already exists
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user - FIXED: Use correct field names
    user_id = str(uuid.uuid4())
    db_user = User(
        user_id=user_id,  # This matches your User model
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate access token using user_id
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=db_user.user_id,  # Use user_id consistently
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=schemas.Token)
def login(
    user_in: schemas.UserLogin,
    db: Session = Depends(deps.get_db)
):
    """Login for access token."""
    # Find user by email
    user = crud.user.get_by_email(db, email=user_in.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.user_id,  # Use user_id not id
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Keep your existing OAuth2 form login endpoint if needed
@router.post("/token", response_model=schemas.Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not crud.user.is_active(user):
        raise HTTPException(
            status_code=400, 
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=schemas.User)
def get_current_user(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get current user profile
    """
    # Convert User model to dictionary with correct field mapping
    user_data = {
        "id": current_user.user_id,  # Map user_id to id expected by schema
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }
    return user_data