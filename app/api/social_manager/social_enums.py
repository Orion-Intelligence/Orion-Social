from enum import IntEnum


class SOCIAL_REQUEST_COMMANDS(IntEnum):
    PROFILE_ONLY = 1
    FOLLOWERS_ONLY = 2
    FOLLOWING_ONLY = 3
    FOLLOWERS_FOLLOWING = 4
    PROFILE_FOLLOWERS = 5
    PROFILE_FOLLOWING = 6
    S_SCRAPE_MULTIPLE = 7
    S_RECON_USER = 8
    S_POSTS = 9
    S_DDG_USERNAMES = 10
    S_DDG_IMAGES = 11
    S_DDG_METADATA = 12


class SOCIAL_PLATFORMS:
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    BEHANCE = "behance"
    VIMEO = "vimeo"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    DUCKDUCKGO = "duckduckgo"


class SOCIAL_CONTENT_TYPES:
    FOLLOWERS = "followers"
    FOLLOWING = "following"
    FRIENDS = "friends"
    MUTUAL = "mutual"
    PROFILE = "profile"

class SITE_DATA:
    ALL_SITES = [
        "2Dimensions", "3dnews", "500px", "7Cups", "9GAG", "About.me", "Academia.edu", "Airbnb", "AllMyLinks", "Amino",
        "Apple Developer", "Archive.org", "Arduino", "Ask.fm", "Author.today", "Bandcamp", "Beacons.ai", "Behance",
        "Bikemap", "BitBucket", "BitcoinTalk", "Blogger", "BuzzFeed", "CNET", "Canva", "Carbonmade", "Cash.app",
        "Civitai", "Clubhouse", "Coco", "Codeforces", "CodePen", "Coroflot", "Crello", "CurseForge", "DeviantArt",
        "Discord", "Docker Hub", "Dribbble", "Ello", "Etsy", "Facebook", "Flickr", "Flipboard", "Forum.xda-developers",
        "Freesound", "FriendFeed", "Gab", "GitHub", "GitLab", "Goodreads", "Gravatar", "Gumroad", "HackerNews",
        "Houzz", "IFTTT", "Imgur", "Instagram", "Issuu", "Itch.io", "Keybase", "Kickstarter", "Last.fm", "Letterboxd",
        "Linktree", "LiveJournal", "Mastodon", "Medium", "Mix", "Myspace", "NPM", "Newgrounds", "NotABot", "OK.ru",
        "OnlyFans", "Patreon", "PayPal", "Pinterest", "ProductHunt", "PyPi", "Quora", "Reddit", "Replit", "Roblox",
        "Signal", "Slack", "SlideShare", "SoundCloud", "SourceForge", "Spotify", "StackExchange", "StackOverflow",
        "Steam", "Strava", "Telegram", "TikTok", "Trello", "TripAdvisor", "Tumblr", "Twitch", "Twitter", "Untappd",
        "VK", "VSCO", "Vimeo", "Virb", "Weasyl", "Webflow", "Wix", "WordPress.com", "WordPressOrg", "Wattpad",
        "Wikipedia", "YouTube", "YouTube User", "Zotero", "devRant", "eBay", "last.fm", "mixcloud"
    ]

    FOCUSED_SITES = [
        "GitHub", "GitLab", "BitBucket", "Docker Hub", "NPM", "PyPi", "SourceForge",
        "Reddit", "HackerNews", "StackOverflow",
        "Telegram", "Keybase", "VK",
        "Twitter", "Facebook", "Instagram",
        "Pastebin", "About.me",
        "Codepen", "Repl.it",
        "Kaggle", "Quora",
        "Wikipedia",
        "YouTube", "YouTube User",
        "TikTok", "Twitch",
        "Tumblr",
        "Pinterest",
        "WordPressOrg",
    ]

    TOP_10_SITES = [
        "YouTube",
        "Facebook",
        "Instagram",
        "Twitter",
        "Wikipedia",
        "GitHub",
        "Reddit",
        "TikTok",
        "StackOverflow",
        "Twitch",
    ]
