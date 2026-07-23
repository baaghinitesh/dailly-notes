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

PLAYLISTS = {
    "Tutorials": "PLA9WHIULlzLs",
    "Introductory": "PLLQusXO8cwRc",
    "Shorts": "PLamO7b9OnT4M"
}

def fetch_playlist_videos_rss(playlist_id):
    videos = []
    try:
        url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            xml_content = response.read().decode("utf-8")
            
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
    except Exception as e:
        print(f"❌ Failed fetching playlist {playlist_id} via RSS: {e}")
        return []

def fetch_playlist_videos(playlist_id):
    if not API_KEY:
        print(f"⚠️ YOUTUBE_API_KEY environment variable is missing. Attempting RSS fallback for playlist {playlist_id}...")
        return fetch_playlist_videos_rss(playlist_id)
        
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
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                
            if "items" in data:
                for item in data["items"]:
                    snippet = item.get("snippet", {})
                    resource_id = snippet.get("resourceId", {})
                    video_id = resource_id.get("videoId")
                    title = snippet.get("title", "")
                    
                    if video_id and title not in ("Deleted video", "Private video"):
                        thumbnails = snippet.get("thumbnails", {})
                        # Get best available thumbnail
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
        print(f"❌ Failed fetching playlist {playlist_id}: {e}")
        return []

def fetch_channel_latest_videos(channel_id):
    videos = []
    try:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            xml_content = response.read().decode("utf-8")
            
        entries = re.findall(r"<entry>([\s\S]*?)</entry>", xml_content)
        for entry in entries:
            video_id_match = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entry)
            title_match = re.search(r"<title>([^<]+)</title>", entry)
            description_match = re.search(r"<media:description>([\s\S]*?)</media:description>", entry)
            thumbnail_match = re.search(r'<media:thumbnail[^>]+url="([^"]+)"', entry)
            published_match = re.search(r"<published>([^<]+)</published>", entry)
            link_match = re.search(r'<link[^>]+href="([^"]+)"', entry)
            
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
                video_link = link_match.group(1).strip() if link_match else ""
                
                is_short = ("/shorts/" in video_link) or ("#shorts" in title.lower()) or ("#shorts" in description.lower())
                
                if title not in ("Deleted video", "Private video"):
                    videos.append({
                        "id": video_id,
                        "title": title,
                        "description": description,
                        "thumbnail": thumbnail_url,
                        "publishedAt": published_at,
                        "is_short": is_short
                    })
        return videos
    except Exception as e:
        print(f"❌ Failed fetching channel feed: {e}")
        return []

def main():
    print("🚀 Starting YouTube Playlists Synchronizer (Python)...")
    structured_data = {}
    
    # 1. Fetch from playlists
    for category_name, playlist_id in PLAYLISTS.items():
        print(f"📥 Fetching: {category_name} (Playlist: {playlist_id})...")
        videos = fetch_playlist_videos(playlist_id)
        structured_data[category_name] = videos
        
    # 2. Fetch latest channel uploads to catch any loose videos
    channel_id = "UCmwmvG7HZbUFP0RAbtEo-KQ"
    print(f"📥 Fetching latest videos directly from channel feed (Channel: {channel_id})...")
    channel_videos = fetch_channel_latest_videos(channel_id)
    
    # Check for each channel video if it's already represented in structured_data
    existing_ids = set()
    for cat_name, v_list in structured_data.items():
        for v in v_list:
            existing_ids.add(v["id"])
            
    added_count = 0
    for cv in channel_videos:
        if cv["id"] not in existing_ids:
            # Auto-categorize
            if cv["is_short"]:
                target_cat = "Shorts"
            elif "tutorial" in cv["title"].lower() or "how to" in cv["title"].lower():
                target_cat = "Tutorials"
            else:
                target_cat = "Introductory"
                
            video_item = {
                "id": cv["id"],
                "title": cv["title"],
                "description": cv["description"],
                "thumbnail": cv["thumbnail"],
                "publishedAt": cv["publishedAt"]
            }
            
            structured_data[target_cat].append(video_item)
            existing_ids.add(cv["id"])
            added_count += 1
            print(f"➕ Auto-added loose channel video '{cv['title']}' to category '{target_cat}'")
            
    # Sort all lists by publication date descending
    for category_name in PLAYLISTS.keys():
        structured_data[category_name].sort(key=lambda x: x["publishedAt"], reverse=True)
        print(f"✅ Loaded {len(structured_data[category_name])} videos for {category_name}")
        
    output_path = os.path.join("topics", "youtube-videos.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
    print("✨ YouTube video database synchronization complete!")

if __name__ == "__main__":
    main()
