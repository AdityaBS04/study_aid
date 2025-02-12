import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket = os.getenv('S3_BUCKET')

    async def upload_file(self, file_content, file_name, content_type):
        """Upload a file to S3"""
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=file_name,
                Body=file_content,
                ContentType=content_type
            )
            return f"s3://{self.bucket}/{file_name}"
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {str(e)}")

    async def get_file(self, file_name):
        """Get a file from S3"""
        try:
            response = self.s3.get_object(
                Bucket=self.bucket,
                Key=file_name
            )
            return response['Body'].read()
        except Exception as e:
            raise Exception(f"Error retrieving file from S3: {str(e)}")