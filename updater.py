import urllib.request
import urllib.error
import re
import json

def get_fresh_cookie():
    urls_to_try = [
        "https://toffeelive.com/",
        "https://toffeelive.com/live",
        "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://toffeelive.com/",
        "Origin": "https://toffeelive.com",
        "X-Requested-With": "com.toffee.android"
    }

    for probe_url in urls_to_try:
        try:
            req = urllib.request.Request(probe_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                set_cookie = response.headers.get("Set-Cookie", "")
                match = re.search(r"Edge-Cache-Cookie=[^;]+", set_cookie)
                if match:
                    print(f"Fetched cookie from {probe_url}")
                    return match.group(0)
        except urllib.error.HTTPError as e:
            # ৪০৩ বা রিডাইরেক্ট হেডার্স থেকেও কুকি রিড করা হবে
            set_cookie = e.headers.get("Set-Cookie", "") if e.headers else ""
            match = re.search(r"Edge-Cache-Cookie=[^;]+", set_cookie)
            if match:
                print(f"Fetched cookie from error headers of {probe_url}")
                return match.group(0)
        except Exception as e:
            print(f"Error probing {probe_url}: {e}")

    return ""

fresh_cookie = get_fresh_cookie()
print(f"Active Live Cookie: {fresh_cookie}")

channels = [
    {
        "category": "LIVE",
        "name": "TOFFEE Sports VIP",
        "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8",
        "logo": "https://images.toffeelive.com/images/program/19779/logo/240x240/mobile_logo_975410001725875598.png",
        "cookie": fresh_cookie,
        "user_agent": "okhttp/4.11.0",
        "referer": "https://toffeelive.com/",
        "origin": "https://toffeelive.com"
    },
    {
        "category": "News Channel",
        "name": "Somoy TV",
        "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8",
        "logo": "https://images.toffeelive.com/images/program/340/logo/240x240/mobile_logo_094417001655891123.png",
        "cookie": fresh_cookie,
        "user_agent": "okhttp/4.11.0",
        "referer": "https://toffeelive.com/",
        "origin": "https://toffeelive.com"
    }
]

with open("toffee_NS_Player.m3u", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print("Playlist generated successfully!")
