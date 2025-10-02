import sqlite3

def view_tables():
    # Connect to the database
    conn = sqlite3.connect('instance/test.db')
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n=== Tables in database ===")
    for table in tables:
        table_name = table[0]
        print(f"\n Table: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
            
        # Get table contents
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if rows:
            print("\nContents:")
            for row in rows:
                print(f"  {row}")
        else:
            print("\nTable is empty")
        print("-" * 50)

    conn.close()

if __name__ == "__main__":
    view_tables()