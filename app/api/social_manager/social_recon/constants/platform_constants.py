class BlueskyConstants:
    NAME = "Bluesky"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._-]{1,253}$"
    PROFILE_URL = "https://bsky.app/profile/{username}"
    API_URL = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}"
    DEFAULT_DOMAIN = ".bsky.social"


class FacebookConstants:
    NAME = "Facebook"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9.]{4,50}$"
    PROFILE_URL = "https://www.facebook.com/{username}"
    GENERIC = {"facebook", "facebook - log in or sign up"}
    PAGE_PATTERN = r"\b[\d.,]+[KMB]?\s+likes\s*·\s*[\d.,]+[KMB]?\s+(?:talking about this|were here|followers)"
    LIKES = r"([\d.,]+[KMB]?)\s+likes"
    FOLLOWERS = r"([\d.,]+[KMB]?)\s+followers"
    TALKING = r"([\d.,]+[KMB]?)\s+talking about this"
    AVATAR_KEYS = ("profilePicLarge", "profilePicMedium", "profile_pic_url")
    COVER_KEYS = ("coverPhoto", "cover_photo")


class InstagramConstants:
    NAME = "Instagram"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._]{1,30}$"
    PROFILE_URL = "https://www.instagram.com/{username}/"
    GENERIC = {"instagram"}
    AVATAR_KEYS = ("profile_pic_url_hd", "profile_pic_url")
    COVER_KEYS = ()
    HANDLE = r"\(@([^)]+)\)"
    NAME_SPLIT = " (@"
    BIO_SPLIT = ' on Instagram: "'


class PinterestConstants:
    NAME = "Pinterest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9_]{3,30}$"
    PROFILE_URL = "https://www.pinterest.com/{username}/"
    PROFILE_MARKER = "- profile"
    MAX_BYTES = 1_600_000
    AVATAR_KEYS = ("image_xlarge_url", "image_medium_url")
    COVER_KEYS = ("profile_cover_url", "image_cover_url")
    FULL_NAME = r'"full_name":"([^"]+)"'
    ABOUT = r'"about":"([^"]*)"'
    FOLLOWERS = r'"follower_count":(\d+)'
    FOLLOWING = r'"following_count":(\d+)'
    HANDLE = r"\(([^)]+)\)"


class QuoraConstants:
    NAME = "Quora"
    CRAWL_TYPE = "playwright"
    GRAMMAR = r"^[A-Za-z0-9-]{2,80}$"
    PROFILE_URL = "https://www.quora.com/profile/{username}"
    AVATAR_KEYS = ("profileImageUrl", "photoUrl")
    COVER_KEYS = ()


class RedditConstants:
    NAME = "Reddit"
    CRAWL_TYPE = "playwright"
    GRAMMAR = r"^[A-Za-z0-9_-]{3,20}$"
    PROFILE_URL = "https://www.reddit.com/user/{username}"
    ABOUT_URL = "https://www.reddit.com/user/{username}/about.json"
    GENERIC = {"reddit", "reddit - the heart of the internet", "reddit - dive into anything"}
    RESOURCE_DESCRIPTION = r'<shreddit-(?:subreddit|post|profile)-[a-z-]*header[^>]*\sdescription="([^"]+)"'
    RESOURCE_MARKERS = ("<shreddit-subreddit-header", "<shreddit-post")
    MISSING_USER = "nobody on Reddit goes by that name"


class ThreadsConstants:
    NAME = "Threads"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._]{1,30}$"
    PROFILE_URL = "https://www.threads.net/@{username}"
    LOGIN_MARKER = "log in"
    AVATAR_KEYS = ("profile_pic_url_hd", "profile_pic_url")
    COVER_KEYS = ()
    HANDLE = r"\(@([^)]+)\)"
    NAME_SPLIT = " (@"
    FOLLOWERS = r"([\d.,]+[KMB]?)\s+Followers"
    THREADS = r"([\d.,]+[KMB]?)\s+Threads"
    BIO = r"Threads\s*•\s*(.+?)\.\s*See the latest"


class TikTokConstants:
    NAME = "TikTok"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._]{2,24}$"
    PROFILE_URL = "https://www.tiktok.com/@{username}"
    OEMBED_URL = "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}"
    DATA_KEY = "userInfo"
    NOT_FOUND = ('"statusCode":10202', "couldn't find this account")


class TwitchConstants:
    NAME = "Twitch"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9_]{4,25}$"
    PROFILE_URL = "https://www.twitch.tv/{username}"
    GQL_URL = "https://gql.twitch.tv/gql"
    GQL_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    GQL_QUERY = (
        '{{user(login:"{username}"){{id login displayName description '
        "profileImageURL(width:300) bannerImageURL offlineImageURL createdAt primaryColorHex "
        "roles{{isPartner isAffiliate}} followers{{totalCount}}}}}}"
    )


class XConstants:
    NAME = "X"
    CRAWL_TYPE = "playwright"
    GRAMMAR = r"^[A-Za-z0-9_]{1,15}$"
    PROFILE_URL = "https://x.com/{username}"
    SYNDICATION_URL = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"
    GENERIC = {"x", "x. it’s what’s happening / x", "profile / x", "user profile not found - x | 404 error"}


class YouTubeConstants:
    NAME = "YouTube"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._-]{3,30}$"
    PROFILE_URL = "https://www.youtube.com/@{username}"
    MAX_BYTES = 2_800_000
    AVATAR_KEYS = ("avatar_url", "thumbnailUrl")
    COVER_KEYS = ()
    COVER_PATTERN = r'"imageBannerViewModel".{0,400}?"url":"(https?://[^"]+)"'
    SUBSCRIBERS = r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([^"]+)"'
    OEMBED = "https://www.youtube.com/oembed?format=json&url={url}"


class OKRuConstants:
    NAME = "OK.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://ok.ru/{username}"
    GENERIC = {"ok", "ok.ru", "одноклассники"}
    AVATAR_KEYS = ("pic_2", "pic_1")
    COVER_KEYS = ()


class BilibiliConstants:
    NAME = "Bilibili"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,32}$"
    PROFILE_URL = "https://space.bilibili.com/{username}"
    API_URL = "https://api.bilibili.com/x/web-interface/card?mid={username}&photo=true"
    GENERIC = {"bilibili", "哔哩哔哩 (゜-゜)つロ 干杯~-bilibili"}
    AVATAR_KEYS = ("face", "avatar")
    COVER_KEYS = ("top_photo",)


class BaiduTiebaConstants:
    NAME = "Baidu Tieba"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[^\s/?#&]{1,64}$"
    PROFILE_URL = "https://tieba.baidu.com/home/main?un={username}"
    PANEL_URL = "https://tieba.baidu.com/home/get/panel?un={username}"


class MastodonConstants:
    NAME = "Mastodon"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://mastodon.social/@{username}"
    API_URL = "https://mastodon.social/api/v1/accounts/lookup?acct={username}"
    GENERIC = {"mastodon", "the page you are looking for isn't here. - mastodon"}
    AVATAR_KEYS = ("avatar_static", "avatar")
    COVER_KEYS = ("header_static", "header")


class MeWeConstants:
    NAME = "MeWe"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://mewe.com/i/{username}"
    NOT_FOUND_PATH = "/404"
    GENERIC = {"mewe", "mewe - the next-gen social network"}
    GENERIC_DESCRIPTIONS = ("brilliant features with no bs",)


class RumbleConstants:
    NAME = "Rumble"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://rumble.com/user/{username}"
    AVATAR_KEYS = ("thumb", "avatar")
    COVER_KEYS = ("cover",)


class KickConstants:
    NAME = "Kick"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,25}$"
    PROFILE_URL = "https://kick.com/{username}"
    API_URL = "https://kick.com/api/v2/channels/{username}"


class Lemon8Constants:
    NAME = "Lemon8"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._]{1,30}$"
    PROFILE_URL = "https://www.lemon8-app.com/@{username}"
    AVATAR_KEYS = ("avatar_url", "avatar")
    COVER_KEYS = ()


class VSCOConstants:
    NAME = "VSCO"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9-]{1,30}$"
    PROFILE_URL = "https://vsco.co/{username}/gallery"
    GENERIC = {"vsco", "vsco - not found"}
    AVATAR_KEYS = ("responsive_url", "profile_image")
    COVER_KEYS = ()


class FlickrConstants:
    NAME = "Flickr"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9@._-]{1,64}$"
    PROFILE_URL = "https://www.flickr.com/people/{username}"
    GENERIC = {"flickr", "flickr: page not found"}
    MAX_BYTES = 1_100_000
    AVATAR_KEYS = ("buddyicon", "iconurl")
    COVER_KEYS = ("coverphoto",)
    PHOTO_COUNT = r'person-profile-models","photoCount":(\d+)'


class BehanceConstants:
    NAME = "Behance"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.behance.net/{username}"
    GENERIC = {"behance", "behance :: not found"}
    AVATAR_KEYS = ("276", "138")
    COVER_KEYS = ("banner_image_url",)
    IMPERSONATE = "safari"


class DribbbleConstants:
    NAME = "Dribbble"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://dribbble.com/{username}"
    GENERIC = {"dribbble", "dribbble - discover the world’s top designers & creative professionals"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ()


class ImgurConstants:
    NAME = "Imgur"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://imgur.com/user/{username}"
    API_URL = "https://api.imgur.com/account/v1/accounts/{username}?client_id=546c25a59c58ad7"


class ArtStationConstants:
    NAME = "ArtStation"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.artstation.com/{username}"
    API_URL = "https://www.artstation.com/users/{username}.json"
    GENERIC = {"artstation", "artstation - not found"}
    AVATAR_KEYS = ("large_avatar_url", "medium_avatar_url")
    COVER_KEYS = ("cover_url",)
    SOCIAL_KEYS = {
        "twitter_url": "twitter", "facebook_url": "facebook", "instagram_url": "instagram",
        "linkedin_url": "linkedin", "behance_url": "behance", "deviantart_url": "deviantart",
        "imdb_url": "imdb", "tumblr_url": "tumblr", "website_url": "website",
    }


class BandcampConstants:
    NAME = "Bandcamp"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9-]{1,64}$"
    PROFILE_URL = "https://{username}.bandcamp.com"
    GENERIC = {"bandcamp", "signup | bandcamp"}
    AVATAR_KEYS = ("art_id",)
    COVER_KEYS = ()


