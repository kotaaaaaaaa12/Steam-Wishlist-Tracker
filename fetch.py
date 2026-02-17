import requests

STEAM_ID = "76561199497975097"
URL = f"https://store.steampowered.com/wishlist/profiles/{STEAM_ID}/wishlistdata/?l=japanese"

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

r = requests.get(URL, headers=headers)

print("Status:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("First 200 chars:")
print(r.text[:200])
