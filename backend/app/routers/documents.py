from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import uuid
from datetime import datetime
from ..utils.s3 import S3Client
from ..database.models import Document
from ..database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()
s3_client = S3Client()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Generate unique ID
        doc_id = str(uuid.uuid4())
        
        # Read file content
        content = await file.read()
        
        # Upload to S3
        s3_key = f"documents/{doc_id}/{file.filename}"
        await s3_client.upload_file(content, s3_key, file.content_type)
        
        # Create database entry
        with get_db() as db:
            document = Document(
                id=doc_id,
                filename=file.filename,
                s3_key=s3_key,
                content_type=file.content_type,
                status="uploaded",
                upload_date=datetime.utcnow()
            )
            db.add(document)
            db.commit()
            
        return {
            "id": doc_id,
            "filename": file.filename,
            "message": "Document uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_documents():
    with get_db() as db:
        documents = db.query(Document).all()
        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status,
                "uploadDate": doc.upload_date.isoformat(),
                "contentType": doc.content_type
            }
            for doc in documents
        ]