class LastFmConstants:
    NAME = "Last.fm"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,15}$"
    PROFILE_URL = "https://www.last.fm/user/{username}"
    GENERIC = {"last.fm", "page not found | last.fm"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    NAME_RE = r"(.+?)[’']s Music Profile"
    SCROBBLES = r"\(([\d,]+) (?:scrobbles|tracks played)\)"
    TOP_ARTISTS = r"top artists:\s*(.+?)\.\s*Get your own"


class GoodreadsConstants:
    NAME = "Goodreads"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.goodreads.com/{username}"
    GENERIC = {"goodreads", "page not found"}
    AVATAR_KEYS = ("image_url", "profile_image")
    COVER_KEYS = ()
    TITLE_USERNAME = r"^.*?\(([^)]+)\)"
    TITLE_BOOKS = r"\(([\d,]+)\s+books?\)"
    TITLE_LOCATION = r"\)\s*-\s*(.+?)\s*\([\d,]+\s+books?\)"


class LetterboxdConstants:
    NAME = "Letterboxd"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{2,15}$"
    PROFILE_URL = "https://letterboxd.com/{username}/"
    GENERIC = {"letterboxd", "letterboxd - not found"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    NAME_RE = r"(.+?)[’']s profile"
    FILMS = r"([\d,]+) films? watched"
    FAVORITES = r"Favorites:\s*(.+?)(?:\.\s*Bio:|$)"
    BIO = r"Bio:\s*(.+)"


class AcademiaEduConstants:
    NAME = "Academia.edu"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://independent.academia.edu/{username}"
    GENERIC = {"academia.edu", "academia.edu - share research"}
    AVATAR_KEYS = ("photo",)
    COVER_KEYS = ()
    INTERESTS = r"\.interests\s*=\s*(\[.*?\])"
    MAX_INTERESTS = 20


class StackOverflowConstants:
    NAME = "Stack Overflow"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://stackoverflow.com/users/{username}"
    GENERIC = {"page not found - stack overflow", "stack overflow", "user not found - stack overflow"}
    QUESTION_API = "https://api.stackexchange.com/2.3/questions/{id}?site=stackoverflow"
    QUESTION_RE = r"/(?:questions|q)/(\d+)"
    AVATAR_KEYS = ("profile_image",)
    COVER_KEYS = ()


class StackExchangeConstants:
    NAME = "Stack Exchange"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://stackexchange.com/users/{username}"
    GENERIC = {"page not found - stack exchange", "stack exchange", "user not found - stack exchange"}
    AVATAR_KEYS = ("profile_image",)
    COVER_KEYS = ()


class GitHubConstants:
    NAME = "GitHub"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$"
    PROFILE_URL = "https://github.com/{username}"
    API_URL = "https://api.github.com/users/{username}"
    REPO_API = "https://api.github.com/repos/{owner}/{repo}"
    REPO_RE = r"github\.com/([^/?#]+)/([^/?#]+)"


class GitLabConstants:
    NAME = "GitLab"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,255}$"
    PROFILE_URL = "https://gitlab.com/{username}"
    API_URL = "https://gitlab.com/api/v4/users?username={username}"
    PROJECT_API = "https://gitlab.com/api/v4/projects/{path}"
    PROJECT_RE = r"gitlab\.com/(.+)"


class HackerNewsConstants:
    NAME = "Hacker News"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,15}$"
    PROFILE_URL = "https://news.ycombinator.com/user?id={username}"
    API_URL = "https://hacker-news.firebaseio.com/v0/user/{username}.json"


class ProductHuntConstants:
    NAME = "Product Hunt"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://www.producthunt.com/@{username}"
    GENERIC = {"product hunt", "product hunt – the best new products in tech."}
    AVATAR_KEYS = ("profile_image", "avatar")
    COVER_KEYS = ()
    IMPERSONATE = "safari"


class MediumConstants:
    NAME = "Medium"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://medium.com/@{username}"
    API_URL = "https://medium.com/@{username}?format=json"
    JSON_PREFIX = "])}while(1);</x>"


class SubstackConstants:
    NAME = "Substack"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://substack.com/@{username}"
    GENERIC = {"substack", "substack - a new economic engine for culture"}
    AVATAR_KEYS = ("photo_url", "avatar")
    COVER_KEYS = ("cover_photo_url",)


class FandomConstants:
    NAME = "Fandom"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://community.fandom.com/wiki/User:{username}"
    GENERIC = {"community central | fandom", "fandom"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class SteamCommunityConstants:
    NAME = "Steam Community"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,32}$"
    PROFILE_URL = "https://steamcommunity.com/id/{username}"
    XML_URL = "https://steamcommunity.com/id/{username}?xml=1"
    GENERIC = {"steam community", "steam community :: error"}
    AVATAR_KEYS = ("avatarFull", "avatarMedium")
    COVER_KEYS = ()
    XML_FIELD = r"<{tag}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{tag}>"


class RobloxConstants:
    NAME = "Roblox"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{3,20}$"
    PROFILE_URL = "https://www.roblox.com/users/profile?username={username}"
    RESOLVE_URL = "https://users.roblox.com/v1/usernames/users"
    DETAIL_URL = "https://users.roblox.com/v1/users/{id}"
    AVATAR_URL = "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={id}&size=420x420&format=Png&isCircular=false"
    GENERIC = {"page cannot be found or no longer exists - roblox", "roblox"}
    AVATAR_KEYS = ("imageUrl",)
    COVER_KEYS = ()


class GameJoltConstants:
    NAME = "Game Jolt"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,30}$"
    PROFILE_URL = "https://gamejolt.com/@{username}"
    API_URL = "https://gamejolt.com/site-api/web/profile/@{username}"


class MyAnimeListConstants:
    NAME = "MyAnimeList"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,16}$"
    PROFILE_URL = "https://myanimelist.net/profile/{username}"
    GENERIC = {"404 not found - myanimelist.net", "myanimelist"}
    AVATAR_KEYS = ("userimages",)
    COVER_KEYS = ()


class AniListConstants:
    NAME = "AniList"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,20}$"
    PROFILE_URL = "https://anilist.co/user/{username}"
    GQL_URL = "https://graphql.anilist.co"
    GQL_QUERY = (
        "query($name:String){User(name:$name){id name about "
        "avatar{large medium} bannerImage createdAt updatedAt donatorTier donatorBadge "
        "statistics{anime{count minutesWatched} manga{count chaptersRead}}}}"
    )


class InterPalsConstants:
    NAME = "InterPals"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.interpals.net/{username}"
    GENERIC = {"interpals"}
    AVATAR_KEYS = ()
    COVER_KEYS = ()


class LiveJournalConstants:
    NAME = "LiveJournal"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,15}$"
    PROFILE_URL = "https://{username}.livejournal.com/profile"
    GENERIC = {"livejournal", "livejournal: discover global communities of bloggers who share your unique passions and interests."}
    AVATAR_KEYS = ("userpic",)
    COVER_KEYS = ()


class PlurkConstants:
    NAME = "Plurk"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://www.plurk.com/{username}"
    GENERIC = {"plurk", "plurk - a social journal for your life", "user not found! - plurk"}
    AVATAR_KEYS = ("avatar_big", "avatar")
    COVER_KEYS = ("profile_cover",)


class MisskeyConstants:
    NAME = "Misskey"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,20}$"
    PROFILE_URL = "https://misskey.io/@{username}"
    API_URL = "https://misskey.io/api/users/show"
    GENERIC = {"misskey", "misskey.io"}
    AVATAR_KEYS = ("avatarUrl",)
    COVER_KEYS = ("bannerUrl",)


class NostrConstants:
    NAME = "Nostr"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9._@-]{1,128}$"
    PROFILE_URL = "https://njump.me/{username}"
    GENERIC_DESCRIPTIONS = ("njump is",)


