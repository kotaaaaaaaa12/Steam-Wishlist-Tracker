import os
import requests
import json
import time

API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = "76561199497975097"  # ←自分のID64

# ① Wishlist取得
wishlist_url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
params = {
    "key": API_KEY,
    "steamid": STEAM_ID
}

r = requests.get(wishlist_url, params=params)
data = r.json()

if "response" not in data:
    print("Wishlist取得失敗")
    exit(1)

appids = [item["appid"] for item in data["response"]["items"]]

result = []

# ② 各ゲームの価格取得
for appid in appids:
    detail_url = f"https://store.steampowered.com/api/appdetails"
    detail_params = {
        "appids": appid,
        "cc": "jp",
        "l": "japanese"
    }

    res = requests.get(detail_url, params=detail_params)
    detail = res.json()

    if not detail[str(appid)]["success"]:
        continue

    app_data = detail[str(appid)]["data"]

    if "price_overview" not in app_data:
        continue

    price = app_data["price_overview"]

    discount = price["discount_percent"]
    final_price = price["final"] / 100  # 円に変換

    if discount > 0 and final_price <= 1000:
        result.append({
            "appid": appid,
            "name": app_data["name"],
            "final_price": final_price,
            "discount_percent": discount
        })

    time.sleep(1)  # レート制限回避

# ③ JSON保存
with open("wishlist_sale_under_1000.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("完了:", len(result), "件ヒット")
