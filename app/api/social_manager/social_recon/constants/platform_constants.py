class BlueskyConstants:
    NAME = "Bluesky"
    GRAMMAR = r"^[A-Za-z0-9._-]{1,253}$"
    PROFILE_URL = "https://bsky.app/profile/{username}"
    API_URL = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}"
    DEFAULT_DOMAIN = ".bsky.social"


class DiscordConstants:
    NAME = "Discord"
    PROFILE_URL = "https://discord.com/users/{username}"
    SUPPORTED = False
    REASON = "profile lookup requires an authenticated bot token; the public page renders no user data"


class FacebookConstants:
    NAME = "Facebook"
    GRAMMAR = r"^[A-Za-z0-9.]{4,50}$"
    PROFILE_URL = "https://www.facebook.com/{username}"
    GENERIC = {"facebook", "facebook - log in or sign up"}
    AVATAR_KEYS = ("profilePicLarge", "profilePicMedium", "profile_pic_url")
    COVER_KEYS = ("coverPhoto", "cover_photo")


class InstagramConstants:
    NAME = "Instagram"
    GRAMMAR = r"^[A-Za-z0-9._]{1,30}$"
    PROFILE_URL = "https://www.instagram.com/{username}/"
    GENERIC = {"instagram"}
    AVATAR_KEYS = ("profile_pic_url_hd", "profile_pic_url")
    COVER_KEYS = ()


class LinkedInConstants:
    NAME = "LinkedIn"
    GRAMMAR = r"^[A-Za-z0-9-]{3,100}$"
    PROFILE_URL = "https://www.linkedin.com/in/{username}"
    GENERIC = {"linkedin", "sign up | linkedin", "linkedin login, sign in | linkedin"}
    AVATAR_KEYS = ("profilePicture", "displayImageUrl")
    COVER_KEYS = ("backgroundImage",)


class PinterestConstants:
    NAME = "Pinterest"
    GRAMMAR = r"^[A-Za-z0-9_]{3,30}$"
    PROFILE_URL = "https://www.pinterest.com/{username}/"
    PROFILE_MARKER = "- profile"
    MAX_BYTES = 1_600_000
    AVATAR_KEYS = ("image_xlarge_url", "image_medium_url")
    COVER_KEYS = ("profile_cover_url", "image_cover_url")


class QuoraConstants:
    NAME = "Quora"
    GRAMMAR = r"^[A-Za-z0-9-]{2,80}$"
    PROFILE_URL = "https://www.quora.com/profile/{username}"
    AVATAR_KEYS = ("profileImageUrl", "photoUrl")
    COVER_KEYS = ()


class RedditConstants:
    NAME = "Reddit"
    GRAMMAR = r"^[A-Za-z0-9_-]{3,20}$"
    PROFILE_URL = "https://www.reddit.com/user/{username}"
    ABOUT_URL = "https://www.reddit.com/user/{username}/about.json"


class SnapchatConstants:
    NAME = "Snapchat"
    GRAMMAR = r"^[A-Za-z0-9._-]{3,15}$"
    PROFILE_URL = "https://www.snapchat.com/add/{username}"
    AVATAR_KEYS = ("bitmojiAvatarUrl", "profilePictureUrl", "avatarUrl")
    COVER_KEYS = ()


class ThreadsConstants:
    NAME = "Threads"
    GRAMMAR = r"^[A-Za-z0-9._]{1,30}$"
    PROFILE_URL = "https://www.threads.net/@{username}"
    LOGIN_MARKER = "log in"
    AVATAR_KEYS = ("profile_pic_url_hd", "profile_pic_url")
    COVER_KEYS = ()


class TikTokConstants:
    NAME = "TikTok"
    GRAMMAR = r"^[A-Za-z0-9._]{2,24}$"
    PROFILE_URL = "https://www.tiktok.com/@{username}"
    OEMBED_URL = "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}"
    IMAGE_NOTE = "no avatar available over http: profile oembed carries no thumbnail and the profile html is a script shell"


class TwitchConstants:
    NAME = "Twitch"
    GRAMMAR = r"^[A-Za-z0-9_]{4,25}$"
    PROFILE_URL = "https://www.twitch.tv/{username}"
    GQL_URL = "https://gql.twitch.tv/gql"
    GQL_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    GQL_QUERY = (
        '{{user(login:"{username}"){{id displayName description '
        "profileImageURL(width:300) bannerImageURL offlineImageURL "
        "followers{{totalCount}}}}}}"
    )


class WhatsAppConstants:
    NAME = "WhatsApp"
    PROFILE_URL = "https://wa.me/{username}"
    SUPPORTED = False
    REASON = "wa.me serves an identical share page for every input and exposes no username directory"


class XConstants:
    NAME = "X"
    GRAMMAR = r"^[A-Za-z0-9_]{1,15}$"
    PROFILE_URL = "https://x.com/{username}"
    SYNDICATION_URL = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"


class YouTubeConstants:
    NAME = "YouTube"
    GRAMMAR = r"^[A-Za-z0-9._-]{3,30}$"
    PROFILE_URL = "https://www.youtube.com/@{username}"
    MAX_BYTES = 2_800_000
    AVATAR_KEYS = ("avatar_url", "thumbnailUrl")
    COVER_KEYS = ()
    COVER_PATTERN = r'"imageBannerViewModel".{0,400}?"url":"(https?://[^"]+)"'
