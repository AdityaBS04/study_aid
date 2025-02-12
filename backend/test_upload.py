import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_file_upload():
    try:
        # Create S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Create a test file
        test_content = "This is a test file for S3 upload."
        with open("test.txt", "w") as f:
            f.write(test_content)
        
        # Upload file
        bucket = os.getenv('S3_BUCKET')
        print(f"Uploading test.txt to {bucket}...")
        
        s3.upload_file(
            'test.txt',
            bucket,
            'test/test.txt'
        )
        
        print("File uploaded successfully!")
        
        # List objects to verify
        print("\nBucket contents after upload:")
        response = s3.list_objects_v2(Bucket=bucket)
        for obj in response['Contents']:
            print(f"- {obj['Key']}")
            
    except Exception as e:
        print(f"Error during upload test: {e}")
    finally:
        # Clean up test file
        if os.path.exists("test.txt"):
            os.remove("test.txt")

if __name__ == "__main__":
    test_file_upload()