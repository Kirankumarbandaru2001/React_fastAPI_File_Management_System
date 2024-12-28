from fastapi import APIRouter, File, UploadFile

from app.services.file_storage import save_file

router = APIRouter()
# File upload
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    await save_file(file)
    return {"message": f"File {file.filename} uploaded successfully!"}
