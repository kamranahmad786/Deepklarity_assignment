import urllib.request
import ssl

url = "https://www.simplyrecipes.com/recipes/best_lasagna/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f"Testing with urllib.request: {url}")
try:
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=context, timeout=20) as response:
        print(f"Status: {response.getcode()}")
        print(f"Length: {len(response.read())}")
        print("Success!")
except Exception as e:
    print(f"Failed: {e}")
