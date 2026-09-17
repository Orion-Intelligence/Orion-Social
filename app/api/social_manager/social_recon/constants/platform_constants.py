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
    IMPERSONATE = "safari"
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
    IMPERSONATE = "safari"
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
    IMPERSONATE = "safari"
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
    IMPERSONATE = 'safari'
    PRESENCE = ('Personal Tools',)
    ABSENCE = ()
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
    IMPERSONATE = "safari"
    GENERIC = set()


class ThemeForestConstants:
    NAME = "ThemeForest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://themeforest.net/user/{username}"
    IMPERSONATE = "safari"
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
    PRESENCE = ('profile',)
    ABSENCE = ('THROW_NOT_FOUND_EXCEPTION',)
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
    IMPERSONATE = 'safari'
    PRESENCE = ('collectionName',)
    ABSENCE = ('subheading',)
    GENERIC = {'istock'}


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
    PRESENCE = ('Wikidot user since',)
    ABSENCE = ('User does not exist.',)
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
    IMPERSONATE = "safari"
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
    IMPERSONATE = "safari"
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
    PRESENCE = ('u-username', 'user-page', 'user-title', 'user-panel', 'user-joined')
    ABSENCE = ('\t\t<h1>404 Page Not Found</h1>\r', '<title>404 Page Not Found</title>\r', 'info-page ibox', '\t\t<p>Or maybe the <a href=', '\t\t<p>Were you looking for the <a href=')
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
    IMPERSONATE = "edge101"
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
    PRESENCE = ('s setlist.fm | setlist.fm</title>',)
    ABSENCE = ("Sorry, the page you requested doesn't exist",)
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
    IMPERSONATE = "safari"
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
    IMPERSONATE = "safari"
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
    PRESENCE = ('loginname',)
    ABSENCE = ('.stage img',)
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
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
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
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
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
    IMPERSONATE = "chrome116"
    PRESENCE = ('<title>\u041f\u0440\u043e\u0444\u0438\u043b\u044c.',)
    ABSENCE = ('\u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430 \u0441\u0432\u044f\u0436\u0438\u0442\u0435\u0441\u044c \u0441 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u043e\u043c',)
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
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
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
    PRESENCE = ('biography', 'biography-full', 'profile-sidebar', 'profile-content', 'state')
    ABSENCE = ('<title>Your photo journal | Blipfoto</title>',)
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
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
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
    PRESENCE = ('You must be logged in to do that.', './memberlist.php?mode=viewprofile')
    ABSENCE = ('No members found for this search criterion.', 'Не найдено ни одного пользователя по заданным критериям')
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


class SniperforumsComConstants:
    NAME = "sniperforums.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sniperforums.com/members/?username={username}"
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


class TruthbookConstants:
    NAME = "Truthbook"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://truthbook.com/forum/memberlist.php?username={username}"
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
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
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
    IMPERSONATE = "safari"
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
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class VauxhallownersnetworkCoUkConstants:
    NAME = "vauxhallownersnetwork.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.vauxhallownersnetwork.co.uk/members/?username={username}"
    GENERIC = set()


class MineplexComConstants:
    NAME = "mineplex.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mineplex.com/members/?username={username}"
    GENERIC = set()



class N2ndcareersCommunityDiscourseGroupConstants:
    NAME = "2ndcareers-community.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://2ndcareers-community.discourse.group/u/{username}"
    API_URL = "https://2ndcareers-community.discourse.group/u/{username}.json"
    GENERIC = set()

class N810videoComConstants:
    NAME = "810video.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://810video.com/a/{username}"
    GENERIC = set()

class N8wayrunComConstants:
    NAME = "8wayrun.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://8wayrun.com/members/?username={username}"
    GENERIC = {"notable members", "notable members | 8wayrun.com"}

class ALilianGardenDiscourseGroupConstants:
    NAME = "a-lilian-garden.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://a-lilian-garden.discourse.group/u/{username}"
    API_URL = "https://a-lilian-garden.discourse.group/u/{username}.json"
    GENERIC = set()

class AiidaDiscourseGroupConstants:
    NAME = "aiida.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://aiida.discourse.group/u/{username}"
    API_URL = "https://aiida.discourse.group/u/{username}.json"
    GENERIC = set()

class AluraConstants:
    NAME = "Alura"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cursos.alura.com.br/user/{username}"
    GENERIC = set()

class AmebaConstants:
    NAME = "Ameba"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://profile.ameba.jp/ameba/{username}/"
    GENERIC = set()

class AmpFlipboardComConstants:
    NAME = "amp.flipboard.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://amp.flipboard.com/@{username}"
    GENERIC = set()

class AnchorecommunityDiscourseGroupConstants:
    NAME = "anchorecommunity.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://anchorecommunity.discourse.group/u/{username}"
    API_URL = "https://anchorecommunity.discourse.group/u/{username}.json"
    GENERIC = set()

class AniSocialConstants:
    NAME = "ani.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ani.social/u/{username}"
    API_URL = "https://ani.social/api/v3/user?username={username}"
    COMMUNITY_API = "https://ani.social/api/v3/community?name={id}"
    GENERIC = set()

class AngaraConstants:
    NAME = "Angara"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://angara.net/user/{username}"
    GENERIC = {"angara.net"}

class AntiscamSpaceConstants:
    NAME = "antiscam.space"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://antiscam.space/members/?username={username}"
    GENERIC = {"notable members", "полезные пользователи"}

class AppleinsiderRuConstants:
    NAME = "appleinsider.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://appleinsider.ru/author/{username}"
    GENERIC = set()

class ArduinoForumConstants:
    NAME = "Arduino Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.arduino.cc/u/{username}"
    API_URL = "https://forum.arduino.cc/u/{username}.json"
    GENERIC = set()

class ArgosCommunityDiscourseGroupConstants:
    NAME = "argos-community.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://argos-community.discourse.group/u/{username}"
    API_URL = "https://argos-community.discourse.group/u/{username}.json"
    GENERIC = set()

class ArhrockConstants:
    NAME = "Arhrock"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://arhrock.info/forum/members/?username={username}"
    GENERIC = {"notable members", "полезные пользователи"}

class AskBioexcelEuConstants:
    NAME = "ask.bioexcel.eu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ask.bioexcel.eu/u/{username}"
    API_URL = "https://ask.bioexcel.eu/u/{username}.json"
    GENERIC = set()

class AskVrchatComConstants:
    NAME = "ask.vrchat.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ask.vrchat.com/u/{username}"
    API_URL = "https://ask.vrchat.com/u/{username}.json"
    GENERIC = set()

class AskmrrobotDiscoursehostingNetConstants:
    NAME = "askmrrobot.discoursehosting.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://askmrrobot.discoursehosting.net/u/{username}"
    API_URL = "https://askmrrobot.discoursehosting.net/u/{username}.json"
    GENERIC = set()

class AsktugConstants:
    NAME = "AskTUG"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://asktug.com/u/{username}"
    API_URL = "https://asktug.com/u/{username}.json"
    GENERIC = set()

class AtlasDiscourseGroupConstants:
    NAME = "atlas.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://atlas.discourse.group/u/{username}"
    API_URL = "https://atlas.discourse.group/u/{username}.json"
    GENERIC = set()

class AuthorTodayConstants:
    NAME = "author.today"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://author.today/u/{username}"
    GENERIC = set()

class AvoneMeConstants:
    NAME = "avone.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://avone.me/a/{username}"
    GENERIC = set()

class AwfulSystemsConstants:
    NAME = "awful.systems"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://awful.systems/u/{username}"
    API_URL = "https://awful.systems/api/v3/user?username={username}"
    COMMUNITY_API = "https://awful.systems/api/v3/community?name={id}"
    GENERIC = set()

class AwgOsdrSpaceConstants:
    NAME = "awg.osdr.space"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://awg.osdr.space/u/{username}"
    API_URL = "https://awg.osdr.space/u/{username}.json"
    GENERIC = set()

class BackstagePolyendComConstants:
    NAME = "backstage.polyend.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://backstage.polyend.com/u/{username}"
    API_URL = "https://backstage.polyend.com/u/{username}.json"
    GENERIC = set()

class BambuLabForumConstants:
    NAME = "Bambu Lab Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.bambulab.com/u/{username}"
    API_URL = "https://forum.bambulab.com/u/{username}.json"
    GENERIC = set()

class BarkVideoConstants:
    NAME = "bark.video"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bark.video/a/{username}"
    GENERIC = set()

class BbsEeclubTopConstants:
    NAME = "bbs.eeclub.top"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bbs.eeclub.top/u/{username}"
    API_URL = "https://bbs.eeclub.top/u/{username}.json"
    GENERIC = set()

class BbsFit2cloudComConstants:
    NAME = "bbs.fit2cloud.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bbs.fit2cloud.com/u/{username}"
    API_URL = "https://bbs.fit2cloud.com/u/{username}.json"
    GENERIC = set()

class BchartsComBrConstants:
    NAME = "bcharts.com.br"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bcharts.com.br/u/{username}"
    API_URL = "https://bcharts.com.br/u/{username}.json"
    GENERIC = set()

class BelgaeSocialConstants:
    NAME = "belgae.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://belgae.social/u/{username}"
    API_URL = "https://belgae.social/api/v3/user?username={username}"
    COMMUNITY_API = "https://belgae.social/api/v3/community?name={id}"
    GENERIC = set()

class BestFriendsChatConstants:
    NAME = "best-friends.chat"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://best-friends.chat/@{username}"
    API_URL = "https://best-friends.chat/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()
    AVATAR_KEYS = ("avatar_static", "avatar")
    COVER_KEYS = ("header_static", "header")

class BeRealConstants:
    NAME = "BeReal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bere.al/{username}"
    GENERIC = {"bereal"}

class BginDiscourseGroupConstants:
    NAME = "bgin.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bgin.discourse.group/u/{username}"
    API_URL = "https://bgin.discourse.group/u/{username}.json"
    GENERIC = set()

class BiggerpocketsConstants:
    NAME = "Biggerpockets"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.biggerpockets.com/users/{username}"
    GENERIC = set()

class BiohackingForumConstants:
    NAME = "biohacking.forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://biohacking.forum/u/{username}"
    API_URL = "https://biohacking.forum/u/{username}.json"
    GENERIC = set()

class BldgsimOnebuildingOrgConstants:
    NAME = "bldgsim.onebuilding.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bldgsim.onebuilding.org/u/{username}"
    API_URL = "https://bldgsim.onebuilding.org/u/{username}.json"
    GENERIC = set()

class BlenderartistsOrgConstants:
    NAME = "blenderartists.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://blenderartists.org/u/{username}"
    API_URL = "https://blenderartists.org/u/{username}.json"
    GENERIC = set()

class BlizzhackersDiscourseGroupConstants:
    NAME = "blizzhackers.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://blizzhackers.discourse.group/u/{username}"
    API_URL = "https://blizzhackers.discourse.group/u/{username}.json"
    GENERIC = set()

class BlocsforumDiscoursehostingNetConstants:
    NAME = "blocsforum.discoursehosting.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://blocsforum.discoursehosting.net/u/{username}"
    API_URL = "https://blocsforum.discoursehosting.net/u/{username}.json"
    GENERIC = set()

class BlogzZaclysComConstants:
    NAME = "blogz.zaclys.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://blogz.zaclys.com/{username}"
    GENERIC = set()

class BndDiscourseGroupConstants:
    NAME = "bnd.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bnd.discourse.group/u/{username}"
    API_URL = "https://bnd.discourse.group/u/{username}.json"
    GENERIC = set()

class BoardsCore77ComConstants:
    NAME = "boards.core77.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://boards.core77.com/u/{username}"
    API_URL = "https://boards.core77.com/u/{username}.json"
    GENERIC = set()

class BoardTtvchannelComConstants:
    NAME = "board.ttvchannel.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://board.ttvchannel.com/u/{username}"
    API_URL = "https://board.ttvchannel.com/u/{username}.json"
    GENERIC = set()

class BoardMddcDevConstants:
    NAME = "board.mddc.dev"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://board.mddc.dev/members/?username={username}"
    GENERIC = {"notable members"}

class BrighteonSocialConstants:
    NAME = "brighteon.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://brighteon.social/@{username}"
    API_URL = "https://brighteon.social/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()
    AVATAR_KEYS = ("avatar_static", "avatar")
    COVER_KEYS = ("header_static", "header")

class BroadbandgenieDiscourseGroupConstants:
    NAME = "broadbandgenie.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://broadbandgenie.discourse.group/u/{username}"
    API_URL = "https://broadbandgenie.discourse.group/u/{username}.json"
    GENERIC = set()

class BuilderMetamaskIoConstants:
    NAME = "builder.metamask.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://builder.metamask.io/u/{username}"
    API_URL = "https://builder.metamask.io/u/{username}.json"
    GENERIC = set()

class BunproConstants:
    NAME = "Bunpro"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.bunpro.jp/u/{username}"
    API_URL = "https://community.bunpro.jp/u/{username}.json"
    GENERIC = set()

class CImConstants:
    NAME = "c.im"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://c.im/@{username}"
    API_URL = "https://c.im/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()
    AVATAR_KEYS = ("avatar_static", "avatar")
    COVER_KEYS = ("header_static", "header")

class CaddyCommunityConstants:
    NAME = "caddy.community"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://caddy.community/u/{username}"
    API_URL = "https://caddy.community/u/{username}.json"
    GENERIC = set()

class CajunthredsDiscourseGroupConstants:
    NAME = "cajunthreds.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cajunthreds.discourse.group/u/{username}"
    API_URL = "https://cajunthreds.discourse.group/u/{username}.json"
    GENERIC = set()

class CalculixDiscourseGroupConstants:
    NAME = "calculix.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://calculix.discourse.group/u/{username}"
    API_URL = "https://calculix.discourse.group/u/{username}.json"
    GENERIC = set()

class CanadianfootballForumConstants:
    NAME = "canadianfootball.forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://canadianfootball.forum/u/{username}"
    API_URL = "https://canadianfootball.forum/u/{username}.json"
    GENERIC = set()

class CarrdCoConstants:
    NAME = "Carrd.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9-]{1,63}$"
    PROFILE_URL = "https://{username}.carrd.co"
    GENERIC = {"carrd", "site not found", "404"}

class CavesConstants:
    NAME = "Caves"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://caves.ru/members/?username={username}"
    GENERIC = {"notable members"}

class ChaosfursSocialConstants:
    NAME = "chaosfurs.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://chaosfurs.social/@{username}"
    API_URL = "https://chaosfurs.social/api/v1/accounts/lookup?acct={username}"
    GENERIC = set()
    AVATAR_KEYS = ("avatar_static", "avatar")
    COVER_KEYS = ("header_static", "header")

class ChapelDiscourseGroupConstants:
    NAME = "chapel.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://chapel.discourse.group/u/{username}"
    API_URL = "https://chapel.discourse.group/u/{username}.json"
    GENERIC = set()

class ChiefdelphiComConstants:
    NAME = "chiefdelphi.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.chiefdelphi.com/u/{username}"
    API_URL = "https://www.chiefdelphi.com/u/{username}.json"
    GENERIC = set()

class ClDesmosComConstants:
    NAME = "cl.desmos.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cl.desmos.com/u/{username}"
    API_URL = "https://cl.desmos.com/u/{username}.json"
    GENERIC = set()

class ClashLangDiscourseGroupConstants:
    NAME = "clash-lang.discourse.group"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://clash-lang.discourse.group/u/{username}"
    API_URL = "https://clash-lang.discourse.group/u/{username}.json"
    GENERIC = set()

class ClarityFmConstants:
    NAME = "clarity.fm"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://clarity.fm/{username}"
    GENERIC = {"clarity"}

class ClipPlaceConstants:
    NAME = "clip.place"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://clip.place/a/{username}"
    GENERIC = set()

class CloudromanceComConstants:
    NAME = "cloudromance.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cloudromance.com/{username}"
    GENERIC = set()

class ClubMinistryoftestingComConstants:
    NAME = "club.ministryoftesting.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://club.ministryoftesting.com/u/{username}"
    API_URL = "https://club.ministryoftesting.com/u/{username}.json"
    GENERIC = set()

class ClubModevolComConstants:
    NAME = "club.modevol.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://club.modevol.com/u/{username}"
    API_URL = "https://club.modevol.com/u/{username}.json"
    GENERIC = set()

class CocosCommunityConstants:
    NAME = "Cocos Community"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.cocos.org/u/{username}"
    API_URL = "https://forum.cocos.org/u/{username}.json"
    GENERIC = set()

class CnetConstants:
    NAME = "CNET"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.cnet.com/profiles/{username}/"
    GENERIC = {"cnet"}

class CnodeJsConstants:
    NAME = "CNode.js"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cnodejs.org/user/{username}"
    GENERIC = set()

class CoddyConstants:
    NAME = "Coddy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://coddy.tech/user/{username}"
    GENERIC = {"coddy"}

class CodesellerRuConstants:
    NAME = "codeseller.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://codeseller.ru/author/{username}"
    GENERIC = set()

class CodedexConstants:
    NAME = "Codédex"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.codedex.io/@{username}"
    GENERIC = {"codédex", "codedex"}

class ColorlibsupportComConstants:
    NAME = "colorlibsupport.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://colorlibsupport.com/u/{username}"
    API_URL = "https://colorlibsupport.com/u/{username}.json"
    GENERIC = set()

class CommonsCommondreamsOrgConstants:
    NAME = "commons.commondreams.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://commons.commondreams.org/u/{username}"
    API_URL = "https://commons.commondreams.org/u/{username}.json"
    GENERIC = set()

class CommonsIshtarCollectiveNetConstants:
    NAME = "commons.ishtar-collective.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://commons.ishtar-collective.net/u/{username}"
    API_URL = "https://commons.ishtar-collective.net/u/{username}.json"
    GENERIC = set()

class CommunitySmarthomeComConstants:
    NAME = "community-smarthome.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community-smarthome.com/u/{username}"
    API_URL = "https://community-smarthome.com/u/{username}.json"
    GENERIC = set()

class CommunityAbbyFrConstants:
    NAME = "community.abby.fr"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.abby.fr/u/{username}"
    API_URL = "https://community.abby.fr/u/{username}.json"
    GENERIC = set()

class CommunityAdminforgeDeConstants:
    NAME = "community.adminforge.de"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.adminforge.de/u/{username}"
    API_URL = "https://community.adminforge.de/u/{username}.json"
    GENERIC = set()

class CommunityAliceblueonlineComConstants:
    NAME = "community.aliceblueonline.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.aliceblueonline.com/u/{username}"
    API_URL = "https://community.aliceblueonline.com/u/{username}.json"
    GENERIC = set()

class CommunityAmazondeveloperComConstants:
    NAME = "community.amazondeveloper.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.amazondeveloper.com/u/{username}"
    API_URL = "https://community.amazondeveloper.com/u/{username}.json"
    GENERIC = set()

class CommunityAmperecomputingComConstants:
    NAME = "community.amperecomputing.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.amperecomputing.com/u/{username}"
    API_URL = "https://community.amperecomputing.com/u/{username}.json"
    GENERIC = set()

class CommunityAnkihubNetConstants:
    NAME = "community.ankihub.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ankihub.net/u/{username}"
    API_URL = "https://community.ankihub.net/u/{username}.json"
    GENERIC = set()

class CommunityAnovaculinaryComConstants:
    NAME = "community.anovaculinary.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.anovaculinary.com/u/{username}"
    API_URL = "https://community.anovaculinary.com/u/{username}.json"
    GENERIC = set()

class CommunityAnvizComConstants:
    NAME = "community.anviz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.anviz.com/u/{username}"
    API_URL = "https://community.anviz.com/u/{username}.json"
    GENERIC = set()

class CommunityAphhiveOrgConstants:
    NAME = "community.aphhive.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.aphhive.org/u/{username}"
    API_URL = "https://community.aphhive.org/u/{username}.json"
    GENERIC = set()

class CommunityApollographqlComConstants:
    NAME = "community.apollographql.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.apollographql.com/u/{username}"
    API_URL = "https://community.apollographql.com/u/{username}.json"
    GENERIC = set()

class CommunityAppfarmIoConstants:
    NAME = "community.appfarm.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.appfarm.io/u/{username}"
    API_URL = "https://community.appfarm.io/u/{username}.json"
    GENERIC = set()

class CommunityAppinesFrConstants:
    NAME = "community.appines.fr"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.appines.fr/u/{username}"
    API_URL = "https://community.appines.fr/u/{username}.json"
    GENERIC = set()

class CommunityAppinventorMitEduConstants:
    NAME = "community.appinventor.mit.edu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.appinventor.mit.edu/u/{username}"
    API_URL = "https://community.appinventor.mit.edu/u/{username}.json"
    GENERIC = set()

class CommunityArduboyComConstants:
    NAME = "community.arduboy.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.arduboy.com/u/{username}"
    API_URL = "https://community.arduboy.com/u/{username}.json"
    GENERIC = set()

class CommunityAristotlemetadataComConstants:
    NAME = "community.aristotlemetadata.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.aristotlemetadata.com/u/{username}"
    API_URL = "https://community.aristotlemetadata.com/u/{username}.json"
    GENERIC = set()

class CommunityAsepriteOrgConstants:
    NAME = "community.aseprite.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.aseprite.org/u/{username}"
    API_URL = "https://community.aseprite.org/u/{username}.json"
    GENERIC = set()

class CommunityAsteriskOrgConstants:
    NAME = "community.asterisk.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.asterisk.org/u/{username}"
    API_URL = "https://community.asterisk.org/u/{username}.json"
    GENERIC = set()

class CommunityAuth0ComConstants:
    NAME = "community.auth0.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.auth0.com/u/{username}"
    API_URL = "https://community.auth0.com/u/{username}.json"
    GENERIC = set()