class MicroBlogConstants:
    NAME = "Micro.blog"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://micro.blog/{username}"
    GENERIC = {"micro.blog"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class VimeoConstants:
    NAME = "Vimeo"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://vimeo.com/{username}"
    API_URL = "https://vimeo.com/api/v2/{username}/info.json"
    VIDEO_API = "https://vimeo.com/api/v2/video/{id}.json"
    VIDEO_RE = r"vimeo\.com/(\d+)"


class PatreonConstants:
    NAME = "Patreon"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.patreon.com/{username}"
    GENERIC = {"not found | patreon", "patreon"}
    AVATAR_KEYS = ("avatar_photo_url",)
    COVER_KEYS = ("cover_photo_url",)


class LinktreeConstants:
    NAME = "Linktree"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://linktr.ee/{username}"
    GENERIC = {"linktree", "linktree | page not found"}
    AVATAR_KEYS = ("profilePictureUrl",)
    COVER_KEYS = ()
    SOCIAL_LINKS = r'"type":"[^"]+","url":"(https?:(?:[^"\\]|\\.)+?)"'


class AboutMeConstants:
    NAME = "About.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://about.me/{username}"
    GENERIC = {"about.me"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ("background_url",)
    DATA_KEY = "profile"
    LINK_PLATFORMS = frozenset({
        "twitter", "instagram", "linkedin", "facebook", "youtube", "github",
        "pinterest", "tumblr", "flickr", "vimeo", "behance", "dribbble", "soundcloud",
    })


class GravatarConstants:
    NAME = "Gravatar"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://gravatar.com/{username}"
    API_URL = "https://gravatar.com/{username}.json"


class KeybaseConstants:
    NAME = "Keybase"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{2,16}$"
    PROFILE_URL = "https://keybase.io/{username}"
    API_URL = "https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}"


class DockerHubConstants:
    NAME = "Docker Hub"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9]{4,30}$"
    PROFILE_URL = "https://hub.docker.com/u/{username}"
    API_URL = "https://hub.docker.com/v2/users/{username}"


class OpenSeaConstants:
    NAME = "OpenSea"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^(?:0x[a-fA-F0-9]{40}|[A-Za-z0-9_]{2,32})$"
    PROFILE_URL = "https://opensea.io/{username}"
    GENERIC = {"opensea", "opensea, exchange everything — token trading and nft marketplace"}
    DATA_KEY = "profileByIdentifierV2"
    MAX_BYTES = 1_600_000


class CodePenConstants:
    NAME = "CodePen"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://codepen.io/{username}"
    GENERIC = {"404 on codepen", "codepen"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    NAME_SUFFIX = " on CodePen"


class ChessComConstants:
    NAME = "Chess.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{3,25}$"
    PROFILE_URL = "https://www.chess.com/member/{username}"
    API_URL = "https://api.chess.com/pub/player/{username}"


class LichessConstants:
    NAME = "Lichess"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{2,30}$"
    PROFILE_URL = "https://lichess.org/@/{username}"
    API_URL = "https://lichess.org/api/user/{username}"


class SpeedrunComConstants:
    NAME = "Speedrun.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.speedrun.com/users/{username}"
    API_URL = "https://www.speedrun.com/api/v1/users/{username}"


class DailymotionConstants:
    NAME = "Dailymotion"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.dailymotion.com/{username}"
    API_URL = "https://api.dailymotion.com/user/{username}?fields=id,screenname,username,description,avatar_720_url,cover_url,url,followers_total,videos_total,views_total,created_time,country,language,verified"
    DEFAULT_AVATAR = "dmcdn.net/d/"


class GIPHYConstants:
    NAME = "GIPHY"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://giphy.com/{username}"
    GENERIC = {"gifs - find & share on giphy", "giphy"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ("banner_url",)
    NAME_MARKER = " GIFs on GIPHY"


class UnsplashConstants:
    NAME = "Unsplash"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,60}$"
    PROFILE_URL = "https://unsplash.com/@{username}"
    GENERIC = {"page not found | unsplash", "unsplash"}
    AVATAR_KEYS = ("profile_image",)
    COVER_KEYS = ()


class PexelsConstants:
    NAME = "Pexels"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.pexels.com/@{username}"
    GENERIC = {"error 404 - pexels", "pexels"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    NAME_SUFFIX = " - Photography"
    FOLLOWERS = r'"followers_count":(\d+)'
    PHOTOS = r'"photos_count":(\d+)'


class WikipediaConstants:
    NAME = "Wikipedia"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[^\s/?#&:]{1,85}$"
    PROFILE_URL = "https://en.wikipedia.org/wiki/User:{username}"
    API_URL = "https://en.wikipedia.org/w/api.php?action=query&list=users&ususers={username}&usprop=registration|editcount|groups&format=json"


class XINGConstants:
    NAME = "XING"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.xing.com/profile/{username}"
    GENERIC = {"404 - not found | xing", "xing"}
    AVATAR_KEYS = ("profileImage",)
    COVER_KEYS = ()


class WellfoundConstants:
    NAME = "Wellfound"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://wellfound.com/u/{username}"
    GENERIC = {"page not found - 404 | wellfound", "wellfound"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ()


class HabrConstants:
    NAME = "Habr"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://habr.com/ru/users/{username}/"
    GENERIC = {"habr", "хабр"}
    AVATAR_KEYS = ("avatarUrl",)
    COVER_KEYS = ()


class PikabuConstants:
    NAME = "Pikabu"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://pikabu.ru/@{username}"
    GENERIC = {"404. страница не найдена", "pikabu", "пикабу"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class WordPressComConstants:
    NAME = "WordPress.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9.-]{1,63}$"
    PROFILE_URL = "https://{username}.wordpress.com"
    API_URL = "https://public-api.wordpress.com/rest/v1.1/sites/{username}.wordpress.com"


class MixcloudConstants:
    NAME = "Mixcloud"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.mixcloud.com/{username}/"
    API_URL = "https://api.mixcloud.com/{username}/"
    CLOUDCAST_API = "https://api.mixcloud.com/{path}/"
    CLOUDCAST_RE = r"mixcloud\.com/([^/?#]+/[^/?#]+)"


class ItchIoConstants:
    NAME = "itch.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9_-]{1,63}$"
    PROFILE_URL = "https://{username}.itch.io"
    GENERIC = {"itch.io"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    NAME_SUFFIX = " - itch.io"
    REL_ME = r'href="(https?://[^"]+)"\s+rel="me"'


class MinecraftConstants:
    NAME = "Minecraft"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,16}$"
    PROFILE_URL = "https://namemc.com/profile/{username}"
    API_URL = "https://api.mojang.com/users/profiles/minecraft/{username}"


class OsuConstants:
    NAME = "osu!"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9_ \[\]-]{1,32}$"
    PROFILE_URL = "https://osu.ppy.sh/users/{username}"
    GENERIC = {"osu!"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ("cover_url",)
    INITIAL_DATA = r'data-initial-data="([^"]+)"'


class CodeforcesConstants:
    NAME = "Codeforces"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.-]{3,24}$"
    PROFILE_URL = "https://codeforces.com/profile/{username}"
    API_URL = "https://codeforces.com/api/user.info?handles={username}"


class LeetCodeConstants:
    NAME = "LeetCode"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://leetcode.com/u/{username}/"
    GENERIC = {"leetcode", "page not found - leetcode"}
    AVATAR_KEYS = ("userAvatar",)
    COVER_KEYS = ()
    GQL_URL = "https://leetcode.com/graphql"
    GQL_QUERY = (
        "query($u:String!){matchedUser(username:$u){username githubUrl twitterUrl linkedinUrl "
        "profile{realName aboutMe userAvatar ranking countryName company school websites reputation postViewCount}}}"
    )


class HackerRankConstants:
    NAME = "HackerRank"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.hackerrank.com/profile/{username}"
    API_URL = "https://www.hackerrank.com/rest/contests/master/hackers/{username}/profile"


class CodewarsConstants:
    NAME = "Codewars"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.codewars.com/users/{username}"
    API_URL = "https://www.codewars.com/api/v1/users/{username}"


class KaggleConstants:
    NAME = "Kaggle"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9]{1,64}$"
    PROFILE_URL = "https://www.kaggle.com/{username}"
    GENERIC = {"kaggle", "kaggle: your home for data science"}
    AVATAR_KEYS = ("avatarUrl",)
    COVER_KEYS = ()


class CratesIoConstants:
    NAME = "crates.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://crates.io/users/{username}"
    API_URL = "https://crates.io/api/v1/users/{username}"


class DEVCommunityConstants:
    NAME = "DEV Community"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://dev.to/{username}"
    API_URL = "https://dev.to/api/users/by_username?url={username}"


class HashnodeConstants:
    NAME = "Hashnode"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://hashnode.com/@{username}"
    GENERIC = {"hashnode", "user not found | hashnode"}
    AVATAR_KEYS = ("profilePicture",)
    COVER_KEYS = ()
    HANDLE = r"\(@([^)]+)\)"
    NAME_SPLIT = " (@"
    DESC_TRIM = "Read the latest articles"


class GumroadConstants:
    NAME = "Gumroad"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9-]{1,63}$"
    PROFILE_URL = "https://{username}.gumroad.com"
    GENERIC = {"gumroad", "page not found (404) - gumroad"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ()
    NAME_PREFIX = "Subscribe to "


class RedbubbleConstants:
    NAME = "Redbubble"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.redbubble.com/people/{username}/shop"
    GENERIC = {"404 page not found | redbubble | redbubble", "redbubble"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class KitsuConstants:
    NAME = "Kitsu"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://kitsu.io/users/{username}"
    API_URL = "https://kitsu.io/api/edge/users?filter[name]={username}"


class RubyGemsConstants:
    NAME = "RubyGems"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://rubygems.org/profiles/{username}"
    GENERIC = {"page not found | rubygems.org", "rubygems.org"}
    AVATAR_KEYS = ()
    COVER_KEYS = ()


class ScratchConstants:
    NAME = "Scratch"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{3,20}$"
    PROFILE_URL = "https://scratch.mit.edu/users/{username}/"
    API_URL = "https://api.scratch.mit.edu/users/{username}"
    PROJECT_API = "https://api.scratch.mit.edu/projects/{id}"
    STUDIO_API = "https://api.scratch.mit.edu/studios/{id}"


class HouzzConstants:
    NAME = "Houzz"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.houzz.com/user/{username}"
    GENERIC = {"page not found"}
    AVATAR_KEYS = ("profileImage",)
    COVER_KEYS = ()


class SmuleConstants:
    NAME = "Smule"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.-]{1,64}$"
    PROFILE_URL = "https://www.smule.com/{username}"
    GENERIC = {"smule", "smule | page not found (404)"}
    AVATAR_KEYS = ("pic_url",)
    COVER_KEYS = ()


class NotionConstants:
    NAME = "Notion"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.notion.so/@{username}"
    GENERIC = {"notion", "page not found"}
    AVATAR_KEYS = ("profile_photo",)
    COVER_KEYS = ()


class TellonymConstants:
    NAME = "Tellonym"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.]{1,30}$"
    PROFILE_URL = "https://tellonym.me/{username}"
    AVATAR_KEYS = ("avatarFileName",)
    COVER_KEYS = ()


class BIGOLIVEConstants:
    NAME = "BIGO LIVE"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.-]{1,64}$"
    PROFILE_URL = "https://www.bigo.tv/user/{username}"
    GENERIC = {"bigo live", "bigo live - broadcast & explore live streaming"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()
    ABSENT_MARKER = "account-inactivation"


class EBayConstants:
    NAME = "eBay"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.*-]{1,64}$"
    PROFILE_URL = "https://www.ebay.com/usr/{username}"
    GENERIC = {"ebay", "ebay home", "error page | ebay", "security measure"}
    AVATAR_KEYS = ()
    COVER_KEYS = ()


class SlideShareConstants:
    NAME = "SlideShare"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.slideshare.net/{username}"
    GENERIC = {"page no longer exists"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class AudiomackConstants:
    NAME = "Audiomack"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://audiomack.com/{username}"
    GENERIC = {"audiomack", "audiomack - music platform empowering artists & fans | audiomack"}
    AVATAR_KEYS = ("image",)
    COVER_KEYS = ()


class BeaconsConstants:
    NAME = "Beacons"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.-]{1,64}$"
    PROFILE_URL = "https://beacons.ai/{username}"
    GENERIC = {"beacons", "beacons | mobile websites for creators"}
    AVATAR_KEYS = ("profilePicture",)
    COVER_KEYS = ()
    HANDLE = r"@([A-Za-z0-9_.-]+)"
    BIO_TRIM = ("Featured links:", "Email signup", "Shop featured")
    BIO_DEFAULT = ("make your own beacons page", "make your own page like this")


class SpotifyConstants:
    NAME = "Spotify"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://open.spotify.com/user/{username}"
    GENERIC = {"spotify – web player", "spotify - web player", "spotify – web player: music for everyone", "spotify - web player: music for everyone"}
    GENERIC_DESCRIPTIONS = ("spotify is a digital music service", "listen to")


class TraktConstants:
    NAME = "Trakt"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://trakt.tv/users/{username}"
    GENERIC = {"trakt", "trakt web: profile"}
    NOT_FOUND_TITLE = "404: nothingness. the void."
    GENERIC_DESCRIPTIONS = ("trakt web:", "trakt:")


class OnlyFansConstants:
    NAME = "OnlyFans"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9_.-]{1,64}$"
    PROFILE_URL = "https://onlyfans.com/{username}"
    GENERIC = {"onlyfans"}
    GENERIC_DESCRIPTIONS = ("onlyfans is the social platform",)


class FigmaConstants:
    NAME = "Figma"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.figma.com/@{username}"
    GENERIC_DESCRIPTIONS = ("figma is the",)


class BitChuteConstants:
    NAME = "BitChute"
    CRAWL_TYPE = "playwright"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.bitchute.com/channel/{username}/"
    GENERIC_DESCRIPTIONS = ("bitchute is",)


class DeviantArtConstants:
    NAME = "DeviantArt"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9-]{3,20}$"
    PROFILE_URL = "https://www.deviantart.com/{username}"


