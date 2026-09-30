import os
import requests
import json
import time

API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = "76561199497975097"

wishlist_url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/"

# get my wishlist
r = requests.get(
    wishlist_url,
    params={"key": API_KEY, "steamid": STEAM_ID},
    timeout=10
)

data = r.json()

if "response" not in data:
    print("Failed to get wishlist")
    exit(1)

items = data["response"]["items"]
results = []

for item in items:
    appid = item["appid"]

    try:
        r = requests.get(
            "https://store.steampowered.com/api/appdetails",
            params={
                "appids": appid,
                "cc": "jp",
                "l": "japanese"
            },
            timeout=10
        )

        r.raise_for_status()
        info = json.loads(r.content.decode("utf-8-sig"))

    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Failed to get {appid}: {e}")
        time.sleep(1)
        continue

    game = info.get(str(appid))

    if not game or not game.get("success"):
        time.sleep(1)
        continue

    game = game.get("data", {})
    price = game.get("price_overview")

    # free games / games without a price
    if not price:
        time.sleep(1)
        continue

    discount = price["discount_percent"]
    final_price = price["final"] / 100

    if discount > 0 and final_price <= 1000:
        results.append({
            "appid": appid,
            "name": game["name"],
            "final_price": final_price,
            "discount_percent": discount
        })

    time.sleep(1)

with open("wishlist_sale_under_1000.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Done. Found {len(results)} games.")
