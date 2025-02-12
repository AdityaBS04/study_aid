import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_s3_connection():
    try:
        # Create S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Test bucket access
        bucket = os.getenv('S3_BUCKET')
        response = s3.list_objects_v2(Bucket=bucket)
        
        print("Successfully connected to S3!")
        print(f"Bucket: {bucket}")
        print("\nExisting objects in bucket:")
        
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print("Bucket is empty")
            
    except Exception as e:
        print(f"Error connecting to S3: {e}")

if __name__ == "__main__":
    test_s3_connection()