import os
import json
import sys
import urllib.request
import urllib.parse
import re
import html

# Reconfigure stdout to use UTF-8 to prevent unicode print crashes on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = "UCmwmvG7HZbUFP0RAbtEo-KQ"
UPLOADS_PLAYLIST_ID = "UUmwmvG7HZbUFP0RAbtEo-KQ"

PLAYLISTS = {
    "Tutorials": "PLA9WHIULlzLs",
    "Introductory": "PLLQusXO8cwRc",
    "Shorts": "PLamO7b9OnT4M"
}

def parse_xml_entries(xml_content):
    videos = []
    entries = re.findall(r"<entry>([\s\S]*?)</entry>", xml_content)
    for entry in entries:
        video_id_match = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entry)
        title_match = re.search(r"<title>([^<]+)</title>", entry)
        description_match = re.search(r"<media:description>([\s\S]*?)</media:description>", entry)
        thumbnail_match = re.search(r'<media:thumbnail[^>]+url="([^"]+)"', entry)
        published_match = re.search(r"<published>([^<]+)</published>", entry)
        
        if video_id_match and title_match:
            video_id = video_id_match.group(1).strip()
            title = html.unescape(title_match.group(1).strip())
            description = html.unescape(description_match.group(1).strip()) if description_match else ""
            
            thumbnail_url = ""
            if thumbnail_match:
                thumbnail_url = thumbnail_match.group(1).strip()
            if not thumbnail_url:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                
            published_at = published_match.group(1).strip() if published_match else ""
            
            if title not in ("Deleted video", "Private video"):
                videos.append({
                    "id": video_id,
                    "title": title,
                    "description": description,
                    "thumbnail": thumbnail_url,
                    "publishedAt": published_at
                })
    return videos

def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_content = response.read().decode("utf-8")
        return parse_xml_entries(xml_content)
    except Exception as e:
        print(f"⚠️ Failed fetching RSS from {url}: {e}")
        return []

def is_short_video(video_id, title, description):
    text = (title + " " + description).lower()
    if "#shorts" in text or "#short" in text or "#reel" in text:
        return True
    try:
        req = urllib.request.Request(
            f"https://www.youtube.com/shorts/{video_id}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            method="HEAD"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            final_url = resp.geturl()
            if "/shorts/" in final_url:
                return True
    except Exception:
        pass
    return False

def fetch_playlist_videos_api(playlist_id):
    if not API_KEY:
        return []
    videos = []
    next_page_token = ""
    try:
        while True:
            params = {
                "part": "snippet",
                "maxResults": 50,
                "playlistId": playlist_id,
                "key": API_KEY
            }
            if next_page_token:
                params["pageToken"] = next_page_token
            query_string = urllib.parse.urlencode(params)
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?{query_string}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
            if "items" in data:
                for item in data["items"]:
                    snippet = item.get("snippet", {})
                    resource_id = snippet.get("resourceId", {})
                    video_id = resource_id.get("videoId")
                    title = snippet.get("title", "")
                    if video_id and title not in ("Deleted video", "Private video"):
                        thumbnails = snippet.get("thumbnails", {})
                        thumbnail_url = ""
                        for size in ("maxres", "high", "medium", "default"):
                            if size in thumbnails and "url" in thumbnails[size]:
                                thumbnail_url = thumbnails[size]["url"]
                                break
                        if not thumbnail_url:
                            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        videos.append({
                            "id": video_id,
                            "title": title,
                            "description": snippet.get("description", ""),
                            "thumbnail": thumbnail_url,
                            "publishedAt": snippet.get("publishedAt", "")
                        })
            next_page_token = data.get("nextPageToken", "")
            if not next_page_token:
                break
        return videos
    except Exception as e:
        print(f"❌ Failed fetching playlist {playlist_id} via API: {e}")
        return []

def main():
    print("🚀 Starting YouTube Playlists & Channel Synchronizer...")
    structured_data = {
        "Tutorials": [],
        "Introductory": [],
        "Shorts": []
    }
    
    seen_ids = set()

    # 1. Fetch defined playlists
    for category_name, playlist_id in PLAYLISTS.items():
        print(f"📥 Fetching defined playlist: {category_name} ({playlist_id})...")
        videos = []
        if API_KEY:
            videos = fetch_playlist_videos_api(playlist_id)
        if not videos:
            rss_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
            videos = fetch_rss(rss_url)
        
        for v in videos:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                structured_data[category_name].append(v)
        print(f"   Loaded {len(videos)} videos for {category_name}")

    # 2. Fetch all channel uploads to ensure NO new video or short is missed
    print(f"📥 Fetching entire channel uploads for {CHANNEL_ID}...")
    channel_videos = []
    if API_KEY:
        channel_videos = fetch_playlist_videos_api(UPLOADS_PLAYLIST_ID)
    if not channel_videos:
        # Try both channel uploads playlist RSS and channel ID RSS
        channel_videos = fetch_rss(f"https://www.youtube.com/feeds/videos.xml?playlist_id={UPLOADS_PLAYLIST_ID}")
        if not channel_videos:
            channel_videos = fetch_rss(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}")
    
    print(f"   Found {len(channel_videos)} total channel uploads.")
    
    # Classify channel videos not yet in structured_data
    unassigned_count = 0
    for v in channel_videos:
        if v["id"] in seen_ids:
            continue
        seen_ids.add(v["id"])
        unassigned_count += 1
        
        # Check if it's a short
        if is_short_video(v["id"], v["title"], v["description"]):
            structured_data["Shorts"].append(v)
            print(f"   + Added short: {v['title'][:40]}...")
        else:
            title_lower = v["title"].lower()
            if any(k in title_lower for k in ["tutorial", "how to", "guide", "walkthrough", "step by step"]):
                structured_data["Tutorials"].append(v)
                print(f"   + Added tutorial: {v['title'][:40]}...")
            else:
                structured_data["Introductory"].append(v)
                print(f"   + Added introductory video: {v['title'][:40]}...")

    # Sort each category descending by published date
    for cat in structured_data:
        structured_data[cat].sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
        print(f"✅ Total {cat}: {len(structured_data[cat])}")

    output_path = os.path.join("topics", "youtube-videos.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
    print("✨ YouTube video database synchronization complete!")
    return structured_data

if __name__ == "__main__":
    main()
