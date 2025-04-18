import requests

def send_to_discord(webhook_url, content):
    data = {
        "content": content
    }
    
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message. Status code: {response.status_code}")
