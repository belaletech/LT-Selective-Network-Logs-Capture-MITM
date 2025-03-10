# Capturing Network Logs for LambdaTest Real Device Native App Automation

## **Use Case**
We need to capture **3-5 minutes** of network logs during an **8-minute test execution** for **LambdaTest real device native app automation**.

## **Requirements**
1. **Capture network logs** using **LT Tunnel and MITM Proxy** setup.
2. **Start recording** network logs when a specific API request is detected:
   - **Start API Request:** `https:xyz`
3. **Stop recording** network logs when a specific API request is detected:
   - **Stop API Request:** `https:abc`

## **Proposed Approach**
- **Set up MITM Proxy locally** to intercept and log network traffic.
- **Configure LT Tunnel** to route traffic through the proxy.
- **Apply filtering logic:**
  - Start capturing logs when the request URL matches the **Start API**.
  - Stop capturing logs when the request URL matches the **Stop API**.

## **Setup Instructions**

### **Step 1: Install MITM Proxy**
#### **Windows**
Download the MITM Proxy installer from [here](https://downloads.mitmproxy.org/11.1.3/mitmproxy-11.1.3-windows-x86_64-installer.exe) and install it.

#### **Mac/Linux**
Install MITM Proxy using the following command:
```sh
brew install mitmproxy  # macOS
sudo apt install mitmproxy  # Linux
```

### **Step 2: Configure Proxy Settings**
1. Open the proxy settings on your laptop.
2. Set the proxy address to `localhost` and port to `8181` (or any other preferred port).
3. Start MITM Proxy using the command:
   ```sh
   mitmproxy --listen-port 8181
   ```
4. Download and install the MITM certificate from `http://mitm.it/`.

### **Step 3: Setup Python Script for Network Logging**
Install dependencies:
```sh
pip install mitmproxy
```

Create a Python script (`filter_logs.py`):
```python
from mitmproxy import http
import json
import os

# Target API requests
START_API = "https:xyz"
STOP_API = "https:abc"

# Directory and file path for saving logs
LOG_DIR = r"D:/network_logs"
LOG_FILE = os.path.join(LOG_DIR, "network_log.json")

# Flag to check whether we are recording logs
recording = False
logs = []

def request(flow: http.HTTPFlow):
    global recording, logs
    url = flow.request.url
    method = flow.request.method
    
    if START_API in url and method == "GET":
        recording = True
        logs.clear()  # Reset logs
        print(f"✅ Started capturing network logs at: {url}")

    if recording:
        log_entry = {
            "url": flow.request.url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            "query_params": dict(flow.request.query),
            "timestamp": flow.request.timestamp_start
        }
        logs.append(log_entry)

    if STOP_API in url and method == "GET" and recording:
        recording = False
        print(f"🛑 Stopped capturing network logs at: {url}")
        save_logs()

def save_logs():
    """Save captured logs to a JSON file."""
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        print(f"📄 Network logs saved to '{LOG_FILE}'")
    except Exception as e:
        print(f"[ERROR] Failed to save logs: {e}")
```

### **Step 4: Start Network Logging**
Run the following command to start MITM Proxy and log network requests:
```sh
mitmdump -s filter_logs.py --listen-port 8181
```

### **Step 5: Start LambdaTest Tunnel**
Use the following command to start the LambdaTest tunnel with proxy settings:
```sh
LT --user <your-email> --key <your-access-key> \
   --proxy-host localhost --proxy-port 8181 \
   --ingress-only --tunnelName MyTunnel
```
Replace `<your-email>` and `<your-access-key>` with your LambdaTest credentials.

### **Step 6: Start Your Test with Tunnel**
Once the tunnel is running, start your test execution. The logs will be captured and stored in `D:/network_logs/network_log.json`.

## **Conclusion**
This setup allows selective network logging during automation tests, ensuring only relevant traffic is captured. You can modify the script to fit your use case.

