import platform
import uuid
import requests
from getmac import get_mac_address
import time

# Configuration: Replace with your Server's IP address
SERVER_URL = "http://127.0.0.1:5000/report"

def collect_data():
    try:
        # Get location/network data
        net_data = requests.get("http://ip-api.com/json/", timeout=5).json()
    except:
        net_data = {}

    return {
        "machine_id": str(uuid.getnode()), # Uses hardware-based ID
        "os": f"{platform.system()} {platform.release()}",
        "mac": get_mac_address(),
        "public_ip": net_data.get("query", "N/A"),
        "isp": net_data.get("isp", "N/A"),
        "city": net_data.get("city", "Unknown"),
        "last_seen": time.ctime()
    }

def send_report():
    data = collect_data()
    try:
        response = requests.post(SERVER_URL, json=data, timeout=5)
        print(f"Report sent! Server status: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    # In a real scenario, you'd put this in a loop or a cron job
    send_report()