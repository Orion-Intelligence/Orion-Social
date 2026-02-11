from ddgs import DDGS
from typing import List, Dict, Any
from urllib.parse import urlparse
import re


def extract_username_from_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if not path:
            return None
        
        if path.startswith("@"):
            return path.replace("@", "").split("/")[0]
        
        parts = path.split("/")
        username = parts[0] if parts else None
        
        if username and not any(keyword in username.lower() for keyword in ["search", "explore", "hashtag", "tag", "p", "reel", "post"]):
            return username
        
        return None
    except Exception:
        return None


def extract_real_name(title: str, snippet: str) -> str:
    if not title:
        return None
    
    title_clean = title.strip()
    
    if "(" in title_clean and ")" in title_clean:
        real_name = title_clean.split("(")[0].strip()
        if real_name:
            return real_name
    
    if " - " in title_clean:
        real_name = title_clean.split(" - ")[0].strip()
        if real_name and len(real_name) > 2:
            return real_name
    
    if "@" in title_clean:
        real_name = title_clean.split("@")[0].strip()
        if real_name and len(real_name) > 2:
            return real_name
    
    if "|" in title_clean:
        real_name = title_clean.split("|")[0].strip()
        if real_name and len(real_name) > 2:
            return real_name
    
    return title_clean if len(title_clean) > 2 else None


def scrape_usernames(username: str, platform: str, limit: int = 10) -> Dict[str, Any]:
    platform = platform.lower().strip()
    
    platform_domain = f"{platform}.com" if not platform.endswith(".com") else platform
    
    search_query = f'site:{platform_domain} "{username}"'
    
    profiles = []
    seen_usernames = set()
    
    try:
        with DDGS() as ddgs:
            text_results = ddgs.text(search_query, max_results=limit * 3)
            
            for r in text_results:
                if len(profiles) >= limit:
                    break
                
                url = r.get("href")
                title = r.get("title", "")
                snippet = r.get("body", "")
                
                if not url or platform_domain not in url:
                    continue
                
                extracted_username = extract_username_from_url(url)
                
                if not extracted_username or extracted_username in seen_usernames:
                    continue
                
                real_name = extract_real_name(title, snippet)
                
                seen_usernames.add(extracted_username)
                
                profiles.append({
                    "username": extracted_username,
                    "real_name": real_name,
                    "profile_url": url,
                    "title": title,
                    "snippet": snippet,
                    "platform": platform
                })
        
        return {
            "searched_username": username,
            "platform": platform,
            "total_found": len(profiles),
            "usernames": list(seen_usernames),
            "profiles": profiles
        }
    
    except Exception as e:
        return {
            "searched_username": username,
            "platform": platform,
            "error": str(e),
            "total_found": 0,
            "usernames": [],
            "profiles": []
        }


def scrape_images(username: str, platform: str, limit: int = 10) -> Dict[str, Any]:
    platform = platform.lower().strip()
    
    search_query = f"{username} {platform}"
    image_results = []
    
    try:
        with DDGS() as ddgs:
            image_search_results = ddgs.images(search_query, max_results=limit)
            
            for img in image_search_results:
                image_url = img.get("image")
                if image_url:
                    image_results.append({
                        "image_url": image_url,
                        "thumbnail": img.get("thumbnail"),
                        "title": img.get("title"),
                        "source": img.get("source")
                    })
        
        return {
            "searched_username": username,
            "platform": platform,
            "total_found": len(image_results),
            "images": image_results
        }
    
    except Exception as e:
        return {
            "searched_username": username,
            "platform": platform,
            "error": str(e),
            "total_found": 0,
            "images": []
        }





