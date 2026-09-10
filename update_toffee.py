import json
import os
import requests
import sys
from datetime import datetime

def generate_toffee_playlist():
    print("🔄 Fetching latest Toffee channels & cookies...")
    SOURCE_URL = "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/main/toffee_channel_data.json"
    
    try:
        response = requests.get(SOURCE_URL, timeout=30)
        response.raise_for_status()  # ✅ 4xx/5xx error ধরবে
        
        data = response.json()
        channels = data.get("channels", [])
        
        if not channels:
            print("❌ No channels found in source!")
            sys.exit(1)  # ✅ GitHub Actions কে জানাবে fail হয়েছে

        output_data = {
            "name": "Shamim Live TV - Toffee Auto Updated Playlist",
            "owner": "Shamim Pipon",
            "channels_amount": len(channels),  # ✅ actual count
            "updated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "channels": channels
        }
        
        with open("toffee_channel_data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"✅ 'toffee_channel_data.json' saved! ({len(channels)} channels)")

        m3u_content = "#EXTM3U\n"
        skipped = 0
        
        for ch in channels:
            name = ch.get("name", "Unknown")
            link = ch.get("link", "").strip()
            logo = ch.get("logo", "")
            category = ch.get("category_name", "LIVE")
            headers = ch.get("headers", {})
            cookie = headers.get("cookie", "")
            ua = headers.get("user-agent", "okhttp/4.11.0")

            if not link:  # ✅ empty link স্কিপ
                skipped += 1
                continue

            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            if cookie:
                m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
            m3u_content += f'#EXTVLCOPT:http-referrer=https://toffeelive.com/\n'
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n'
            m3u_content += f'{link}\n\n'

        with open("toffee_playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print(f"✅ 'toffee_playlist.m3u' saved! (skipped {skipped} empty links)")

    except requests.exceptions.Timeout:
        print("❌ Request timed out!")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_toffee_playlist()
