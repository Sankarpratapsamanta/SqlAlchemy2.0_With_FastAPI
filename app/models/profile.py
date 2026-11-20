from sqlalchemy import String,ForeignKey

from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database import Base

class Profile(Base):
    __tablename__="profiles"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    bio:Mapped[str]=mapped_column(String(500),nullable=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True,nullable=False)
    user:Mapped["User"]=relationship(back_populates="profile")
    