import requests
import json

STEAM_ID = "76561199497975097"
URL = f"https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/?l=japanese"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://store.steampowered.com/",
}

try:
    r = requests.get(URL, headers=headers, timeout=10)
    print("Status Code:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))
    print("First 300 chars of response:")
    print(r.text[:300])

    if "application/json" not in r.headers.get("Content-Type", ""):
        print("Response is not JSON. Aborting.")
        exit(0)

    data = r.json()

except Exception as e:
    print("Request failed:", e)
    exit(0)

result = []

for appid, info in data.items():
    if info.get("discount_pct", 0) > 0:
        discounted_price = info.get("discounted_price")
        if discounted_price and discounted_price <= 100000:
            result.append({
                "appid": appid,
                "name": info.get("name"),
                "discount_pct": info.get("discount_pct"),
                "discounted_price": discounted_price / 100
            })

with open("wishlist_sale_under_1000.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("JSON generated successfully.")
