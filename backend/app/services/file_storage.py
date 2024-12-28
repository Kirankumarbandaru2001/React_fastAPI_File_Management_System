import boto3, os
from fastapi import UploadFile
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
load_dotenv()
AWS_S3_BUCKET= os.getenv("AWS_S3_BUCKET"),
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID"),
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# Function to save file to S3
async def save_file(file: UploadFile):
    try:
        # Read the file content
        file_content = await file.read()

        # Upload the file to S3
        s3_client.put_object(
            Bucket=AWS_S3_BUCKET,
            Key=file.filename,
            Body=file_content
        )

        print(f"File {file.filename} uploaded successfully to S3.")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: AWS credentials not found or incomplete. {str(e)}")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