class CommunityAutomationedgeComConstants:
    NAME = "community.automationedge.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.automationedge.com/u/{username}"
    API_URL = "https://community.automationedge.com/u/{username}.json"
    GENERIC = set()

class CommunityAvgComConstants:
    NAME = "community.avg.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.avg.com/u/{username}"
    API_URL = "https://community.avg.com/u/{username}.json"
    GENERIC = set()

class CommunityAweberComConstants:
    NAME = "community.aweber.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.aweber.com/u/{username}"
    API_URL = "https://community.aweber.com/u/{username}.json"
    GENERIC = set()

class CommunityBaserowIoConstants:
    NAME = "community.baserow.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.baserow.io/u/{username}"
    API_URL = "https://community.baserow.io/u/{username}.json"
    GENERIC = set()

class CommunityBearAppConstants:
    NAME = "community.bear.app"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.bear.app/u/{username}"
    API_URL = "https://community.bear.app/u/{username}.json"
    GENERIC = set()

class CommunityBitmovinComConstants:
    NAME = "community.bitmovin.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.bitmovin.com/u/{username}"
    API_URL = "https://community.bitmovin.com/u/{username}.json"
    GENERIC = set()

class CommunityBlokadaOrgConstants:
    NAME = "community.blokada.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.blokada.org/u/{username}"
    API_URL = "https://community.blokada.org/u/{username}.json"
    GENERIC = set()

class CommunityBloomreachComConstants:
    NAME = "community.bloomreach.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.bloomreach.com/u/{username}"
    API_URL = "https://community.bloomreach.com/u/{username}.json"
    GENERIC = set()

class CommunityBlynkCcConstants:
    NAME = "community.blynk.cc"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.blynk.cc/u/{username}"
    API_URL = "https://community.blynk.cc/u/{username}.json"
    GENERIC = set()

class CommunityBrainMapOrgConstants:
    NAME = "community.brain-map.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.brain-map.org/u/{username}"
    API_URL = "https://community.brain-map.org/u/{username}.json"
    GENERIC = set()


class CommunityBrevoComConstants:
    NAME = "community.brevo.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.brevo.com/u/{username}"
    API_URL = "https://community.brevo.com/u/{username}.json"
    GENERIC = set()

class CommunityBrewwComConstants:
    NAME = "community.breww.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.breww.com/u/{username}"
    API_URL = "https://community.breww.com/u/{username}.json"
    GENERIC = set()

class CommunityBrightpatternComConstants:
    NAME = "community.brightpattern.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.brightpattern.com/u/{username}"
    API_URL = "https://community.brightpattern.com/u/{username}.json"
    GENERIC = set()

class CommunityCambiumnetworksComConstants:
    NAME = "community.cambiumnetworks.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.cambiumnetworks.com/u/{username}"
    API_URL = "https://community.cambiumnetworks.com/u/{username}.json"
    GENERIC = set()

class CommunityCarbide3dComConstants:
    NAME = "community.carbide3d.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.carbide3d.com/u/{username}"
    API_URL = "https://community.carbide3d.com/u/{username}.json"
    GENERIC = set()

class CommunityCartalkComConstants:
    NAME = "community.cartalk.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.cartalk.com/u/{username}"
    API_URL = "https://community.cartalk.com/u/{username}.json"
    GENERIC = set()

class CommunityCertifythewebComConstants:
    NAME = "community.certifytheweb.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.certifytheweb.com/u/{username}"
    API_URL = "https://community.certifytheweb.com/u/{username}.json"
    GENERIC = set()

class CommunityCesiumComConstants:
    NAME = "community.cesium.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.cesium.com/u/{username}"
    API_URL = "https://community.cesium.com/u/{username}.json"
    GENERIC = set()

class CommunityClarkComConstants:
    NAME = "community.clark.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.clark.com/u/{username}"
    API_URL = "https://community.clark.com/u/{username}.json"
    GENERIC = set()

class CommunityCoopsTechConstants:
    NAME = "community.coops.tech"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.coops.tech/u/{username}"
    API_URL = "https://community.coops.tech/u/{username}.json"
    GENERIC = set()

class CommunityCrewaiComConstants:
    NAME = "community.crewai.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.crewai.com/u/{username}"
    API_URL = "https://community.crewai.com/u/{username}.json"
    GENERIC = set()

class CommunityCrossrefOrgConstants:
    NAME = "community.crossref.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.crossref.org/u/{username}"
    API_URL = "https://community.crossref.org/u/{username}.json"
    GENERIC = set()

class CommunityCybozuDevConstants:
    NAME = "community.cybozu.dev"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.cybozu.dev/u/{username}"
    API_URL = "https://community.cybozu.dev/u/{username}.json"
    GENERIC = set()

class CommunityDataquestIoConstants:
    NAME = "community.dataquest.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.dataquest.io/u/{username}"
    API_URL = "https://community.dataquest.io/u/{username}.json"
    GENERIC = set()

class CommunityDatocmsComConstants:
    NAME = "community.datocms.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.datocms.com/u/{username}"
    API_URL = "https://community.datocms.com/u/{username}.json"
    GENERIC = set()

class CommunityDeltaExchangeConstants:
    NAME = "community.delta.exchange"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.delta.exchange/u/{username}"
    API_URL = "https://community.delta.exchange/u/{username}.json"
    GENERIC = set()

class CommunityDerivComConstants:
    NAME = "community.deriv.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.deriv.com/u/{username}"
    API_URL = "https://community.deriv.com/u/{username}.json"
    GENERIC = set()

class CommunityDeveloperAtlassianComConstants:
    NAME = "community.developer.atlassian.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.developer.atlassian.com/u/{username}"
    API_URL = "https://community.developer.atlassian.com/u/{username}.json"
    GENERIC = set()

class CommunityDirectusComConstants:
    NAME = "community.directus.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.directus.com/u/{username}"
    API_URL = "https://community.directus.com/u/{username}.json"
    GENERIC = set()

class CommunityDopplerComConstants:
    NAME = "community.doppler.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.doppler.com/u/{username}"
    API_URL = "https://community.doppler.com/u/{username}.json"
    GENERIC = set()

class CommunityDremioComConstants:
    NAME = "community.dremio.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.dremio.com/u/{username}"
    API_URL = "https://community.dremio.com/u/{username}.json"
    GENERIC = set()

class CommunityEFoundationConstants:
    NAME = "community.e.foundation"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.e.foundation/u/{username}"
    API_URL = "https://community.e.foundation/u/{username}.json"
    GENERIC = set()

class CommunityElfsightComConstants:
    NAME = "community.elfsight.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.elfsight.com/u/{username}"
    API_URL = "https://community.elfsight.com/u/{username}.json"
    GENERIC = set()

class CommunityEmmaAppComConstants:
    NAME = "community.emma-app.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.emma-app.com/u/{username}"
    API_URL = "https://community.emma-app.com/u/{username}.json"
    GENERIC = set()

class CommunityEndlessosComConstants:
    NAME = "community.endlessos.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.endlessos.com/u/{username}"
    API_URL = "https://community.endlessos.com/u/{username}.json"
    GENERIC = set()

class CommunityEpinowcastOrgConstants:
    NAME = "community.epinowcast.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.epinowcast.org/u/{username}"
    API_URL = "https://community.epinowcast.org/u/{username}.json"
    GENERIC = set()

class CommunityEspboyComConstants:
    NAME = "community.espboy.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.espboy.com/u/{username}"
    API_URL = "https://community.espboy.com/u/{username}.json"
    GENERIC = set()

class CommunityEufyComConstants:
    NAME = "community.eufy.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.eufy.com/u/{username}"
    API_URL = "https://community.eufy.com/u/{username}.json"
    GENERIC = set()

class CommunityEvolveauthoringComConstants:
    NAME = "community.evolveauthoring.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.evolveauthoring.com/u/{username}"
    API_URL = "https://community.evolveauthoring.com/u/{username}.json"
    GENERIC = set()

class CommunityFastlyComConstants:
    NAME = "community.fastly.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.fastly.com/u/{username}"
    API_URL = "https://community.fastly.com/u/{username}.json"
    GENERIC = set()

class CommunityFiberyIoConstants:
    NAME = "community.fibery.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.fibery.io/u/{username}"
    API_URL = "https://community.fibery.io/u/{username}.json"
    GENERIC = set()

class CommunityFirebasestudioDevConstants:
    NAME = "community.firebasestudio.dev"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.firebasestudio.dev/u/{username}"
    API_URL = "https://community.firebasestudio.dev/u/{username}.json"
    GENERIC = set()

class CommunityFireblocksComConstants:
    NAME = "community.fireblocks.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.fireblocks.com/u/{username}"
    API_URL = "https://community.fireblocks.com/u/{username}.json"
    GENERIC = set()

class CommunityFirecoreComConstants:
    NAME = "community.firecore.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.firecore.com/u/{username}"
    API_URL = "https://community.firecore.com/u/{username}.json"
    GENERIC = set()

class CommunityForestadminComConstants:
    NAME = "community.forestadmin.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.forestadmin.com/u/{username}"
    API_URL = "https://community.forestadmin.com/u/{username}.json"
    GENERIC = set()

class CommunityFrameWorkConstants:
    NAME = "community.frame.work"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.frame.work/u/{username}"
    API_URL = "https://community.frame.work/u/{username}.json"
    GENERIC = set()

class CommunityFreepbxOrgConstants:
    NAME = "community.freepbx.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.freepbx.org/u/{username}"
    API_URL = "https://community.freepbx.org/u/{username}.json"
    GENERIC = set()

class CommunityFunnelishComConstants:
    NAME = "community.funnelish.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.funnelish.com/u/{username}"
    API_URL = "https://community.funnelish.com/u/{username}.json"
    GENERIC = set()

class CommunityFutureaudioworkshopComConstants:
    NAME = "community.futureaudioworkshop.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.futureaudioworkshop.com/u/{username}"
    API_URL = "https://community.futureaudioworkshop.com/u/{username}.json"
    GENERIC = set()

class CommunityGainiumIoConstants:
    NAME = "community.gainium.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gainium.io/u/{username}"
    API_URL = "https://community.gainium.io/u/{username}.json"
    GENERIC = set()

class CommunityGamedevTvConstants:
    NAME = "community.gamedev.tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gamedev.tv/u/{username}"
    API_URL = "https://community.gamedev.tv/u/{username}.json"
    GENERIC = set()

class CommunityGatlingIoConstants:
    NAME = "community.gatling.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gatling.io/u/{username}"
    API_URL = "https://community.gatling.io/u/{username}.json"
    GENERIC = set()

class CommunityGemsofwarComConstants:
    NAME = "community.gemsofwar.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gemsofwar.com/u/{username}"
    API_URL = "https://community.gemsofwar.com/u/{username}.json"
    GENERIC = set()

class CommunityGeodynamicsOrgConstants:
    NAME = "community.geodynamics.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.geodynamics.org/u/{username}"
    API_URL = "https://community.geodynamics.org/u/{username}.json"
    GENERIC = set()

class CommunityGetmailspringComConstants:
    NAME = "community.getmailspring.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.getmailspring.com/u/{username}"
    API_URL = "https://community.getmailspring.com/u/{username}.json"
    GENERIC = set()

class CommunityGetpostmanComConstants:
    NAME = "community.getpostman.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.getpostman.com/u/{username}"
    API_URL = "https://community.getpostman.com/u/{username}.json"
    GENERIC = set()

class CommunityGetswipeInConstants:
    NAME = "community.getswipe.in"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.getswipe.in/u/{username}"
    API_URL = "https://community.getswipe.in/u/{username}.json"
    GENERIC = set()

class CommunityGigperformerComConstants:
    NAME = "community.gigperformer.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gigperformer.com/u/{username}"
    API_URL = "https://community.gigperformer.com/u/{username}.json"
    GENERIC = set()

class CommunityGladysassistantComConstants:
    NAME = "community.gladysassistant.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gladysassistant.com/u/{username}"
    API_URL = "https://community.gladysassistant.com/u/{username}.json"
    GENERIC = set()

class CommunityGlideappsComConstants:
    NAME = "community.glideapps.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.glideapps.com/u/{username}"
    API_URL = "https://community.glideapps.com/u/{username}.json"
    GENERIC = set()

class CommunityGrafanaComConstants:
    NAME = "community.grafana.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.grafana.com/u/{username}"
    API_URL = "https://community.grafana.com/u/{username}.json"
    GENERIC = set()

class CommunityGraylogOrgConstants:
    NAME = "community.graylog.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.graylog.org/u/{username}"
    API_URL = "https://community.graylog.org/u/{username}.json"
    GENERIC = set()

class CommunityHedgedocOrgConstants:
    NAME = "community.hedgedoc.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.hedgedoc.org/u/{username}"
    API_URL = "https://community.hedgedoc.org/u/{username}.json"
    GENERIC = set()

class CommunityHitpawComConstants:
    NAME = "community.hitpaw.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.hitpaw.com/u/{username}"
    API_URL = "https://community.hitpaw.com/u/{username}.json"
    GENERIC = set()

class CommunityHomeAssistantIoConstants:
    NAME = "community.home-assistant.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.home-assistant.io/u/{username}"
    API_URL = "https://community.home-assistant.io/u/{username}.json"
    GENERIC = set()

class CommunityHomeyAppConstants:
    NAME = "community.homey.app"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.homey.app/u/{username}"
    API_URL = "https://community.homey.app/u/{username}.json"
    GENERIC = set()

class CommunityIcingaComConstants:
    NAME = "community.icinga.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.icinga.com/u/{username}"
    API_URL = "https://community.icinga.com/u/{username}.json"
    GENERIC = set()

class CommunityIcons8ComConstants:
    NAME = "community.icons8.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.icons8.com/u/{username}"
    API_URL = "https://community.icons8.com/u/{username}.json"
    GENERIC = set()

class CommunityInfiniteflightComConstants:
    NAME = "community.infiniteflight.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.infiniteflight.com/u/{username}"
    API_URL = "https://community.infiniteflight.com/u/{username}.json"
    GENERIC = set()

class CommunityInfluxdataComConstants:
    NAME = "community.influxdata.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.influxdata.com/u/{username}"
    API_URL = "https://community.influxdata.com/u/{username}.json"
    GENERIC = set()

class CommunityInkbirdComConstants:
    NAME = "community.inkbird.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.inkbird.com/u/{username}"
    API_URL = "https://community.inkbird.com/u/{username}.json"
    GENERIC = set()

class CommunityInvvestCoConstants:
    NAME = "community.invvest.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[\w.@-]{1,80}$"
    PROFILE_URL = "https://community.invvest.co/u/{username}"
    API_URL = "https://community.invvest.co/u/{username}.json"
    GENERIC = set()

class CommunityIotawattComConstants:
    NAME = "community.iotawatt.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.iotawatt.com/u/{username}"
    API_URL = "https://community.iotawatt.com/u/{username}.json"
    GENERIC = set()

class CommunityIpfireOrgConstants:
    NAME = "community.ipfire.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ipfire.org/u/{username}"
    API_URL = "https://community.ipfire.org/u/{username}.json"
    GENERIC = set()

class CommunityIpinfoIoConstants:
    NAME = "community.ipinfo.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ipinfo.io/u/{username}"
    API_URL = "https://community.ipinfo.io/u/{username}.json"
    GENERIC = set()

class CommunityJenkinsIoConstants:
    NAME = "community.jenkins.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.jenkins.io/u/{username}"
    API_URL = "https://community.jenkins.io/u/{username}.json"
    GENERIC = set()

class CommunityJitsiOrgConstants:
    NAME = "community.jitsi.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.jitsi.org/u/{username}"
    API_URL = "https://community.jitsi.org/u/{username}.json"
    GENERIC = set()

class CommunityJoinmastodonOrgConstants:
    NAME = "community.joinmastodon.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.joinmastodon.org/u/{username}"
    API_URL = "https://community.joinmastodon.org/u/{username}.json"
    GENERIC = set()

class CommunityJupiterMoneyConstants:
    NAME = "community.jupiter.money"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.jupiter.money/u/{username}"
    API_URL = "https://community.jupiter.money/u/{username}.json"
    GENERIC = set()

class CommunityKodularIoConstants:
    NAME = "community.kodular.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.kodular.io/u/{username}"
    API_URL = "https://community.kodular.io/u/{username}.json"
    GENERIC = set()

class CommunityLatromiComBrConstants:
    NAME = "community.latromi.com.br"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.latromi.com.br/u/{username}"
    API_URL = "https://community.latromi.com.br/u/{username}.json"
    GENERIC = set()

class CommunityLivekitIoConstants:
    NAME = "community.livekit.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.livekit.io/u/{username}"
    API_URL = "https://community.livekit.io/u/{username}.json"
    GENERIC = set()

class CommunityLocalwpComConstants:
    NAME = "community.localwp.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.localwp.com/u/{username}"
    API_URL = "https://community.localwp.com/u/{username}.json"
    GENERIC = set()

class CommunityLsstOrgConstants:
    NAME = "community.lsst.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.lsst.org/u/{username}"
    API_URL = "https://community.lsst.org/u/{username}.json"
    GENERIC = set()

class CommunityMailpileIsConstants:
    NAME = "community.mailpile.is"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.mailpile.is/u/{username}"
    API_URL = "https://community.mailpile.is/u/{username}.json"
    GENERIC = set()

class CommunityMappedinComConstants:
    NAME = "community.mappedin.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.mappedin.com/u/{username}"
    API_URL = "https://community.mappedin.com/u/{username}.json"
    GENERIC = set()

class CommunityMemfaultComConstants:
    NAME = "community.memfault.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.memfault.com/u/{username}"
    API_URL = "https://community.memfault.com/u/{username}.json"
    GENERIC = set()

class CommunityMilkvIoConstants:
    NAME = "community.milkv.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.milkv.io/u/{username}"
    API_URL = "https://community.milkv.io/u/{username}.json"
    GENERIC = set()

class CommunityMindstudioAiConstants:
    NAME = "community.mindstudio.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.mindstudio.ai/u/{username}"
    API_URL = "https://community.mindstudio.ai/u/{username}.json"
    GENERIC = set()

class CommunityMonzoComConstants:
    NAME = "community.monzo.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.monzo.com/u/{username}"
    API_URL = "https://community.monzo.com/u/{username}.json"
    GENERIC = set()

class CommunityMorphmarketComConstants:
    NAME = "community.morphmarket.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.morphmarket.com/u/{username}"
    API_URL = "https://community.morphmarket.com/u/{username}.json"
    GENERIC = set()

class CommunityMorsemicroComConstants:
    NAME = "community.morsemicro.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.morsemicro.com/u/{username}"
    API_URL = "https://community.morsemicro.com/u/{username}.json"
    GENERIC = set()

class CommunityMrtrixOrgConstants:
    NAME = "community.mrtrix.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.mrtrix.org/u/{username}"
    API_URL = "https://community.mrtrix.org/u/{username}.json"
    GENERIC = set()

class CommunityMycroftAiConstants:
    NAME = "community.mycroft.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.mycroft.ai/u/{username}"
    API_URL = "https://community.mycroft.ai/u/{username}.json"
    GENERIC = set()

class CommunityNaBaicellsComConstants:
    NAME = "community.na.baicells.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.na.baicells.com/u/{username}"
    API_URL = "https://community.na.baicells.com/u/{username}.json"
    GENERIC = set()

class CommunityNaturephotographersNetworkConstants:
    NAME = "community.naturephotographers.network"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.naturephotographers.network/u/{username}"
    API_URL = "https://community.naturephotographers.network/u/{username}.json"
    GENERIC = set()

class CommunityNeo4jComConstants:
    NAME = "community.neo4j.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.neo4j.com/u/{username}"
    API_URL = "https://community.neo4j.com/u/{username}.json"
    GENERIC = set()

class CommunityNetdataCloudConstants:
    NAME = "community.netdata.cloud"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.netdata.cloud/u/{username}"
    API_URL = "https://community.netdata.cloud/u/{username}.json"
    GENERIC = set()

class CommunityNethserverOrgConstants:
    NAME = "community.nethserver.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.nethserver.org/u/{username}"
    API_URL = "https://community.nethserver.org/u/{username}.json"
    GENERIC = set()

class CommunityNetwrixComConstants:
    NAME = "community.netwrix.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.netwrix.com/u/{username}"
    API_URL = "https://community.netwrix.com/u/{username}.json"
    GENERIC = set()

class CommunityNextwComConstants:
    NAME = "community.nextw.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.nextw.com/u/{username}"
    API_URL = "https://community.nextw.com/u/{username}.json"
    GENERIC = set()

class CommunityNianticspatialComConstants:
    NAME = "community.nianticspatial.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.nianticspatial.com/u/{username}"
    API_URL = "https://community.nianticspatial.com/u/{username}.json"
    GENERIC = set()

class CommunityNlnetlabsNlConstants:
    NAME = "community.nlnetlabs.nl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.nlnetlabs.nl/u/{username}"
    API_URL = "https://community.nlnetlabs.nl/u/{username}.json"
    GENERIC = set()

class CommunityNocodbComConstants:
    NAME = "community.nocodb.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.nocodb.com/u/{username}"
    API_URL = "https://community.nocodb.com/u/{username}.json"
    GENERIC = set()

class CommunityNolocoIoConstants:
    NAME = "community.noloco.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.noloco.io/u/{username}"
    API_URL = "https://community.noloco.io/u/{username}.json"
    GENERIC = set()

class CommunityNortonComConstants:
    NAME = "community.norton.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.norton.com/u/{username}"
    API_URL = "https://community.norton.com/u/{username}.json"
    GENERIC = set()

class CommunityNtppoolOrgConstants:
    NAME = "community.ntppool.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ntppool.org/u/{username}"
    API_URL = "https://community.ntppool.org/u/{username}.json"
    GENERIC = set()

