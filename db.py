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
    with get_db_connection() as conn:
        # 1. Reports Table (No threats column anymore)
        conn.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            machine_id TEXT, alias TEXT, os TEXT, public_ip TEXT, mac TEXT, 
            isp TEXT, city TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # 2. Threats Table (Foreign Key to reports)
        conn.execute('''CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            process_name TEXT,
            pid INTEGER,
            username TEXT,
            FOREIGN KEY(report_id) REFERENCES reports(id)
        )''')
        conn.commit()

def rename_machine(machine_id, new_alias):
    """Updates the alias for every report associated with this machine ID."""
    with get_db_connection() as conn:
        conn.execute("UPDATE reports SET alias = ? WHERE machine_id = ?", (new_alias, machine_id))
        conn.commit()

def save_report(data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Look up existing alias first
        existing = conn.execute("SELECT alias FROM reports WHERE machine_id = ? AND alias IS NOT NULL LIMIT 1", 
                                (data.get('machine_id'),)).fetchone()
        current_alias = existing['alias'] if existing else None

        cursor.execute('''INSERT INTO reports (machine_id, alias, os, public_ip, mac, isp, city) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (data.get('machine_id'), current_alias, data.get('os'), 
                        data.get('public_ip'), data.get('mac'), data.get('isp'), data.get('city')))
        
        # 2. Get the ID of the report we just created
        report_id = cursor.lastrowid
        
        # 3. Insert each threat into the threats table
        threats = data.get('threats', [])
        for t in threats:
            cursor.execute('''INSERT INTO threats (report_id, process_name, pid, username) 
                              VALUES (?, ?, ?, ?)''', 
                           (report_id, t.get('name'), t.get('pid'), t.get('username')))
        conn.commit()

def get_latest_reports():
    """Fetches the most recent report for every machine and checks for threats."""
    query = """
    SELECT r.*, 
           (SELECT COUNT(*) FROM threats t WHERE t.report_id = r.id) AS threat_count
    FROM reports r
    WHERE r.id IN (SELECT MAX(id) FROM reports GROUP BY machine_id)
    ORDER BY r.timestamp DESC
    """
    with get_db_connection() as conn:
        return conn.execute(query).fetchall()

def get_history(machine_id):
    query = """
    SELECT r.timestamp, r.public_ip, r.mac, r.city, r.alias, t.process_name, t.pid, t.username
    FROM reports r
    LEFT JOIN threats t ON r.id = t.report_id
    WHERE r.machine_id = ?
    ORDER BY r.timestamp DESC
    """
    with get_db_connection() as conn:
        return conn.execute(query, (machine_id,)).fetchall()