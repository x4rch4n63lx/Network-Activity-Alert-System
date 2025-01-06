# ===================================================================================
# Created By     : x_4rch4n63l_x
# Created On     : 1/5/2025 - 9:50PM 
# Script Purpose : Network Activity Alert System coded in Python using psutil
# Description    : This script provides real-time monitoring of network traffic, specifically:
#                  1. Displays download and upload rates in Mbps.
#                  2. Updates network statistics every second.
#                  3. Formats and prints network traffic data in a user-friendly manner.
#                  4. Sends alerts to Discord when thresholds are exceeded.
#
# Features       : 
#                  - Real-time network traffic monitoring.
#                  - Clear display of download and upload speeds.
#                  - Continuous update of network statistics for precise monitoring.
#                  - Sends alerts to Discord when network activity exceeds defined thresholds.
#
# Requirements   :
#                  - Install the psutil library using: pip install psutil
#                  - Install the requests library using: pip install requests
# ===================================================================================
import psutil
import time
import requests

WEBHOOK_URL = "WEBHOOK_URL"

CONNECTION_THRESHOLD = 10
DOWNLOAD_THRESHOLD = 100.0  # Mbps
UPLOAD_THRESHOLD = 100.0  # Mbps

def send_alert(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Alert sent to Discord!")
    else:
        print(f"Failed to send alert to Discord. Response code: {response.status_code}")

def convert_to_mbps(bytes):
    return bytes / 1024 / 1024 * 8

def main():
    interval = 1
    print(f"{'Time':<20} {'Download (Mbps)':<20} {'Upload (Mbps)':<20} {'Connections':<20}")
    
    while True:
        net_io_start = psutil.net_io_counters()
        connections_start = len(psutil.net_connections())
        
        time.sleep(interval)
        
        net_io_end = psutil.net_io_counters()
        connections_end = len(psutil.net_connections())

        download_rate = convert_to_mbps(net_io_end.bytes_recv - net_io_start.bytes_recv) / interval
        upload_rate = convert_to_mbps(net_io_end.bytes_sent - net_io_start.bytes_sent) / interval
        connections = connections_end - connections_start

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"{current_time:<20} {download_rate:<20.2f} {upload_rate:<20.2f} {connections:<20}")

        if connections > CONNECTION_THRESHOLD or download_rate > DOWNLOAD_THRESHOLD or upload_rate > UPLOAD_THRESHOLD:
            alert_message = (
                f"High activity detected:\n"
                f"Time: {current_time}\n"
                f"Download rate: {download_rate:.2f} Mbps\n"
                f"Upload rate: {upload_rate:.2f} Mbps\n"
                f"Connections: {connections}\n"
            )
            send_alert(alert_message)

if __name__ == '__main__':
    main()