class CommunityOmniavisItConstants:
    NAME = "community.omniavis.it"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.omniavis.it/u/{username}"
    API_URL = "https://community.omniavis.it/u/{username}.json"
    GENERIC = set()

class CommunityOnixComConstants:
    NAME = "community.onix.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.onix.com/u/{username}"
    API_URL = "https://community.onix.com/u/{username}.json"
    GENERIC = set()

class CommunityOpenaiComConstants:
    NAME = "community.openai.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openai.com/u/{username}"
    API_URL = "https://community.openai.com/u/{username}.json"
    GENERIC = set()

class CommunityOpenastronomyOrgConstants:
    NAME = "community.openastronomy.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openastronomy.org/u/{username}"
    API_URL = "https://community.openastronomy.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenbisChConstants:
    NAME = "community.openbis.ch"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openbis.ch/u/{username}"
    API_URL = "https://community.openbis.ch/u/{username}.json"
    GENERIC = set()

class CommunityOpenconversationalAiConstants:
    NAME = "community.openconversational.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openconversational.ai/u/{username}"
    API_URL = "https://community.openconversational.ai/u/{username}.json"
    GENERIC = set()

class CommunityOpendronemapOrgConstants:
    NAME = "community.opendronemap.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.opendronemap.org/u/{username}"
    API_URL = "https://community.opendronemap.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenemsIoConstants:
    NAME = "community.openems.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openems.io/u/{username}"
    API_URL = "https://community.openems.io/u/{username}.json"
    GENERIC = set()

class CommunityOpenflOrgConstants:
    NAME = "community.openfl.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openfl.org/u/{username}"
    API_URL = "https://community.openfl.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenfoodnetworkOrgConstants:
    NAME = "community.openfoodnetwork.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openfoodnetwork.org/u/{username}"
    API_URL = "https://community.openfoodnetwork.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenhabOrgConstants:
    NAME = "community.openhab.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openhab.org/u/{username}"
    API_URL = "https://community.openhab.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenpbsOrgConstants:
    NAME = "community.openpbs.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openpbs.org/u/{username}"
    API_URL = "https://community.openpbs.org/u/{username}.json"
    GENERIC = set()

class CommunityOpenrentCoUkConstants:
    NAME = "community.openrent.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.openrent.co.uk/u/{username}"
    API_URL = "https://community.openrent.co.uk/u/{username}.json"
    GENERIC = set()

class CommunityOpentargetsOrgConstants:
    NAME = "community.opentargets.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.opentargets.org/u/{username}"
    API_URL = "https://community.opentargets.org/u/{username}.json"
    GENERIC = set()

class CommunityOvhcloudComConstants:
    NAME = "community.ovhcloud.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ovhcloud.com/u/{username}"
    API_URL = "https://community.ovhcloud.com/u/{username}.json"
    GENERIC = set()

class CommunityP2puOrgConstants:
    NAME = "community.p2pu.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.p2pu.org/u/{username}"
    API_URL = "https://community.p2pu.org/u/{username}.json"
    GENERIC = set()

class CommunityParticleIoConstants:
    NAME = "community.particle.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.particle.io/u/{username}"
    API_URL = "https://community.particle.io/u/{username}.json"
    GENERIC = set()

class CommunityPenpotAppConstants:
    NAME = "community.penpot.app"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.penpot.app/u/{username}"
    API_URL = "https://community.penpot.app/u/{username}.json"
    GENERIC = set()

class CommunityPerplexityAiConstants:
    NAME = "community.perplexity.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.perplexity.ai/u/{username}"
    API_URL = "https://community.perplexity.ai/u/{username}.json"
    GENERIC = set()

class CommunityPickaxeCoConstants:
    NAME = "community.pickaxe.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.pickaxe.co/u/{username}"
    API_URL = "https://community.pickaxe.co/u/{username}.json"
    GENERIC = set()

class CommunityPinterestBizConstants:
    NAME = "community.pinterest.biz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.pinterest.biz/u/{username}"
    API_URL = "https://community.pinterest.biz/u/{username}.json"
    GENERIC = set()

class CommunityPix4dComConstants:
    NAME = "community.pix4d.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.pix4d.com/u/{username}"
    API_URL = "https://community.pix4d.com/u/{username}.json"
    GENERIC = set()

class CommunityPlotlyComConstants:
    NAME = "community.plotly.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.plotly.com/u/{username}"
    API_URL = "https://community.plotly.com/u/{username}.json"
    GENERIC = set()

class CommunityPodloveOrgConstants:
    NAME = "community.podlove.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.podlove.org/u/{username}"
    API_URL = "https://community.podlove.org/u/{username}.json"
    GENERIC = set()

class CommunityPostmanComConstants:
    NAME = "community.postman.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.postman.com/u/{username}"
    API_URL = "https://community.postman.com/u/{username}.json"
    GENERIC = set()

class CommunityPrivacyideaOrgConstants:
    NAME = "community.privacyidea.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.privacyidea.org/u/{username}"
    API_URL = "https://community.privacyidea.org/u/{username}.json"
    GENERIC = set()

class CommunityPuzzlequest3ComConstants:
    NAME = "community.puzzlequest3.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.puzzlequest3.com/u/{username}"
    API_URL = "https://community.puzzlequest3.com/u/{username}.json"
    GENERIC = set()

class CommunityQuickfileCoUkConstants:
    NAME = "community.quickfile.co.uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.quickfile.co.uk/u/{username}"
    API_URL = "https://community.quickfile.co.uk/u/{username}.json"
    GENERIC = set()

class CommunityRachioComConstants:
    NAME = "community.rachio.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.rachio.com/u/{username}"
    API_URL = "https://community.rachio.com/u/{username}.json"
    GENERIC = set()

class CommunityRampComConstants:
    NAME = "community.ramp.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ramp.com/u/{username}"
    API_URL = "https://community.ramp.com/u/{username}.json"
    GENERIC = set()

class CommunityRapydNetConstants:
    NAME = "community.rapyd.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.rapyd.net/u/{username}"
    API_URL = "https://community.rapyd.net/u/{username}.json"
    GENERIC = set()

class CommunityRetoolComConstants:
    NAME = "community.retool.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.retool.com/u/{username}"
    API_URL = "https://community.retool.com/u/{username}.json"
    GENERIC = set()

class CommunityRevolutionarygamesstudioComConstants:
    NAME = "community.revolutionarygamesstudio.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.revolutionarygamesstudio.com/u/{username}"
    API_URL = "https://community.revolutionarygamesstudio.com/u/{username}.json"
    GENERIC = set()

class CommunityRobotimeComConstants:
    NAME = "community.robotime.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.robotime.com/u/{username}"
    API_URL = "https://community.robotime.com/u/{username}.json"
    GENERIC = set()

class CommunityRootsmagicComConstants:
    NAME = "community.rootsmagic.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.rootsmagic.com/u/{username}"
    API_URL = "https://community.rootsmagic.com/u/{username}.json"
    GENERIC = set()

class CommunityRstudioComConstants:
    NAME = "community.rstudio.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.rstudio.com/u/{username}"
    API_URL = "https://community.rstudio.com/u/{username}.json"
    GENERIC = set()

class CommunitySat4allComConstants:
    NAME = "community.sat4all.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.sat4all.com/u/{username}"
    API_URL = "https://community.sat4all.com/u/{username}.json"
    GENERIC = set()

class CommunitySeqeraIoConstants:
    NAME = "community.seqera.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.seqera.io/u/{username}"
    API_URL = "https://community.seqera.io/u/{username}.json"
    GENERIC = set()

class CommunityShipheroComConstants:
    NAME = "community.shiphero.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.shiphero.com/u/{username}"
    API_URL = "https://community.shiphero.com/u/{username}.json"
    GENERIC = set()

class CommunityShopifyComConstants:
    NAME = "community.shopify.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.shopify.com/u/{username}"
    API_URL = "https://community.shopify.com/u/{username}.json"
    GENERIC = set()

class CommunityShopifyDevConstants:
    NAME = "community.shopify.dev"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.shopify.dev/u/{username}"
    API_URL = "https://community.shopify.dev/u/{username}.json"
    GENERIC = set()

class CommunitySigmacomputingComConstants:
    NAME = "community.sigmacomputing.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.sigmacomputing.com/u/{username}"
    API_URL = "https://community.sigmacomputing.com/u/{username}.json"
    GENERIC = set()

class CommunitySimplefocComConstants:
    NAME = "community.simplefoc.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.simplefoc.com/u/{username}"
    API_URL = "https://community.simplefoc.com/u/{username}.json"
    GENERIC = set()

class CommunitySmartthingsComConstants:
    NAME = "community.smartthings.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.smartthings.com/u/{username}"
    API_URL = "https://community.smartthings.com/u/{username}.json"
    GENERIC = set()

class CommunitySolderedComConstants:
    NAME = "community.soldered.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.soldered.com/u/{username}"
    API_URL = "https://community.soldered.com/u/{username}.json"
    GENERIC = set()

class CommunitySparkpntComConstants:
    NAME = "community.sparkpnt.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.sparkpnt.com/u/{username}"
    API_URL = "https://community.sparkpnt.com/u/{username}.json"
    GENERIC = set()

class CommunitySpritelyInstituteConstants:
    NAME = "community.spritely.institute"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.spritely.institute/u/{username}"
    API_URL = "https://community.spritely.institute/u/{username}.json"
    GENERIC = set()

class CommunityStapeIoConstants:
    NAME = "community.stape.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.stape.io/u/{username}"
    API_URL = "https://community.stape.io/u/{username}.json"
    GENERIC = set()

class CommunityStardogComConstants:
    NAME = "community.stardog.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.stardog.com/u/{username}"
    API_URL = "https://community.stardog.com/u/{username}.json"
    GENERIC = set()

class CommunityStarknetIoConstants:
    NAME = "community.starknet.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.starknet.io/u/{username}"
    API_URL = "https://community.starknet.io/u/{username}.json"
    GENERIC = set()

class CommunityStepsmashComConstants:
    NAME = "community.stepsmash.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.stepsmash.com/u/{username}"
    API_URL = "https://community.stepsmash.com/u/{username}.json"
    GENERIC = set()

class CommunityStereolabsComConstants:
    NAME = "community.stereolabs.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.stereolabs.com/u/{username}"
    API_URL = "https://community.stereolabs.com/u/{username}.json"
    GENERIC = set()

class CommunitySuitecrmComConstants:
    NAME = "community.suitecrm.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.suitecrm.com/u/{username}"
    API_URL = "https://community.suitecrm.com/u/{username}.json"
    GENERIC = set()

class CommunitySunnypilotAiConstants:
    NAME = "community.sunnypilot.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.sunnypilot.ai/u/{username}"
    API_URL = "https://community.sunnypilot.ai/u/{username}.json"
    GENERIC = set()

class CommunityTagoIoConstants:
    NAME = "community.tago.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tago.io/u/{username}"
    API_URL = "https://community.tago.io/u/{username}.json"
    GENERIC = set()

class CommunityTawkToConstants:
    NAME = "community.tawk.to"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tawk.to/u/{username}"
    API_URL = "https://community.tawk.to/u/{username}.json"
    GENERIC = set()

class CommunityTeableAiConstants:
    NAME = "community.teable.ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.teable.ai/u/{username}"
    API_URL = "https://community.teable.ai/u/{username}.json"
    GENERIC = set()

class CommunityTempestEarthConstants:
    NAME = "community.tempest.earth"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tempest.earth/u/{username}"
    API_URL = "https://community.tempest.earth/u/{username}.json"
    GENERIC = set()

class CommunityTheboxingmanagergameComConstants:
    NAME = "community.theboxingmanagergame.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.theboxingmanagergame.com/u/{username}"
    API_URL = "https://community.theboxingmanagergame.com/u/{username}.json"
    GENERIC = set()

class CommunityTheta360GuideConstants:
    NAME = "community.theta360.guide"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.theta360.guide/u/{username}"
    API_URL = "https://community.theta360.guide/u/{username}.json"
    GENERIC = set()

class CommunityThevirtualinstructorComConstants:
    NAME = "community.thevirtualinstructor.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.thevirtualinstructor.com/u/{username}"
    API_URL = "https://community.thevirtualinstructor.com/u/{username}.json"
    GENERIC = set()

class CommunityThunkableComConstants:
    NAME = "community.thunkable.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.thunkable.com/u/{username}"
    API_URL = "https://community.thunkable.com/u/{username}.json"
    GENERIC = set()

class CommunityTogglComConstants:
    NAME = "community.toggl.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.toggl.com/u/{username}"
    API_URL = "https://community.toggl.com/u/{username}.json"
    GENERIC = set()

class CommunityTourradarComConstants:
    NAME = "community.tourradar.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tourradar.com/u/{username}"
    API_URL = "https://community.tourradar.com/u/{username}.json"
    GENERIC = set()

class CommunityTrading212ComConstants:
    NAME = "community.trading212.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.trading212.com/u/{username}"
    API_URL = "https://community.trading212.com/u/{username}.json"
    GENERIC = set()

class CommunityTradovateComConstants:
    NAME = "community.tradovate.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tradovate.com/u/{username}"
    API_URL = "https://community.tradovate.com/u/{username}.json"
    GENERIC = set()

class CommunityTraefikIoConstants:
    NAME = "community.traefik.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.traefik.io/u/{username}"
    API_URL = "https://community.traefik.io/u/{username}.json"
    GENERIC = set()

class CommunityTransifexComConstants:
    NAME = "community.transifex.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.transifex.com/u/{username}"
    API_URL = "https://community.transifex.com/u/{username}.json"
    GENERIC = set()

class CommunityTransloaditComConstants:
    NAME = "community.transloadit.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.transloadit.com/u/{username}"
    API_URL = "https://community.transloadit.com/u/{username}.json"
    GENERIC = set()

class CommunityTulipCoConstants:
    NAME = "community.tulip.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.tulip.co/u/{username}"
    API_URL = "https://community.tulip.co/u/{username}.json"
    GENERIC = set()

class CommunityUltralyticsComConstants:
    NAME = "community.ultralytics.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.ultralytics.com/u/{username}"
    API_URL = "https://community.ultralytics.com/u/{username}.json"
    GENERIC = set()

class CommunityUmbrelComConstants:
    NAME = "community.umbrel.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.umbrel.com/u/{username}"
    API_URL = "https://community.umbrel.com/u/{username}.json"
    GENERIC = set()

class CommunityUnixComConstants:
    NAME = "community.unix.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.unix.com/u/{username}"
    API_URL = "https://community.unix.com/u/{username}.json"
    GENERIC = set()

class CommunityUpstoxComConstants:
    NAME = "community.upstox.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.upstox.com/u/{username}"
    API_URL = "https://community.upstox.com/u/{username}.json"
    GENERIC = set()

class CommunityUsconcealedcarryComConstants:
    NAME = "community.usconcealedcarry.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.usconcealedcarry.com/u/{username}"
    API_URL = "https://community.usconcealedcarry.com/u/{username}.json"
    GENERIC = set()

class CommunityVercelComConstants:
    NAME = "community.vercel.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.vercel.com/u/{username}"
    API_URL = "https://community.vercel.com/u/{username}.json"
    GENERIC = set()

class CommunityVtexComConstants:
    NAME = "community.vtex.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.vtex.com/u/{username}"
    API_URL = "https://community.vtex.com/u/{username}.json"
    GENERIC = set()

class CommunityWayfarerScopelyComConstants:
    NAME = "community.wayfarer.scopely.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.wayfarer.scopely.com/u/{username}"
    API_URL = "https://community.wayfarer.scopely.com/u/{username}.json"
    GENERIC = set()

class DiscourseMozillaOrgConstants:
    NAME = "discourse.mozilla.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.mozilla.org/u/{username}"
    API_URL = "https://discourse.mozilla.org/u/{username}.json"
    GENERIC = set()

class ForumsDockerComConstants:
    NAME = "forums.docker.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.docker.com/u/{username}"
    API_URL = "https://forums.docker.com/u/{username}.json"
    GENERIC = set()

class DiscussPythonConstants:
    NAME = "DiscussPython"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.python.org/u/{username}"
    API_URL = "https://discuss.python.org/u/{username}.json"
    GENERIC = set()

class ForumGhostOrgConstants:
    NAME = "forum.ghost.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.ghost.org/u/{username}"
    API_URL = "https://forum.ghost.org/u/{username}.json"
    GENERIC = set()

class DiscussElasticCoConstants:
    NAME = "Discuss.Elastic.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.elastic.co/u/{username}"
    API_URL = "https://discuss.elastic.co/u/{username}.json"
    GENERIC = set()

class FreecodecampConstants:
    NAME = "Freecodecamp"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.freecodecamp.org/forum/u/{username}"
    API_URL = "https://www.freecodecamp.org/forum/u/{username}.json"
    GENERIC = set()

class ForumsSketchupComConstants:
    NAME = "forums.sketchup.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.sketchup.com/u/{username}"
    API_URL = "https://forums.sketchup.com/u/{username}.json"
    GENERIC = set()

class DiscussHashicorpComConstants:
    NAME = "discuss.hashicorp.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.hashicorp.com/u/{username}"
    API_URL = "https://discuss.hashicorp.com/u/{username}.json"
    GENERIC = set()

class RustLangConstants:
    NAME = "Rust-lang"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://users.rust-lang.org/u/{username}"
    API_URL = "https://users.rust-lang.org/u/{username}.json"
    GENERIC = set()

class MetaDiscourseConstants:
    NAME = "MetaDiscourse"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://meta.discourse.org/u/{username}"
    API_URL = "https://meta.discourse.org/u/{username}.json"
    GENERIC = set()

class ForumInaturalistOrgConstants:
    NAME = "forum.inaturalist.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.inaturalist.org/u/{username}"
    API_URL = "https://forum.inaturalist.org/u/{username}.json"
    GENERIC = set()

class SublimeForumConstants:
    NAME = "SublimeForum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.sublimetext.com/u/{username}"
    API_URL = "https://forum.sublimetext.com/u/{username}.json"
    GENERIC = set()

class DiscourseHaskellOrgConstants:
    NAME = "discourse.haskell.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.haskell.org/u/{username}"
    API_URL = "https://discourse.haskell.org/u/{username}.json"
    GENERIC = set()

class DiscourseJupyterOrgConstants:
    NAME = "discourse.jupyter.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.jupyter.org/u/{username}"
    API_URL = "https://discourse.jupyter.org/u/{username}.json"
    GENERIC = set()

class ForumsSteinbergNetConstants:
    NAME = "forums.steinberg.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.steinberg.net/u/{username}"
    API_URL = "https://forums.steinberg.net/u/{username}.json"
    GENERIC = set()

class ForumSnapcraftIoConstants:
    NAME = "forum.snapcraft.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.snapcraft.io/u/{username}"
    API_URL = "https://forum.snapcraft.io/u/{username}.json"
    GENERIC = set()

class DiscoursePiHoleConstants:
    NAME = "DiscoursePi-hole"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.pi-hole.net/u/{username}"
    API_URL = "https://discourse.pi-hole.net/u/{username}.json"
    GENERIC = set()

class ScalaLangConstants:
    NAME = "Scala-lang"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://users.scala-lang.org/u/{username}"
    API_URL = "https://users.scala-lang.org/u/{username}.json"
    GENERIC = set()

class ForumShotcutOrgConstants:
    NAME = "forum.shotcut.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.shotcut.org/u/{username}"
    API_URL = "https://forum.shotcut.org/u/{username}.json"
    GENERIC = set()

class ForumsVisualParadigmComConstants:
    NAME = "forums.visual-paradigm.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.visual-paradigm.com/u/{username}"
    API_URL = "https://forums.visual-paradigm.com/u/{username}.json"
    GENERIC = set()

class ForumZorinComConstants:
    NAME = "forum.zorin.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.zorin.com/u/{username}"
    API_URL = "https://forum.zorin.com/u/{username}.json"
    GENERIC = set()

class MapillaryForumConstants:
    NAME = "Mapillary Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.mapillary.com/u/{username}"
    API_URL = "https://forum.mapillary.com/u/{username}.json"
    GENERIC = set()

class OpenframeworksConstants:
    NAME = "openframeworks"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.openframeworks.cc/u/{username}"
    API_URL = "https://forum.openframeworks.cc/u/{username}.json"
    GENERIC = set()

class SupportIlovegrowingmarijuanaComConstants:
    NAME = "support.ilovegrowingmarijuana.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://support.ilovegrowingmarijuana.com/u/{username}"
    API_URL = "https://support.ilovegrowingmarijuana.com/u/{username}.json"
    GENERIC = set()

class ForumGarudalinuxOrgConstants:
    NAME = "forum.garudalinux.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.garudalinux.org/u/{username}"
    API_URL = "https://forum.garudalinux.org/u/{username}.json"
    GENERIC = set()

class QuartertothreeConstants:
    NAME = "Quartertothree"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.quartertothree.com/u/{username}"
    API_URL = "https://forum.quartertothree.com/u/{username}.json"
    GENERIC = set()

class SignalConstants:
    NAME = "Signal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.signalusers.org/u/{username}"
    API_URL = "https://community.signalusers.org/u/{username}.json"
    GENERIC = set()

class GolangbridgeConstants:
    NAME = "Golangbridge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.golangbridge.org/u/{username}"
    API_URL = "https://forum.golangbridge.org/u/{username}.json"
    GENERIC = set()

class ITVDNForumConstants:
    NAME = "ITVDN Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.itvdn.com/u/{username}"
    API_URL = "https://forum.itvdn.com/u/{username}.json"
    GENERIC = set()

class LeasehackrConstants:
    NAME = "leasehackr"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.leasehackr.com/u/{username}"
    API_URL = "https://forum.leasehackr.com/u/{username}.json"
    GENERIC = set()

