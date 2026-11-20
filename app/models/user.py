from datetime import datetime,timezone
from sqlalchemy import String,Boolean,DateTime,text,CheckConstraint

from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__=(
        CheckConstraint(
            "age >= 18",
            name="check_user_age"
        ),
    )
    
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    email:Mapped[str]=mapped_column(String(150),unique=True,nullable=False)
    age:Mapped[int]=mapped_column(nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,server_default=text("true"),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),server_default=text("CURRENT_TIMESTAMP"),nullable=False)
    
    
    profile:Mapped["Profile"]=relationship(back_populates="user",cascade="all, delete-orphan")
    
    posts:Mapped[list["Post"]]=relationship(back_populates="user",cascade="all, delete-orphan")
    