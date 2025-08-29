import requests
import re
import time
import csv
import os
import json

url = "https://astrolabe.nwnarelith.com/api/portal"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,pl;q=0.8",
    "if-none-match": '"rmfefx2kea8t5"',
    "priority": "u=1, i",
    "referer": "https://astrolabe.nwnarelith.com/portal",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-arch": "",
    "sec-ch-ua-bitness": "64",
    "sec-ch-ua-full-version": "139.0.7258.139",
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="99.0.0.0", "Google Chrome";v="139.0.7258.139", "Chromium";v="139.0.7258.139"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-model": "Nexus 5",
    "sec-ch-ua-platform": "Android",
    "sec-ch-ua-platform-version": "6.0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
}

csv_file = "visible_names.csv"

while True:
    # Reload settings from config.json each loop
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        interval = config.get("interval", 60)
        user_session_value = config.get("user-session", "")
    except Exception as e:
        print("Error loading config.json:", e)
        interval = 60
        user_session_value = ""

    cookies = {
        "phpbb3_1qw03_k": "",
        "phpbb3_1qw03_u": "8350",
        "phpbb3_1qw03_sid": "35acc0cec55bf374becba11b302f79bf",
        "cf_clearance": ".kbcT.SKXwSW4kwQS5x2hBBnTCVEdWKPMj2znD5FnRM-1756468226-1.2.1.1-BtEihFPbx1y80xAurubF1yheOJLeilFhsD3gdsyhvO78KF25xioI.4x7La0eZoRefIdhQThCnEu3jObcp1y99eAyzQrw5_81KJt54oT03Eg15tFjKr4RSLNvVinJU8_5q_3EY_SDOKyNKRXMot4gm3KDWzUm8rVI0pNIVGML6q9g7OrUqOAZpBCi5s7GentVvfcD.UV.Ex25pFrUkZF4bbRyXfJlMZbIb7Qc4.lvNtc",
        "user-session": user_session_value
    }

    # Record timestamp before making request
    timestamp = int(time.time())

    response = requests.get(url, headers=headers, cookies=cookies)

    print("Status:", response.status_code)

    if response.status_code == 200:
        text = response.text
        # Regex to capture all values of "visibleName":"..."
        names = re.findall(r'"visibleName"\s*:\s*"(.*?)"', text)

        print("Found visibleName values:")
        for name in names:
            print(name)

        # Write results to CSV
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["visibleName", "timestamp"])
            for name in names:
                writer.writerow([name, timestamp])

        print(f"Saved {len(names)} names to {csv_file} with timestamp {timestamp}")
    else:
        print("Error:", response.text)

    print(f"Waiting {interval} seconds before next request...")
    time.sleep(interval)
