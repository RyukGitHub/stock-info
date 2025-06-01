import requests
import os

def send_csv_to_discord_webhook(file_path, message="Here is today's stock report!"):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL not set in environment variables.")
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "text/csv")}
        data = {"content": message}
        response = requests.post(webhook_url, data=data, files=files)
        if response.status_code in (200, 204):
            print("CSV sent to Discord successfully.")
        else:
            print(f"Failed to send CSV to Discord: {response.status_code} {response.text}")
