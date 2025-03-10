from mitmproxy import http
import json
import os

# Target API requests
START_API = "https://prodapi.metweb.ie/observations/dublin/today"
STOP_API = "https://maps.google.com/maps-api-v3/api/js/59/8/map.js"

# Directory and file path for saving logs
LOG_DIR = r"D:/albertson"
LOG_FILE = os.path.join(LOG_DIR, "network_log2.json")

# Flag to check whether we are recording logs
recording = False
logs = []

def request(flow: http.HTTPFlow):
    global recording, logs

    url = flow.request.url
    method = flow.request.method
    print(f"🔍 Inspecting request: {flow.request.url}")

    # Start recording when the START_API request is detected
    if START_API in url and method == "GET":
        recording = True
        logs.clear()  # Reset logs
        print(f"✅ Started capturing network logs at: {url}")

    # Capture logs if recording is enabled
    if recording:
        log_entry = {
            "url": flow.request.url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            # "query_params": dict(flow.request.urlencoded_form),
            "query_params": dict(flow.request.query),
            "timestamp": flow.request.timestamp_start
        }
        logs.append(log_entry)
        print(f"[LOG] Captured request: {method} {url}")

    # Stop recording when STOP_API request is detected
    if STOP_API in url and method == "GET" and recording:
        recording = False
        print(f"🛑 Stopped capturing network logs at: {url}")
        save_logs()  # Save logs to a file

def save_logs():
    """Save captured logs to a JSON file."""
    try:
        # Ensure directory exists
        if not os.path.exists(LOG_DIR):
            print(f"[INFO] Directory {LOG_DIR} does not exist. Creating it...")
            os.makedirs(LOG_DIR)

        # Save logs to the file
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        print(f"📄 Network logs saved to '{LOG_FILE}'")
    except Exception as e:
        print(f"[ERROR] Failed to save logs: {e}")
