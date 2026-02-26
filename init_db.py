import sqlite3
import re
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")
# remove 'sqlite:///' prefix for sqlite3 module
DB_FILE = DB_URL.replace("sqlite:///", "")

def clean_sql_server_ddl_for_sqlite(ddl: str) -> str:
    """
    Converts SQL Server specific DDL to SQLite compatible DDL.
    """
    # Replace NVARCHAR and VARCHAR with TEXT
    ddl = re.sub(r'NVARCHAR\(\d+\)', 'TEXT', ddl)
    ddl = re.sub(r'VARCHAR\(\d+\)', 'TEXT', ddl)
    
    # Replace INT IDENTITY with INTEGER AUTOINCREMENT
    ddl = ddl.replace('INT IDENTITY PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    
    # Replace DATETIME2 with TEXT (SQLite stores dates as text/numeric/integer)
    ddl = ddl.replace('DATETIME2', 'TEXT')
    
    # Replace BIT with INTEGER
    ddl = ddl.replace('BIT', 'INTEGER')
    
    # Remove SYSUTCDATETIME() default (SQLite uses CURRENT_TIMESTAMP)
    ddl = ddl.replace('SYSUTCDATETIME()', 'CURRENT_TIMESTAMP')
    
    # DECIMAL to REAL
    ddl = re.sub(r'DECIMAL\(\d+,\d+\)', 'REAL', ddl)
    
    return ddl

def init_db():
    if os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} already exists. Skipping initialization.")
        return

    print(f"Initializing database at {DB_FILE}...")
    
    with open("schema.sql", "r") as f:
        sql_server_ddl = f.read()

    # Split by CREATE TABLE to process individually
    statements = [s.strip() + ";" for s in sql_server_ddl.split(';') if s.strip()]
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    for stmt in statements:
        sqlite_stmt = clean_sql_server_ddl_for_sqlite(stmt)
        try:
            cursor.execute(sqlite_stmt)
        except Exception as e:
            print(f"Error executing statement:\n{sqlite_stmt}\nError: {e}")
            
    # Insert comprehensive dummy data across all tables to test scenarios
    dummy_data = [
        
        "INSERT INTO Sites (SiteId, SiteCode, SiteName, City, Country) VALUES (1, 'NYC01', 'New York HQ', 'New York', 'USA');",
        "INSERT INTO Sites (SiteId, SiteCode, SiteName, City, Country) VALUES (2, 'LDN01', 'London Office', 'London', 'UK');",
        "INSERT INTO Sites (SiteId, SiteCode, SiteName, City, Country) VALUES (3, 'TYO01', 'Tokyo Branch', 'Tokyo', 'Japan');",
        "INSERT INTO Locations (LocationId, SiteId, LocationCode, LocationName) VALUES (1, 1, 'FL1', 'Floor 1');",
        "INSERT INTO Locations (LocationId, SiteId, LocationCode, LocationName) VALUES (2, 2, 'FL2', 'Floor 2');",
        
        
        "INSERT INTO Customers (CustomerId, CustomerCode, CustomerName) VALUES (1, 'CUST1', 'Acme Corp');",
        "INSERT INTO Customers (CustomerId, CustomerCode, CustomerName) VALUES (2, 'CUST2', 'Globex Inc');",
        "INSERT INTO Vendors (VendorId, VendorCode, VendorName) VALUES (1, 'V001', 'Tech Supplies Inc');",
        "INSERT INTO Vendors (VendorId, VendorCode, VendorName) VALUES (2, 'V002', 'Office Furniture Co');",
        "INSERT INTO Vendors (VendorId, VendorCode, VendorName) VALUES (3, 'V003', 'Enterprise Software Ltd');",
        
        
        "INSERT INTO Items (ItemId, ItemCode, ItemName, Category) VALUES (1, 'ITM-L1', 'Laptop', 'Electronics');",
        "INSERT INTO Items (ItemId, ItemCode, ItemName, Category) VALUES (2, 'ITM-D1', 'Desk', 'Furniture');",
        "INSERT INTO Items (ItemId, ItemCode, ItemName, Category) VALUES (3, 'ITM-M1', 'Monitor', 'Electronics');",

        
        "INSERT INTO Assets (AssetTag, AssetName, SiteId, Category, Status, Cost, PurchaseDate, VendorId) VALUES ('AST-001', 'Dell XPS 15', 1, 'Electronics', 'Active', 1500.00, '2023-01-15', 1);",
        "INSERT INTO Assets (AssetTag, AssetName, SiteId, Category, Status, Cost, PurchaseDate, VendorId) VALUES ('AST-002', 'MacBook Pro', 2, 'Electronics', 'Active', 2500.00, '2024-02-10', 1);",
        "INSERT INTO Assets (AssetTag, AssetName, SiteId, Category, Status, Cost, PurchaseDate, VendorId) VALUES ('AST-003', 'Herman Miller Chair', 1, 'Furniture', 'Active', 800.00, '2024-01-20', 2);",
        "INSERT INTO Assets (AssetTag, AssetName, SiteId, Category, Status, Cost, PurchaseDate, VendorId) VALUES ('AST-004', 'Broken Monitor', 1, 'Electronics', 'Disposed', 300.00, '2022-05-11', 1);",
        "INSERT INTO Assets (AssetTag, AssetName, SiteId, Category, Status, Cost, PurchaseDate, VendorId) VALUES ('AST-005', 'Standing Desk', 3, 'Furniture', 'Active', 600.00, '2024-03-05', 2);",

        
        "INSERT INTO Bills (BillId, VendorId, BillNumber, BillDate, TotalAmount) VALUES (1, 1, 'B-1001', '2024-01-15', 5000.00);",
        "INSERT INTO Bills (BillId, VendorId, BillNumber, BillDate, TotalAmount) VALUES (2, 3, 'B-1002', '2024-02-20', 12000.00);",
        "INSERT INTO Bills (BillId, VendorId, BillNumber, BillDate, TotalAmount) VALUES (3, 1, 'B-1003', '2024-04-10', 3000.00);",

        
        "INSERT INTO PurchaseOrders (POId, PONumber, VendorId, PODate, Status) VALUES (1, 'PO-2024-01', 1, '2024-05-01', 'Open');",
        "INSERT INTO PurchaseOrders (POId, PONumber, VendorId, PODate, Status) VALUES (2, 'PO-2024-02', 2, '2024-05-02', 'Closed');",
        "INSERT INTO PurchaseOrders (POId, PONumber, VendorId, PODate, Status) VALUES (3, 'PO-2024-03', 3, '2024-05-03', 'Open');",

        
        "INSERT INTO SalesOrders (SOId, SONumber, CustomerId, SODate, Status) VALUES (1, 'SO-101', 1, date('now', '-1 month'), 'Closed');",
        "INSERT INTO SalesOrders (SOId, SONumber, CustomerId, SODate, Status) VALUES (2, 'SO-102', 2, date('now', '-1 month'), 'Open');",
        "INSERT INTO SalesOrders (SOId, SONumber, CustomerId, SODate, Status) VALUES (3, 'SO-103', 1, date('now', '-2 month'), 'Closed');"
    ]
    
    for stmt in dummy_data:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"Error inserting dummy data: {e}")
            
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
