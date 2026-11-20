from sqlalchemy import Text,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database import Base

class Comment(Base):
    __tablename__="comments"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    content:Mapped[str]=mapped_column(Text,nullable=False)
    post_id:Mapped[int]=mapped_column(ForeignKey("posts.id"),nullable=False)
    post:Mapped["Post"]=relationship(back_populates="comments")