import requests
import json

STEAM_ID = "76561199497975097"
URL = f"https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/?l=japanese"

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)
data = r.json()

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
