import json
import os
import requests
from datetime import datetime

# ১. আমাদের নিজেদের স্থায়ী চ্যানেল ডাটাবেজ (সকল ৭৫টি চ্যানেল)
BASE_CHANNELS = [
    {"name": "TOFFEE Sports VIP", "category": "LIVE", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/19779/logo/240x240/mobile_logo_975410001725875598.png"},
    {"name": "TOFFEE Movies VIP", "category": "LIVE", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_movie/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/2708/logo/240x240/mobile_logo_724353001725875591.png"},
    {"name": "TOFFEE Dramas VIP", "category": "LIVE", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_drama/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/44878/logo/240x240/mobile_logo_764950001725875605.png"},
    {"name": "CNN VIP", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cnn/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/333/logo/240x240/mobile_logo_146607001735536058.png"},
    {"name": "Somoy TV", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png"},
    {"name": "Independent TV", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/independent_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/ES_cZZsBNnOkwJLW1Oz1/posters/b872b8f5-cb6b-45a1-a1cd-7609df51d614.png"},
    {"name": "Desh TV", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/desh_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/6Hz1PJwBcqxnFHJBhgkV/posters/845f1e3f-987a-47cc-a48d-ee12d8f4d419.png"},
    {"name": "Jamuna TV", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/jamuna_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/PiL635oBEef-9-uV2uCe/posters/36f380e0-6c71-4b27-a73b-2afb3ce7e982.png"},
    {"name": "ATN News", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_news/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/NCLx35oBEef-9-uVh-Dg/posters/af9773c7-7971-41a2-9b78-121fcb240c48.png"},
    {"name": "ATN Bangla", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_bangla/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/MCLv35oBEef-9-uVH-D2/posters/0d1e571c-ebb2-4277-9814-760a4f1603a6.png"},
    {"name": "Nexus TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/nexus_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/FHz5PJwBcqxnFHJBdAqW/posters/419869ac-8ddf-4909-86c1-b69f0a3adf13.png"},
    {"name": "Movie Bangla", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/movie_bangla/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/CXz4PJwBcqxnFHJBPwrG/posters/2f913e34-3a6c-45e6-9f1f-97bf129a2ff5.png"},
    {"name": "Mohona TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/mohona_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/-Xz3PJwBcqxnFHJBDAlE/posters/fecea361-8b60-4aeb-a530-6e27eee8178a.png"},
    {"name": "Ananda TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/anandatv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//wCM3l5sBEef-9-uVXFvD/posters/d80f7aee-5bd7-4edc-97eb-ead0e3ebbe09.png"},
    {"name": "Bijoy TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/bijoytv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//bns4l5sBcqxnFHJBVZ32/posters/feaf9f3d-cc3b-4a3d-81a3-2cb703e561eb.png"},
    {"name": "Global TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/global_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/0y_tDJsBNnOkwJLWNrdE/posters/2ff058e1-630f-4657-8dc6-b677e65642c5.png"},
    {"name": "Channel S", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/channel_s/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//WyPuDJsBEef-9-uVUA_z/posters/ea20055c-a824-443c-8083-ce8e2da8b922.png"},
    {"name": "Bangla TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/bangla_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//JiK-_poBEef-9-uVZv6L/posters/757a328e-70d6-45de-b093-0a843c69ade7.png"},
    {"name": "Asian TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/asian_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//MyK__poBEef-9-uVmf5l/posters/1eadef5b-28e7-4dc2-b42f-c67a3357c9a0.png"},
    {"name": "Channel i", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/channel_i/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/qnv835oBcqxnFHJBuQcB/posters/348dfac3-c1e0-485d-a72b-3d282c9e2c73.png"},
    {"name": "Ekhon TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekhon_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/o3v235oBcqxnFHJBkAdC/posters/159af631-796d-4342-a2a7-c272f32bcd32.png"},
    {"name": "Rajdhani TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/rajdhani_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/KECGB54BuUSiBsg_dHyj/posters/d032f456-c7e8-4fd4-928b-ea5359960ed7.png"},
    {"name": "Islamic TV", "category": "বাংলাদেশী চ্যানেল", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/islamic_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/jehEA54BIxFjn23xAmdw/posters/f20b1b2e-3662-4da5-a71b-3f769d2a9a4e.png"},
    {"name": "Ekattor TV", "category": "News Channel", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekattor_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//PS_La5oBNnOkwJLWLRN_/posters/e8c444fd-ee3b-4bf3-bb0a-f969bc295f82.png"},
    {"name": "BAN VS AUS", "category": "Sports Channels", "cdn": "https://prod-cdn01-live.toffeelive.com/live/BDVSAUS-26/0/master_3000.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/JOg0jZ4BIxFjn23xbePr/posters/683d682a-5589-48e4-b08c-1afe5dc9c3e4.png"},
    {"name": "Euro Sport HD", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/euro_sports_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/4388/logo/240x240/mobile_logo_422191001674119624.png"},
    {"name": "ICC Test Championship Highlights", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/icc_wtc_final/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/PnZefJcBcqxnFHJBoxca/posters/955ae898-8336-4936-8d78-c6b8866e35f7.png"},
    {"name": "SONY SPORTS TEN 1 HD", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_1_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/603/logo/240x240/mobile_logo_237244001666780563.png"},
    {"name": "SONY SPORTS TEN 2 HD", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_2_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/604/logo/240x240/mobile_logo_093449001666780976.png"},
    {"name": "SONY SPORTS TEN 5 HD", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_5_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/606/logo/240x240/mobile_logo_689539001672145843.png"},
    {"name": "SONY TEN Cricket", "category": "Sports Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ten_cricket/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/301891/logo/240x240/mobile_logo_578686001735197654.png"},
    {"name": "BFL Live 1", "category": "Sports Channels", "cdn": "https://mprod-cdn.toffeelive.com/live/match-11/index.m3u8", "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRl6-ZPZ6UT3YhXilJF9fxtHzCqIt6mD71Dmg2_D-ZUsg&s=10"},
    {"name": "BFL Live 2", "category": "Sports Channels", "cdn": "https://mprod-cdn.toffeelive.com/live/match-12/index.m3u8", "logo": "https://assets-prod.services.toffeelive.com//MXnGgJkBcqxnFHJBILyR/posters/035a24dd-4d88-4fc2-99a1-275a5bc97bf5.png"},
    {"name": "BFL Live 3", "category": "Sports Channels", "cdn": "https://mprod-cdn.toffeelive.com/live/match-13/index.m3u8", "logo": "https://assets-prod.services.toffeelive.com//LnlKhJkBcqxnFHJBU8GM/posters/74e6a7bb-f850-4ec5-991f-7a882b04db37.png"},
    {"name": "BFL Live 4", "category": "Sports Channels", "cdn": "https://mprod-cdn.toffeelive.com/live/match-18/index.m3u8", "logo": "https://assets-prod.services.toffeelive.com//Ey9jtJoBNnOkwJLWw06R/posters/4e83252b-223d-42a6-a56b-8598aa17e2e8.png"},
    {"name": "Cartoon Network HD", "category": "Kids", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/26942/logo/240x240/mobile_logo_443429001678950505.png"},
    {"name": "Cartoon Network", "category": "Kids", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_sd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/27232/logo/240x240/mobile_logo_320294001679201065.png"},
    {"name": "Pogo", "category": "Kids", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/pogo_sd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/27159/logo/240x240/mobile_logo_740957001679201029.png"},
    {"name": "Discovery Kids", "category": "Kids", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_kids/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/611/logo/240x240/mobile_logo_430542001673177743.png"},
    {"name": "SONY YAY VIP", "category": "Kids", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyyay/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/612/logo/240x240/mobile_logo_091186001666784752.png"},
    {"name": "Zee Bangla VIP", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/340/logo/240x240/mobile_logo_094417001655891123.png"},
    {"name": "Zee Anmol", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_anmol/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/7x0Jd5YBEef-9-uVv_Gy/posters/f630a176-73cc-48d7-94cf-69ba0d201b36.png"},
    {"name": "Zing", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zing_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/DK8dd5YBrjBfS2_Ru22e/posters/a89a1e2e-677c-4a8a-9a66-dff5e0b921c8.png"},
    {"name": "Hum TV", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_tv/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/303937/logo/240x240/mobile_logo_880134001738072763.png"},
    {"name": "Hum Masala", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_masala/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/303947/logo/240x240/mobile_logo_203789001738235600.png"},
    {"name": "Hum Sitarey", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_sitaray/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/303948/logo/240x240/mobile_logo_350939001738236112.png"},
    {"name": "Sony Aat VIP", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyaath/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/343/logo/240x240/mobile_logo_496322001666780228.png"},
    {"name": "SONY ENTERTAINMENT TELEVISION HD VIP", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyentertainmnt_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/602/logo/240x240/mobile_logo_495351001666780441.png"},
    {"name": "SONY ENTERTAINMENT TELEVISION", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_entertainment/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/57/logo/240x240/mobile_logo_149299001666780350.png"},
    {"name": "B4U Music VIP", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/b4u_music/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/367/logo/115x115/mobile_logo_886909001563629905.png"},
    {"name": "SONY SAB HD VIP", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonysab_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/2420/logo/240x240/mobile_logo_688156001666785674.png"},
    {"name": "Zee TV HD", "category": "Entertainment Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_tv_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/644/logo/240x240/mobile_logo_649814001655891557.png"},
    {"name": "SONY MAX HD VIP", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_max_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/641/logo/240x240/mobile_logo_440775001666782769.png"},
    {"name": "Zee Bangla Cinema", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla_cinema/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_256,q_75,f_webp/-C7MX5UBv9knK3AHdKOi/posters/b0f0bfe0-f1f3-48b3-83ce-203cd44cafe2.png"},
    {"name": "Zee Bollywood", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bollywood/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_png,w_300,q_85/OnSlPJYBcqxnFHJB6lFX/posters/4818f95a-c64a-490f-b310-a49aec026d71.png"},
    {"name": "Zee Action", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_action/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/Pc3RD5YBtpl-Sbt7doxr/posters/d0f337ab-a7e6-4eed-bc7b-7d51fdc70a0f.png"},
    {"name": "SONY MAX VIP", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_max/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/352/logo/240x240/mobile_logo_612341001666782969.png"},
    {"name": "SONY PIX HD VIP", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonypix_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/2419/logo/240x240/mobile_logo_287412001666784602.png"},
    {"name": "Zee Cafe", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_cafe_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/U3QEd5YBcqxnFHJBpYzc/posters/3442d493-0c71-44b9-b12f-8e600d5eab91.png"},
    {"name": "B4U Movies VIP", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/b4u_movies/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/366/logo/240x240/mobile_logo_702115001663003759.png"},
    {"name": "SONY MAX 2 VIP", "category": "Movie Channels", "cdn": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonymax_2/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/353/logo/240x240/mobile_logo_044841001666779831.png"}
]

# ২. ডাইনামিক কুকি জেনারেটর (সরাসরি টুফি সিডিএন থেকে)
def fetch_toffee_cookie():
    print("🍪 Fetching fresh Toffee Edge-Cache-Cookie...")
    COOKIE_SOURCES = [
        "https://toffee-stream-keeper.lovable.app/toffee_ns.json"
    ]
    for src in COOKIE_SOURCES:
        try:
            res = requests.get(src, timeout=15)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("cookie") and "Edge-Cache-Cookie" in item.get("cookie"):
                            print("✅ Fresh Toffee Cookie acquired successfully!")
                            return item.get("cookie")
        except Exception as e:
            print(f"Warning fetching cookie: {e}")
    return ""

def build_independent_toffee_playlist():
    print("🚀 Generating 100% Self-Hosted Independent Toffee Catalog...")
    current_cookie = fetch_toffee_cookie()

    output_data = {
        "name": "Shamim Live TV - Self Hosted Toffee Playlist",
        "owner": "Shamim Pipon",
        "channels_amount": len(BASE_CHANNELS),
        "updated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "channels": []
    }

    m3u_content = "#EXTM3U\n"

    for ch in BASE_CHANNELS:
        ua = "okhttp/4.11.0"
        channel_obj = {
            "name": ch["name"],
            "link": ch["cdn"],
            "logo": ch["logo"],
            "category_name": ch["category"],
            "headers": {
                "cookie": current_cookie,
                "user-agent": ua,
                "referer": "https://toffeelive.com/"
            }
        }
        output_data["channels"].append(channel_obj)

        m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
        if current_cookie:
            m3u_content += f'#EXTVLCOPT:http-cookie={current_cookie}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=https://toffeelive.com/\n'
        m3u_content += f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["category"]}",{ch["name"]}\n'
        m3u_content += f'{ch["cdn"]}\n\n'

    with open("toffee_channel_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    with open("toffee_playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"🎉 Generated {len(BASE_CHANNELS)} channels into 'toffee_channel_data.json' and 'toffee_playlist.m3u'!")

if __name__ == "__main__":
    build_independent_toffee_playlist()
