from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    documents = relationship("Document", back_populates="owner")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    url = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_type = Column(String, index=True)  # Add the file type field
    owner = relationship("User", back_populates="documents")
