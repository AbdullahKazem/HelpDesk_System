# import requests

# # Replace these with your actual IDs
# WORKSPACE_ID = "wkspace_01K1KN589PPRF3J4S8MZ62N28R"  # From dashboard URL
# BOT_ID = "WPGTH1DN"              # From bot settings/URL
# API_KEY = "bp_bak_e840Q99rdwWufQ_AmgdYYxeOOIM-FgCt4w39"    # From Workspace → API Keys

# url = f"https://api.botpress.cloud/v1/bots/{BOT_ID}/converse"  # Remove workspace ID from domain

# response = requests.post(
#     url,
#     headers={"Authorization": f"Bearer {API_KEY}"},
#     json={"text": "Hello!", "userId": "user-123"}
# )
# print("Status Code:", response.status_code)
# print("Raw Response:", response.text)  
# print(response.json()["responses"][0]["text"])  # Bot's reply
# # Handle response
# if response.status_code == 200:
#     print("Bot replied:", response.json()["responses"][0]["text"])
# else:
#     print("Error:", response.status_code, response.text)
# # "https://cdn.botpress.cloud/webchat/v3.2/shareable.html?configUrl=https://files.bpcontent.cloud/2025/08/01/20/20250801203353-WPGTH1DN.json"
# https://cdn.botpress.cloud/webchat/v3.2/shareable.html?configUrl=https://files.bpcontent.cloud/2025/08/01/20/20250801203353-WPGTH1DN.json
import requests

BOT_ID = "WPGTH1DN"  # Confirm this matches your bot's ID
API_KEY = "bp_bak_ZtfJ_RH0Bug46jCBxblqABJoz2IflUL1fD9E"

# Correct endpoint (NO workspace ID)
url = f"https://api.botpress.cloud/v1/bots/{BOT_ID}/converse"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "text": "Hello!",
    "userId": "user-123"  # Can be any unique string
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")  # Will show raw error if any
    
    if response.status_code == 200:
        print("Success! Bot replied:", response.json()["responses"][0]["text"])
    elif response.status_code == 404:
        print("""
        ❌ 404 Error: Possible causes:
        1. Incorrect BOT_ID (current: {BOT_ID})
        2. Bot not published (go to Botpress → Publish)
        3. Invalid API endpoint (current: {url})
        """)
    else:
        print("Unexpected error:", response.text)

except Exception as e:
    print("Request failed:", str(e))