class DouyinConstants:
    NAME = "Douyin"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://www.douyin.com/user/{username}"


class FiveHundredPxConstants:
    NAME = "500px"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://500px.com/p/{username}"


class GabConstants:
    NAME = "Gab"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://gab.com/{username}"


class GettrConstants:
    NAME = "GETTR"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://gettr.com/user/{username}"


class KuaishouConstants:
    NAME = "Kuaishou"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://www.kuaishou.com/profile/{username}"


class MindsConstants:
    NAME = "Minds"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_]{1,50}$"
    PROFILE_URL = "https://www.minds.com/{username}"


class ParlerConstants:
    NAME = "Parler"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://parler.com/{username}"


class PixivConstants:
    NAME = "Pixiv"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,32}$"
    PROFILE_URL = "https://www.pixiv.net/users/{username}"


class ResearchGateConstants:
    NAME = "ResearchGate"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.researchgate.net/profile/{username}"


class SoundCloudConstants:
    NAME = "SoundCloud"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_-]{3,25}$"
    PROFILE_URL = "https://soundcloud.com/{username}"


class StravaConstants:
    NAME = "Strava"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,32}$"
    PROFILE_URL = "https://www.strava.com/athletes/{username}"


class TelegramConstants:
    NAME = "Telegram"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_]{4,32}$"
    PROFILE_URL = "https://t.me/{username}"


class TruthSocialConstants:
    NAME = "Truth Social"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_]{1,30}$"
    PROFILE_URL = "https://truthsocial.com/@{username}"


class TumblrConstants:
    NAME = "Tumblr"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9-]{1,32}$"
    PROFILE_URL = "https://www.tumblr.com/{username}"


class VKConstants:
    NAME = "VK"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_.]{5,32}$"
    PROFILE_URL = "https://vk.com/{username}"


class WattpadConstants:
    NAME = "Wattpad"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.wattpad.com/user/{username}"


class WeiboConstants:
    NAME = "Weibo"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://weibo.com/u/{username}"


class XiaohongshuConstants:
    NAME = "Xiaohongshu"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://www.xiaohongshu.com/user/profile/{username}"


class ZhihuConstants:
    NAME = "Zhihu"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://www.zhihu.com/people/{username}"


class LinkedInConstants:
    NAME = "LinkedIn"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9-]{3,100}$"
    PROFILE_URL = "https://www.linkedin.com/in/{username}"


class SnapchatConstants:
    NAME = "Snapchat"
    CRAWL_TYPE = "online"
    GRAMMAR = "^[A-Za-z0-9._-]{3,15}$"
    PROFILE_URL = "https://www.snapchat.com/add/{username}"


class ImoConstants:
    NAME = "imo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://imo.im/{username}"
    GENERIC = set()

class LineConstants:
    NAME = "LINE"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://line.me/ti/p/{username}"
    GENERIC = {'add line friend'}

class MessengerConstants:
    NAME = "Messenger"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://m.me/{username}"
    GENERIC = {'messenger'}

class NaverCafeConstants:
    NAME = "Naver Cafe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cafe.naver.com/{username}"
    GENERIC = {'네이버 카페'}

class QQConstants:
    NAME = "QQ"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://user.qzone.qq.com/{username}"
    GENERIC = {'404'}

class ViberConstants:
    NAME = "Viber"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://invite.viber.com/?g2={username}"
    GENERIC = {'community landing page on viber'}

class WeChatConstants:
    NAME = "WeChat"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://u.wechat.com/{username}"
    GENERIC = {'wechat - connects with over 1 billion users | chats · calls · life services'}

class YuboConstants:
    NAME = "Yubo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://yubo.live/{username}"
    GENERIC = set()

class DiscordConstants:
    NAME = "Discord"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discord.com/users/{username}"
    GENERIC = {'discord', 'discord - group chat that’s all fun & games'}

class WhatsAppConstants:
    NAME = "WhatsApp"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wa.me/{username}"
    GENERIC = {'share on whatsapp'}

class WordPressOrgConstants:
    NAME = "WordPressOrg"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profiles.wordpress.org/{username}/"
    GENERIC = set()

class SourceForgeConstants:
    NAME = "SourceForge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sourceforge.net/u/{username}/profile"
    GENERIC = set()

class BloggerConstants:
    NAME = "Blogger"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.blogspot.com"
    GENERIC = set()

class BloggerBloggerComConstants:
    NAME = "Blogger (blogger.com)"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.blogger.com/profile/{username}"
    GENERIC = set()

class TripAdvisorConstants:
    NAME = "TripAdvisor"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tripadvisor.com/members/{username}"
    GENERIC = set()

class MyspaceConstants:
    NAME = "Myspace"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://myspace.com/{username}"
    GENERIC = set()

class ThemeForestConstants:
    NAME = "ThemeForest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://themeforest.net/user/{username}"
    GENERIC = set()

class WeforumConstants:
    NAME = "Weforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.weforum.org/people/{username}"
    GENERIC = set()

class FreepikConstants:
    NAME = "Freepik"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.freepik.com/author/{username}"
    GENERIC = set()

class ChangeOrgConstants:
    NAME = "Change.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.change.org/o/{username}"
    GENERIC = set()

class SlackConstants:
    NAME = "Slack"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.slack.com"
    GENERIC = set()

class DisqusConstants:
    NAME = "Disqus"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://disqus.com/{username}"
    GENERIC = set()

class NPMConstants:
    NAME = "NPM"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.npmjs.com/~{username}"
    GENERIC = set()

class DigitalOceanConstants:
    NAME = "DigitalOcean"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.digitalocean.com/community/users/{username}"
    GENERIC = set()

class InstructablesConstants:
    NAME = "Instructables"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.instructables.com/member/{username}"
    GENERIC = set()

class AmebloConstants:
    NAME = "Ameblo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ameblo.jp/{username}"
    GENERIC = set()

class HuggingFaceConstants:
    NAME = "HuggingFace"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://huggingface.co/{username}"
    GENERIC = set()

class LaracastConstants:
    NAME = "Laracast"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://laracasts.com/@{username}"
    GENERIC = set()

class BitBucketConstants:
    NAME = "BitBucket"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bitbucket.org/{username}/"
    GENERIC = set()

class UpworkConstants:
    NAME = "Upwork"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://upwork.com/fl/{username}"
    GENERIC = set()

class IStockConstants:
    NAME = "iStock"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.istockphoto.com/ru/portfolio/{username}"
    GENERIC = {'istock'}

class PastebinConstants:
    NAME = "Pastebin"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pastebin.com/u/{username}"
    GENERIC = set()

class FoursquareConstants:
    NAME = "Foursquare"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://foursquare.com/{username}"
    GENERIC = set()

class DiscogsConstants:
    NAME = "Discogs"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.discogs.com/user/{username}"
    API_URL = "https://api.discogs.com/users/{username}"
    ARTIST_API = "https://api.discogs.com/artists/{id}"
    GENERIC = set()

class KofiConstants:
    NAME = "kofi"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ko-fi.com/{username}"
    GENERIC = set()

class RottentomatoesConstants:
    NAME = "Rottentomatoes"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.rottentomatoes.com/critic/{username}/movies"
    GENERIC = set()

class SmugmugConstants:
    NAME = "Smugmug"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.smugmug.com/"
    GENERIC = set()

class DuolingoConstants:
    NAME = "Duolingo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.duolingo.com/profile/{username}"
    GENERIC = set()

class UstreamConstants:
    NAME = "Ustream"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.ustream.tv/channel/adam{username}"
    GENERIC = set()

class WikidotConstants:
    NAME = "Wikidot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.wikidot.com/user:info/{username}"
    GENERIC = set()

class ImageShackConstants:
    NAME = "ImageShack"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://imageshack.com/user/{username}"
    GENERIC = {'imageshack - best place for all of your image hosting and image sharing needs'}

class BuyMeACoffeeConstants:
    NAME = "BuyMeACoffee"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://buymeacoff.ee/{username}"
    GENERIC = set()

class GiteaConstants:
    NAME = "Gitea"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gitea.com/{username}"
    GENERIC = set()

class GeniusConstants:
    NAME = "Genius"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://genius.com/{username}"
    GENERIC = set()

class HubPagesConstants:
    NAME = "HubPages"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hubpages.com/@{username}"
    GENERIC = set()

class PbaseConstants:
    NAME = "Pbase"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pbase.com/{username}/profile"
    GENERIC = {'pbase unknown artist'}

class GeeksforGeeksConstants:
    NAME = "Geeksfor Geeks"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://auth.geeksforgeeks.org/user/{username}"
    GENERIC = {'undefined   | geeksforgeeks profile', 'undefined | geeksforgeeks profile'}

class CodebergOrgConstants:
    NAME = "codeberg.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://codeberg.org/{username}"
    GENERIC = set()

class AllRecipesConstants:
    NAME = "AllRecipes"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.allrecipes.com/cook/{username}"
    GENERIC = {'sign in to allrecipes'}

class CodecanyonConstants:
    NAME = "Codecanyon"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://codecanyon.net/user/{username}"
    GENERIC = set()

class CodecademyConstants:
    NAME = "Codecademy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.codecademy.com/profiles/{username}"
    GENERIC = {'profile not found | codecademy'}

class PolygonConstants:
    NAME = "Polygon"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.polygon.com/users/{username}"
    GENERIC = set()

class PCGamerConstants:
    NAME = "PCGamer"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.pcgamer.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | pc gamer forums'}

class DreamstimeConstants:
    NAME = "Dreamstime"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.dreamstime.com/{username}_info"
    GENERIC = set()

class SpeakerdeckConstants:
    NAME = "Speakerdeck"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://speakerdeck.com/{username}"
    GENERIC = set()

class NextcloudForumConstants:
    NAME = "Nextcloud Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://help.nextcloud.com/u/{username}/summary"
    GENERIC = set()

