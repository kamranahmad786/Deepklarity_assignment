from curl_cffi import requests

urls = [
    "https://www.allrecipes.com/recipe/11679/homemade-macaroni-and-cheese/",
    "https://www.simplyrecipes.com/recipes/best_lasagna/",
    "https://www.foodnetwork.com/recipes/tyler-florence/the-ultimate-baked-macaroni-and-cheese-recipe-1941655"
]

for url in urls:
    print(f"\nTesting: {url}")
    try:
        # impersonate='chrome120' mimics the TLS/HTTP fingerprint of Chrome 120
        response = requests.get(url, impersonate="chrome120", timeout=20)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"SUCCESS! Length: {len(response.text)}")
            if "application/ld+json" in response.text:
                print("JSON-LD found.")
        else:
            print(f"FAILED: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
