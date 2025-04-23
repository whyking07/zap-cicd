from zapv2 import ZAPv2
from requests.auth import HTTPBasicAuth
from datetime import datetime
import requests
import json
import os
import time
 
# === CONFIG ===
API_KEY = 'tree9bcbidk9o0t8gamt77ccvs'
ZAP = ZAPv2(apikey=API_KEY, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})
TARGET = 'http://localhost:8000'
USERNAME = 'admin'
PASSWORD = 'pass123'
 
# === Timestamp & Report File Setup ====
timestammp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_path = os.path.join('zap_reports', f'zap_auth_scan_{timestammp}.html')
os.makedirs('zap_reports',exist_ok=True)
 
# 1. Make Auth Req (Prime ZAP's session)
print("[*] Making authenticated request to /private to prime session...")
requests.get(f"{TARGET}/private", auth=HTTPBasicAuth(USERNAME,PASSWORD), proxies = {
    "http": "http://127.0.0.1:8090"
})
# ===2. Start the Spider ====
print("[*] Starting the Spider...")
scan_id = ZAP.spider.scan(TARGET)
 
while int(ZAP.spider.status(scan_id)) < 100:
    print(f"Spider progress: {ZAP.spider.status(scan_id)}%")
    time.sleep(2)
 
print("Spider complete")
# PAssive Scan
while int(ZAP.pscan.records_to_scan) > 0:
    print(f"  Waiting for passive scanning... {ZAP.pscan.records_to_scan} records remaining.")
    time.sleep(2)
 
# === STEP 4: Active scan ===
print("[*] Starting active scan...")
ascan_id = ZAP.ascan.scan(TARGET)
while int(ZAP.ascan.status(ascan_id)) < 100:
    print(f"  Active scan progress: {ZAP.ascan.status(ascan_id)}%")
    time.sleep(5)
 
# === STEP 5: Print and Save Alerts ===
alerts = ZAP.core.alerts(baseurl=TARGET)
print(f"\n[✓] Total Alerts Found: {len(alerts)}")
for alert in alerts:
    print(f"- {alert['alert']} ({alert['risk']}) @ {alert['url']}")
 
# === STEP 6: Save JSON and HTML Reports ===
with open(f'zap_reports/zap_alerts_{timestammp}.json', 'w') as f:
    json.dump(alerts, f, indent=2)
 
# HTML Report (simple version)
html_report = ZAP.core.htmlreport()
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html_report)