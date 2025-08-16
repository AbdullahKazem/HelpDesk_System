import requests

BOT_ID = "WPGTH1DN"
API_KEY = "bp_bak_ZtfJ_RH0Bug46jCBxblqABJoz2IflUL1fD9E"

def full_diagnostic():
    base_urls = [
        "https://api.botpress.cloud",
        "https://api.eu.botpress.cloud"
    ]
    
    endpoints = [
        "/v1/bots",
        f"/v1/bots/{BOT_ID}",
        f"/v1/bots/{BOT_ID}/converse"
    ]
    
    for base in base_urls:
        print(f"\nTesting {base}:")
        for endpoint in endpoints:
            url = base + endpoint
            try:
                response = requests.get(
                    url,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    timeout=5
                )
                print(f"{url} → {response.status_code}")
                if response.status_code == 200:
                    print(f"Bot Name: {response.json().get('name')}")
            except Exception as e:
                print(f"{url} → Error: {str(e)}")

full_diagnostic()