class HiveosFarmConstants:
    NAME = "hiveos.farm"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.hiveos.farm/u/{username}"
    API_URL = "https://forum.hiveos.farm/u/{username}.json"
    GENERIC = set()

class UMHOOPSConstants:
    NAME = "UMHOOPS"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.umhoops.com/u/{username}"
    API_URL = "https://forum.umhoops.com/u/{username}.json"
    GENERIC = set()

class TravisConstants:
    NAME = "Travis"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://travis-ci.community/u/{username}"
    API_URL = "https://travis-ci.community/u/{username}.json"
    GENERIC = set()

class SourcerunsConstants:
    NAME = "sourceruns"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.sourceruns.org/u/{username}"
    API_URL = "https://forums.sourceruns.org/u/{username}.json"
    GENERIC = set()

class SupportBlueSystemsComConstants:
    NAME = "support.blue-systems.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://support.blue-systems.com/u/{username}"
    API_URL = "https://support.blue-systems.com/u/{username}.json"
    GENERIC = set()

class HiveonComForumConstants:
    NAME = "hiveon.com forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hiveon.com/forum/u/{username}"
    API_URL = "https://hiveon.com/forum/u/{username}.json"
    GENERIC = set()

class SupportWirenboardComConstants:
    NAME = "support.wirenboard.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://support.wirenboard.com/u/{username}"
    API_URL = "https://support.wirenboard.com/u/{username}.json"
    GENERIC = set()

class ForumCsCartRuConstants:
    NAME = "forum.cs-cart.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.cs-cart.ru/u/{username}"
    API_URL = "https://forum.cs-cart.ru/u/{username}.json"
    GENERIC = set()

class VolkswagenLvivUaConstants:
    NAME = "volkswagen.lviv.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://volkswagen.lviv.ua/members/?username={username}"
    GENERIC = set()

class Tfw2005ComConstants:
    NAME = "tfw2005.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.tfw2005.com/boards/members/?username={username}"
    GENERIC = set()

class FacultyOfMedicineConstants:
    NAME = "FacultyOfMedicine"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.facmedicine.com/members/?username={username}"
    GENERIC = set()

class GeodesistConstants:
    NAME = "Geodesist"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://geodesist.ru/members/?username={username}"
    GENERIC = set()

class TheMainboardComConstants:
    NAME = "the-mainboard.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://the-mainboard.com/index.php/members/?username={username}"
    GENERIC = set()

class ForumBestflowersRuConstants:
    NAME = "forum.bestflowers.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.bestflowers.ru/members/?username={username}"
    GENERIC = set()

class ForumsSonicretroOrgConstants:
    NAME = "forums.sonicretro.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.sonicretro.org/members/?username={username}"
    GENERIC = set()

class FinforumConstants:
    NAME = "Finforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://finforum.net/members/?username={username}"
    GENERIC = set()

class WasmInConstants:
    NAME = "wasm.in"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wasm.in/members/?username={username}"
    GENERIC = set()

class DiscussFlarumOrgConstants:
    NAME = "discuss.flarum.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.flarum.org/u/{username}"
    GENERIC = set()

class GalactictalkOrgConstants:
    NAME = "galactictalk.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://galactictalk.org/u/{username}"
    GENERIC = set()

class FlarumEsConstants:
    NAME = "flarum.es"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://flarum.es/u/{username}"
    GENERIC = set()

class ForumFibraClickConstants:
    NAME = "forum.fibra.click"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.fibra.click/u/{username}"
    GENERIC = set()

class FlutterforumOrgConstants:
    NAME = "flutterforum.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://flutterforum.org/u/{username}"
    GENERIC = set()

class DiscussFlarumOrgCnConstants:
    NAME = "discuss.flarum.org.cn"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.flarum.org.cn/u/{username}"
    GENERIC = set()

class MasseffectUniverseComConstants:
    NAME = "masseffect-universe.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://masseffect-universe.com/index/8-0-{username}"
    GENERIC = set()

class CalendlyConstants:
    NAME = "Calendly"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://calendly.com/{username}"
    GENERIC = set()

class IssuuConstants:
    NAME = "Issuu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://issuu.com/{username}"
    GENERIC = set()

class ForumsOperaComConstants:
    NAME = "forums.opera.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.opera.com/user/{username}"
    GENERIC = set()

class FlickrGroupsConstants:
    NAME = "Flickr Groups"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.flickr.com/groups/{username}"
    GENERIC = set()

class CyberHarvardEduConstants:
    NAME = "cyber.harvard.edu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cyber.harvard.edu/people/{username}"
    GENERIC = set()

class OpenStreetMapConstants:
    NAME = "OpenStreetMap"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.openstreetmap.org/user/{username}"
    GENERIC = set()

class TwitterConstants:
    NAME = "Twitter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://twitter.com/{username}"
    GENERIC = set()

class BleachFandomConstants:
    NAME = "BleachFandom"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bleach.fandom.com/ru/wiki/%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA:{username}"
    GENERIC = set()

class CodeSnippetWikiConstants:
    NAME = "Code Snippet Wiki"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://codesnippets.fandom.com/wiki/User:{username}"
    GENERIC = set()

class ArmchairgmConstants:
    NAME = "Armchairgm"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://armchairgm.fandom.com/wiki/User:{username}"
    GENERIC = set()

class BuzzFeedConstants:
    NAME = "BuzzFeed"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://buzzfeed.com/{username}"
    GENERIC = set()

class NPMPackageConstants:
    NAME = "NPM-Package"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.npmjs.com/package/{username}"
    GENERIC = set()

class BattleraprusConstants:
    NAME = "Battleraprus"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://battleraprus.fandom.com/ru/wiki/%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA:{username}"
    GENERIC = set()

class OKConstants:
    NAME = "OK"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ok.ru/{username}"
    GENERIC = set()

class PaypalConstants:
    NAME = "Paypal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.paypal.com/paypalme/{username}"
    GENERIC = set()

class MyMailRuBkRuConstants:
    NAME = "My.Mail.ru@bk.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/bk/{username}/"
    GENERIC = set()

class MyMailRuYandexRuConstants:
    NAME = "My.Mail.ru@yandex.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/yandex.ru/{username}/"
    GENERIC = set()

class MyMailRuGmailComConstants:
    NAME = "My.Mail.ru@gmail.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/gmail.com/{username}/"
    GENERIC = set()

class DjsktLnkToConstants:
    NAME = "djskt.lnk.to"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://djskt.lnk.to/{username}"
    GENERIC = set()

class MyMailRuMailRuConstants:
    NAME = "My.Mail.ru@mail.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/mail/{username}/"
    GENERIC = set()

class TradingViewConstants:
    NAME = "TradingView"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tradingview.com/u/{username}"
    GENERIC = set()

class MyMailRuListRuConstants:
    NAME = "My.Mail.ru@list.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/list/{username}/"
    GENERIC = set()

class KickstarterConstants:
    NAME = "Kickstarter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.kickstarter.com/profile/{username}"
    GENERIC = set()

class TosterConstants:
    NAME = "Toster"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://qna.habr.com/user/{username}"
    GENERIC = set()

class MyMailRuVKConstants:
    NAME = "My.Mail.ru@VK"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/vk/{username}"
    GENERIC = set()

class MyMailRuYaRuConstants:
    NAME = "My.Mail.ru@ya.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/ya.ru/{username}/"
    GENERIC = set()

class WolframalphaForumConstants:
    NAME = "Wolframalpha Forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.wolfram.com/web/{username}/home"
    GENERIC = set()

class MyMailRuOKConstants:
    NAME = "My.Mail.ru@OK"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.mail.ru/ok/{username}"
    GENERIC = set()

class SteemitConstants:
    NAME = "Steemit"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://steemit.com/@{username}"
    GENERIC = set()

class IFTTTConstants:
    NAME = "IFTTT"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.ifttt.com/p/{username}"
    GENERIC = set()

class LinuxfoundationConstants:
    NAME = "linuxfoundation"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.linuxfoundation.org/profile/{username}"
    GENERIC = set()

class ChessConstants:
    NAME = "Chess"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.chess.com/member/{username}"
    GENERIC = set()

class ArtsyConstants:
    NAME = "Artsy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.artsy.net/artist/{username}"
    GENERIC = set()

class GiteeConstants:
    NAME = "Gitee"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gitee.com/{username}"
    GENERIC = set()

class DonorboxConstants:
    NAME = "Donorbox"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://donorbox.org/{username}"
    GENERIC = set()

class MixConstants:
    NAME = "Mix"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mix.com/{username}"
    GENERIC = set()

class Flightradar24Constants:
    NAME = "Flightradar24"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://my.flightradar24.com/{username}"
    GENERIC = set()

class MetacriticConstants:
    NAME = "Metacritic"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.metacritic.com/user/{username}"
    GENERIC = set()

class MyMiniFactoryConstants:
    NAME = "MyMiniFactory"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.myminifactory.com/users/{username}"
    GENERIC = set()

class BoostyConstants:
    NAME = "Boosty"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://boosty.to/{username}"
    GENERIC = set()

class N8nCommunityConstants:
    NAME = "N8n Community"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.n8n.io/u/{username}/summary"
    GENERIC = set()

class MssgMeConstants:
    NAME = "mssg.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mssg.me/{username}"
    GENERIC = set()

class TinkoffInvestConstants:
    NAME = "Tinkoff Invest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tbank.ru/invest/social/profile/{username}/"
    GENERIC = set()

class VelogConstants:
    NAME = "Velog"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://velog.io/@{username}/posts"
    GENERIC = set()

class MstdnSocialConstants:
    NAME = "Mstdn.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mstdn.social/@{username}"
    GENERIC = set()

class DestructoidConstants:
    NAME = "Destructoid"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.destructoid.com/?name={username}"
    GENERIC = set()

class PeriscopeMainConstants:
    NAME = "PeriscopeMain"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.periscope.tv/{username}/"
    GENERIC = set()

class MuffinGroupConstants:
    NAME = "MuffinGroup"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.muffingroup.com/betheme/profile/{username}"
    GENERIC = set()

class TelescopeAcConstants:
    NAME = "telescope.ac"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://telescope.ac/{username}"
    GENERIC = set()

class MastodonSocialConstants:
    NAME = "mastodon.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mastodon.social/@{username}"
    GENERIC = set()

class ChaosSocialConstants:
    NAME = "chaos.social"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://chaos.social/@{username}"
    GENERIC = set()

class SocialTchncsDeConstants:
    NAME = "social.tchncs.de"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://social.tchncs.de/@{username}"
    GENERIC = set()

class NiftygatewayConstants:
    NAME = "Niftygateway"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://niftygateway.com/profile/{username}"
    GENERIC = set()

class AknigaConstants:
    NAME = "Akniga"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://akniga.org/profile/{username}"
    GENERIC = set()

class OverclockersConstants:
    NAME = "Overclockers"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://overclockers.ru/cpubase/user/{username}"
    GENERIC = set()

class GlobalvoicesConstants:
    NAME = "Globalvoices"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://globalvoices.org/author/{username}/"
    GENERIC = set()

class DealabsConstants:
    NAME = "Dealabs"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.dealabs.com/profile/{username}"
    GENERIC = set()

class TerrariaForumsConstants:
    NAME = "Terraria Forums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.terraria.org/index.php?search/42798315/&c[users]={username}&o=relevance"
    GENERIC = set()

class TunaConstants:
    NAME = "Tuna"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tuna.voicemod.net/user/{username}"
    GENERIC = set()

class ShorByConstants:
    NAME = "shor.by"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://shor.by/{username}"
    GENERIC = set()

class WeedmapsConstants:
    NAME = "Weedmaps"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://weedmaps.com/brands/{username}"
    GENERIC = set()

class MastodonCloudConstants:
    NAME = "mastodon.cloud"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mastodon.cloud/@{username}"
    GENERIC = set()

class N3dtodayConstants:
    NAME = "3dtoday"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://3dtoday.ru/blogs/{username}"
    GENERIC = set()

class PromoDJConstants:
    NAME = "PromoDJ"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://promodj.com/{username}"
    GENERIC = set()

class EmpowherConstants:
    NAME = "Empowher"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.empowher.com/users/{username}"
    GENERIC = set()

class MydealzConstants:
    NAME = "Mydealz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mydealz.de/profile/{username}"
    GENERIC = set()

class ManyLinkConstants:
    NAME = "many.link"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://many.link/{username}"
    GENERIC = set()

class VirgoolConstants:
    NAME = "Virgool"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://virgool.io/@{username}"
    GENERIC = set()

class SessionizeComConstants:
    NAME = "sessionize.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sessionize.com/{username}/"
    GENERIC = set()

class StudfileConstants:
    NAME = "Studfile"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://studfile.net/users/{username}/"
    IMPERSONATE = "safari"
    GENERIC = set()

class IllustratorsConstants:
    NAME = "Illustrators"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://illustrators.ru/users/{username}"
    GENERIC = set()

class FLRuConstants:
    NAME = "FL.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.fl.ru/users/{username}"
    GENERIC = set()

class EintrachtConstants:
    NAME = "Eintracht"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.eintracht.de/fans/{username}"
    GENERIC = set()

class InfourokConstants:
    NAME = "Infourok"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://infourok.ru/user/{username}"
    GENERIC = set()

class IphonesRuConstants:
    NAME = "Iphones.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.iphones.ru/iNotes/author/{username}?profile=1"
    GENERIC = set()

class SpletnikConstants:
    NAME = "Spletnik"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://spletnik.ru/user/{username}"
    GENERIC = set()

class MouthshutConstants:
    NAME = "Mouthshut"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mouthshut.com/{username}"
    GENERIC = set()

class TravellersPointConstants:
    NAME = "TravellersPoint"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.travellerspoint.com/users/{username}"
    GENERIC = set()

class VeroConstants:
    NAME = "Vero"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vero.co/{username}"
    GENERIC = set()

class MastodonXyzConstants:
    NAME = "mastodon.xyz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mastodon.xyz/@{username}"
    GENERIC = set()

class FramapiafConstants:
    NAME = "Framapiaf"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://framapiaf.org/@{username}"
    GENERIC = set()

class SmartLabRuConstants:
    NAME = "smart-lab.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://smart-lab.ru/profile/{username}/"
    GENERIC = set()

class DonationsAlertsConstants:
    NAME = "DonationsAlerts"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.donationalerts.com/r/{username}"
    GENERIC = set()

class MywedConstants:
    NAME = "Mywed"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mywed.com/ru/photographer/{username}/"
    GENERIC = set()

class SparkConstants:
    NAME = "Spark"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://spark.ru/startup/{username}"
    GENERIC = set()

class VgtimesConstants:
    NAME = "Vgtimes"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vgtimes.ru/user/{username}"
    GENERIC = set()

class CollectorsComConstants:
    NAME = "collectors.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.collectors.com/profile/{username}"
    GENERIC = set()

class LibrariesConstants:
    NAME = "Libraries"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://libraries.io/github/{username}/"
    GENERIC = set()

class Suomi24Constants:
    NAME = "Suomi24"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.suomi24.fi/profiili/{username}"
    GENERIC = set()

class TrashboxRuConstants:
    NAME = "Trashbox.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://trashbox.ru/users/{username}"
    GENERIC = set()

class TruelancerConstants:
    NAME = "Truelancer"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.truelancer.com/freelancer/{username}"
    GENERIC = set()

class MylotConstants:
    NAME = "Mylot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mylot.com/{username}"
    GENERIC = set()

class N7dachConstants:
    NAME = "7dach"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://7dach.ru/profile/{username}"
    GENERIC = set()

class ShazooConstants:
    NAME = "Shazoo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://shazoo.ru/users/{username}"
    GENERIC = set()

class AppSamsungfoodComConstants:
    NAME = "app.samsungfood.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://app.samsungfood.com/u/{username}"
    GENERIC = set()

class NickNameRuConstants:
    NAME = "Nick-name.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nick-name.ru/nickname/{username}/"
    GENERIC = set()

class ForumTauckConstants:
    NAME = "ForumTauck"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.tauck.com/profile/{username}"
    GENERIC = set()

class ForestConstants:
    NAME = "Forest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forest.ru/forum/user/{username}/"
    GENERIC = set()

class KwejkConstants:
    NAME = "Kwejk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kwejk.pl/uzytkownik/{username}#/tablica/"
    GENERIC = set()

class PepperNLConstants:
    NAME = "Pepper NL"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nl.pepper.com/profile/{username}"
    GENERIC = set()

class BitpapaComConstants:
    NAME = "bitpapa.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bitpapa.com/ru/user/{username}"
    GENERIC = set()

class ModxProConstants:
    NAME = "Modx_pro"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://modx.pro/users/{username}"
    GENERIC = set()

class DasaugeConstants:
    NAME = "Dasauge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://dasauge.co.uk/-{username}"
    GENERIC = set()

class ChollometroConstants:
    NAME = "Chollometro"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.chollometro.com/profile/{username}"
    GENERIC = set()

class ShikimoriConstants:
    NAME = "Shikimori"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://shikimori.one/{username}"
    GENERIC = set()

class AllhockeyConstants:
    NAME = "Allhockey"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://allhockey.ru/blog/{username}"
    GENERIC = set()

class StereoConstants:
    NAME = "Stereo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://stereo.ru/users/@{username}"
    GENERIC = set()

class MamuliConstants:
    NAME = "Mamuli"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mamuli.club/profile/{username}"
    GENERIC = set()

class AddonsWagoConstants:
    NAME = "Addons.wago"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://addons.wago.io/user/{username}"
    GENERIC = set()

class LoriConstants:
    NAME = "Lori"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lori.ru/{username}"
    GENERIC = set()

class SnoothConstants:
    NAME = "Snooth"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.snooth.com/author/{username}/"
    GENERIC = set()

class TellonymMeConstants:
    NAME = "Tellonym.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tellonym.me/{username}"
    GENERIC = set()

class PentesterLabConstants:
    NAME = "Pentester Lab"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pentesterlab.com/profile/{username}"
    GENERIC = set()

class SocialLibremOneConstants:
    NAME = "SocialLibremOne"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://social.librem.one/@{username}"
    GENERIC = set()

class PromodescuentosConstants:
    NAME = "Promodescuentos"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.promodescuentos.com/profile/{username}"
    GENERIC = set()

class PepperPLConstants:
    NAME = "Pepper PL"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pepper.pl/profile/{username}"
    GENERIC = set()

class NglLinkConstants:
    NAME = "ngl.link"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ngl.link/{username}"
    GENERIC = set()

class PreisjaegerConstants:
    NAME = "Preisjaeger"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.preisjaeger.at/profile/{username}"
    GENERIC = set()

class HouseMixesComConstants:
    NAME = "House-Mixes.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.house-mixes.com/profile/{username}"
    GENERIC = set()

class VoicesevasConstants:
    NAME = "Voicesevas"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://voicesevas.ru/user/{username}/"
    GENERIC = set()

class DonatePayConstants:
    NAME = "DonatePay"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://donatepay.ru/don/{username}"
    GENERIC = set()

class ProglibConstants:
    NAME = "Proglib"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://proglib.io/u/{username}/posts"
    GENERIC = set()

class OmoimotConstants:
    NAME = "Omoimot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://omoimot.ru/users/{username}"
    GENERIC = set()

class CapitalcityCombatsConstants:
    NAME = "CapitalcityCombats"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://capitalcity.combats.com/inf.pl?{username}"
    GENERIC = set()

class DemonscityConstants:
    NAME = "Demonscity"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://demonscity.combats.com/inf.pl?{username}"
    GENERIC = set()

class XboxGamertagConstants:
    NAME = "Xbox Gamertag"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://xboxgamertag.com/search/{username}"
    GENERIC = set()

class KashalotConstants:
    NAME = "Kashalot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kashalot.com/users/{username}/"
    GENERIC = set()

class NewreporterConstants:
    NAME = "Newreporter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://newreporter.org/author/{username}/"
    GENERIC = set()

class IgrarenaConstants:
    NAME = "igrarena"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.igrarena.ru/members/?username={username}"
    GENERIC = set()

class HomskComConstants:
    NAME = "homsk.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://homsk.com/profile/{username}"
    GENERIC = set()

class NesiditsaConstants:
    NAME = "Nesiditsa"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nesiditsa.ru/members/{username}/"
    GENERIC = set()

class ServeradminConstants:
    NAME = "Serveradmin"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://serveradmin.ru/author/{username}"
    GENERIC = set()

class PsyeraConstants:
    NAME = "Psyera"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://psyera.ru/user/{username}"
    GENERIC = set()

class CyberDefendersConstants:
    NAME = "Cyber Defenders"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cyberdefenders.org/p/{username}"
    GENERIC = set()

class WritercenterConstants:
    NAME = "Writercenter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://writercenter.ru/profile/{username}/"
    GENERIC = set()

class KloombaComConstants:
    NAME = "kloomba.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kloomba.com/users/{username}"
    GENERIC = set()

class GentlemintConstants:
    NAME = "Gentlemint"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gentlemint.com/users/{username}/"
    GENERIC = set()

class LenovConstants:
    NAME = "Lenov"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lenov.ru/user/{username}/"
    GENERIC = set()

class ConnosrConstants:
    NAME = "Connosr"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.connosr.com/@{username}"
    GENERIC = set()

class StudworkConstants:
    NAME = "Studwork"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://studwork.org/info/{username}"
    GENERIC = set()

class BezuzytecznaConstants:
    NAME = "Bezuzyteczna"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bezuzyteczna.pl/uzytkownicy/{username}"
    GENERIC = set()

class BgforumConstants:
    NAME = "Bgforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bgforum.ru/user/{username}/"
    GENERIC = set()

class ChamskoPlConstants:
    NAME = "Chamsko.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.chamsko.pl/profil/{username}"
    GENERIC = set()

class CastingcallclubConstants:
    NAME = "Castingcallclub"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.castingcall.club/{username}"
    GENERIC = set()