class MaxConstants:
    NAME = "Max"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://max.ru/{username}"
    GENERIC = {'max — быстрое и легкое приложение для общения и решения повседневных задач', 'max — быстрое и легкое приложение для общения и решения пов…'}

class TVTropesConstants:
    NAME = "TVTropes"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tvtropes.org/pmwiki/pmwiki.php/Tropers/{username}"
    GENERIC = set()

class TistoryConstants:
    NAME = "Tistory"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.tistory.com/"
    GENERIC = set()

class JSFiddleConstants:
    NAME = "JSFiddle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://jsfiddle.net/user/{username}/"
    GENERIC = set()

class GamesRadarConstants:
    NAME = "GamesRadar"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.gamesradar.com/uk/author/{username}/"
    GENERIC = set()

class GeocachingConstants:
    NAME = "Geocaching"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.geocaching.com/p/?u={username}"
    GENERIC = set()

class GogConstants:
    NAME = "Gog"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.gog.com/u/{username}"
    GENERIC = set()

class CoubConstants:
    NAME = "Coub"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://coub.com/{username}"
    GENERIC = set()

class OdyseeConstants:
    NAME = "Odysee"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://odysee.com/@{username}"
    GENERIC = {'odysee'}

class ReplitConstants:
    NAME = "Replit"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://replit.com/@{username}"
    GENERIC = set()

class HackMDConstants:
    NAME = "Hack MD"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hackmd.io/@{username}"
    GENERIC = set()

class INaturalistConstants:
    NAME = "iNaturalist"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.inaturalist.org/lists/{username}"
    GENERIC = set()

class TemplateMonsterConstants:
    NAME = "TemplateMonster"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.templatemonster.com/authors/{username}/"
    GENERIC = set()

class TeletypeConstants:
    NAME = "Teletype"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://teletype.in/@{username}"
    GENERIC = set()

class CTANConstants:
    NAME = "CTAN"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ctan.org/author/{username}"
    GENERIC = set()

class OpenCollectiveConstants:
    NAME = "OpenCollective"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://opencollective.com/{username}"
    GENERIC = set()

class GiantbombConstants:
    NAME = "Giantbomb"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.giantbomb.com/profile/{username}"
    GENERIC = set()

class JAlbumNetConstants:
    NAME = "jAlbum.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.jalbum.net/"
    GENERIC = set()

class NewgroundsConstants:
    NAME = "Newgrounds"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.newgrounds.com"
    GENERIC = set()

class SlidesConstants:
    NAME = "Slides"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://slides.com/{username}"
    GENERIC = set()

class UltimateGuitarConstants:
    NAME = "Ultimate-Guitar"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ultimate-guitar.com/u/{username}"
    GENERIC = set()

class ContentlyConstants:
    NAME = "Contently"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.contently.com/"
    GENERIC = {'contently: content for regulated industries'}

class CreativeMarketConstants:
    NAME = "CreativeMarket"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://creativemarket.com/users/{username}"
    GENERIC = set()

class OpenSourceConstants:
    NAME = "OpenSource"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://opensource.com/users/{username}"
    GENERIC = set()

class ImgflipConstants:
    NAME = "Imgflip"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://imgflip.com/user/{username}"
    GENERIC = set()

class HackadayConstants:
    NAME = "Hackaday"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hackaday.io/{username}"
    GENERIC = set()

class FodorsConstants:
    NAME = "Fodors"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.fodors.com/community/profile/{username}/forum-activity"
    GENERIC = set()

class Designs99Constants:
    NAME = "Designs99"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://99designs.com/profiles/{username}"
    GENERIC = set()

class PeriscopeConstants:
    NAME = "Periscope"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pscp.tv/{username}"
    GENERIC = set()

class FreesoundConstants:
    NAME = "Freesound"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://freesound.org/people/{username}/"
    GENERIC = set()

class MetalArchivesConstants:
    NAME = "Metal-archives"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.metal-archives.com/users/{username}"
    GENERIC = set()

class KongregateConstants:
    NAME = "Kongregate"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.kongregate.com/accounts/{username}"
    GENERIC = set()

class SoupConstants:
    NAME = "Soup"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.soup.io/author/{username}"
    GENERIC = {'soup.io'}

class FurAffinityConstants:
    NAME = "Fur Affinity"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.furaffinity.net/gallery/{username}"
    GENERIC = set()

class ItemFixConstants:
    NAME = "ItemFix"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.itemfix.com/c/{username}"
    GENERIC = {'itemfix - channel:'}

class NintendoLifeConstants:
    NAME = "Nintendo Life"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.nintendolife.com/users/{username}"
    GENERIC = set()

class CarbonmadeConstants:
    NAME = "Carbonmade"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.carbonmade.com"
    GENERIC = set()

class ModDBConstants:
    NAME = "ModDB"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.moddb.com/members/{username}"
    GENERIC = set()

class AudiojungleConstants:
    NAME = "Audiojungle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://audiojungle.net/user/{username}"
    GENERIC = set()

class TinderConstants:
    NAME = "Tinder"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tinder.com/@{username}"
    GENERIC = set()

class DomestikaOrgConstants:
    NAME = "domestika.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.domestika.org/{username}"
    GENERIC = set()

class NoblogsConstants:
    NAME = "Noblogs"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://noblogs.org/members/{username}/"
    GENERIC = set()

class SetlistConstants:
    NAME = "Setlist"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.setlist.fm/user/{username}"
    GENERIC = set()

class StarCitizenConstants:
    NAME = "Star Citizen"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://robertsspaceindustries.com/citizens/{username}"
    ORG_URL = "https://robertsspaceindustries.com/orgs/{sid}"
    PAIRS = r'<span class="label">([^<]+)</span>\s*<strong class="value">([^<]*)</strong>'
    MONIKER = r'<div class="info">\s*<p class="entry">\s*<strong class="value">([^<]+)</strong>'
    RANK = r'<span class="value">\s*([^<]+?)\s*</span>'
    AVATAR = r'<div class="thumb">\s*<img src="([^"]+)"'
    BIO = r'<div class="entry bio">\s*<div class="value">(.*?)</div>'
    ORG_TITLE = r"^(.*?)\s*\[([^\]]+)\]\s*-\s*Organizations"
    ORG_MEMBERS = r'([\d,]+)\s*</span>\s*<span[^>]*>\s*members'

class JigsawplanetConstants:
    NAME = "Jigsawplanet"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.jigsawplanet.com/{username}"
    GENERIC = set()

class NamuwikiConstants:
    NAME = "Namuwiki"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://namu.wiki/w/%EC%82%AC%EC%9A%A9%EC%9E%90:{username}"
    GENERIC = set()

class GaiaOnlineConstants:
    NAME = "GaiaOnline"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.gaiaonline.com/profiles/{username}"
    GENERIC = {'general error | gaia online'}

class MemriseConstants:
    NAME = "Memrise"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.memrise.com/user/{username}/"
    GENERIC = set()

class ArchiveOfOurOwnConstants:
    NAME = "ArchiveOfOurOwn"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://archiveofourown.org/users/{username}"
    GENERIC = set()

class PlanetMinecraftConstants:
    NAME = "PlanetMinecraft"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.planetminecraft.com/member/{username}"
    GENERIC = set()

class MuseScoreConstants:
    NAME = "Muse Score"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://musescore.com/{username}"
    GENERIC = set()

class TheOdysseyOnlineConstants:
    NAME = "TheOdysseyOnline"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.theodysseyonline.com/user/@{username}"
    GENERIC = set()

class SportsRuConstants:
    NAME = "sports.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.sports.ru/profile/{username}/"
    GENERIC = set()

class PicsartConstants:
    NAME = "Picsart"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://picsart.com/u/{username}"
    GENERIC = {'picsart'}

class WowheadConstants:
    NAME = "Wowhead"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.wowhead.com/user={username}"
    GENERIC = set()

class ArmorgamesConstants:
    NAME = "Armorgames"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://armorgames.com/user/{username}"
    GENERIC = set()

class FotkiConstants:
    NAME = "Fotki"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://members.fotki.com/{username}/about/"
    GENERIC = {"making sure you're not a bot!"}

class PaltalkConstants:
    NAME = "Paltalk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.paltalk.com/people/users/{username}"
    GENERIC = {'chat room member on paltalk'}

class VideoHiveConstants:
    NAME = "VideoHive"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://videohive.net/user/{username}"
    GENERIC = set()

class ClubhouseConstants:
    NAME = "Clubhouse"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.clubhouse.com/@{username}"
    GENERIC = set()

class ProzaRuConstants:
    NAME = "Proza.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.proza.ru/avtor/{username}"
    GENERIC = {'проза.ру'}

class NameprosConstants:
    NAME = "Namepros"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.namepros.com//members/?username={username}"
    GENERIC = {'notable members', 'notable members | namepros'}

class WriteAsConstants:
    NAME = "write.as"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://write.as/{username}"
    GENERIC = set()

class WarriorForumConstants:
    NAME = "Warrior Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.warriorforum.com/members/{username}.html"
    GENERIC = set()

class AreNaConstants:
    NAME = "are.na"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.are.na/{username}"
    GENERIC = set()

class WykopConstants:
    NAME = "Wykop"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.wykop.pl/ludzie/{username}/"
    GENERIC = set()

class ResidentAdvisorConstants:
    NAME = "ResidentAdvisor"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.residentadvisor.net/profile/{username}"
    GENERIC = {'ra'}

class SporcleConstants:
    NAME = "Sporcle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.sporcle.com/user/{username}/people"
    GENERIC = set()

class TreehouseConstants:
    NAME = "Treehouse"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://teamtreehouse.com/profiles/{username}"
    GENERIC = {'treehouse | sign in'}

class CoroflotConstants:
    NAME = "Coroflot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.coroflot.com/{username}"
    GENERIC = set()

class JeuxVideoConstants:
    NAME = "JeuxVideo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.jeuxvideo.com/profil/{username}?mode=infos"
    GENERIC = set()

class StihiRuConstants:
    NAME = "Stihi.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.stihi.ru/avtor/{username}"
    GENERIC = {'стихи.ру'}

class ExposureConstants:
    NAME = "Exposure"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.exposure.co/"
    GENERIC = set()

class LyricsTranslateConstants:
    NAME = "LyricsTranslate"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lyricstranslate.com/sco/translator/{username}"
    GENERIC = set()

class GuruConstants:
    NAME = "Guru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.guru.com/freelancers/{username}"
    GENERIC = set()

