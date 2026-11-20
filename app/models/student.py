from sqlalchemy import String,Text,ForeignKey

from sqlalchemy.orm import (Mapped,mapped_column,relationship)

from app.database import Base
from app.models.associations import student_course

class Student(Base):
    __tablename__="students"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    courses:Mapped[list["Course"]]=relationship(secondary=student_course,back_populates="students")