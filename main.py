import sqlite3
from fastmcp import FastMCP

mcp = FastMCP(name="expense tracker")


DB_PATH = "remote_expense.db"
RESOURCE_PATH = "categories.json"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS expense(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     date TEXT NOT NULL,
                     amount REAL NOT NULL,
                     category TEXT NOT NULL,
                     subcategory TEXT DEFAULT '',
                     note TEXT DEFAULT ''
                     )

        """)

init_db()


@mcp.tool
def add_expense(date: str, amount: float, category: str, subcategory: str = '', note: str=''):
    "This tool add expense to the database"
    with get_connection() as conn:
        curr =  conn.execute(
            """
                INSERT INTO expense(date, amount, category, subcategory, note) VALUES(?, ?, ?, ?, ?)

            """,
            (date, amount, category, subcategory, note)
        )
        
        return {"status": "ok", "id": curr.lastrowid}
    

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(RESOURCE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(
        transport='http',
        host = "0.0.0.0",
        port= 8000
    )