class GutefrageConstants:
    NAME = "Gutefrage"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.gutefrage.net/nutzer/{username}"
    GENERIC = set()

class CoderwallConstants:
    NAME = "Coderwall"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://coderwall.com/{username}"
    GENERIC = set()

class ObservableConstants:
    NAME = "Observable"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://observablehq.com/@{username}"
    GENERIC = {'page not found | observable'}

class PushSquareConstants:
    NAME = "PushSquare"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pushsquare.com/users/{username}"
    GENERIC = set()

class CodementorConstants:
    NAME = "Codementor"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.codementor.io/{username}"
    GENERIC = set()

class N4gConstants:
    NAME = "N4g"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://n4g.com/user/home/{username}"
    GENERIC = set()

class LomographyConstants:
    NAME = "Lomography"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.lomography.com/homes/{username}"
    GENERIC = set()

class PixelfedSocialConstants:
    NAME = "pixelfed.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pixelfed.social/{username}/"
    API_URL = "https://pixelfed.social/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()

class NeoseekerConstants:
    NAME = "Neoseeker"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.neoseeker.com/members/{username}/"
    GENERIC = set()

class SytheConstants:
    NAME = "Sythe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.sythe.org/members/?username={username}"
    GENERIC = set()

class FilmWebConstants:
    NAME = "FilmWeb"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.filmweb.pl/user/{username}"
    GENERIC = set()

class ListalConstants:
    NAME = "Listal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.listal.com/"
    GENERIC = {'listal - list the stuff you love! movies, tv, music, games and books'}

class SpatialConstants:
    NAME = "Spatial"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.spatial.io/@{username}"
    GENERIC = set()

class ParagraphConstants:
    NAME = "Paragraph"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://paragraph.com/@{username}"
    GENERIC = set()

class NotabugOrgConstants:
    NAME = "notabug.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://notabug.org/{username}"
    GENERIC = set()

class MydramalistConstants:
    NAME = "Mydramalist"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mydramalist.com/profile/{username}"
    GENERIC = set()

class PinkbikeConstants:
    NAME = "Pinkbike"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pinkbike.com/u/{username}/"
    GENERIC = set()

class ThechiveConstants:
    NAME = "Thechive"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://thechive.com/author/{username}"
    GENERIC = set()

class GoldderbyConstants:
    NAME = "Goldderby"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.goldderby.com/members/{username}/"
    GENERIC = set()

class MeetMeConstants:
    NAME = "MeetMe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.meetme.com/{username}"
    GENERIC = set()

class FlyertalkConstants:
    NAME = "Flyertalk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.flyertalk.com/forum/members/{username}.html"
    GENERIC = set()

class GBAtempNetConstants:
    NAME = "GBAtemp.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gbatemp.net//members/?username={username}"
    GENERIC = {'notable members', 'notable members | gbatemp.net - the independent video game community'}

class BrusheezyConstants:
    NAME = "Brusheezy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.brusheezy.com/members/{username}"
    GENERIC = {'free photoshop brushes at brusheezy!', 'photoshop resources for everyone.'}

class AvforumsConstants:
    NAME = "Avforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.avforums.com/members/?username={username}"
    GENERIC = set()

class MobypictureConstants:
    NAME = "Mobypicture"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mobypicture.com/user/{username}"
    GENERIC = set()

class DLiveConstants:
    NAME = "DLive"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://dlive.tv/{username}"
    GENERIC = {'dlive service discontinued'}

class TrueAchievementsConstants:
    NAME = "TrueAchievements"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.trueachievements.com/gamer/{username}"
    GENERIC = set()

class PhysicsforumsConstants:
    NAME = "Physicsforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.physicsforums.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members • physics forums - science by humans'}

class OpenGameArtConstants:
    NAME = "Open Game Art"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://opengameart.org/users/{username}"
    GENERIC = set()

class LobstersConstants:
    NAME = "Lobsters"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lobste.rs/u/{username}"
    GENERIC = set()

class IFunnyConstants:
    NAME = "iFunny"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.ifunny.co/user/{username}"
    GENERIC = set()

class TopcoderConstants:
    NAME = "Topcoder"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profiles.topcoder.com/{username}/"
    GENERIC = {'topcoder top technology talent on-demand'}

class PicturepushComConstants:
    NAME = "picturepush.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.picturepush.com/"
    GENERIC = {'photo upload and online photo albums - picturepush'}

class VoicesConstants:
    NAME = "Voices"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.voices.com/actors/{username}"
    GENERIC = set()

class NhattaoComConstants:
    NAME = "nhattao.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.nhattao.com/members/?username={username}"
    GENERIC = set()

class ReplItConstants:
    NAME = "Repl.it"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://repl.it/@{username}"
    GENERIC = set()

class UsernamePortfolioboxNetConstants:
    NAME = "{username}.portfoliobox.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.portfoliobox.net"
    GENERIC = set()

class DcinsideConstants:
    NAME = "Dcinside"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gallog.dcinside.com/{username}"
    GENERIC = set()

class DigitalPointConstants:
    NAME = "DigitalPoint"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.digitalpoint.com/members/?username={username}"
    GENERIC = set()

class AsciinemaConstants:
    NAME = "Asciinema"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://asciinema.org/~{username}"
    GENERIC = set()

class CfdOnlineConstants:
    NAME = "cfd-online"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.cfd-online.com/Forums/members/{username}.html"
    GENERIC = set()

class FunnyjunkConstants:
    NAME = "Funnyjunk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://funnyjunk.com/user/{username}"
    GENERIC = set()

class GloriaTvConstants:
    NAME = "gloria.tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gloria.tv/{username}"
    GENERIC = set()

class FicwadConstants:
    NAME = "Ficwad"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ficwad.com/a/{username}/favorites/authors"
    GENERIC = set()

class TriplineConstants:
    NAME = "Tripline"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tripline.net/{username}"
    GENERIC = set()

class DeepDreamGeneratorConstants:
    NAME = "DeepDreamGenerator"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://deepdreamgenerator.com/u/{username}"
    GENERIC = set()

class N1xConstants:
    NAME = "1x"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://1x.com/{username}"
    GENERIC = {'1x.com • in pursuit of the sublime'}

class PokecommunityConstants:
    NAME = "Pokecommunity"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pokecommunity.com/members/?username={username}"
    GENERIC = set()

class SamlibConstants:
    NAME = "Samlib"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://samlib.ru/e/{username}"
    GENERIC = set()

class GoodgameRuConstants:
    NAME = "goodgame.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://goodgame.ru/channel/{username}"
    GENERIC = set()

class PlingConstants:
    NAME = "Pling"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pling.com/u/{username}/"
    GENERIC = {"making sure you're not a bot!"}

class HardforumConstants:
    NAME = "Hardforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hardforum.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | [h]ard|forum'}

class N23hqConstants:
    NAME = "23hq"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.23hq.com/{username}"
    GENERIC = set()

class AndroidforumsConstants:
    NAME = "Androidforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://androidforums.com/members/?username={username}"
    GENERIC = set()

class ComedyConstants:
    NAME = "Comedy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.comedy.co.uk/profile/{username}/"
    GENERIC = set()

class YouPicConstants:
    NAME = "YouPic"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://youpic.com/photographer/{username}/"
    GENERIC = set()

class PolarstepsConstants:
    NAME = "Polarsteps"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://polarsteps.com/{username}"
    GENERIC = {'polarsteps', 'polarsteps - automatic travel tracker - explore. dream. discover.'}

class PlatziConstants:
    NAME = "Platzi"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://platzi.com/p/{username}/"
    GENERIC = set()

class WritingforumsOrgConstants:
    NAME = "writingforums.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.writingforums.org//members/?username={username}"
    GENERIC = set()

class ChatujmeCzConstants:
    NAME = "Chatujme.cz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profil.chatujme.cz/{username}"
    GENERIC = set()

class AntiquersConstants:
    NAME = "Antiquers"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.antiquers.com/members/?username={username}"
    GENERIC = {'notable members | antiques board'}

class BigsoccerConstants:
    NAME = "Bigsoccer"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.bigsoccer.com/members/?username={username}"
    GENERIC = {'notable members | bigsoccer forum'}

class SkyblockConstants:
    NAME = "Skyblock"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://skyblock.net/members/?username={username}"
    GENERIC = {'notable members | skyblock'}

class HiveBlogConstants:
    NAME = "Hive Blog"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hive.blog/@{username}"
    GENERIC = set()

class JoyreactorCcConstants:
    NAME = "joyreactor.cc"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://joyreactor.cc/user/{username}"
    GENERIC = {'главная - прикольные картинки, мемы, комиксы, гифки на joyreactor'}

class ViewBugConstants:
    NAME = "ViewBug"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.viewbug.com/member/{username}"
    GENERIC = set()

class ExophaseConstants:
    NAME = "Exophase"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.exophase.com/user/{username}/"
    GENERIC = set()

class WebdeveloperComConstants:
    NAME = "webdeveloper.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://webdeveloper.com/u/{username}"
    GENERIC = set()

class FediversePartyConstants:
    NAME = "fediverse.party"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fediverse.party/en/{username}"
    GENERIC = set()

class WeblancerConstants:
    NAME = "Weblancer"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.weblancer.net/users/{username}/"
    GENERIC = set()

class SugoidesuConstants:
    NAME = "Sugoidesu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sugoidesu.net/members/?username={username}"
    GENERIC = set()

class ProfiRuConstants:
    NAME = "profi.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profi.ru/profile/{username}/"
    GENERIC = set()

class ThoughtsComConstants:
    NAME = "thoughts.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://thoughts.com/members/{username}"
    GENERIC = {'for sale domain: thoughts.com'}

class GapyearConstants:
    NAME = "Gapyear"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.gapyear.com/members/{username}"
    GENERIC = set()

class MyinstantsConstants:
    NAME = "Myinstants"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.myinstants.com/profile/{username}/"
    GENERIC = set()

class SmokingmeatforumsComConstants:
    NAME = "smokingmeatforums.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://smokingmeatforums.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | smoking meat forums - the best smoking meat forum on earth!'}

class ReibertConstants:
    NAME = "Reibert"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://reibert.info//members/?username={username}"
    GENERIC = set()

class FreelancehuntConstants:
    NAME = "Freelancehunt"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://freelancehunt.com/freelancer/{username}.html"
    GENERIC = set()

class AtcoderConstants:
    NAME = "Atcoder"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://atcoder.jp/users/{username}"
    GENERIC = set()

class JetpunkConstants:
    NAME = "Jetpunk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.jetpunk.com/users/{username}"
    GENERIC = set()

