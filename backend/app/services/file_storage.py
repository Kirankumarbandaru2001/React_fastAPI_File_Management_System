import boto3
from fastapi import UploadFile

# Dummy function for file storage (simulating AWS S3)
async def save_file(file: UploadFile, location: str):
    with open(location, "wb") as buffer:
        buffer.write(await file.read())
