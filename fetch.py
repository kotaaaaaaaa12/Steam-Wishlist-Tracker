import os
import requests
import json
import time

API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = "76561199497975097"

# ① Wishlist取得
wishlist_url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
params = {
    "key": API_KEY,
    "steamid": STEAM_ID
}

r = requests.get(wishlist_url, params=params, timeout=10)
data = r.json()

if "response" not in data:
    print("Wishlist取得失敗")
    exit(1)

appids = [item["appid"] for item in data["response"]["items"]]
result = []

# ② 各ゲームの価格取得
for appid in appids:
    detail_url = "https://store.steampowered.com/api/appdetails"
    detail_params = {
        "appids": appid,
        "cc": "jp",
        "l": "japanese"
    }

    try:
        res = requests.get(detail_url, params=detail_params, timeout=10)
        res.raise_for_status()
        detail = json.loads(res.content.decode('utf-8-sig'))
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"[SKIP] appid={appid} 取得失敗: {e}")
        time.sleep(1)
        continue

    app_info = detail.get(str(appid))
    if app_info is None:
        print(f"[SKIP] appid={appid} レスポンスにキーなし")
        time.sleep(1)
        continue

    if not app_info.get("success"):
        time.sleep(1)
        continue

    app_data = app_info.get("data", {})
    if "price_overview" not in app_data:
        time.sleep(1)
        continue

    price = app_data["price_overview"]
    discount = price["discount_percent"]
    final_price = price["final"] / 100

    if discount > 0 and final_price <= 1000:
        result.append({
            "appid": appid,
            "name": app_data["name"],
            "final_price": final_price,
            "discount_percent": discount
        })

    time.sleep(1)

# ③ JSON保存
with open("wishlist_sale_under_1000.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("完了:", len(result), "件ヒット")
