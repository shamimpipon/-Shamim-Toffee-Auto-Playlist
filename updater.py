import urllib.request
import re
import json

PROBE_URL = "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8"
headers = {
    "User-Agent": "okhttp/4.11.0",
    "Referer": "https://toffeelive.com/",
    "Origin": "https://toffeelive.com",
    "X-Requested-With": "com.toffee.android"
}

def get_fresh_cookie():
    try:
        req = urllib.request.Request(PROBE_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            set_cookie = response.headers.get("Set-Cookie", "")
            match = re.search(r"Edge-Cache-Cookie=[^;]+", set_cookie)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"Error fetching live cookie: {e}")
    return "" # কোনো ব্যাকআপ ছাড়া সরাসরি খালি স্ট্রিং

fresh_cookie = get_fresh_cookie()

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
