"""
This module handles sending messages to a Discord channel via webhook.
"""

import requests

def send_to_discord(webhook_url, content):
    """
    Send a message to a Discord webhook.
    """
    data = {
        "content": content
    }

    response = requests.post(webhook_url, json=data, timeout=10)

    if response.status_code == 204:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message. Status code: {response.status_code}")