class CaringbridgeConstants:
    NAME = "Caringbridge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.caringbridge.org/visit/{username}"
    GENERIC = set()

class CryptomatorForumConstants:
    NAME = "CryptomatorForum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.cryptomator.org/u/{username}"
    GENERIC = set()

class CytoidIoConstants:
    NAME = "Cytoid.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cytoid.io/profile/{username}"
    GENERIC = set()

class BuzznetConstants:
    NAME = "Buzznet"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.buzznet.com/author/{username}"
    GENERIC = set()

class DangerousthingsComConstants:
    NAME = "Dangerousthings.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.dangerousthings.com/u/{username}"
    GENERIC = set()

class DevtribeConstants:
    NAME = "Devtribe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://devtribe.ru/user/{username}"
    GENERIC = set()

class FosstodonConstants:
    NAME = "Fosstodon"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fosstodon.org/@{username}"
    GENERIC = set()

class FclmnewsConstants:
    NAME = "Fclmnews"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fclmnews.ru/user/{username}"
    GENERIC = set()

class G2gComConstants:
    NAME = "G2g.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.g2g.com/{username}"
    GENERIC = set()

class GeniusArtistsConstants:
    NAME = "GeniusArtists"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://genius.com/artists/{username}"
    GENERIC = set()

class GrailedConstants:
    NAME = "Grailed"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.grailed.com/{username}"
    GENERIC = set()

class HondaConstants:
    NAME = "Honda"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://honda.org.ua/forum/user/{username}"
    GENERIC = set()

class JbzdConstants:
    NAME = "Jbzd"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://jbzd.com.pl/uzytkownik/{username}"
    GENERIC = set()

class IonicFrameworkConstants:
    NAME = "IonicFramework"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.ionicframework.com/u/{username}"
    GENERIC = set()

class JoplinAppConstants:
    NAME = "JoplinApp"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.joplinapp.org/u/{username}"
    GENERIC = set()

class FireworktvConstants:
    NAME = "Fireworktv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://fireworktv.com/ch/{username}"
    GENERIC = set()

class JellyfinWeblateConstants:
    NAME = "Jellyfin Weblate"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://translate.jellyfin.org/user/{username}/"
    GENERIC = set()

class LineMeConstants:
    NAME = "line.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://line.me/R/ti/p/@{username}?from=page"
    GENERIC = set()

class ListedToConstants:
    NAME = "Listed.to"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://listed.to/@{username}"
    GENERIC = set()

class ManutdConstants:
    NAME = "Manutd"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://manutd.one/user/{username}"
    GENERIC = set()

class MartechConstants:
    NAME = "Martech"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://martech.org/author/{username}/"
    GENERIC = set()

class Megane2Constants:
    NAME = "Megane2"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://megane2.ru/forum/members/?username={username}"
    GENERIC = set()

class NyaaSiConstants:
    NAME = "Nyaa.si"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nyaa.si/user/{username}"
    GENERIC = set()

class Oglaszamy24hConstants:
    NAME = "Oglaszamy24h"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://oglaszamy24h.pl/profil,{username}"
    GENERIC = set()

class PartyvibeConstants:
    NAME = "Partyvibe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.partyvibe.org/members/{username}/"
    GENERIC = set()

class RigczClubConstants:
    NAME = "Rigcz.club"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://rigcz.club/@{username}"
    GENERIC = set()

class RcloneForumConstants:
    NAME = "RcloneForum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.rclone.org/u/{username}"
    GENERIC = set()

class MipedConstants:
    NAME = "Miped"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://miped.ru/user/{username}"
    GENERIC = set()


class SchlockConstants:
    NAME = "Schlock"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://schlock.ru/author/{username}"
    GENERIC = set()

class SoobshestvaConstants:
    NAME = "Soobshestva"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.soobshestva.ru/forum/user/{username}/"
    GENERIC = set()

class SwapdConstants:
    NAME = "Swapd"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://swapd.co/u/{username}"
    GENERIC = set()

class SuzuriJpConstants:
    NAME = "Suzuri.jp"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://suzuri.jp/{username}"
    GENERIC = set()

class SzmerInfoConstants:
    NAME = "Szmer.info"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://szmer.info/u/{username}"
    GENERIC = set()

class ShitpostBot5000Constants:
    NAME = "ShitpostBot5000"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.shitpostbot.com/user/{username}"
    GENERIC = set()

class TorrentSoftConstants:
    NAME = "Torrent-soft"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://torrent-soft.net/user/{username}/"
    GENERIC = set()

class TruckersMPRuConstants:
    NAME = "TruckersMP.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://truckersmp.ru/{username}"
    GENERIC = set()

class UsaLifeConstants:
    NAME = "Usa.life"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://usa.life/{username}"
    GENERIC = set()

class WordnikConstants:
    NAME = "Wordnik"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.wordnik.com/users/{username}"
    GENERIC = set()

class UncUaConstants:
    NAME = "unc.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://unc.ua/{username}"
    GENERIC = set()

class WwwKinokopilkaProConstants:
    NAME = "www.kinokopilka.pro"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.kinokopilka.pro/users/{username}"
    GENERIC = set()

class PurephotoConstants:
    NAME = "Purephoto"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.purephoto.com/{username}"
    GENERIC = set()

class BulbappComConstants:
    NAME = "bulbapp.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bulbapp.com/{username}"
    GENERIC = set()

class CommunityRoonlabsComConstants:
    NAME = "community.roonlabs.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.roonlabs.com/u/{username}"
    GENERIC = set()

class PhotoshopKoponaComConstants:
    NAME = "photoshop-kopona.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://photoshop-kopona.com/ru/user/{username}/"
    GENERIC = set()

class DiscourseMcStanOrgConstants:
    NAME = "discourse.mc-stan.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.mc-stan.org/u/{username}"
    GENERIC = set()

class TikbuddyComConstants:
    NAME = "tikbuddy.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tikbuddy.com/en/tiktok/{username}"
    GENERIC = set()

class DiscourseJulialangOrgConstants:
    NAME = "discourse.julialang.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.julialang.org/u/{username}"
    GENERIC = set()

class DiscourseNoderedOrgConstants:
    NAME = "discourse.nodered.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discourse.nodered.org/u/{username}"
    GENERIC = set()

class DiscussCircleciComConstants:
    NAME = "discuss.circleci.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.circleci.com/u/{username}"
    GENERIC = set()

class DiscussKubernetesIoConstants:
    NAME = "discuss.kubernetes.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.kubernetes.io/u/{username}"
    GENERIC = set()

class DiscussKotlinlangOrgConstants:
    NAME = "discuss.kotlinlang.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.kotlinlang.org/u/{username}"
    GENERIC = set()

class DiscussPixlsUsConstants:
    NAME = "discuss.pixls.us"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.pixls.us/u/{username}"
    GENERIC = set()

class EnIllogicopediaOrgConstants:
    NAME = "en.illogicopedia.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://en.illogicopedia.org/wiki/User:{username}"
    GENERIC = set()

class DjagiConstants:
    NAME = "Djagi"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.djagi.com/cards/{username}"
    GENERIC = set()

class DiscussProsemirrorNetConstants:
    NAME = "discuss.prosemirror.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.prosemirror.net/u/{username}"
    GENERIC = set()

class ElixirforumComConstants:
    NAME = "elixirforum.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://elixirforum.com/u/{username}"
    GENERIC = set()

class EnUncyclopediaCoConstants:
    NAME = "en.uncyclopedia.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://en.uncyclopedia.co/wiki/User:{username}"
    GENERIC = set()

class DiscussPytorchOrgConstants:
    NAME = "discuss.pytorch.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.pytorch.org/u/{username}"
    GENERIC = set()

class ForumBananaPiOrgConstants:
    NAME = "forum.banana-pi.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.banana-pi.org/u/{username}"
    GENERIC = set()

class FlipsnackComConstants:
    NAME = "flipsnack.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://flipsnack.com/{username}"
    GENERIC = set()

class ForumCfxReConstants:
    NAME = "forum.cfx.re"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.cfx.re/u/{username}"
    GENERIC = set()

class FfmBioConstants:
    NAME = "ffm.bio"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ffm.bio/{username}"
    GENERIC = set()

class ForumObsidianMdConstants:
    NAME = "forum.obsidian.md"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.obsidian.md/u/{username}"
    GENERIC = set()

class ForumCockroachlabsComConstants:
    NAME = "forum.cockroachlabs.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.cockroachlabs.com/u/{username}"
    GENERIC = set()

class ForumFreecodecampOrgConstants:
    NAME = "forum.freecodecamp.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.freecodecamp.org/u/{username}"
    GENERIC = set()

class ForumGitlabComConstants:
    NAME = "forum.gitlab.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.gitlab.com/u/{username}"
    GENERIC = set()

class ForumGolangbridgeOrgConstants:
    NAME = "forum.golangbridge.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.golangbridge.org/u/{username}"
    GENERIC = set()

class ForumJuceComConstants:
    NAME = "forum.juce.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.juce.com/u/{username}"
    GENERIC = set()

class ForumLeasehackrComConstants:
    NAME = "forum.leasehackr.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.leasehackr.com/u/{username}/summary"
    GENERIC = set()

class ForumSeeedstudioComConstants:
    NAME = "forum.seeedstudio.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.seeedstudio.com/u/{username}"
    GENERIC = set()

class DiscussHuelComConstants:
    NAME = "discuss.huel.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discuss.huel.com/u/{username}"
    GENERIC = set()

class DiscoursedbOrgConstants:
    NAME = "discoursedb.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discoursedb.org/wiki/User:{username}"
    GENERIC = set()

class ForumsBalenaIoConstants:
    NAME = "forums.balena.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.balena.io/u/{username}"
    GENERIC = set()

class ForumUipathComConstants:
    NAME = "forum.uipath.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.uipath.com/u/{username}"
    GENERIC = set()

class ForumsLawrencesystemsComConstants:
    NAME = "forums.lawrencesystems.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.lawrencesystems.com/u/{username}"
    GENERIC = set()

class FlirticEeConstants:
    NAME = "flirtic.ee"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://flirtic.ee/{username}"
    GENERIC = set()

class ForumsPimoroniComConstants:
    NAME = "forums.pimoroni.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.pimoroni.com/u/{username}"
    GENERIC = set()

class ExploretalentComConstants:
    NAME = "exploretalent.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://exploretalent.com/{username}"
    GENERIC = set()

class ForumBonsaimiraiComConstants:
    NAME = "forum.bonsaimirai.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.bonsaimirai.com/u/{username}"
    GENERIC = set()

class KidicaruswikiOrgConstants:
    NAME = "kidicaruswiki.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kidicaruswiki.org/wiki/User:{username}"
    GENERIC = set()

class ForumsWyzecamComConstants:
    NAME = "forums.wyzecam.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.wyzecam.com/u/{username}"
    GENERIC = set()

class MetroidwikiOrgConstants:
    NAME = "metroidwiki.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://metroidwiki.org/wiki/User:{username}"
    GENERIC = set()

class ForumsTNationComConstants:
    NAME = "forums.t-nation.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.t-nation.com/u/{username}"
    GENERIC = set()

class MetaDiscourseOrgConstants:
    NAME = "meta.discourse.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://meta.discourse.org/u/{username}"
    GENERIC = set()

class MintmeComConstants:
    NAME = "mintme.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mintme.com/token/{username}"
    GENERIC = set()

class ForumSublimetextComConstants:
    NAME = "forum.sublimetext.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.sublimetext.com/u/{username}"
    GENERIC = set()

class NookipediaComConstants:
    NAME = "nookipedia.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nookipedia.com/wiki/User:{username}"
    GENERIC = set()

class PatchComConstants:
    NAME = "patch.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://patch.com/users/{username}"
    GENERIC = set()

class PttwebCcConstants:
    NAME = "pttweb.cc"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pttweb.cc/user/{username}"
    GENERIC = set()

class Mql5ComConstants:
    NAME = "mql5.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mql5.com/es/users/{username}"
    GENERIC = set()

class SplatoonwikiOrgConstants:
    NAME = "splatoonwiki.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://splatoonwiki.org/wiki/User:{username}"
    GENERIC = set()

class StrategywikiOrgConstants:
    NAME = "strategywiki.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://strategywiki.org/wiki/User:{username}"
    GENERIC = set()

class StellerCoConstants:
    NAME = "steller.co"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://steller.co/{username}"
    GENERIC = set()

class TalkMacpowerusersComConstants:
    NAME = "talk.macpowerusers.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://talk.macpowerusers.com/u/{username}"
    GENERIC = set()

class SsbwikiComConstants:
    NAME = "ssbwiki.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ssbwiki.com/User:{username}"
    GENERIC = set()

class UbuntuMateCommunityConstants:
    NAME = "ubuntu-mate.community"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ubuntu-mate.community/u/{username}"
    GENERIC = set()

class UsersRustLangOrgConstants:
    NAME = "users.rust-lang.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://users.rust-lang.org/u/{username}"
    GENERIC = set()

class WikiThemanaworldOrgConstants:
    NAME = "wiki.themanaworld.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wiki.themanaworld.org/wiki/User:{username}"
    GENERIC = set()

class SketchfabComConstants:
    NAME = "sketchfab.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://sketchfab.com/{username}"
    GENERIC = set()

class WikiTeamfortressComConstants:
    NAME = "wiki.teamfortress.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wiki.teamfortress.com/wiki/User:{username}"
    GENERIC = set()

class AetherhubConstants:
    NAME = "aetherhub"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://aetherhub.com/User/{username}"
    GENERIC = set()

class RawgIoConstants:
    NAME = "rawg.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://rawg.io/@{username}"
    GENERIC = set()

class DimensionalMeConstants:
    NAME = "DimensionalMe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.dimensional.me/{username}"
    GENERIC = set()

class HackerSploitConstants:
    NAME = "Hacker Sploit"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.hackersploit.org/u/{username}"
    GENERIC = set()

class ChaturbatorSuConstants:
    NAME = "chaturbator.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://chaturbator.su/{username}?pagespeed=noscript"
    GENERIC = set()

class PepperdealsConstants:
    NAME = "Pepperdeals"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.pepperdeals.se/profile/{username}"
    GENERIC = set()

class HolopinConstants:
    NAME = "Holopin"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://holopin.io/@{username}"
    GENERIC = set()

class PlaystrategyConstants:
    NAME = "Playstrategy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://playstrategy.org/@/{username}"
    GENERIC = set()

class CurseForgeConstants:
    NAME = "Curse Forge"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.curseforge.com/members/{username}/projects"
    GENERIC = set()

class PolymarketConstants:
    NAME = "Polymarket"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://polymarket.com/@{username}"
    GENERIC = set()

class CTFtimeConstants:
    NAME = "CTFtime"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ctftime.org/team/{username}"
    GENERIC = set()

class ZoraConstants:
    NAME = "Zora"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://zora.co/@{username}"
    GENERIC = set()

class TrepupComConstants:
    NAME = "trepup.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://trepup.com/{username}"
    GENERIC = set()

class WewinRuConstants:
    NAME = "wewin.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wewin.ru/user/{username}"
    GENERIC = set()

class BitPapaConstants:
    NAME = "BitPapa"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bitpapa.com/ru/user/{username}"
    GENERIC = set()

class SEOForumConstants:
    NAME = "SEOForum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://seoforum.com/@{username}"
    GENERIC = set()

class MinfinComUaConstants:
    NAME = "minfin.com.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://minfin.com.ua/users/{username}/"
    GENERIC = set()

class ValorantForumsConstants:
    NAME = "Valorant Forums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://valorantforums.com/u/{username}"
    GENERIC = set()

class TonometerbotConstants:
    NAME = "Tonometerbot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tonometerbot.com/@/{username}"
    GENERIC = set()

class DiveforumConstants:
    NAME = "Diveforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://diveforum.spb.ru/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Извините',)
    GENERIC = set()

class SteamGroupConstants:
    NAME = "Steam (Group)"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://steamcommunity.com/groups/{username}"
    PRESENCE = ()
    ABSENCE = ('No group could be retrieved for the given URL',)
    GENERIC = set()

class WeldConstants:
    NAME = "Weld"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://weld.in.ua/forum/member.php/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.',)
    GENERIC = set()

class ApelmonOdUaConstants:
    NAME = "apelmon.od.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://apelmon.od.ua/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N74507UcozRuConstants:
    NAME = "74507.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://74507.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DiigoConstants:
    NAME = "Diigo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.diigo.com/interact_api/load_profile_info?name={username}"
    PRESENCE = ()
    ABSENCE = ('{}',)
    GENERIC = set()

class UcozConstants:
    NAME = "Ucoz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ArmybootsUcozRuConstants:
    NAME = "armyboots.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://armyboots.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AfsocUcozRuConstants:
    NAME = "afsoc.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://afsoc.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FableroUcozRuConstants:
    NAME = "fablero.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fablero.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AlpanfUcozRuConstants:
    NAME = "alpanf.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://alpanf.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AntalyaUcozRuConstants:
    NAME = "antalya.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://antalya.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ArmyRusUcozRuConstants:
    NAME = "army-rus.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://army-rus.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AntizombieUcozRuConstants:
    NAME = "antizombie.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://antizombie.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SlashdotConstants:
    NAME = "Slashdot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://slashdot.org/~{username}"
    PRESENCE = ()
    ABSENCE = ('user you requested does not exist',)
    GENERIC = set()

class DoubanConstants:
    NAME = "Douban"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.douban.com/people/{username}/"
    PRESENCE = ('db-usr-profile',)
    ABSENCE = ('返回首页',)
    GENERIC = set()

