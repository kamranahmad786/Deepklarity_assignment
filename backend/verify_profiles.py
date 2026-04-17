from curl_cffi import requests

# curl_cffi v0.13.0 common profiles
profiles = ["chrome110", "chrome101", "safari15_5"]
urls = [
    "https://www.simplyrecipes.com/recipes/best_lasagna/",
    "https://www.allrecipes.com/recipe/11679/homemade-macaroni-and-cheese/"
]

for url in urls:
    print(f"\n--- Testing: {url} ---")
    for profile in profiles:
        try:
            print(f"Trying profile: {profile}")
            res = requests.get(url, impersonate=profile, timeout=15)
            print(f"  Status: {res.status_code}")
            if res.status_code == 200:
                print(f"  SUCCESS with {profile}")
                break
        except Exception as e:
            print(f"  Error with {profile}: {e}")
