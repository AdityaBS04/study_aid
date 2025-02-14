import psycopg2

try:
    # Connect to existing clutch_ai database
    conn = psycopg2.connect(
        host="clutch-ai-db.chcgw8co2m64.ap-south-1.rds.amazonaws.com",
        database="clutch_ai",  # Use existing database
        user="postgres",
        password="clutch_AI",
        port="5432"
    )
    print("Successfully connected to clutch_ai database!")
    
    # List all tables
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print("\nExisting tables:")
    for table in tables:
        print(f"- {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Connection failed: {e}")