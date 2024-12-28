from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import User, Document
from .services import process_document, query_with_qa_model, extract_text_from_url
from .auth import authenticate_user, create_session
from .database import SessionLocal

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    query: str

@app.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_session(user)
    return {"message": "Login successful", "access_token": access_token}

@app.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        file_url = process_document(file)
        document = Document(url=file_url, filename=file.filename, file_type=file.content_type, user_id=user.id)
        db.add(document)
        db.commit()
        return {"message": "Document uploaded successfully", "file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query_document(query_request: QueryRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve the relevant document from the database
        document = db.query(Document).filter(Document.filename == query_request.query).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Extract text from the document URL (S3 or local path)
        document_text = extract_text_from_url(document.url)

        if not document_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from the document")

        # Process the query with the RAG agent or QA model
        answer = query_with_qa_model(query_request.query, document_text)

        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

