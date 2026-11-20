from sqlalchemy import String,Text,ForeignKey

from sqlalchemy.orm import (Mapped,mapped_column,relationship)

from app.database import Base


class Post(Base):
    __tablename__="posts"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(200),nullable=False)
    content:Mapped[str]=mapped_column(Text,nullable=False)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"]=relationship(back_populates="posts")
    comments:Mapped[list["Comment"]]=relationship(back_populates="post",cascade="all, delete-orphan")