class RappadConstants:
    NAME = "Rappad"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.rappad.co/users/{username}"
    GENERIC = set()

class NationStatesNationConstants:
    NAME = "NationStates Nation"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nationstates.net/nation={username}"
    GENERIC = set()

class EthresearConstants:
    NAME = "Ethresear"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ethresear.ch/u/{username}/summary"
    GENERIC = set()

class HomebrewtalkComConstants:
    NAME = "homebrewtalk.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.homebrewtalk.com/members/?username={username}"
    GENERIC = set()

class LemmyWorldConstants:
    NAME = "Lemmy World"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lemmy.world/u/{username}"
    API_URL = "https://lemmy.world/api/v3/user?username={username}"
    COMMUNITY_API = "https://lemmy.world/api/v3/community?name={id}"
    GENERIC = set()

class ZoomirIrConstants:
    NAME = "Zoomir.ir"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.zoomit.ir/user/{username}"
    GENERIC = set()

class CentConstants:
    NAME = "Cent"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://beta.cent.co/@{username}"
    GENERIC = {'/@zzq9xkdoesnotexist42qz'}

class VjudgeConstants:
    NAME = "Vjudge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://VJudge.net/user/{username}"
    GENERIC = set()

class TheSimsResourceConstants:
    NAME = "TheSimsResource"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.thesimsresource.com/members/{username}/"
    GENERIC = set()

class VgtimesGamesConstants:
    NAME = "Vgtimes/Games"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vgtimes.ru/games/{username}/forum/"
    GENERIC = set()

class WindowsforumConstants:
    NAME = "Windowsforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://windowsforum.com/members/?username={username}"
    GENERIC = set()

class WarpcastConstants:
    NAME = "Warpcast"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://warpcast.com/{username}"
    GENERIC = set()

class TopmateConstants:
    NAME = "Topmate"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://topmate.io/{username}"
    GENERIC = set()

class TyperacerConstants:
    NAME = "Typeracer"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://data.typeracer.com/pit/profile?user={username}"
    GENERIC = {'profile not found (typeracer pit stop)'}

class DevRantConstants:
    NAME = "devRant"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://devrant.com/users/{username}"
    GENERIC = {'devrant - a fun community for developers to connect over code, tech & life as a programmer'}

class RmmediaConstants:
    NAME = "Rmmedia"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://rmmedia.ru/members/?username={username}"
    GENERIC = {'полезные пользователи', 'полезные пользователи | rmmedia.ru'}

class HometheaterforumConstants:
    NAME = "Hometheaterforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.hometheaterforum.com/community/members/?username={username}"
    GENERIC = set()

class VLRConstants:
    NAME = "VLR"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.vlr.gg/user/{username}"
    GENERIC = set()

class HackingWithSwiftConstants:
    NAME = "HackingWithSwift"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.hackingwithswift.com/users/{username}"
    GENERIC = set()

class PokemonShowdownConstants:
    NAME = "Pokemon Showdown"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pokemonshowdown.com/users/{username}"
    GENERIC = set()

class MynicknameComConstants:
    NAME = "mynickname.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mynickname.com/{username}"
    GENERIC = set()

class EthereumMagiciansConstants:
    NAME = "Ethereum-magicians"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ethereum-magicians.org/u/{username}/summary"
    GENERIC = set()

class GovloopConstants:
    NAME = "Govloop"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.govloop.com/members/{username}"
    GENERIC = set()

class DesignspirationConstants:
    NAME = "Designspiration"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://designspiration.com/{username}/"
    GENERIC = set()

class PolitforumsConstants:
    NAME = "Politforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.politforums.net/free/profile.php?showuser={username}"
    GENERIC = set()

class IcheckmoviesConstants:
    NAME = "Icheckmovies"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.icheckmovies.com/profiles/{username}"
    GENERIC = set()

class CrevadoConstants:
    NAME = "Crevado"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.crevado.com"
    GENERIC = set()

class MonkeytypeConstants:
    NAME = "Monkeytype"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://monkeytype.com/profile/{username}"
    GENERIC = {'monkeytype | a minimalistic, customizable typing test'}

class E621Constants:
    NAME = "E621"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://e621.net/users/{username}"
    GENERIC = set()

class GvectorsConstants:
    NAME = "Gvectors"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gvectors.com/forum/profile/{username}/"
    GENERIC = set()

class RollitupConstants:
    NAME = "Rollitup"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.rollitup.org/members/?username={username}"
    GENERIC = {'notable members', 'notable members | rollitup'}

class RiveAppConstants:
    NAME = "rive.app"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://rive.app/a/{username}"
    GENERIC = set()

class MstdnIoConstants:
    NAME = "mstdn.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mstdn.io/@{username}"
    API_URL = "https://mstdn.io/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()

class LightstalkingComConstants:
    NAME = "lightstalking.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.lightstalking.com/author/{username}/"
    GENERIC = set()

class GuruShotsConstants:
    NAME = "GuruShots"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gurushots.com/{username}/photos"
    GENERIC = {'gurushots | the world', "gurushots | the world's greatest photography game"}

class WeasylConstants:
    NAME = "Weasyl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.weasyl.com/~{username}"
    GENERIC = set()

class TouristlinkConstants:
    NAME = "Touristlink"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.touristlink.com/user/{username}"
    GENERIC = {'members across the world'}

class W7forumsConstants:
    NAME = "W7forums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.w7forums.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | windows 7 forums'}

class FragmentConstants:
    NAME = "Fragment"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fragment.com/username/{username}"
    GENERIC = {'auctions for usernames', 'fragment'}

class AllTheLyricsConstants:
    NAME = "AllTheLyrics"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.allthelyrics.com/forum/member.php?username={username}"
    GENERIC = {'lyrics forum'}

class NothingCommunityConstants:
    NAME = "Nothing Community"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nothing.community/u/{username}"
    GENERIC = set()

class ClozemasterConstants:
    NAME = "Clozemaster"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.clozemaster.com/players/{username}"
    GENERIC = {'learn language in context - clozemaster'}

class N999MdConstants:
    NAME = "999.md"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://999.md/ru/profile/{username}"
    GENERIC = set()

class ArrseConstants:
    NAME = "Arrse"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.arrse.co.uk//community/members/?username={username}"
    GENERIC = set()

class N1001tracklistsConstants:
    NAME = "1001tracklists"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.1001tracklists.com/user/{username}/index.html"
    GENERIC = set()

class LiviosConstants:
    NAME = "Livios"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.livios.be/nl/forum/leden/{username}"
    GENERIC = {'livios', 'livios stopt — expertise leeft verder bij mijnenergie'}

class PronounsPageConstants:
    NAME = "Pronouns.page"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pronouns.page/@{username}"
    GENERIC = set()

class AuConstants:
    NAME = "Au"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://au.ru/user/{username}/"
    GENERIC = set()

class ListographyConstants:
    NAME = "Listography"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://listography.com/{username}"
    GENERIC = {'listography: error'}

class Millerovo161RuConstants:
    NAME = "millerovo161.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://millerovo161.ru/index/8-0-{username}"
    GENERIC = set()

class RlocmanConstants:
    NAME = "Rlocman"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.rlocman.ru/forum/member.php?username={username}"
    GENERIC = set()

class Aminus3Constants:
    NAME = "Aminus3"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.aminus3.com/"
    GENERIC = set()

class ElixirforumConstants:
    NAME = "Elixirforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://elixirforum.com/u/{username}/summary"
    GENERIC = set()

class EGPUConstants:
    NAME = "eGPU"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://egpu.io/forums/profile/{username}/"
    GENERIC = set()

class VintageMustangComConstants:
    NAME = "vintage-mustang.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vintage-mustang.com/members/?username={username}"
    GENERIC = set()

class ForumHrConstants:
    NAME = "forum.hr"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.forum.hr/member.php?username={username}"
    GENERIC = set()

class School2dobrinkaRuConstants:
    NAME = "school2dobrinka.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://school2dobrinka.ru/index/8-0-{username}"
    GENERIC = set()

class JigidiConstants:
    NAME = "Jigidi"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.jigidi.com/user/{username}"
    GENERIC = {'jigidi'}

class ChemportConstants:
    NAME = "Chemport"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.chemport.ru/forum/memberlist.php?username={username}"
    GENERIC = set()

class SnbforumsConstants:
    NAME = "Snbforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.snbforums.com/members/?username={username}"
    GENERIC = set()

class RedcafeConstants:
    NAME = "Redcafe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.redcafe.net/members/?username={username}"
    GENERIC = {'notable members', 'notable members | redcafe.net'}

class ShowmeConstants:
    NAME = "Showme"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.showme.com/{username}"
    GENERIC = set()

class OfficeForumsConstants:
    NAME = "Office-forums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.office-forums.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | microsoft office forums'}

class SubaruoutbackOrgConstants:
    NAME = "subaruoutback.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://subaruoutback.org/members/?username={username}"
    GENERIC = set()

class SvtperformanceComConstants:
    NAME = "svtperformance.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://svtperformance.com/members/?username={username}"
    GENERIC = set()

class RailforumsCoUkConstants:
    NAME = "railforums.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.railforums.co.uk/members/?username={username}"
    GENERIC = set()

class SubaruforesterOrgConstants:
    NAME = "subaruforester.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://subaruforester.org/members/?username={username}"
    GENERIC = set()

class RubyForumConstants:
    NAME = "Ruby-forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.ruby-forum.com/u/{username}/summary"
    GENERIC = set()

class BlipfotoConstants:
    NAME = "Blipfoto"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.blipfoto.com/{username}"
    GENERIC = set()

class NitroTypeConstants:
    NAME = "Nitro Type"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.nitrotype.com/racer/{username}"
    GENERIC = {'nitro type | competitive typing game | race your friends'}

class BlastConstants:
    NAME = "Blast"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.blast.hk/members/?username={username}"
    GENERIC = {'полезные пользователи', 'полезные пользователи | blasthack - explosive gamehacking'}

class VishivalochkaRuConstants:
    NAME = "vishivalochka.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vishivalochka.ru/index/8-0-{username}"
    GENERIC = set()

class CSLordsConstants:
    NAME = "CS-Lords"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cs-lords.ru/index/8-0-{username}"
    GENERIC = set()

class NiketalkConstants:
    NAME = "Niketalk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://niketalk.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | niketalk'}

class ThefirearmsforumConstants:
    NAME = "Thefirearmsforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.thefirearmsforum.com/members/?username={username}"
    GENERIC = set()