class MorshanskUcozRuConstants:
    NAME = "morshansk.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://morshansk.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AviabazaMeriaUcozRuConstants:
    NAME = "aviabaza-meria.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://aviabaza-meria.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EasyjobUcozRuConstants:
    NAME = "easyjob.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://easyjob.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GebirgsUcozRuConstants:
    NAME = "gebirgs.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gebirgs.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LosinopetrovskUcozRuConstants:
    NAME = "losinopetrovsk.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://losinopetrovsk.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Kursk46UcozRuConstants:
    NAME = "kursk46.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kursk46.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OopkmoskvaUcozRuConstants:
    NAME = "oopkmoskva.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://oopkmoskva.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OvoUcozRuConstants:
    NAME = "ovo.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ovo.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PvAfghanUcozRuConstants:
    NAME = "pv-afghan.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pv-afghan.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SalekhardnewsUcozRuConstants:
    NAME = "salekhardnews.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://salekhardnews.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ProCssteamUcozRuConstants:
    NAME = "pro-cssteam.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pro-cssteam.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PunxUcozRuConstants:
    NAME = "punx.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://punx.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RusMmmUcozRuConstants:
    NAME = "rus-mmm.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rus-mmm.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TarjaturunenUcozRuConstants:
    NAME = "tarjaturunen.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tarjaturunen.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VirtualAutoUcozRuConstants:
    NAME = "virtual-auto.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://virtual-auto.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WeaponsasUcozRuConstants:
    NAME = "weaponsas.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://weaponsas.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XakerminusUcozRuConstants:
    NAME = "xakerminus.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xakerminus.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZabseloUcozRuConstants:
    NAME = "zabselo.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zabselo.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SfinxCatsUcozRuConstants:
    NAME = "sfinx-cats.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sfinx-cats.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RottweilerUcozRuConstants:
    NAME = "rottweiler.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rottweiler.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GomelDogsUcozRuConstants:
    NAME = "gomel-dogs.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gomel-dogs.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LaiUcozRuConstants:
    NAME = "lai.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lai.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZennenhundUcozRuConstants:
    NAME = "zennenhund.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zennenhund.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Nada25UcozRuConstants:
    NAME = "nada25.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nada25.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LegendarusVeoUcozRuConstants:
    NAME = "legendarus-veo.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://legendarus-veo.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DayLapkuUcozRuConstants:
    NAME = "day-lapku.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://day-lapku.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ShansonUcozRuConstants:
    NAME = "shanson.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://shanson.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VadyaUcozRuConstants:
    NAME = "vadya.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vadya.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EyorkieUcozRuConstants:
    NAME = "eyorkie.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://eyorkie.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class UgriUcozRuConstants:
    NAME = "ugri.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ugri.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MilnerelenaUcozRuConstants:
    NAME = "milnerelena.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://milnerelena.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZebestUcozRuConstants:
    NAME = "zebest.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zebest.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class P1ratUcozRuConstants:
    NAME = "p1rat.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://p1rat.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HmkidsUcozRuConstants:
    NAME = "hmkids.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://hmkids.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class StroyneemvmesteUcozRuConstants:
    NAME = "stroyneemvmeste.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://stroyneemvmeste.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AllmusUcozRuConstants:
    NAME = "allmus.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://allmus.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RotarusofiUcozRuConstants:
    NAME = "rotarusofi.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rotarusofi.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WebmediaUcozRuConstants:
    NAME = "webmedia.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://webmedia.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AnkordUcozRuConstants:
    NAME = "ankord.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ankord.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VideomuzonUcozRuConstants:
    NAME = "videomuzon.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://videomuzon.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DjfintUcozRuConstants:
    NAME = "djfint.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://djfint.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SerwisUcozRuConstants:
    NAME = "serwis.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://serwis.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AviaforumUcozRuConstants:
    NAME = "aviaforum.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://aviaforum.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TachographUcozRuConstants:
    NAME = "tachograph.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tachograph.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ScbUcozRuConstants:
    NAME = "scb.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://scb.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DeutschAuto68UcozRuConstants:
    NAME = "deutsch-auto68.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://deutsch-auto68.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KrumUcozRuConstants:
    NAME = "krum.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://krum.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PlaylistIptvUcozRuConstants:
    NAME = "playlist-iptv.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://playlist-iptv.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MamkiPapkiUcozRuConstants:
    NAME = "mamki-papki.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mamki-papki.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OskolfishingUcozRuConstants:
    NAME = "oskolfishing.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://oskolfishing.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TerralightUcozRuConstants:
    NAME = "terralight.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://terralight.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MyTucsonUcozRuConstants:
    NAME = "my-tucson.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://my-tucson.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MagicSquareUcozRuConstants:
    NAME = "magic-square.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://magic-square.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FreeProxyUcozRuConstants:
    NAME = "free-proxy.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://free-proxy.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Nokia6233UcozRuConstants:
    NAME = "nokia6233.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nokia6233.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PotystoronyUcozRuConstants:
    NAME = "potystorony.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://potystorony.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GoddamnUcozRuConstants:
    NAME = "goddamn.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://goddamn.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BabymamaUcozRuConstants:
    NAME = "babymama.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://babymama.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PoshtovikUcozRuConstants:
    NAME = "poshtovik.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://poshtovik.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AutocbUcozRuConstants:
    NAME = "autocb.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://autocb.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class So4ineniyaUcozRuConstants:
    NAME = "so4ineniya.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://so4ineniya.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TonetoUcozRuConstants:
    NAME = "toneto.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://toneto.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NicholassparksUcozRuConstants:
    NAME = "nicholassparks.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nicholassparks.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FatUcozRuConstants:
    NAME = "fat.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fat.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HolodilshchikUcozRuConstants:
    NAME = "holodilshchik.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://holodilshchik.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SladkiydesertUcozRuConstants:
    NAME = "sladkiydesert.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sladkiydesert.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CatinbootsUcozRuConstants:
    NAME = "catinboots.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://catinboots.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NicefriendcatsUcozRuConstants:
    NAME = "nicefriendcats.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nicefriendcats.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Dok17UcozRuConstants:
    NAME = "dok17.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dok17.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DcsoftUcozRuConstants:
    NAME = "dcsoft.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dcsoft.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CadaverzianUcozRuConstants:
    NAME = "cadaverzian.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cadaverzian.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class YrasUcozRuConstants:
    NAME = "yras.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://yras.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PioBetsUcozRuConstants:
    NAME = "pio-bets.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pio-bets.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ChelentanoUcozRuConstants:
    NAME = "chelentano.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://chelentano.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NuzarUcozRuConstants:
    NAME = "nuzar.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nuzar.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FaillyuboiUcozRuConstants:
    NAME = "faillyuboi.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://faillyuboi.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ClanSgUcozRuConstants:
    NAME = "clan-sg.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://clan-sg.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MytechbookUcozRuConstants:
    NAME = "mytechbook.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mytechbook.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DiablocoolUcozRuConstants:
    NAME = "diablocool.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://diablocool.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LakshmiFmUcozRuConstants:
    NAME = "lakshmi-fm.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lakshmi-fm.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SchoninUcozRuConstants:
    NAME = "schonin.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://schonin.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Memory57UcozRuConstants:
    NAME = "memory57.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://memory57.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KfirZahavUcozRuConstants:
    NAME = "kfir-zahav.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kfir-zahav.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DeathNoteUcozRuConstants:
    NAME = "death-note.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://death-note.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PirohimicUcozRuConstants:
    NAME = "pirohimic.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pirohimic.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SoftDenizUcozRuConstants:
    NAME = "soft-deniz.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://soft-deniz.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WarezPiratiUcozRuConstants:
    NAME = "warez-pirati.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://warez-pirati.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SatElectronicsUcozRuConstants:
    NAME = "sat-electronics.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sat-electronics.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ProSvetUcozRuConstants:
    NAME = "pro-svet.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pro-svet.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ChastyscUcozRuConstants:
    NAME = "chastysc.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://chastysc.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BaggiUcozRuConstants:
    NAME = "baggi.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://baggi.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BuyforexUcozRuConstants:
    NAME = "buyforex.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://buyforex.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LifewayUcozRuConstants:
    NAME = "lifeway.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lifeway.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TorrentsIgraUcozRuConstants:
    NAME = "torrents-igra.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://torrents-igra.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MomentsUcozRuConstants:
    NAME = "moments.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://moments.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class InetjobUcozRuConstants:
    NAME = "inetjob.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://inetjob.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Pogz5615UcozRuConstants:
    NAME = "pogz5615.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pogz5615.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DhelpUcozRuConstants:
    NAME = "dhelp.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dhelp.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FoxrecordUcozRuConstants:
    NAME = "foxrecord.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://foxrecord.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KonibodomUcozRuConstants:
    NAME = "konibodom.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://konibodom.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class UralSlobodaUcozRuConstants:
    NAME = "ural-sloboda.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ural-sloboda.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BbclubUcozRuConstants:
    NAME = "bbclub.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://bbclub.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SmartplayUcozRuConstants:
    NAME = "smartplay.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://smartplay.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class StrUpravlenieUcozRuConstants:
    NAME = "str-upravlenie.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://str-upravlenie.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N655iapUcozRuConstants:
    NAME = "655iap.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://655iap.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NkCsUcozRuConstants:
    NAME = "nk-cs.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nk-cs.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KuziniUcozRuConstants:
    NAME = "kuzini.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kuzini.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BashteploventUcozRuConstants:
    NAME = "bashteplovent.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://bashteplovent.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SvoimirykamiUcozRuConstants:
    NAME = "svoimirykami.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://svoimirykami.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CollegyUcozRuConstants:
    NAME = "collegy.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://collegy.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HackappUcozRuConstants:
    NAME = "hackapp.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://hackapp.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AnschulaUcozRuConstants:
    NAME = "anschula.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://anschula.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LnameUcozRuConstants:
    NAME = "lname.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lname.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ElPizzaUcozRuConstants:
    NAME = "el-pizza.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://el-pizza.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BereaUcozRuConstants:
    NAME = "berea.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://berea.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CosmoforumUcozRuConstants:
    NAME = "cosmoforum.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cosmoforum.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Zdorov10UcozRuConstants:
    NAME = "zdorov10.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zdorov10.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VgorahUcozRuConstants:
    NAME = "vgorah.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vgorah.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SibcoinsUcozRuConstants:
    NAME = "sibcoins.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sibcoins.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SnegovayaPadUcozRuConstants:
    NAME = "snegovaya-pad.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://snegovaya-pad.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CoffeeworldUcozRuConstants:
    NAME = "coffeeworld.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://coffeeworld.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HulyagankaUcozRuConstants:
    NAME = "hulyaganka.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://hulyaganka.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TaxiBelgorodUcozRuConstants:
    NAME = "taxi-belgorod.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://taxi-belgorod.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Dzhida2000UcozRuConstants:
    NAME = "dzhida2000.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dzhida2000.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IcookUcozRuConstants:
    NAME = "icook.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://icook.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AikidoMariupolUcozRuConstants:
    NAME = "aikido-mariupol.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://aikido-mariupol.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Rielt55UcozRuConstants:
    NAME = "rielt55.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rielt55.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CssNn52RusUcozRuConstants:
    NAME = "css-nn-52-rus.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://css-nn-52-rus.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NarutoRolegameUcozRuConstants:
    NAME = "naruto-rolegame.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://naruto-rolegame.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DoytruntUcozRuConstants:
    NAME = "doytrunt.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://doytrunt.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KraskiprazdnikaUcozRuConstants:
    NAME = "kraskiprazdnika.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kraskiprazdnika.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ActikomUcozRuConstants:
    NAME = "actikom.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://actikom.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MarymUcozRuConstants:
    NAME = "marym.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://marym.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AdminSoftUcozRuConstants:
    NAME = "admin-soft.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://admin-soft.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IcqTelefonUcozRuConstants:
    NAME = "icq-telefon.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://icq-telefon.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZvukinadezdyUcozRuConstants:
    NAME = "zvukinadezdy.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://zvukinadezdy.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Remont56UcozRuConstants:
    NAME = "remont56.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://remont56.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TrainzVlUcozRuConstants:
    NAME = "trainz-vl.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://trainz-vl.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MozgaNetUcozRuConstants:
    NAME = "mozga-net.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mozga-net.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SebastopolUcozRuConstants:
    NAME = "sebastopol.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sebastopol.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ComplineUcozRuConstants:
    NAME = "compline.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://compline.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FsModsRusUcozRuConstants:
    NAME = "fs-mods-rus.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fs-mods-rus.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N101vzvodUcozRuConstants:
    NAME = "101vzvod.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://101vzvod.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ScooterHelperUcozRuConstants:
    NAME = "scooter-helper.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://scooter-helper.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OpinionUcozRuConstants:
    NAME = "opinion.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://opinion.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SufficitUcozRuConstants:
    NAME = "sufficit.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sufficit.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MinnacUcozRuConstants:
    NAME = "minnac.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://minnac.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DrawingsBaseUcozRuConstants:
    NAME = "drawings-base.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://drawings-base.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GtaFanZoneUcozRuConstants:
    NAME = "gta-fan-zone.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gta-fan-zone.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Pik100UcozRuConstants:
    NAME = "pik100.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pik100.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class UrmaiUrmaevoUcozRuConstants:
    NAME = "urmai-urmaevo.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://urmai-urmaevo.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PluralsightConstants:
    NAME = "Pluralsight"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://app.pluralsight.com/profile/author/{username}"
    PRESENCE = ()
    ABSENCE = ('<title>Not available | Profile</title>', 'renderErrorPage(404)')
    GENERIC = set()

class FreelancerComConstants:
    NAME = "Freelancer.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D={username}&compact=true"
    PRESENCE = ()
    ABSENCE = ('"users":{}',)
    GENERIC = set()

class Top10allserversUcozRuConstants:
    NAME = "top10allservers.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://top10allservers.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CpuUcozRuConstants:
    NAME = "cpu.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cpu.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PopugiUcozRuConstants:
    NAME = "popugi.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://popugi.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DeathLegionUcozRuConstants:
    NAME = "death-legion.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://death-legion.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BeatlUcozRuConstants:
    NAME = "beatl.ucoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://beatl.ucoz.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ForumWordreferenceComConstants:
    NAME = "forum.wordreference.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.wordreference.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class SpartakMskRuConstants:
    NAME = "spartak.msk.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://spartak.msk.ru/guest/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class Vse1UcozComConstants:
    NAME = "vse1.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vse1.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VdvBelarusUcozComConstants:
    NAME = "vdv-belarus.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vdv-belarus.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TopcheatsUcozComConstants:
    NAME = "topcheats.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://topcheats.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ObkonUcozComConstants:
    NAME = "obkon.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://obkon.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PrenatalClubUcozComConstants:
    NAME = "prenatal-club.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://prenatal-club.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RealSpUcozComConstants:
    NAME = "real-sp.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://real-sp.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XorazmViloyatiUcozComConstants:
    NAME = "xorazm-viloyati.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xorazm-viloyati.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TatyanaArtUcozComConstants:
    NAME = "tatyana-art.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tatyana-art.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IgraOnlineUcozComConstants:
    NAME = "igra-online.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://igra-online.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KakvkontakteUcozComConstants:
    NAME = "kakvkontakte.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kakvkontakte.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IcuUcozComConstants:
    NAME = "icu.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://icu.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FirasmartincomeUcozComConstants:
    NAME = "firasmartincome.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://firasmartincome.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TopreklamaUcozComConstants:
    NAME = "topreklama.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://topreklama.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MoedeloUcozComConstants:
    NAME = "moedelo.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://moedelo.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WakeupUcozComConstants:
    NAME = "wakeup.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wakeup.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SharingSatUcozComConstants:
    NAME = "sharing-sat.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sharing-sat.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LesbeyankaUcozComConstants:
    NAME = "lesbeyanka.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lesbeyanka.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HalolUcozComConstants:
    NAME = "halol.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://halol.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N4x4TomskRuConstants:
    NAME = "4x4.tomsk.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://4x4.tomsk.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class GameMobiUcozComConstants:
    NAME = "game-mobi.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://game-mobi.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SenseUcozComConstants:
    NAME = "sense.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sense.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WmUcozComConstants:
    NAME = "wm.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wm.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OstaUcozComConstants:
    NAME = "osta.ucoz.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://osta.ucoz.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AnimeNewsNetworkConstants:
    NAME = "AnimeNewsNetwork"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.animenewsnetwork.com/bbs/phpBB2/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Could not find expected value in database',)
    GENERIC = set()

class CcmixterConstants:
    NAME = "Ccmixter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ccmixter.org/people/{username}/profile"
    PRESENCE = ('Member since',)
    ABSENCE = ('ERROR(2)', "Sorry, we don't know who that is...")
    GENERIC = set()

class LitgeroyUcozNetConstants:
    NAME = "litgeroy.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://litgeroy.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MistralUcozNetConstants:
    NAME = "mistral.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mistral.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AntihackUcozNetConstants:
    NAME = "antihack.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://antihack.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MedknigaUcozNetConstants:
    NAME = "medkniga.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://medkniga.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RapbeatUcozNetConstants:
    NAME = "rapbeat.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rapbeat.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AbcAccountingUcozNetConstants:
    NAME = "abc-accounting.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://abc-accounting.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RabotenkaUcozNetConstants:
    NAME = "rabotenka.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rabotenka.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N0kClanSuConstants:
    NAME = "0k.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://0k.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VegaUcozNetConstants:
    NAME = "vega.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vega.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IptvFreeUcozNetConstants:
    NAME = "iptv-free.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://iptv-free.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VipIcqUcozNetConstants:
    NAME = "vip-icq.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vip-icq.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XitlarUcozNetConstants:
    NAME = "xitlar.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xitlar.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ClubComedyClanSuConstants:
    NAME = "Club-comedy.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://club-comedy.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TraysUcozNetConstants:
    NAME = "trays.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://trays.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NarutoFanUcozNetConstants:
    NAME = "naruto-fan.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://naruto-fan.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ShporgalkiUcozNetConstants:
    NAME = "shporgalki.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://shporgalki.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N5levelUcozNetConstants:
    NAME = "5level.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://5level.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AzhackUcozNetConstants:
    NAME = "azhack.ucoz.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://azhack.ucoz.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ForumsMajorgeeksComConstants:
    NAME = "forums.majorgeeks.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.majorgeeks.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class FireTeamClanSuConstants:
    NAME = "fire-team.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fire-team.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class L2BestClanSuConstants:
    NAME = "l2-best.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://l2-best.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IlanClanSuConstants:
    NAME = "ilan.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ilan.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Mariupol4x4ClanSuConstants:
    NAME = "mariupol4x4.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mariupol4x4.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ShkolnikovClanSuConstants:
    NAME = "shkolnikov.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://shkolnikov.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Warcraft3ftClanSuConstants:
    NAME = "warcraft3ft.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://warcraft3ft.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AppClanSuConstants:
    NAME = "app.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://app.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GrigorovoClanSuConstants:
    NAME = "grigorovo.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://grigorovo.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NecromancersClanSuConstants:
    NAME = "necromancers.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://necromancers.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KomarovoClanSuConstants:
    NAME = "komarovo.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://komarovo.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KinoHitClanSuConstants:
    NAME = "kino-hit.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kino-hit.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GsmStandartClanSuConstants:
    NAME = "gsm-standart.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gsm-standart.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FareastClanSuConstants:
    NAME = "fareast.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fareast.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CybersClanSuConstants:
    NAME = "cybers.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cybers.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TvigraClanSuConstants:
    NAME = "tvigra.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tvigra.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ObmanunetClanSuConstants:
    NAME = "obmanunet.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://obmanunet.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Rt20GetbbRuConstants:
    NAME = "rt20.getbb.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rt20.getbb.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class Rt21GetbbRuConstants:
    NAME = "rt21.getbb.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rt21.getbb.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ManualsClanSuConstants:
    NAME = "manuals.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://manuals.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LnkBioConstants:
    NAME = "lnk.bio"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lnk.bio/{username}"
    PRESENCE = ('data-username',)
    ABSENCE = ('Not Found - Lnk.Bio',)
    GENERIC = set()

class JaparaClanSuConstants:
    NAME = "japara.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://japara.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Symbian9ClanSuConstants:
    NAME = "symbian9.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://symbian9.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LoveMagicClanSuConstants:
    NAME = "love-magic.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://love-magic.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VipCccpClanSuConstants:
    NAME = "vip-cccp.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vip-cccp.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Music2djClanSuConstants:
    NAME = "music2dj.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://music2dj.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MargaritasClanSuConstants:
    NAME = "margaritas.clan.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://margaritas.clan.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AmericanthinkerConstants:
    NAME = "Americanthinker"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.americanthinker.com/author/{username}/"
    PRESENCE = ('Articles:',)
    ABSENCE = ('<title>American Thinker</title>',)
    GENERIC = set()

class Socforum3dnRuConstants:
    NAME = "socforum.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://socforum.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Ekzoticsad3dnRuConstants:
    NAME = "ekzoticsad.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ekzoticsad.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Av3dnRuConstants:
    NAME = "av.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://av.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Jog3dnRuConstants:
    NAME = "jog.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://jog.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Salavat3dnRuConstants:
    NAME = "salavat.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://salavat.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SoftWm3dnRuConstants:
    NAME = "soft-wm.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://soft-wm.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Warframe3dnRuConstants:
    NAME = "warframe.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://warframe.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TeamPros3dnRuConstants:
    NAME = "team-pros.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://team-pros.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Websecurity3dnRuConstants:
    NAME = "websecurity.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://websecurity.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Mytrans3dnRuConstants:
    NAME = "mytrans.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mytrans.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Vracing3dnRuConstants:
    NAME = "vracing.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vracing.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Sherwood3dnRuConstants:
    NAME = "sherwood.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sherwood.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ChristianVideo3dnRuConstants:
    NAME = "christian-video.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://christian-video.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Haogan3dnRuConstants:
    NAME = "haogan.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://haogan.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Muzika3dnRuConstants:
    NAME = "muzika.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://muzika.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GolasaVkFree3dnRuConstants:
    NAME = "golasa-vk-free.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://golasa-vk-free.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N4401013dnRuConstants:
    NAME = "440101.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://440101.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OnlineMovies3dnRuConstants:
    NAME = "online-movies.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://online-movies.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Sayty3dnRuConstants:
    NAME = "sayty.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sayty.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Lock3dnRuConstants:
    NAME = "lock.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://lock.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Vch34693dnRuConstants:
    NAME = "vch3469.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vch3469.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GtGarazh3dnRuConstants:
    NAME = "gt-garazh.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gt-garazh.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DvkStyle3dnRuConstants:
    NAME = "dvk-style.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dvk-style.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Partner3dnRuConstants:
    NAME = "partner.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://partner.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Metroman3dnRuConstants:
    NAME = "metroman.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://metroman.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Sony1273dnRuConstants:
    NAME = "sony127.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sony127.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Karkulis3dnRuConstants:
    NAME = "karkulis.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://karkulis.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Ibmt3dnRuConstants:
    NAME = "ibmt.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ibmt.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N9interi3dnRuConstants:
    NAME = "9interi.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://9interi.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Webdom3dnRuConstants:
    NAME = "webdom.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://webdom.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Binhot3dnRuConstants:
    NAME = "binhot.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://binhot.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RazborkaJapan3dnRuConstants:
    NAME = "razborka-japan.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://razborka-japan.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Nicemusic3dnRuConstants:
    NAME = "nicemusic.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nicemusic.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Jump3dnRuConstants:
    NAME = "jump.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://jump.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Prosmart3dnRuConstants:
    NAME = "prosmart.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://prosmart.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Grodnofish3dnRuConstants:
    NAME = "grodnofish.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://grodnofish.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Tgi3dnRuConstants:
    NAME = "tgi.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tgi.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FocusPocus3dnRuConstants:
    NAME = "focus-pocus.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://focus-pocus.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Ourfunnypets3dnRuConstants:
    NAME = "ourfunnypets.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ourfunnypets.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PortalCs163dnRuConstants:
    NAME = "portal-cs-1-6.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://portal-cs-1-6.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ResourceMta3dnRuConstants:
    NAME = "resource-mta.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://resource-mta.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Viupetra3dnRuConstants:
    NAME = "viupetra.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://viupetra.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WmmailWmmail3dnRuConstants:
    NAME = "wmmail-wmmail.3dn.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wmmail-wmmail.3dn.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MoviMy1RuConstants:
    NAME = "movi.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://movi.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LizaMy1RuConstants:
    NAME = "liza.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://liza.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LetitbitFilmMy1RuConstants:
    NAME = "letitbit-film.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://letitbit-film.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MorozovkaMy1RuConstants:
    NAME = "morozovka.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://morozovka.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LiderdzrMy1RuConstants:
    NAME = "liderdzr.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://liderdzr.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MusicOneMy1RuConstants:
    NAME = "music-one.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://music-one.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KotikMy1RuConstants:
    NAME = "kotik.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kotik.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NovomoskovskMy1RuConstants:
    NAME = "novomoskovsk.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://novomoskovsk.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CrossfaernetMy1RuConstants:
    NAME = "crossfaernet.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://crossfaernet.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VidehelpCompMy1RuConstants:
    NAME = "videhelp-comp.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://videhelp-comp.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TsibulskiyMy1RuConstants:
    NAME = "tsibulskiy.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tsibulskiy.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TheatreMy1RuConstants:
    NAME = "theatre.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://theatre.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WworkMy1RuConstants:
    NAME = "wwork.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wwork.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ArtNataMy1RuConstants:
    NAME = "art-nata.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://art-nata.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FlyMy1RuConstants:
    NAME = "fly.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fly.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AnimelendMy1RuConstants:
    NAME = "animelend.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://animelend.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class VsemobileMy1RuConstants:
    NAME = "vsemobile.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://vsemobile.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ArtColorMy1RuConstants:
    NAME = "art-color.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://art-color.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZareshetkoiMy1RuConstants:
    NAME = "zareshetkoi.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zareshetkoi.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HistroomMy1RuConstants:
    NAME = "histroom.my1.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://histroom.my1.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XenforoComConstants:
    NAME = "xenforo.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://xenforo.com/community/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class N783DoAmConstants:
    NAME = "78-3.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://78-3.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AsecurityDoAmConstants:
    NAME = "asecurity.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://asecurity.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DremelDoAmConstants:
    NAME = "dremel.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dremel.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ForexTraderDoAmConstants:
    NAME = "forex-trader.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forex-trader.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class YerkramasDoAmConstants:
    NAME = "yerkramas.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://yerkramas.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KapustaDoAmConstants:
    NAME = "kapusta.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kapusta.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RussemyaDoAmConstants:
    NAME = "russemya.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://russemya.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MarchenkovDoAmConstants:
    NAME = "marchenkov.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://marchenkov.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FstKolosDoAmConstants:
    NAME = "fst-kolos.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fst-kolos.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TomDoAmConstants:
    NAME = "tom.do.am"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tom.do.am/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AndreiMoySuConstants:
    NAME = "andrei.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://andrei.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AtmClubMoySuConstants:
    NAME = "atm-club.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://atm-club.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AntivirusMoySuConstants:
    NAME = "antivirus.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://antivirus.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZidMoySuConstants:
    NAME = "zid.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zid.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class InfoppsMoySuConstants:
    NAME = "infopps.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://infopps.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MoskoviaMoySuConstants:
    NAME = "moskovia.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://moskovia.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IcqBotMoySuConstants:
    NAME = "icq-bot.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://icq-bot.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ProdigyMoySuConstants:
    NAME = "prodigy.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://prodigy.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SemenovaKlassMoySuConstants:
    NAME = "semenova-klass.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://semenova-klass.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N96MoySuConstants:
    NAME = "96.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://96.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DushschoolMoySuConstants:
    NAME = "dushschool.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dushschool.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GadjetMoySuConstants:
    NAME = "gadjet.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gadjet.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class School1065MoySuConstants:
    NAME = "school1065.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://school1065.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AnimeGrandMoySuConstants:
    NAME = "anime-grand.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://anime-grand.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XyuivetMailcpyMoySuConstants:
    NAME = "xyuivet-mailcpy.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xyuivet-mailcpy.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FutajistStudioMoySuConstants:
    NAME = "futajist-studio.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://futajist-studio.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DubrovoMoySuConstants:
    NAME = "dubrovo.moy.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dubrovo.moy.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KillerUcozUaConstants:
    NAME = "killer.ucoz.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://killer.ucoz.ua/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class StaroverovkaUcozUaConstants:
    NAME = "staroverovka.ucoz.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://staroverovka.ucoz.ua/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GribnikikybaniConstants:
    NAME = "Gribnikikybani"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gribnikikybani.mybb.ru/search.php?action=search&keywords=&author={username}"
    PRESENCE = ()
    ABSENCE = ('По вашему запросу ничего не найдено.',)
    GENERIC = set()

