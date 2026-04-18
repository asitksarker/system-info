import platform
import uuid
import requests
from getmac import get_mac_address
import time
import psutil

# Configuration: Replace with your Server's IP address
SERVER_URL = "http://127.0.0.1:5000/report"

def collect_data():
    #scan processes
    threats = get_suspicious_processes()

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
        "last_seen": time.ctime(),
        "threats": threats
    }

def send_report():
    data = collect_data()
    try:
        response = requests.post(SERVER_URL, json=data, timeout=5)
        print(f"Report sent! Server status: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")

def get_suspicious_processes():
    # A list of tools often used by attackers after they get inside
    blacklist = ['netcat', 'ncat', 'mimikatz', 'wireshark', 'powershell.exe']
    found = []
    
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in blacklist:
                found.append({
                    "name": proc.info['name'],
                    "pid": proc.info.get('pid'),
                    "username": proc.info.get('username') or "N/A"
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found

if __name__ == "__main__":
    send_report()
   
    
    