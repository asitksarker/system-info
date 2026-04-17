from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Simple in-memory storage (clears if server restarts)
fleet_data = {}

# Minimal HTML template to display the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f4f4f9; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #333; color: white; }
        .online { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Connected Devices</h1>
    <table>
        <tr>
            <th>Machine ID</th>
            <th>OS Version</th>
            <th>Public IP</th>
            <th>MAC</th>
            <th>Location</th>
            <th>Last Seen</th>
        </tr>
        {% for id, info in devices.items() %}
        <tr>
            <td>{{ id }}</td>
            <td>{{ info.os }}</td>
            <td>{{ info.public_ip }}</td>
            <td>{{ info.mac }}</td>
            <td>{{ info.city }} ({{ info.isp }})</td>
            <td><span class="online">{{ info.last_seen }}</span></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def init_db():
    conn = sqlite3.connect('fleet.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  machine_id TEXT, os TEXT, public_ip TEXT, 
                  city TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.json
    conn = sqlite3.connect('fleet.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (machine_id, os, public_ip, city, timestamp) VALUES (?, ?, ?, ?, ?)",
              (data['machine_id'], data['os'], data['public_ip'], data['city'], data['last_seen']))
    conn.commit()
    conn.close()
    return {"status": "success"}, 200

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, devices=fleet_data)

if __name__ == "__main__":
    # run on 0.0.0.0 to allow other machines on network to connect
    app.run(host='0.0.0.0', port=5000)