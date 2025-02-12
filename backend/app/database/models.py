from sqlalchemy import Column, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres"

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)  # Path in S3 bucket
    content_type = Column(String, nullable=False)  # PDF/PPTX
    status = Column(String, nullable=False)  # processing/processed/error
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed_content = Column(JSON, nullable=True)  # Extracted text and metadata
    analysis_results = Column(JSON, nullable=True)  # Topic modeling results, keywords, etc.

# Create all tables
Base.metadata.create_all(bind=engine)