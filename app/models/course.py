from sqlalchemy import String,Text,ForeignKey

from sqlalchemy.orm import (Mapped,mapped_column,relationship)

from app.database import Base

from app.models.associations import student_course

class Course(Base):
    __tablename__="courses"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(100),nullable=False)
    students:Mapped[list["Student"]]=relationship(secondary=student_course,back_populates="courses")