class SimfMamaUcozUaConstants:
    NAME = "simf-mama.ucoz.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://simf-mama.ucoz.ua/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PmpkbirskUcozOrgConstants:
    NAME = "pmpkbirsk.ucoz.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://pmpkbirsk.ucoz.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CsRuUcozOrgConstants:
    NAME = "cs-ru.ucoz.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cs-ru.ucoz.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class W2lGUcozOrgConstants:
    NAME = "w2l-g.ucoz.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://w2l-g.ucoz.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RuslangxpUcozOrgConstants:
    NAME = "ruslangxp.ucoz.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ruslangxp.ucoz.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()


class HuntingKareliaRuConstants:
    NAME = "hunting.karelia.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://hunting.karelia.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ManifoldMarketsConstants:
    NAME = "ManifoldMarkets"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://manifold.markets/{username}"
    PRESENCE = ('>Comments</div>', '>Balance log</div>', '>Payments</div>', '@<!-- -->{username}<!-- --> </span>')
    ABSENCE = ('404: Oops!', 'Less than 1% chance anything exists at this url.')
    GENERIC = set()

class ValinorComBrConstants:
    NAME = "valinor.com.br"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.valinor.com.br/forum/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class PartnerkinComConstants:
    NAME = "partnerkin.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://partnerkin.com/user/{username}"
    PRESENCE = ('<title>Профиль',)
    ABSENCE = ('<title></title>',)
    GENERIC = set()

class ForumIgnitioncasinoEuConstants:
    NAME = "forum.ignitioncasino.eu"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.ignitioncasino.eu/u/{username}/summary"
    PRESENCE = ('<meta name="generator" content="Discourse',)
    ABSENCE = ('Oops! That page doesn’t exist or is private.', 'wrap not-found-container')
    GENERIC = set()

class OperConstants:
    NAME = "Oper"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.oper.ru/visitors/info.php?t={username}"
    PRESENCE = ()
    ABSENCE = ('Нет такого пользователя',)
    GENERIC = set()

class ForumsIndiegalaComConstants:
    NAME = "forums.indiegala.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.indiegala.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class GcupRuConstants:
    NAME = "gcup.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gcup.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AniWorldConstants:
    NAME = "Ani World"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://aniworld.to/user/profil/{username}"
    PRESENCE = ()
    ABSENCE = ('Dieses Profil ist nicht verfügbar',)
    GENERIC = set()

class BoardPhpbuilderComConstants:
    NAME = "board.phpbuilder.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://board.phpbuilder.com/u/{username}"
    PRESENCE = ('"attributes":{"username"',)
    ABSENCE = ('NotFound',)
    GENERIC = set()

class PromptBaseConstants:
    NAME = "PromptBase"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://promptbase.com/profile/{username}"
    PRESENCE = ('1',)
    ABSENCE = ('NotFound',)
    GENERIC = set()

class ForumWebRuConstants:
    NAME = "forum.web.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.web.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class PodolskConstants:
    NAME = "podolsk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.podolsk.ru/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class MyjaneConstants:
    NAME = "Myjane"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.myjane.ru/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('<title> - Женские форумы myJane</title>',)
    GENERIC = set()

class TksConstants:
    NAME = "tks"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.tks.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class MedikforumConstants:
    NAME = "Medikforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.medikforum.ru/forum/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumRznInfoConstants:
    NAME = "forum.rzn.info"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.rzn.info/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class AWSSkillsProfileConstants:
    NAME = "AWS Skills Profile"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://skillsprofile.skillbuilder.aws/user/{username}/"
    PRESENCE = ()
    ABSENCE = ('shareProfileAccepted":false',)
    GENERIC = set()

class ForumEndeavourosComConstants:
    NAME = "forum.endeavouros.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.endeavouros.com/u/{username}/summary"
    PRESENCE = ('<meta name="generator" content="Discourse',)
    ABSENCE = ('Oops! That page doesn’t exist or is private.', 'wrap not-found-container')
    GENERIC = set()

class SaMpUcozDeConstants:
    NAME = "sa-mp.ucoz.de"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sa-mp.ucoz.de/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AreKamrbbConstants:
    NAME = "AreKamrbb"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://are.kamrbb.ru/?x=find&f={username}#top"
    PRESENCE = ()
    ABSENCE = ('К сожалению, мы ничего не нашли для вас..',)
    GENERIC = set()

class HyundaitruckclubConstants:
    NAME = "Hyundaitruckclub"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hyundaitruckclub.kamrbb.ru/?x=find&f={username}&type=topics&nick=on#top"
    PRESENCE = ()
    ABSENCE = ('К сожалению, мы ничего не нашли для вас',)
    GENERIC = set()

class VitalFootballConstants:
    NAME = "VitalFootball"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.vitalfootball.co.uk/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class Dota2Constants:
    NAME = "Dota2"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://dota2.ru/forum/search?type=user&keywords={username}&sort_by=username"
    PRESENCE = ()
    ABSENCE = ('Результаты отсутствуют', 'Поиск временно отключен', '<h2>Поиск временно отключен</h2>')
    GENERIC = set()

class IntigritiConstants:
    NAME = "Intigriti"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://app.intigriti.com/profile/{username}"
    PRESENCE = ('avatar-container',)
    ABSENCE = ("We didn't find what you're looking for",)
    GENERIC = set()

class HotcopperConstants:
    NAME = "Hotcopper"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hotcopper.com.au/search/search?type=post&users={username}"
    PRESENCE = ('title-td', 'title is-1', 'pagination ', 'toggle', 'active ')
    ABSENCE = ('error-page', 'error-page home container', 'card-footer-item', '><main id=', 'card-content')
    GENERIC = set()

class PicartoConstants:
    NAME = "Picarto"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ptvintern.picarto.tv/metadescription/{username}"
    PRESENCE = ('"success":true',)
    ABSENCE = ('We are the world\\u2019s leading live streaming platform for creative minds. Come join us',)
    GENERIC = set()

class DpilsScooterUcozLvConstants:
    NAME = "dpils-scooter.ucoz.lv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dpils-scooter.ucoz.lv/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SokalUcozLvConstants:
    NAME = "sokal.ucoz.lv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sokal.ucoz.lv/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FootballConstants:
    NAME = "Football"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.rusfootball.info/user/{username}/"
    PRESENCE = ('class="userprofile"',)
    ABSENCE = ()
    GENERIC = set()

class ArtinvestmentConstants:
    NAME = "artinvestment"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.artinvestment.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class TheAnswerBankConstants:
    NAME = "The AnswerBank"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.theanswerbank.co.uk/members/{username}"
    PRESENCE = ()
    ABSENCE = ('Welcome to the AnswerBank',)
    GENERIC = set()

class RadiokotConstants:
    NAME = "Radiokot"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.radiokot.ru/forum/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumOdUaConstants:
    NAME = "ForumOdUa"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forumodua.com/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class SibmamaConstants:
    NAME = "sibmama"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.sibmama.ru/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Извините',)
    GENERIC = set()

class KosmetistaConstants:
    NAME = "Kosmetista"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kosmetista.ru/profile/{username}/"
    PRESENCE = ('profile-content',)
    ABSENCE = ('Упс! Вот это поворот!',)
    GENERIC = set()

class JuceConstants:
    NAME = "juce"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.juce.com/u/{username}/summary"
    PRESENCE = ('<meta name="generator" content="Discourse',)
    ABSENCE = ('Oops! That page doesn’t exist or is private.', 'wrap not-found-container')
    GENERIC = set()

class StrategeConstants:
    NAME = "Stratege"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.stratege.ru/forums/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class ForumsBluemoonMcfcConstants:
    NAME = "Forums-bluemoon-mcfc"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.bluemoon-mcfc.co.uk/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class GotovimDomaConstants:
    NAME = "GotovimDoma"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gotovim-doma.ru/forum/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('<title> Информация</title>', 'Подходящих тем или сообщений не найдено.')
    GENERIC = set()

class Ww2aircraftNetConstants:
    NAME = "ww2aircraft.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ww2aircraft.net/forum/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class LoveplanetConstants:
    NAME = "Loveplanet"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://loveplanet.ru/page/{username}"
    PRESENCE = ()
    ABSENCE = ('Запрошенная вами страница не найдена.', 'Данные о выбранном пользователе не существуют', 'Information on selected user does not exist')
    GENERIC = set()

class MotorkaConstants:
    NAME = "Motorka"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.motorka.org/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class HpcConstants:
    NAME = "Hpc"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hpc.ru/board/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumsImmigrationComConstants:
    NAME = "forums.immigration.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.immigration.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class TvUcozClubConstants:
    NAME = "tv.ucoz.club"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tv.ucoz.club/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class JustmjRuConstants:
    NAME = "justmj.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://justmj.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SavingadviceComConstants:
    NAME = "savingadvice.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://savingadvice.com/author/{username}/"
    PRESENCE = ('author-', 'author/')
    ABSENCE = ('error404',)
    GENERIC = set()

class SorentoKiaClubRuConstants:
    NAME = "sorento.kia-club.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sorento.kia-club.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumNvworldRuConstants:
    NAME = "forum.nvworld.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.nvworld.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class AnimeUKNewsConstants:
    NAME = "AnimeUKNews"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forums.animeuknews.net/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class HudsonRockConstants:
    NAME = "Hudson Rock"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={username}"
    PRESENCE = ()
    ABSENCE = ('This username is not associated',)
    GENERIC = set()

class DrupalRuConstants:
    NAME = "drupal.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://drupal.ru/username/{username}"
    PRESENCE = ('<ul class="tabs--primary">',)
    ABSENCE = ('Страница не найдена - 404',)
    GENERIC = set()

class QuestionableQuestingConstants:
    NAME = "QuestionableQuesting"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.questionablequesting.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class WowGameRuConstants:
    NAME = "wow-game.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wow-game.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CodebyNetConstants:
    NAME = "Codeby.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://codeby.net/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class SoylentNewsConstants:
    NAME = "SoylentNews"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://soylentnews.org/~{username}"
    PRESENCE = ('class="data_head"',)
    ABSENCE = ('The user you requested does not exist, no matter how much you wish this might be the case.',)
    GENERIC = set()

class ForumKaosxUsConstants:
    NAME = "forum.kaosx.us"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.kaosx.us/u/{username}"
    PRESENCE = ('"attributes":{"username"',)
    ABSENCE = ('NotFound',)
    GENERIC = set()

class AutoladaConstants:
    NAME = "Autolada"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.autolada.ru/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ('postdetails',)
    ABSENCE = ('<title> :: AUTOLADA.RU',)
    GENERIC = set()

class UchportalConstants:
    NAME = "Uchportal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.uchportal.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TamTamConstants:
    NAME = "TamTam"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tamtam.chat/{username}"
    PRESENCE = ('data-tsid="avatar"',)
    ABSENCE = ('Pv3WuoqzAb05NxqHCgZ29Z2jmQ',)
    GENERIC = set()

class YkaKzConstants:
    NAME = "yka.kz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://yka.kz/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RezzoclubRuConstants:
    NAME = "rezzoclub.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://rezzoclub.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SocioforumSuConstants:
    NAME = "socioforum.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.socioforum.su/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class MaidenFansConstants:
    NAME = "MaidenFans"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.maidenfans.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class TurPravdaConstants:
    NAME = "TurPravda"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.turpravda.com/profile/{username}"
    PRESENCE = ('email', ' name')
    ABSENCE = ('Title', ' Shortcut Icon', ' submit')
    GENERIC = set()

class IssueHuntConstants:
    NAME = "IssueHunt"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://issuehunt.io/u/{username}"
    PRESENCE = ()
    ABSENCE = ('The user does not exist.',)
    GENERIC = set()

class RuanekdotRuConstants:
    NAME = "ruanekdot.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ruanekdot.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Pajero4x4RuConstants:
    NAME = "pajero4x4.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.pajero4x4.ru/bbs/phpBB2/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class AppAirnftsComConstants:
    NAME = "app.airnfts.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://app.airnfts.com/creators/{username}"
    PRESENCE = ('username', 'ownerUsername', 'creatorUsername', 'name', 'user')
    ABSENCE = ('user-not-found-div',)
    GENERIC = set()

class RusarmyConstants:
    NAME = "Rusarmy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rusarmy.com/forum/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Указанный пользователь не найден. Пожалуйста, введите другое имя.',)
    GENERIC = set()

class WOWCircleConstants:
    NAME = "WOW Circle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.wowcircle.net/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class ForumCOKComUaConstants:
    NAME = "forum.c-o-k.com.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.c-o-k.com.ua/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ProkoniConstants:
    NAME = "Prokoni"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.prokoni.ru/forum/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Указанный пользователь не найден',)
    GENERIC = set()

class PhorumArmavirRuConstants:
    NAME = "phorum.armavir.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://phorum.armavir.ru/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class WebosForumsRuConstants:
    NAME = "webos-forums.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://webos-forums.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class RecPokerConstants:
    NAME = "rec.poker"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://rec.poker/author/{username}/"
    PRESENCE = ('author-', 'author/')
    ABSENCE = ('error404',)
    GENERIC = set()

class StatusCafeConstants:
    NAME = "Status Cafe"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://status.cafe/users/{username}"
    PRESENCE = ()
    ABSENCE = ('Page Not Found',)
    GENERIC = set()

class MaccentreConstants:
    NAME = "Maccentre"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://maccentre.ru/board/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Извините, такого пользователя не существует',)
    GENERIC = set()

class RUDTPConstants:
    NAME = "RUDTP"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.rudtp.ru/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class CaduserConstants:
    NAME = "Caduser"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.caduser.ru/forum/userlist.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('По вашему запросу ничего не найдено.',)
    GENERIC = set()

class SamesoundRuConstants:
    NAME = "samesound.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://samesound.ru/author/{username}/"
    PRESENCE = ('author-', 'author/')
    ABSENCE = ('error404',)
    GENERIC = set()

class FishingsibConstants:
    NAME = "Fishingsib"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.fishingsib.ru/forum/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Указанный пользователь не найден',)
    GENERIC = set()

class W3challsConstants:
    NAME = "W3challs"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://w3challs.com/profile/{username}"
    PRESENCE = ()
    ABSENCE = ('<title>404 Page not found – W3Challs Hacking Challenges</title>',)
    GENERIC = set()


class NhlConstants:
    NAME = "Nhl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nhl.ru/talks/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Извините, такого пользователя не существует',)
    GENERIC = set()

class PobedishRuConstants:
    NAME = "pobedish.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pobedish.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class VezhaConstants:
    NAME = "Vezha"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vezha.com/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован',)
    GENERIC = set()

class DioramaRuConstants:
    NAME = "diorama.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://diorama.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class BayoushooterConstants:
    NAME = "Bayoushooter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.bayoushooter.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class ForumTradePrintRuConstants:
    NAME = "forum.trade-print.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.trade-print.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class ForumMilRuConstants:
    NAME = "forum-mil.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum-mil.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TrworkshopNetConstants:
    NAME = "trworkshop.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.trworkshop.net/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class NygunforumConstants:
    NAME = "Nygunforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nygunforum.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class AnimebaseConstants:
    NAME = "Animebase"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://animebase.me/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class N3dcadforumsConstants:
    NAME = "3dcadforums"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.3dcadforums.com/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('The specified member cannot be found',)
    GENERIC = set()

class AbackConstants:
    NAME = "Aback"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://aback.com.ua/user/{username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь с таким именем не найден.',)
    GENERIC = set()

class AngelgothicsConstants:
    NAME = "Angelgothics"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://angelgothics.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BandlabConstants:
    NAME = "Bandlab"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.bandlab.com/api/v1.3/users/{username}"
    PRESENCE = ('genres',)
    ABSENCE = ('find any matching element, it might be deleted',)
    GENERIC = set()

class BelmosConstants:
    NAME = "Belmos"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.belmos.ru/forum/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class BbshaveConstants:
    NAME = "Bbshave"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://bbshave.ru/profile/{username}"
    PRESENCE = ()
    ABSENCE = ('Пользователя не существует.',)
    GENERIC = set()

class BlogiPlConstants:
    NAME = "Blogi.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.blogi.pl/osoba,{username}.html"
    PRESENCE = ('Informacje ogólne',)
    ABSENCE = ('Niepoprawny adres.',)
    GENERIC = set()

class ArtpersonaConstants:
    NAME = "Artpersona"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://artpersona.org/cb/userprofile/{username}"
    PRESENCE = ()
    ABSENCE = ('Этот профиль либо больше не существует, либо больше не доступен.',)
    GENERIC = set()

class ChomikujPlConstants:
    NAME = "Chomikuj.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://chomikuj.pl/{username}/"
    PRESENCE = ('Foldery',)
    ABSENCE = ('homik o takiej nazwie nie istnieje',)
    GENERIC = set()

class BookandreaderConstants:
    NAME = "Bookandreader"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.bookandreader.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class ChemistlabConstants:
    NAME = "Chemistlab"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://chemistlab.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Cmet4ukConstants:
    NAME = "Cmet4uk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cmet4uk.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DobroeslovoConstants:
    NAME = "Dobroeslovo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.dobroeslovo.ru/memberlist.php?username={username}"
    PRESENCE = ('You must be logged in to do that.', './memberlist.php?mode=viewprofile')
    ABSENCE = ('No members found for this search criterion.', 'Не найдено ни одного пользователя по заданным критериям')
    GENERIC = set()

class CPlusPlusConstants:
    NAME = "CPlusPlus"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.cplusplus.com/user/{username}/"
    PRESENCE = ()
    ABSENCE = ('404 Page Not Found',)
    GENERIC = set()

class DemotywatoryConstants:
    NAME = "Demotywatory"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://demotywatory.pl/user/{username}"
    PRESENCE = ('Z nami od:',)
    ABSENCE = ('Użytkownik o podanym pseudonimie nie istnieje.',)
    GENERIC = set()

class CssomskConstants:
    NAME = "Cssomsk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.cssomsk.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EzoterikaConversionConstants:
    NAME = "EzoterikaConversion"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ezoterikaconversion.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FicwriterConstants:
    NAME = "Ficwriter"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ficwriter.info/polzovateli/userprofile/{username}.html"
    PRESENCE = ()
    ABSENCE = ('\ufeffЭтот профиль либо больше не существует или не доступен.',)
    GENERIC = set()

class ForumEvavedaConstants:
    NAME = "ForumEvaveda"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.evaveda.com/memberlist.php?username={username}"
    PRESENCE = ('You must be logged in to do that.', './memberlist.php?mode=viewprofile')
    ABSENCE = ('No members found for this search criterion.', 'Не найдено ни одного пользователя по заданным критериям')
    GENERIC = set()

class D3RuConstants:
    NAME = "d3.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://d3.ru/user/{username}/posts"
    PRESENCE = ('/user/',)
    ABSENCE = ('d3.ru — Ничего не найдено!',)
    GENERIC = set()

