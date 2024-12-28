from fastapi import APIRouter, File, UploadFile
from app.services.file_storage import save_file

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    await save_file(file, file_location)
    return {"message": f"File {file.filename} uploaded successfully!"}
