import cloudscraper
import certifi

url = "https://www.foodnetwork.com/recipes/tyler-florence/macaroni-and-cheese-recipe-1915846"
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',
        'desktop': True
    }
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
}

print(f"Testing URL: {url}")
try:
    response = scraper.get(url, headers=headers, timeout=20, verify=certifi.where())
    print(f"Status: {response.status_code}")
    print(f"Length: {len(response.text)}")
    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Failed with text snippet: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
