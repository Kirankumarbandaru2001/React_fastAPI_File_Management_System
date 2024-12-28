from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_url = Column(String, unique=True, index=True)
    doc_metadata = Column(Text)
