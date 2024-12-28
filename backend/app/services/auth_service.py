from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from app.models.user import User
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        return jwt.encode({"sub": username}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return None
