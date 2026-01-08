from sqlalchemy.orm import Mapped, mapped_column

from user_service.infrastructure.persistence.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
