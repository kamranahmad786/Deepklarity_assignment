from curl_cffi import requests
import json

url = "https://www.simplyrecipes.com/recipes/best_lasagna/"

print(f"Testing with curl_cffi: {url}")
try:
    # impersonate='chrome120' mimics the TLS/HTTP fingerprint of Chrome 120
    response = requests.get(url, impersonate="chrome120", timeout=20)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Success! Content length: {len(response.text)}")
        # Check for JSON-LD to confirm it's the real deal
        if "application/ld+json" in response.text:
            print("Verified: Recipe JSON-LD found.")
        else:
            print("Page loaded but no JSON-LD found.")
    else:
        print(f"Failed with status: {response.status_code}")
except Exception as e:
    print(f"Failed with error: {e}")
