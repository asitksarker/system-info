import sqlite3
from config import DB_NAME

def get_db_connection():
    """Utility to create a database connection with Row factory."""
    conn = sqlite3.connect(DB_NAME)
    # This allows us to access columns by name (row['os']) 
    # instead of index (row[2])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the necessary tables if they don't exist."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                machine_id TEXT, 
                os TEXT, 
                public_ip TEXT, 
                mac TEXT,
                isp TEXT,
                city TEXT, 
                threats TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_report(data):
    """Inserts a new telemetry report into the database."""
    # Convert the list of threats into a single string for storage
    threat_string = ", ".join(data.get('threats', []))
    
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO reports (machine_id, os, public_ip, mac, isp, city, threats) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('machine_id'), 
            data.get('os'), 
            data.get('public_ip'), 
            data.get('mac'), 
            data.get('isp'), 
            data.get('city'), 
            threat_string
        ))
        conn.commit()

def get_latest_reports():
    """Fetches the most recent report for every unique machine."""
    query = """
    SELECT * FROM reports 
    WHERE id IN (SELECT MAX(id) FROM reports GROUP BY machine_id)
    ORDER BY timestamp DESC
    """
    with get_db_connection() as conn:
        return conn.execute(query).fetchall()

def get_history(machine_id):
    """Fetches the full audit trail for a specific machine."""
    query = "SELECT * FROM reports WHERE machine_id = ? ORDER BY timestamp DESC"
    with get_db_connection() as conn:
        return conn.execute(query, (machine_id,)).fetchall()