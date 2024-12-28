from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .core.database import SessionLocal, engine, Base
from .models.document import Document
from .services import auth_service, file_storage, document_parser, rag_agent

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Handle document upload."""
    file_url = file_storage.upload_to_s3(file)
    parsed_data = document_parser.parse_document(file_url)
    document = Document(filename=file.filename, file_url=file_url, doc_metadata=parsed_data['content'])
    db.add(document)
    db.commit()
    return {"message": "File uploaded successfully", "document_id": document.id}

@app.post("/query/")
async def query_document(query: str, db: Session = Depends(get_db)):
    """Handle querying documents."""
    response = rag_agent.handle_query(query)
    return {"response": response}

@app.post("/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    token = auth_service.authenticate_user(username, password, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}
