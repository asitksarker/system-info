import platform
import uuid
import requests
from getmac import get_mac_address

def fetch_system_info():
    print("--- Local System Information ---")
    
    # 1. OS Version using 'platform'
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    print(f"OS Version: {os_info}")

    # 2. MAC Address using 'getmac'
    # fetches the MAC address of the default interface
    mac = get_mac_address()
    print(f"MAC Address: {mac}")

    # 3. Unique Identifier using 'uuid'
    # Provides a unique ID for the current execution/machine context
    unique_id = uuid.uuid4()
    print(f"Session UUID: {unique_id}")

    print("\n--- Network & Location Information ---")
    try:
        # 4. Public IP, ISP, and Location using 'requests'
        # use ip-api.com (JSON) for a comprehensive fetch
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()

        if data['status'] == 'success':
            print(f"Public IP:  {data.get('query')}")
            print(f"ISP:        {data.get('isp')}")
            print(f"Location:   {data.get('city')}, {data.get('regionName')}, {data.get('country')}")
            print(f"Lat/Lon:    {data.get('lat')}, {data.get('lon')}")
        else:
            print("Error: Could not retrieve location data.")
            
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    fetch_system_info()