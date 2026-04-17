import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_recipe_page(url):
    import cloudscraper
    import certifi
    
    # Create scraper with more advanced configuration
    from curl_cffi import requests as stealth_requests
    import certifi
    
    # List of browser identities verified for curl_cffi v0.13.0
    identities = ["chrome110", "safari15_5", "chrome101"]
    
    # Add common headers that help bypass some protections
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = None
        current_url = url
        
        # Try different identities and URL variations
        for identity in identities:
            try:
                # Try 1: As provided
                res = stealth_requests.get(current_url, headers=headers, impersonate=identity, timeout=15)
                
                # If 403/404, maybe it needs a trailing slash?
                if res.status_code in [403, 404] and not current_url.endswith('/'):
                    print(f"Retrying {current_url} with trailing slash using {identity}")
                    res = stealth_requests.get(current_url + '/', headers=headers, impersonate=identity, timeout=15)
                
                if res.status_code == 200:
                    response = res
                    break
                
                # If STILL 403/404, try Google Cache (Invisible Fallback)
                if res.status_code in [403, 404]:
                    print(f"Bypassing with Stealth Fallback for {current_url}")
                    cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{current_url}"
                    res = stealth_requests.get(cache_url, headers=headers, impersonate=identity, timeout=15)
                    if res.status_code == 200:
                        response = res
                        break

                print(f"Identity {identity} failed with {res.status_code}")
            except Exception as e:
                print(f"Identity {identity} error: {e}")
                continue

        if response is None:
            return {"error": "Advanced bot detection blocked all attempts.", "status": 403}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find JSON-LD
        json_ld = soup.find_all('script', type='application/ld+json')
        recipe_data = {}
        
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Recipe':
                            recipe_data = item
                            break
                elif data.get('@type') == 'Recipe':
                    recipe_data = data
                
                if recipe_data:
                    break
            except (json.JSONDecodeError, TypeError):
                continue

        # If we didn't find specific JSON-LD, just get the main content text
        # Clean up some tags to reduce noise
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)
        # Limit text length to avoid token limits, but keep enough context
        text = text[:15000] 
        
        return {
            "url": url,
            "raw_text": text,
            "json_ld": recipe_data
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