class AffiliatefixConstants:
    NAME = "Affiliatefix"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.affiliatefix.com/members/?username={username}"
    GENERIC = set()

class SigtalkComConstants:
    NAME = "sigtalk.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sigtalk.com/members/?username={username}"
    GENERIC = set()

class MirStalkeraRuConstants:
    NAME = "mir-stalkera.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mir-stalkera.ru/index/8-0-{username}"
    GENERIC = set()

class MacHelpConstants:
    NAME = "Mac-help"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mac-help.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | mac help forums'}

class FlashflashrevolutionConstants:
    NAME = "Flashflashrevolution"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.flashflashrevolution.com/profile/{username}/"
    GENERIC = set()

class DMOJConstants:
    NAME = "DMOJ"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://dmoj.ca/user/{username}"
    GENERIC = set()

class LadaVestaNetConstants:
    NAME = "lada-vesta.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.lada-vesta.net/member.php?username={username}"
    GENERIC = set()

class SysadminsConstants:
    NAME = "Sysadmins"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sysadmins.ru/member{username}.html"
    GENERIC = set()

class JeepgarageOrgConstants:
    NAME = "jeepgarage.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://jeepgarage.org/members/?username={username}"
    GENERIC = set()

class N4gameforumConstants:
    NAME = "4gameforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://4gameforum.com/members/?username={username}"
    GENERIC = {'выдающиеся пользователи | 4game'}

class Spells8Constants:
    NAME = "Spells8"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.spells8.com/u/{username}"
    GENERIC = set()

class N101010PlConstants:
    NAME = "101010.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://101010.pl/@{username}"
    API_URL = "https://101010.pl/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()

class CryptoHackConstants:
    NAME = "Crypto Hack"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cryptohack.org/user/{username}/"
    GENERIC = {'cryptohack – a free, fun platform for learning cryptography', 'cryptohack – home'}

class PiccsyConstants:
    NAME = "Piccsy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.piccsy.com/"
    GENERIC = set()

class Windows10forumsConstants:
    NAME = "Windows10forums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.windows10forums.com//members/?username={username}"
    GENERIC = {'notable members', 'notable members | windows 10 forums'}

class IfishNetConstants:
    NAME = "ifish.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ifish.net/members/?username={username}"
    GENERIC = set()

class SwedroidSeConstants:
    NAME = "swedroid.se"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://swedroid.se/forum/members/?username={username}"
    GENERIC = set()

class CSSBattleConstants:
    NAME = "CSSBattle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cssbattle.dev/player/{username}"
    GENERIC = {'cssbattle'}

class MacosxConstants:
    NAME = "Macosx"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://macosx.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | mac support'}

class ReligiousForumsConstants:
    NAME = "ReligiousForums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.religiousforums.com/members/?username={username}"
    GENERIC = set()

class Not606ComConstants:
    NAME = "not606.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.not606.com//members/?username={username}"
    GENERIC = {'notable members', 'notable members | not606 - the sports forum'}

class GpodderConstants:
    NAME = "Gpodder"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gpodder.net/user/{username}"
    GENERIC = set()

class MdConstants:
    NAME = "md"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.md/ru/users/{username}"
    GENERIC = set()

class ImoodConstants:
    NAME = "Imood"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.imood.com/users/{username}"
    GENERIC = set()

class ArmtorgConstants:
    NAME = "Armtorg"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://armtorg.ru//forum/memberlist.php?username={username}"
    GENERIC = {'пользователи'}

class RusspussRuConstants:
    NAME = "russpuss.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.russpuss.ru/profile/{username}/"
    GENERIC = set()

class VTwinforumComConstants:
    NAME = "v-twinforum.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://v-twinforum.com/members/?username={username}"
    GENERIC = set()

class FanficslandiaComConstants:
    NAME = "fanficslandia.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fanficslandia.com/index.php/members/?username={username}"
    GENERIC = {'usuarios destacados | fanficslandia - ffl'}

class QbnConstants:
    NAME = "Qbn"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.qbn.com/{username}"
    GENERIC = set()

class LkforumConstants:
    NAME = "Lkforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.lkforum.ru//member.php?username={username}"
    GENERIC = set()

class ClubsnapComConstants:
    NAME = "clubsnap.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.clubsnap.com//members/?username={username}"
    GENERIC = {'notable members', 'notable members | clubsnap photography community'}

class WolpyConstants:
    NAME = "Wolpy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wolpy.com/{username}/profile"
    GENERIC = set()

class WarframeMarketConstants:
    NAME = "Warframe Market"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://warframe.market/profile/{username}"
    GENERIC = set()

class CubecraftNetConstants:
    NAME = "cubecraft.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.cubecraft.net/members/?username={username}"
    GENERIC = {'notable members', 'notable members | cubecraft games'}

class TvGamesConstants:
    NAME = "Tv-games"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tv-games.ru//forum/member.php?username={username}"
    GENERIC = set()

class SniperforumsComConstants:
    NAME = "sniperforums.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sniperforums.com/members/?username={username}"
    GENERIC = set()

class IzobilRuConstants:
    NAME = "izobil.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://izobil.ru/index/8-0-{username}"
    GENERIC = set()

class GoldroyalConstants:
    NAME = "Goldroyal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://goldroyal.net/member.php?username={username}"
    GENERIC = set()

class FCRubinConstants:
    NAME = "FCRubin"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.fcrubin.ru/forum/member.php?username={username}"
    GENERIC = {'форум болельщиков фк рубин'}

class OakleyforumComConstants:
    NAME = "oakleyforum.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.oakleyforum.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | oakley forum'}

class HuntingConstants:
    NAME = "hunting"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.hunting.ru/forum/members/?username={username}"
    GENERIC = set()

class UvelirConstants:
    NAME = "Uvelir"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://uvelir.net//member.php?username={username}"
    GENERIC = set()

class ThelionConstants:
    NAME = "Thelion"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.thelion.com/bin/profile.cgi?c=s&ru_name={username}"
    GENERIC = {'thelion.com - user'}

class XShakerConstants:
    NAME = "XShaker"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.xshaker.net/{username}.html"
    GENERIC = set()

class NucastleCoUkConstants:
    NAME = "nucastle.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.nucastle.co.uk//members/?username={username}"
    GENERIC = {'notable members | nucastle.co.uk - music, events, banter and stuff'}

class RealmeyeConstants:
    NAME = "Realmeye"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.realmeye.com/player/{username}"
    GENERIC = {'just a moment...'}

class HitmanforumConstants:
    NAME = "Hitmanforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.hitmanforum.com/u/{username}/summary"
    GENERIC = set()

class DatingRuConstants:
    NAME = "Dating.Ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://dating.ru/{username}"
    GENERIC = set()

class VolgogradForumConstants:
    NAME = "Volgograd Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.forum-volgograd.ru/members/?username={username}"
    GENERIC = set()

class TigerfanComConstants:
    NAME = "tigerfan.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tigerfan.com//members/?username={username}"
    GENERIC = set()

class ImpalaforumsComConstants:
    NAME = "impalaforums.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://impalaforums.com/members/?username={username}"
    GENERIC = set()

class ForumJizniConstants:
    NAME = "ForumJizni"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.forumjizni.ru/member.php?username={username}"
    GENERIC = {'форум общения больных людей. неизлечимых болезней нет!'}

class XgmGuruConstants:
    NAME = "xgm.guru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://xgm.guru/user/{username}"
    GENERIC = set()

class TexasguntalkConstants:
    NAME = "Texasguntalk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.texasguntalk.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | texas gun talk - the premier texas gun forum'}

class PolitikforumConstants:
    NAME = "Politikforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.politikforum.ru//member.php?username={username}"
    GENERIC = {'политический форум о политических событиях в россии, украине, странах бывшего ссср.'}

class TruthbookConstants:
    NAME = "Truthbook"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://truthbook.com/forum/memberlist.php?username={username}"
    GENERIC = set()

class DefenceForumIndiaConstants:
    NAME = "DefenceForumIndia"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://defenceforumindia.com//members/?username={username}"
    GENERIC = set()

class ForumsDromRuConstants:
    NAME = "forums.drom.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.forumsdrom.ru/member.php?username={username}"
    GENERIC = {'форумы об автомобилях в россии'}

class AntiqueBottlesConstants:
    NAME = "Antique-bottles"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.antique-bottles.net/members/?username={username}"
    GENERIC = set()

class RidemonkeyComConstants:
    NAME = "ridemonkey.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.ridemonkey.com/members/?username={username}"
    GENERIC = set()

class DiscussfastpitchConstants:
    NAME = "Discussfastpitch"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.discussfastpitch.com/members/?username={username}"
    GENERIC = {'notable members', 'notable members | discuss fastpitch softball community'}

class AvtoForumNameConstants:
    NAME = "Avto-forum.name"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://avto-forum.name/members/?username={username}"
    GENERIC = {'browser verification'}

class SpacesConstants:
    NAME = "Spaces"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://spaces.im/mysite/index/{username}/"
    GENERIC = {'загрузка...'}

class RussianFIConstants:
    NAME = "RussianFI"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.russian.fi//forum/member.php?username={username}"
    GENERIC = {'финляндия по-русски'}

class XtratimeOrgConstants:
    NAME = "xtratime.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.xtratime.org/members/?username={username}"
    GENERIC = set()

class NikoncafeComConstants:
    NAME = "nikoncafe.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.nikoncafe.com//members/?username={username}"
    GENERIC = set()

class CowboyszoneComConstants:
    NAME = "cowboyszone.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cowboyszone.com/members/?username={username}"
    GENERIC = set()

class ThebuddyforumConstants:
    NAME = "Thebuddyforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.thebuddyforum.com/members/?username={username}"
    GENERIC = set()

class VauxhallownersnetworkCoUkConstants:
    NAME = "vauxhallownersnetwork.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.vauxhallownersnetwork.co.uk/members/?username={username}"
    GENERIC = set()

class ErogenClubConstants:
    NAME = "Erogen.club"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://erogen.club/members/?username={username}"
    GENERIC = {'полезные пользователи', 'полезные пользователи | клуб «эроген». секс-форум erogen.'}

class MineplexComConstants:
    NAME = "mineplex.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mineplex.com/members/?username={username}"
    GENERIC = set()

class CodersRankConstants:
    NAME = "Coders Rank"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profile.codersrank.io/user/{username}/"
    GENERIC = {"zzq9xkdoesnotexist42qz's codersrank profile"}

class WorldofplayersConstants:
    NAME = "Worldofplayers"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://worldofplayers.ru/members/?username={username}"
    GENERIC = set()