class ForumYuristovConstants:
    NAME = "ForumYuristov"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forumyuristov.ru/members/?username={username}"
    PRESENCE = ()
    ABSENCE = ('Указанный пользователь не найден',)
    GENERIC = set()

class GNewsConstants:
    NAME = "G-news"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://g-news.com.ua/forum_smf/profile/{username}/"
    PRESENCE = ()
    ABSENCE = ('Пользователя не существует.',)
    GENERIC = set()

class GlbyhConstants:
    NAME = "Glbyh"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://glbyh.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class GradleConstants:
    NAME = "Gradle"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://plugins.gradle.org/u/{username}"
    PRESENCE = ('Joined on',)
    ABSENCE = ('User not found',)
    GENERIC = set()

class Citizen4Constants:
    NAME = "Citizen4"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://soc.citizen4.eu/profile/{username}/profile"
    PRESENCE = ('@soc.citizen4.eu',)
    ABSENCE = ('Nie znaleziono',)
    GENERIC = set()

class GulfcoastgunforumConstants:
    NAME = "Gulfcoastgunforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://gulfcoastgunforum.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class JuventuzConstants:
    NAME = "Juventuz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.juventuz.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class KristallovNetConstants:
    NAME = "KristallovNet"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.kristallov.net/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class KinoTvConstants:
    NAME = "Kino-tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.kino-tv-forum.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MdregionConstants:
    NAME = "Mdregion"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mdregion.ru/forum/memberlist.php?username={username}"
    PRESENCE = ('You must be logged in to do that.', './memberlist.php?mode=viewprofile')
    ABSENCE = ('No members found for this search criterion.', 'Не найдено ни одного пользователя по заданным критериям')
    GENERIC = set()

class PiratebuhtaConstants:
    NAME = "Piratebuhta"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://piratebuhta.club/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class OurDJTalkConstants:
    NAME = "OurDJTalk"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ourdjtalk.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class P38forumConstants:
    NAME = "P38forum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://p38forum.com/forums/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class PolleverywhereConstants:
    NAME = "Polleverywhere"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://pollev.com/proxy/api/users/{username}"
    PRESENCE = ('name',)
    ABSENCE = ('ResourceNotFound',)
    GENERIC = set()

class PrvPlConstants:
    NAME = "Prv.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.prv.pl/osoba/{username}"
    PRESENCE = ('LOGIN',)
    ABSENCE = ('Użytkownik nie istnieje.',)
    GENERIC = set()

class RammclanConstants:
    NAME = "Rammclan"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rammclan.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RngfConstants:
    NAME = "Rngf"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rngf.ru/profile.php?mode=viewprofile&u={username}"
    PRESENCE = ()
    ABSENCE = ('Извините, такого пользователя не существует',)
    GENERIC = set()

class RasslabyxaConstants:
    NAME = "Rasslabyxa"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.rasslabyxa.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ReincarnationforumConstants:
    NAME = "Reincarnationforum"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://reincarnationforum.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class ScoutwikiConstants:
    NAME = "Scoutwiki"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://en.scoutwiki.org/User:{username}"
    PRESENCE = ('NewPP limit report',)
    ABSENCE = ('is not registered',)
    GENERIC = set()


class TanukiPlConstants:
    NAME = "Tanuki.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://tanuki.pl/profil/{username}"
    PRESENCE = ('Dołączył',)
    ABSENCE = ('Nie ma takiego użytkownika',)
    GENERIC = set()

class TetrIoConstants:
    NAME = "Tetr.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ch.tetr.io/api/users/{username}"
    PRESENCE = ('success":true',)
    ABSENCE = ('No such user!',)
    GENERIC = set()

class TunefindConstants:
    NAME = "Tunefind"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.tunefind.com/user/profile/{username}"
    PRESENCE = ('Achievements',)
    ABSENCE = ('Page not found',)
    GENERIC = set()


class VineConstants:
    NAME = "Vine"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vine.co/api/users/profiles/vanity/{username}"
    PRESENCE = ('userId',)
    ABSENCE = ('That record does not exist',)
    GENERIC = set()

class WimkinPublicProfileConstants:
    NAME = "WimkinPublicProfile"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wimkin.com/{username}"
    PRESENCE = ('is on WIMKIN',)
    ABSENCE = (' The page you are looking for cannot be found.',)
    GENERIC = set()

class YaUchitelConstants:
    NAME = "Ya-uchitel"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://ya-uchitel.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WordpressSupportConstants:
    NAME = "WordpressSupport"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://wordpress.org/support/users/{username}/"
    PRESENCE = ('s Profile &#124; WordPress.org',)
    ABSENCE = ('User not found',)
    GENERIC = set()

class ZenitbolConstants:
    NAME = "Zenitbol"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zenitbol.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RadioUchebnikConstants:
    NAME = "Radio-uchebnik"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://radio-uchebnik.ru/forum/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class AnalitikaForexRuConstants:
    NAME = "analitika-forex.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://analitika-forex.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CsStrikezOrgConstants:
    NAME = "cs-strikez.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cs-strikez.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EasyenConstants:
    NAME = "easyen"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://easyen.ru/index/8-0-{username}"
    PRESENCE = ('prof_12w_pr', 'udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DieselmasteraRuConstants:
    NAME = "dieselmastera.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dieselmastera.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DizCsRuConstants:
    NAME = "diz-cs.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://diz-cs.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FiresofheavenOrgConstants:
    NAME = "firesofheaven.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.firesofheaven.org/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class EgidaByConstants:
    NAME = "egida.by"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://egida.by/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ExcelworldRuConstants:
    NAME = "excelworld.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://excelworld.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SzerokikadrPlConstants:
    NAME = "Szerokikadr.pl"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.szerokikadr.pl/profil,{username}"
    PRESENCE = ('Profil użytkownika',)
    ABSENCE = ('Nie masz jeszcze konta?',)
    GENERIC = set()

class IzmailonlineComConstants:
    NAME = "izmailonline.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://izmailonline.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MarkweinguitarlessonsComConstants:
    NAME = "markweinguitarlessons.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://markweinguitarlessons.com/forums/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class LithotherapyConstants:
    NAME = "lithotherapy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.lithotherapy.ru/search.php?keywords=&terms=all&author={username}"
    PRESENCE = ()
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()


class MoscherbRuConstants:
    NAME = "moscherb.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://moscherb.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NfClubRuConstants:
    NAME = "nf-club.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nf-club.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OdonvvRuConstants:
    NAME = "odonvv.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://odonvv.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Panzer35RuConstants:
    NAME = "panzer35.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://panzer35.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PrizyvnikmoyRuConstants:
    NAME = "prizyvnikmoy.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://prizyvnikmoy.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class RelaskoRuConstants:
    NAME = "relasko.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://relasko.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NarutoBaseTvConstants:
    NAME = "naruto-base.tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://naruto-base.tv/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SomersoftComConstants:
    NAME = "somersoft.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.somersoft.com/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class SecretKompas3dSuConstants:
    NAME = "secret.kompas3d.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://secret.kompas3d.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SampSektorRuConstants:
    NAME = "samp-sektor.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://samp-sektor.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TheprodigyConstants:
    NAME = "theprodigy"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.theprodigy.ru/index.php?board=13&action=viewprofile&user={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь, чей профиль вы пытаетесь посмотреть, не существует.',)
    GENERIC = set()

class SoldatiRussianRuConstants:
    NAME = "soldati-russian.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://soldati-russian.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class UaodessaComConstants:
    NAME = "uaodessa.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://uaodessa.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TransitClubComConstants:
    NAME = "transit-club.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://transit-club.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ThaicatRuConstants:
    NAME = "thaicat.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://thaicat.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AlisaclubRuConstants:
    NAME = "alisaclub.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://alisaclub.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ForumUHivRuConstants:
    NAME = "forum.u-hiv.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.u-hiv.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CodByConstants:
    NAME = "cod.by"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://cod.by/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GallasyComConstants:
    NAME = "gallasy.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gallasy.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class DrDenisovRuConstants:
    NAME = "dr-denisov.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://dr-denisov.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Goba6372RuConstants:
    NAME = "goba6372.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://goba6372.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WeddingImageRuConstants:
    NAME = "wedding-image.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://wedding-image.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SvadbaOrelComConstants:
    NAME = "svadba-orel.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://svadba-orel.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KlubSkidokRuConstants:
    NAME = "klub-skidok.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://klub-skidok.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class FordatingRuConstants:
    NAME = "fordating.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://fordating.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MagictarotRuConstants:
    NAME = "magictarot.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://magictarot.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class NojayUrtRuConstants:
    NAME = "nojay-urt.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://nojay-urt.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class N4948RuConstants:
    NAME = "4948.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://4948.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EnglishinfoRuConstants:
    NAME = "englishinfo.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://englishinfo.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MamasuperRuConstants:
    NAME = "mamasuper.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mamasuper.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class LedVectorRuConstants:
    NAME = "led-vector.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://led-vector.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class KotelTorgRuConstants:
    NAME = "kotel-torg.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://kotel-torg.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MedvestnicRuConstants:
    NAME = "medvestnic.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://medvestnic.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MoxVoUzConstants:
    NAME = "mox.vo.uz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mox.vo.uz/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MoneysfirstRuConstants:
    NAME = "moneysfirst.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://moneysfirst.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MemoryLolConstants:
    NAME = "memory.lol"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://api.memory.lol/v1/tw/{username}"
    PRESENCE = ('{"accounts":[{',)
    ABSENCE = ('{"accounts":[]}',)
    GENERIC = set()

class SharzhPortretRuConstants:
    NAME = "sharzh-portret.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sharzh-portret.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ShipsondeskInfoConstants:
    NAME = "shipsondesk.info"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://shipsondesk.info/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class BceTytRuConstants:
    NAME = "bce-tyt.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://bce-tyt.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SefirutRuConstants:
    NAME = "sefirut.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sefirut.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SstalkersRuConstants:
    NAME = "sstalkers.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://sstalkers.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ErcevoRuConstants:
    NAME = "ercevo.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ercevo.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ProvincialynewsRuConstants:
    NAME = "provincialynews.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://provincialynews.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Gym5NetConstants:
    NAME = "gym5.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gym5.net/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OnceUponATimeTvRuConstants:
    NAME = "once-upon-a-time-tv.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://once-upon-a-time-tv.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class OkmOrgRuConstants:
    NAME = "okm.org.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://okm.org.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class JekAutoRuConstants:
    NAME = "jek-auto.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://jek-auto.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IsraelrentInfoConstants:
    NAME = "israelrent.info"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://israelrent.info/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MarkSzenprogsRuConstants:
    NAME = "mark.szenprogs.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mark.szenprogs.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Laserwar48RuConstants:
    NAME = "laserwar48.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://laserwar48.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class CentrSpektrRuConstants:
    NAME = "centr-spektr.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://centr-spektr.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()


class Ofc65RuConstants:
    NAME = "ofc65.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ofc65.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class V3deRuConstants:
    NAME = "v3de.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://v3de.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Xn80aqkf5cbXnP1aiConstants:
    NAME = "xn--80aqkf5cb.xn--p1ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xn--80aqkf5cb.xn--p1ai/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZerkalasteklaRuConstants:
    NAME = "zerkalastekla.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zerkalastekla.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Budo52RuConstants:
    NAME = "budo52.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://budo52.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class XristosVoUzConstants:
    NAME = "xristos.vo.uz"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xristos.vo.uz/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Iceberg116RuConstants:
    NAME = "iceberg-116.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://iceberg-116.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class WorldofdragonageRuConstants:
    NAME = "worldofdragonage.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://worldofdragonage.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class PodologSuConstants:
    NAME = "podolog.su"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://podolog.su/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SiSvComConstants:
    NAME = "si-sv.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://si-sv.com/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MastersoapRuConstants:
    NAME = "mastersoap.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mastersoap.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class TalimgerOrgConstants:
    NAME = "talimger.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://talimger.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class GorposmosRuConstants:
    NAME = "gorposmos.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gorposmos.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class EdumonchRuConstants:
    NAME = "edumonch.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://edumonch.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class SalutmRuConstants:
    NAME = "salutm.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://salutm.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ElectronicComponentOrgConstants:
    NAME = "electronic-component.org"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://electronic-component.org/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MusicbunkerRuConstants:
    NAME = "musicbunker.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://musicbunker.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ProfsouzAuRuConstants:
    NAME = "profsouz-au.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://profsouz-au.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class IrteamRuConstants:
    NAME = "irteam.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://irteam.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AheraRuConstants:
    NAME = "ahera.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://ahera.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MircasovRuConstants:
    NAME = "mircasov.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mircasov.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class Xn246kcaal6ajt1cpibnu7d5dtcXnP1aiConstants:
    NAME = "xn--24-6kcaal6ajt1cpibnu7d5dtc.xn--p1ai"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://xn--24-6kcaal6ajt1cpibnu7d5dtc.xn--p1ai/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class HokageTvConstants:
    NAME = "hokage.tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://hokage.tv/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class AributRuConstants:
    NAME = "aribut.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://aribut.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MetrologikaRuConstants:
    NAME = "metrologika.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://metrologika.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MednolitRuConstants:
    NAME = "mednolit.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mednolit.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class MikeleLoconteRuConstants:
    NAME = "mikele-loconte.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://mikele-loconte.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()

class ZapgameRuConstants:
    NAME = "zapgame.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://zapgame.ru/index/8-0-{username}"
    PRESENCE = ('udtlb">Пользователь:</div>', 'Гостям запрещено просматривать данную страницу, пожалуйста войдите на сайт как пользователь.', '<center><b>Личные данные</b>', 'Гостям запрещено просматривать данную страницу, пожалуйста, войдите на сайт как пользователь.', '<img alt="" name="rankimg" border="0" src="/.s/rnk/', 'Гостям запрещено просматривать персональные страницы пользователей.', 'profile-section-name', 'webo4ka_dannii', 'Дата регистрации')
    ABSENCE = ('<title>HTTP 404', 'Пользователь не найден')
    GENERIC = set()


class NiflheimTopConstants:
    NAME = "niflheim.top"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://niflheim.top/members/?username={username}"
    PRESENCE = ('Вы должны быть авторизованы, чтобы выполнить это действие или просмотреть эту страницу.', 'Для того, чтобы это сделать, нужно сначала войти на форум.', 'You must be logged-in to do that.', 'You must be logged in to do that.', 'memberHeader-content', 'profilePage')
    ABSENCE = ('The requested page could not be found.', 'The specified member cannot be found. Please enter a member', 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', "Le membre spécifié est introuvable. Veuillez saisir le nom complet d'un membre.", 'Belirtilen üye bulunamadı. Lütfen bir üyenin tam adını giriniz.')
    GENERIC = set()

class TottenhamhotspurRuConstants:
    NAME = "tottenhamhotspur.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://tottenhamhotspur.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class CommunityGozenhostComConstants:
    NAME = "community.gozenhost.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://community.gozenhost.com/u/{username}"
    PRESENCE = ('"attributes":{"username"',)
    ABSENCE = ('NotFound',)
    GENERIC = set()

class ForumPrihozRuConstants:
    NAME = "forum.prihoz.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.prihoz.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class VideoforumsRuConstants:
    NAME = "videoforums.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://videoforums.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class MindmachineRuConstants:
    NAME = "mindmachine.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://mindmachine.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class NelubitRuConstants:
    NAME = "nelubit.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://nelubit.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ElibraryTipsConstants:
    NAME = "elibrary.tips"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://elibrary.tips/profile/{username}"
    PRESENCE = ('profile-page',)
    ABSENCE = ('pagination',)
    GENERIC = set()

class ForumHistoryRuConstants:
    NAME = "forum-history.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum-history.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class ForumRastrnetRuConstants:
    NAME = "forum.rastrnet.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.rastrnet.ru/member.php?username={username}"
    PRESENCE = ()
    ABSENCE = ('Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'Bu Üye kayıtlı Üyemiz değildir. Bu sebebten dolayı Üyeye ait Profil gösterilemiyor.', 'This user has not registered and therefore does not have a profile to view.', 'Користувач не зареєстрований і не має профілю, який можна переглянути.', 'Deze gebruiker is niet geregistreerd, zodat je zijn of haar profiel niet kunt bekijken.', 'Этот пользователь ещё не зарегистрирован, поэтому его профиль недоступен.')
    GENERIC = set()

class ForumLeague17RuConstants:
    NAME = "forum.league17.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.league17.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class VwBusRuConstants:
    NAME = "vw-bus.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vw-bus.ru/memberlist.php?username={username}"
    PRESENCE = ('You must be logged in to do that.', './memberlist.php?mode=viewprofile')
    ABSENCE = ('No members found for this search criterion.', 'Не найдено ни одного пользователя по заданным критериям')
    GENERIC = set()


class CediaClubRuConstants:
    NAME = "cedia-club.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://cedia-club.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class N308ClubRuConstants:
    NAME = "308-club.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.308-club.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class BashohotaRuConstants:
    NAME = "bashohota.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.bashohota.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class AudiBelarusByConstants:
    NAME = "audi-belarus.by"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://audi-belarus.by/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ChevroletDaewooRuConstants:
    NAME = "chevrolet-daewoo.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://chevrolet-daewoo.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumInjectorserviceComUaConstants:
    NAME = "forum.injectorservice.com.ua"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.injectorservice.com.ua/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumPskovchessRuConstants:
    NAME = "forum.pskovchess.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.pskovchess.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumTathunterRuConstants:
    NAME = "forum.tathunter.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://forum.tathunter.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class FforumRuConstants:
    NAME = "fforum.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://www.fforum.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class MemoriamRuConstants:
    NAME = "memoriam.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://memoriam.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class FraufloraComConstants:
    NAME = "frauflora.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://frauflora.com/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class SpbProjectsRuConstants:
    NAME = "spb-projects.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://spb-projects.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class MitsubishiAsxNetConstants:
    NAME = "mitsubishi-asx.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.mitsubishi-asx.net/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class KidshockeyRuConstants:
    NAME = "kidshockey.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://kidshockey.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class HairforumRuConstants:
    NAME = "hairforum.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://hairforum.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class LyricsTrainingConstants:
    NAME = "lyricsTraining"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://lyricstraining.com/search?user={username}"
    PRESENCE = ('Lyrics by',)
    ABSENCE = ('Sorry, there are no results for your search.',)
    GENERIC = set()

class BreakersTvConstants:
    NAME = "breakers.tv"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://breakers.tv/{username}"
    PRESENCE = ('</span> followers', '{username}</span>', '{username} on Breakers.TV')
    ABSENCE = ("Channel you are looking for doesn't exist", 'Stream Not Found - Breakers.TV')
    GENERIC = set()

class Gaz24ComConstants:
    NAME = "gaz-24.com"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://gaz-24.com/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class ForumVolnistyeRuConstants:
    NAME = "forum.volnistye.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://forum.volnistye.ru/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class VcfmRuConstants:
    NAME = "vcfm.ru"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://vcfm.ru/forum/search.php?author={username}"
    PRESENCE = ('postprofile', ' username-coloured')
    ABSENCE = ('Подходящих тем или сообщений не найдено.',)
    GENERIC = set()

class DiscordBioConstants:
    NAME = "Discord.bio"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://discords.com/api-v2/bio/details/{username}"
    PRESENCE = ()
    ABSENCE = ('User not found',)
    GENERIC = set()

class ShelfConstants:
    NAME = "Shelf"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.shelf.im/{username}"
    PRESENCE = ()
    ABSENCE = ('User Not Found',)
    GENERIC = set()

class BlitzTacticsConstants:
    NAME = "Blitz Tactics"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://blitztactics.com/{username}"
    PRESENCE = ()
    ABSENCE = ("That page doesn't exist",)
    GENERIC = set()

class WeeblyConstants:
    NAME = "Weebly"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://{username}.weebly.com/"
    GENERIC = set()

class WebNodeConstants:
    NAME = "WebNode"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.webnode.cz/"
    GENERIC = set()

class UsernameTildaWsConstants:
    NAME = "{username}.tilda.ws"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.tilda.ws"
    GENERIC = set()

class RajceNetConstants:
    NAME = "Rajce.net"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.rajce.idnes.cz/"
    GENERIC = set()

class NNRUConstants:
    NAME = "NN.RU"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.www.nn.ru/"
    GENERIC = set()

class InsanejournalConstants:
    NAME = "Insanejournal"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://{username}.insanejournal.com/profile"
    PRESENCE = ()
    ABSENCE = ('<TITLE>404 Not Found</TITLE>', 'is not currently registered')
    GENERIC = set()

class YelpConstants:
    NAME = "Yelp"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://{username}.yelp.com/"
    PRESENCE = ('Username', 'Birthday', 'First Name', 'Last Name', 'Email')
    ABSENCE = ('viewName', ' dropdown_user-name')
    GENERIC = set()

class ContactInBioDomainConstants:
    NAME = "ContactInBio (domain)"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "http://{username}.contactin.bio/"
    GENERIC = set()


class OmgLolConstants:
    NAME = "Omg.lol"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.omg.lol"
    GENERIC = set()


class XangaConstants:
    NAME = "Xanga"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.xanga.com/"
    PRESENCE = ('s Xanga Site | Just',)
    ABSENCE = ('Xanga 2.0 is Here!',)
    GENERIC = set()

class JimdoConstants:
    NAME = "Jimdo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://{username}.jimdosite.com"
    GENERIC = set()

class WikipediaConstants:
    NAME = "Wikipedia"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[^\s/?#&:]{1,85}$"
    PROFILE_URL = "https://en.wikipedia.org/wiki/User:{username}"
    API_URL = "https://en.wikipedia.org/w/api.php?action=query&list=users&ususers={username}&usprop=registration|editcount|groups&format=json"

class DuolingoConstants:
    NAME = "Duolingo"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._@-]{1,80}$"
    PROFILE_URL = "https://www.duolingo.com/profile/{username}"
    GENERIC = set()

