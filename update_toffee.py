import json
import os
import requests
from datetime import datetime

def generate_toffee_playlist():
    print("🔄 Fetching latest Toffee channels & cookies...")
    SOURCE_URL = "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/main/toffee_channel_data.json"
    
    try:
        response = requests.get(SOURCE_URL, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            output_data = {
                "name": "Shamim Live TV - Toffee Auto Updated Playlist",
                "owner": "Shamim Pipon",
                "channels_amount": data.get("channels_amount", 0),
                "updated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "channels": data.get("channels", [])
            }
            
            with open("toffee_channel_data.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print("✅ 'toffee_channel_data.json' successfully generated!")

            m3u_content = "#EXTM3U\n"
            for ch in data.get("channels", []):
                name = ch.get("name", "Unknown")
                link = ch.get("link", "")
                logo = ch.get("logo", "")
                category = ch.get("category_name", "LIVE")
                headers = ch.get("headers", {})
                cookie = headers.get("cookie", "")
                ua = headers.get("user-agent", "okhttp/4.11.0")

                m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
                if cookie:
                    m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
                m3u_content += f'#EXTVLCOPT:http-referrer=https://toffeelive.com/\n'
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n'
                m3u_content += f'{link}\n\n'

            with open("toffee_playlist.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("✅ 'toffee_playlist.m3u' successfully generated!")

    except Exception as e:
        print(f"❌ Error updating playlist: {e}")

if __name__ == "__main__":
    generate_toffee_playlist()
