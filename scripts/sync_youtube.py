import os
import json
import sys
import urllib.request
import urllib.parse

API_KEY = os.environ.get("YOUTUBE_API_KEY")

PLAYLISTS = {
    "Tutorials": "PLA9WHIULlzLs",
    "Introductory": "PLLQusXO8cwRc",
    "Shorts": "PLamO7b9OnT4M"
}

def fetch_playlist_videos(playlist_id):
    if not API_KEY:
        print("❌ Error: YOUTUBE_API_KEY environment variable is missing.")
        sys.exit(1)
        
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

def main():
    print("🚀 Starting YouTube Playlists Synchronizer (Python)...")
    structured_data = {}
    
    for category_name, playlist_id in PLAYLISTS.items():
        print(f"📥 Fetching: {category_name} (Playlist: {playlist_id})...")
        videos = fetch_playlist_videos(playlist_id)
        
        # Sort videos by publication date descending
        videos.sort(key=lambda x: x["publishedAt"], reverse=True)
        structured_data[category_name] = videos
        print(f"✅ Loaded {len(videos)} videos for {category_name}")
        
    output_path = os.path.join("topics", "youtube-videos.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
    print("✨ YouTube video database synchronization complete!")

if __name__ == "__main__":
    main()
