from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Storage: { "machine_id": [report1, report2, ...] }
fleet_history = {}

# --- HTML Templates ---

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Fleet Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f4f4f9; }
        table { width: 100%; border-collapse: collapse; background: white; cursor: pointer; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #2c3e50; color: white; }
        tr:hover { background-color: #f1f1f1; }
        .status { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Active Fleet Status</h1>
    <p><i>Click any row to view full report history for that device.</i></p>
    <table>
        <tr>
            <th>Machine ID</th>
            <th>Latest OS</th>
            <th>Public IP</th>
            <th>Last Check-in</th>
            <th>Reports</th>
        </tr>
        {% for id, reports in devices.items() %}
        {% set latest = reports[-1] %}
        <tr onclick="window.location='/history/{{ id }}';">
            <td>{{ id }}</td>
            <td>{{ latest.os }}</td>
            <td>{{ latest.public_ip }}</td>
            <td><span class="status">{{ latest.last_seen }}</span></td>
            <td>{{ reports|length }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

HISTORY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Device History</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 40px; }
        .back-btn { display: inline-block; margin-bottom: 20px; text-decoration: none; color: #3498db; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ddd; font-size: 0.9em; }
        th { background: #ecf0f1; }
    </style>
</head>
<body>
    <a list-btn class="back-btn" href="/">← Back to Dashboard</a>
    <h1>History for Machine: {{ machine_id }}</h1>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Public IP</th>
            <th>MAC</th>
            <th>ISP</th>
            <th>Location</th>
        </tr>
        {% for report in history|reverse %}
        <tr>
            <td>{{ report.last_seen }}</td>
            <td>{{ report.public_ip }}</td>
            <td>{{ report.mac}}</td>
            <td>{{ report.isp }}</td>
            <td>{{ report.city }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# --- Routes ---

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.json
    machine_id = data.get("machine_id")
    
    # Initialize list if machine is new, then append the report
    if machine_id not in fleet_history:
        fleet_history[machine_id] = []
    
    fleet_history[machine_id].append(data)
    
    # Optional: Keep only the last 50 reports to save memory
    if len(fleet_history[machine_id]) > 50:
        fleet_history[machine_id].pop(0)
        
    return {"status": "success"}, 200

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, devices=fleet_history)

@app.route('/history/<machine_id>')
def view_history(machine_id):
    history = fleet_history.get(machine_id, [])
    return render_template_string(HISTORY_HTML, machine_id=machine_id, history=history)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)