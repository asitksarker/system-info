# system-info
Centralized Monitoring Dashboard:

Python based  management system. It consists of a Server that hosts a web dashboard and agents that run on remote machines to report system information and geographic location.


Key Features:

Real-time Dashboard: A Flask-based web interface showing the latest status of all connected assets.

Audit Persistence: Full historical telemetry stored in a permanent SQLite database for forensic investigation.

Threat Detection: Agent-side scanning for tools and suspicious processes (e.g., Mimikatz, Netcat)

Prerequisites:
Python 3.8+ 

1. Required Libraries
flask: Powers the web dashboard and API.

requests: Handles data transmission and Discord alerting.

get-mac: Robust hardware identifier retrieval.

psutil: Deep system and process monitoring.

Setup & Configuration
1. Configure Secrets
Open config.py and provide your settings:
DB_NAME = "fleet.db"

Run python server.py
Dashboard: http://localhost:5000

run python agent.py on machines to monitor
