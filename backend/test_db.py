import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_NAME = 'postgres'  # Using default database
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

try:
    # Attempt to connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    
    print("Successfully connected to the database!")
    
    # Create a cursor
    cur = conn.cursor()
    
    # Execute a simple query to check version
    cur.execute('SELECT version();')
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    # List all tables in the database
    print("\nTables in database:")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = cur.fetchall()
    for table in tables:
        print(f"- {table[0]}")
    
    # Show structure of documents table
    print("\nStructure of documents table:")
    cur.execute("""
        SELECT 
            column_name, 
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = 'documents'
        ORDER BY ordinal_position
    """)
    
    columns = cur.fetchall()
    if columns:
        for column in columns:
            print(f"- {column[0]}")
            print(f"  Type: {column[1]}")
            print(f"  Nullable: {column[2]}")
            print(f"  Default: {column[3]}")
    else:
        print("No documents table found or table is empty")
    
    # Close cursor and connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to the database: {e}")