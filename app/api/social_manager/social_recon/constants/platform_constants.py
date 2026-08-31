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


class PinterestConstants:
    NAME = "Pinterest"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9_]{3,30}$"
    PROFILE_URL = "https://www.pinterest.com/{username}/"
    PROFILE_MARKER = "- profile"
    MAX_BYTES = 1_600_000
    AVATAR_KEYS = ("image_xlarge_url", "image_medium_url")
    COVER_KEYS = ("profile_cover_url", "image_cover_url")


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


class TikTokConstants:
    NAME = "TikTok"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9._]{2,24}$"
    PROFILE_URL = "https://www.tiktok.com/@{username}"
    OEMBED_URL = "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}"
    IMAGE_NOTE = "no avatar available over http: profile oembed carries no thumbnail and the profile html is a script shell"


class TwitchConstants:
    NAME = "Twitch"
    CRAWL_TYPE = "normal"
    GRAMMAR = r"^[A-Za-z0-9_]{4,25}$"
    PROFILE_URL = "https://www.twitch.tv/{username}"
    GQL_URL = "https://gql.twitch.tv/gql"
    GQL_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    GQL_QUERY = (
        '{{user(login:"{username}"){{id displayName description '
        "profileImageURL(width:300) bannerImageURL offlineImageURL "
        "followers{{totalCount}}}}}}"
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
    AVATAR_KEYS = ("buddyicon", "iconurl")
    COVER_KEYS = ("coverphoto",)


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
    GENERIC = {"artstation", "artstation - not found"}
    AVATAR_KEYS = ("large_avatar_url", "medium_avatar_url")
    COVER_KEYS = ("cover_url",)


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


class GoodreadsConstants:
    NAME = "Goodreads"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.goodreads.com/{username}"
    GENERIC = {"goodreads", "page not found"}
    AVATAR_KEYS = ("image_url", "profile_image")
    COVER_KEYS = ()


class LetterboxdConstants:
    NAME = "Letterboxd"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{2,15}$"
    PROFILE_URL = "https://letterboxd.com/{username}/"
    GENERIC = {"letterboxd", "letterboxd - not found"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


class AcademiaEduConstants:
    NAME = "Academia.edu"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://independent.academia.edu/{username}"
    GENERIC = {"academia.edu", "academia.edu - share research"}
    AVATAR_KEYS = ("photo",)
    COVER_KEYS = ()


class StackOverflowConstants:
    NAME = "Stack Overflow"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://stackoverflow.com/users/{username}"
    GENERIC = {"page not found - stack overflow", "stack overflow", "user not found - stack overflow"}
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


class GitLabConstants:
    NAME = "GitLab"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,255}$"
    PROFILE_URL = "https://gitlab.com/{username}"
    API_URL = "https://gitlab.com/api/v4/users?username={username}"


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
    GENERIC = {"steam community", "steam community :: error"}
    AVATAR_KEYS = ("avatarFull", "avatarMedium")
    COVER_KEYS = ()


class RobloxConstants:
    NAME = "Roblox"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_]{3,20}$"
    PROFILE_URL = "https://www.roblox.com/users/profile?username={username}"
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
    GQL_QUERY = "query($name:String){User(name:$name){id name about avatar{large} bannerImage createdAt}}"


class InterPalsConstants:
    NAME = "InterPals"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://www.interpals.net/{username}"
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


class AboutMeConstants:
    NAME = "About.me"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9._-]{1,64}$"
    PROFILE_URL = "https://about.me/{username}"
    GENERIC = {"about.me"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ("background_url",)


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


class CodePenConstants:
    NAME = "CodePen"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://codepen.io/{username}"
    GENERIC = {"404 on codepen", "codepen"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


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
    API_URL = "https://api.dailymotion.com/user/{username}?fields=id,screenname,avatar_360_url,description,followers_total"


class GIPHYConstants:
    NAME = "GIPHY"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_-]{1,64}$"
    PROFILE_URL = "https://giphy.com/{username}"
    GENERIC = {"gifs - find & share on giphy", "giphy"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ("banner_url",)


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


class ItchIoConstants:
    NAME = "itch.io"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9_-]{1,63}$"
    PROFILE_URL = "https://{username}.itch.io"
    GENERIC = {"itch.io"}
    AVATAR_KEYS = ("avatar",)
    COVER_KEYS = ()


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


class GumroadConstants:
    NAME = "Gumroad"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[a-z0-9-]{1,63}$"
    PROFILE_URL = "https://{username}.gumroad.com"
    GENERIC = {"gumroad", "page not found (404) - gumroad"}
    AVATAR_KEYS = ("avatar_url",)
    COVER_KEYS = ()


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


class EBayConstants:
    NAME = "eBay"
    CRAWL_TYPE = "normal"
    GRAMMAR = "^[A-Za-z0-9_.*-]{1,64}$"
    PROFILE_URL = "https://www.ebay.com/usr/{username}"
    GENERIC = {"ebay", "ebay home"}
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
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://imo.im/{username}"


class LineConstants:
    NAME = "LINE"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://line.me/ti/p/{username}"


class MessengerConstants:
    NAME = "Messenger"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://m.me/{username}"


class NaverCafeConstants:
    NAME = "Naver Cafe"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://cafe.naver.com/{username}"


class QQConstants:
    NAME = "QQ"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://user.qzone.qq.com/{username}"


class ViberConstants:
    NAME = "Viber"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://invite.viber.com/?g2={username}"


class WeChatConstants:
    NAME = "WeChat"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://u.wechat.com/{username}"


class YuboConstants:
    NAME = "Yubo"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://yubo.live/{username}"


class DiscordConstants:
    NAME = "Discord"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://discord.com/users/{username}"


class WhatsAppConstants:
    NAME = "WhatsApp"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://wa.me/{username}"


class WordPressOrgConstants:
    NAME = "WordPressOrg"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://profiles.wordpress.org/{username}/"


class SourceForgeConstants:
    NAME = "SourceForge"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://sourceforge.net/u/{username}/profile"


class BloggerConstants:
    NAME = "Blogger"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.blogspot.com"


class BloggerBloggerComConstants:
    NAME = "Blogger (blogger.com)"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.blogger.com/profile/{username}"


class TripAdvisorConstants:
    NAME = "TripAdvisor"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://tripadvisor.com/members/{username}"


class MyspaceConstants:
    NAME = "Myspace"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://myspace.com/{username}"


class ThemeForestConstants:
    NAME = "ThemeForest"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://themeforest.net/user/{username}"


class WeforumConstants:
    NAME = "Weforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.weforum.org/people/{username}"


class FreepikConstants:
    NAME = "Freepik"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.freepik.com/author/{username}"


class ChangeOrgConstants:
    NAME = "Change.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.change.org/o/{username}"


class SlackConstants:
    NAME = "Slack"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.slack.com"


class DisqusConstants:
    NAME = "Disqus"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://disqus.com/{username}"


class NPMConstants:
    NAME = "NPM"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.npmjs.com/~{username}"


class DigitalOceanConstants:
    NAME = "DigitalOcean"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.digitalocean.com/community/users/{username}"


class InstructablesConstants:
    NAME = "Instructables"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.instructables.com/member/{username}"


class AmebloConstants:
    NAME = "Ameblo"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ameblo.jp/{username}"


class HuggingFaceConstants:
    NAME = "HuggingFace"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://huggingface.co/{username}"


class LaracastConstants:
    NAME = "Laracast"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://laracasts.com/@{username}"


class BitBucketConstants:
    NAME = "BitBucket"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://bitbucket.org/{username}/"


class UpworkConstants:
    NAME = "Upwork"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://upwork.com/fl/{username}"


class IStockConstants:
    NAME = "iStock"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.istockphoto.com/ru/portfolio/{username}"


class PastebinConstants:
    NAME = "Pastebin"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://pastebin.com/u/{username}"


class FoursquareConstants:
    NAME = "Foursquare"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://foursquare.com/{username}"


class DiscogsConstants:
    NAME = "Discogs"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.discogs.com/user/{username}"


class KofiConstants:
    NAME = "kofi"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ko-fi.com/{username}"


class RottentomatoesConstants:
    NAME = "Rottentomatoes"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.rottentomatoes.com/critic/{username}/movies"


class SmugmugConstants:
    NAME = "Smugmug"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.smugmug.com/"


class DuolingoConstants:
    NAME = "Duolingo"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.duolingo.com/profile/{username}"


class UstreamConstants:
    NAME = "Ustream"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.ustream.tv/channel/adam{username}"


class WikidotConstants:
    NAME = "Wikidot"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.wikidot.com/user:info/{username}"


class ImageShackConstants:
    NAME = "ImageShack"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://imageshack.com/user/{username}"


class BuyMeACoffeeConstants:
    NAME = "BuyMeACoffee"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://buymeacoff.ee/{username}"


class GiteaConstants:
    NAME = "Gitea"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gitea.com/{username}"


class GeniusConstants:
    NAME = "Genius"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://genius.com/{username}"


class HubPagesConstants:
    NAME = "HubPages"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://hubpages.com/@{username}"


class PbaseConstants:
    NAME = "Pbase"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://pbase.com/{username}/profile"


class GeeksforGeeksConstants:
    NAME = "Geeksfor Geeks"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://auth.geeksforgeeks.org/user/{username}"


class CodebergOrgConstants:
    NAME = "codeberg.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://codeberg.org/{username}"


class AllRecipesConstants:
    NAME = "AllRecipes"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.allrecipes.com/cook/{username}"


class CodecanyonConstants:
    NAME = "Codecanyon"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://codecanyon.net/user/{username}"


class CodecademyConstants:
    NAME = "Codecademy"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.codecademy.com/profiles/{username}"


class PolygonConstants:
    NAME = "Polygon"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.polygon.com/users/{username}"


class PCGamerConstants:
    NAME = "PCGamer"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://forums.pcgamer.com/members/?username={username}"


class DreamstimeConstants:
    NAME = "Dreamstime"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.dreamstime.com/{username}_info"


class SpeakerdeckConstants:
    NAME = "Speakerdeck"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://speakerdeck.com/{username}"


class NextcloudForumConstants:
    NAME = "Nextcloud Forum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://help.nextcloud.com/u/{username}/summary"


class MaxConstants:
    NAME = "Max"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://max.ru/{username}"


class TVTropesConstants:
    NAME = "TVTropes"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://tvtropes.org/pmwiki/pmwiki.php/Tropers/{username}"


class TistoryConstants:
    NAME = "Tistory"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.tistory.com/"


class JSFiddleConstants:
    NAME = "JSFiddle"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://jsfiddle.net/user/{username}/"


class GamesRadarConstants:
    NAME = "GamesRadar"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.gamesradar.com/uk/author/{username}/"


class GeocachingConstants:
    NAME = "Geocaching"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.geocaching.com/p/?u={username}"


class GogConstants:
    NAME = "Gog"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.gog.com/u/{username}"


class CoubConstants:
    NAME = "Coub"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://coub.com/{username}"


class OdyseeConstants:
    NAME = "Odysee"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://odysee.com/@{username}"


class ReplitConstants:
    NAME = "Replit"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://replit.com/@{username}"


class HackMDConstants:
    NAME = "Hack MD"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://hackmd.io/@{username}"


class INaturalistConstants:
    NAME = "iNaturalist"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.inaturalist.org/lists/{username}"


class TemplateMonsterConstants:
    NAME = "TemplateMonster"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.templatemonster.com/authors/{username}/"


class TeletypeConstants:
    NAME = "Teletype"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://teletype.in/@{username}"


class CTANConstants:
    NAME = "CTAN"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ctan.org/author/{username}"


class OpenCollectiveConstants:
    NAME = "OpenCollective"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://opencollective.com/{username}"


class GiantbombConstants:
    NAME = "Giantbomb"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.giantbomb.com/profile/{username}"


class JAlbumNetConstants:
    NAME = "jAlbum.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.jalbum.net/"


class NewgroundsConstants:
    NAME = "Newgrounds"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.newgrounds.com"


class SlidesConstants:
    NAME = "Slides"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://slides.com/{username}"


class UltimateGuitarConstants:
    NAME = "Ultimate-Guitar"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ultimate-guitar.com/u/{username}"


class ContentlyConstants:
    NAME = "Contently"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.contently.com/"


class CreativeMarketConstants:
    NAME = "CreativeMarket"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://creativemarket.com/users/{username}"


class OpenSourceConstants:
    NAME = "OpenSource"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://opensource.com/users/{username}"


class ImgflipConstants:
    NAME = "Imgflip"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://imgflip.com/user/{username}"


class HackadayConstants:
    NAME = "Hackaday"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://hackaday.io/{username}"


class FodorsConstants:
    NAME = "Fodors"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.fodors.com/community/profile/{username}/forum-activity"


class Designs99Constants:
    NAME = "Designs99"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://99designs.com/profiles/{username}"


class PeriscopeConstants:
    NAME = "Periscope"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.pscp.tv/{username}"


class FreesoundConstants:
    NAME = "Freesound"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://freesound.org/people/{username}/"


class MetalArchivesConstants:
    NAME = "Metal-archives"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.metal-archives.com/users/{username}"


class KongregateConstants:
    NAME = "Kongregate"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.kongregate.com/accounts/{username}"


class SoupConstants:
    NAME = "Soup"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.soup.io/author/{username}"


class FurAffinityConstants:
    NAME = "Fur Affinity"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.furaffinity.net/gallery/{username}"


class ItemFixConstants:
    NAME = "ItemFix"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.itemfix.com/c/{username}"


class NintendoLifeConstants:
    NAME = "Nintendo Life"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.nintendolife.com/users/{username}"


class CarbonmadeConstants:
    NAME = "Carbonmade"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.carbonmade.com"


class ModDBConstants:
    NAME = "ModDB"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.moddb.com/members/{username}"


class AudiojungleConstants:
    NAME = "Audiojungle"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://audiojungle.net/user/{username}"


class TinderConstants:
    NAME = "Tinder"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.tinder.com/@{username}"


class DomestikaOrgConstants:
    NAME = "domestika.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.domestika.org/{username}"


class NoblogsConstants:
    NAME = "Noblogs"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://noblogs.org/members/{username}/"


class SetlistConstants:
    NAME = "Setlist"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.setlist.fm/user/{username}"


class StarCitizenConstants:
    NAME = "Star Citizen"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://robertsspaceindustries.com/citizens/{username}"


class JigsawplanetConstants:
    NAME = "Jigsawplanet"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.jigsawplanet.com/{username}"


class NamuwikiConstants:
    NAME = "Namuwiki"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://namu.wiki/w/%EC%82%AC%EC%9A%A9%EC%9E%90:{username}"


class GaiaOnlineConstants:
    NAME = "GaiaOnline"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.gaiaonline.com/profiles/{username}"


class MemriseConstants:
    NAME = "Memrise"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.memrise.com/user/{username}/"


class ArchiveOfOurOwnConstants:
    NAME = "ArchiveOfOurOwn"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://archiveofourown.org/users/{username}"


class PlanetMinecraftConstants:
    NAME = "PlanetMinecraft"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.planetminecraft.com/member/{username}"


class MuseScoreConstants:
    NAME = "Muse Score"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://musescore.com/{username}"


class TheOdysseyOnlineConstants:
    NAME = "TheOdysseyOnline"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.theodysseyonline.com/user/@{username}"


class SportsRuConstants:
    NAME = "sports.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.sports.ru/profile/{username}/"


class PicsartConstants:
    NAME = "Picsart"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://picsart.com/u/{username}"


class WowheadConstants:
    NAME = "Wowhead"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.wowhead.com/user={username}"


class ArmorgamesConstants:
    NAME = "Armorgames"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://armorgames.com/user/{username}"


class FotkiConstants:
    NAME = "Fotki"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://members.fotki.com/{username}/about/"


class PaltalkConstants:
    NAME = "Paltalk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.paltalk.com/people/users/{username}"


class VideoHiveConstants:
    NAME = "VideoHive"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://videohive.net/user/{username}"


class ClubhouseConstants:
    NAME = "Clubhouse"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.clubhouse.com/@{username}"


class ProzaRuConstants:
    NAME = "Proza.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.proza.ru/avtor/{username}"


class NameprosConstants:
    NAME = "Namepros"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.namepros.com//members/?username={username}"


class WriteAsConstants:
    NAME = "write.as"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://write.as/{username}"


class WarriorForumConstants:
    NAME = "Warrior Forum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.warriorforum.com/members/{username}.html"


class AreNaConstants:
    NAME = "are.na"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.are.na/{username}"


class WykopConstants:
    NAME = "Wykop"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.wykop.pl/ludzie/{username}/"


class ResidentAdvisorConstants:
    NAME = "ResidentAdvisor"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.residentadvisor.net/profile/{username}"


class SporcleConstants:
    NAME = "Sporcle"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.sporcle.com/user/{username}/people"


class TreehouseConstants:
    NAME = "Treehouse"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://teamtreehouse.com/profiles/{username}"


class CoroflotConstants:
    NAME = "Coroflot"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.coroflot.com/{username}"


class JeuxVideoConstants:
    NAME = "JeuxVideo"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.jeuxvideo.com/profil/{username}?mode=infos"


class StihiRuConstants:
    NAME = "Stihi.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.stihi.ru/avtor/{username}"


class ExposureConstants:
    NAME = "Exposure"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.exposure.co/"


class LyricsTranslateConstants:
    NAME = "LyricsTranslate"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://lyricstranslate.com/sco/translator/{username}"


class GuruConstants:
    NAME = "Guru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.guru.com/freelancers/{username}"


class GutefrageConstants:
    NAME = "Gutefrage"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.gutefrage.net/nutzer/{username}"


class CoderwallConstants:
    NAME = "Coderwall"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://coderwall.com/{username}"


class ObservableConstants:
    NAME = "Observable"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://observablehq.com/@{username}"


class PushSquareConstants:
    NAME = "PushSquare"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.pushsquare.com/users/{username}"


class CodementorConstants:
    NAME = "Codementor"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.codementor.io/{username}"


class N4gConstants:
    NAME = "N4g"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://n4g.com/user/home/{username}"


class LomographyConstants:
    NAME = "Lomography"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.lomography.com/homes/{username}"


class PixelfedSocialConstants:
    NAME = "pixelfed.social"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://pixelfed.social/{username}/"


class NeoseekerConstants:
    NAME = "Neoseeker"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.neoseeker.com/members/{username}/"


class SytheConstants:
    NAME = "Sythe"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.sythe.org/members/?username={username}"


class FilmWebConstants:
    NAME = "FilmWeb"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.filmweb.pl/user/{username}"


class ListalConstants:
    NAME = "Listal"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.listal.com/"


class SpatialConstants:
    NAME = "Spatial"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.spatial.io/@{username}"


class ParagraphConstants:
    NAME = "Paragraph"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://paragraph.com/@{username}"


class NotabugOrgConstants:
    NAME = "notabug.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://notabug.org/{username}"


class MydramalistConstants:
    NAME = "Mydramalist"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.mydramalist.com/profile/{username}"


class PinkbikeConstants:
    NAME = "Pinkbike"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.pinkbike.com/u/{username}/"


class ThechiveConstants:
    NAME = "Thechive"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://thechive.com/author/{username}"


class GoldderbyConstants:
    NAME = "Goldderby"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.goldderby.com/members/{username}/"


class MeetMeConstants:
    NAME = "MeetMe"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.meetme.com/{username}"


class FlyertalkConstants:
    NAME = "Flyertalk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.flyertalk.com/forum/members/{username}.html"


class GBAtempNetConstants:
    NAME = "GBAtemp.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gbatemp.net//members/?username={username}"


class BrusheezyConstants:
    NAME = "Brusheezy"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.brusheezy.com/members/{username}"


class AvforumsConstants:
    NAME = "Avforums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.avforums.com/members/?username={username}"


class MobypictureConstants:
    NAME = "Mobypicture"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.mobypicture.com/user/{username}"


class DLiveConstants:
    NAME = "DLive"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://dlive.tv/{username}"


class TrueAchievementsConstants:
    NAME = "TrueAchievements"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.trueachievements.com/gamer/{username}"


class PhysicsforumsConstants:
    NAME = "Physicsforums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.physicsforums.com/members/?username={username}"


class OpenGameArtConstants:
    NAME = "Open Game Art"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://opengameart.org/users/{username}"


class LobstersConstants:
    NAME = "Lobsters"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://lobste.rs/u/{username}"


class IFunnyConstants:
    NAME = "iFunny"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.ifunny.co/user/{username}"


class TopcoderConstants:
    NAME = "Topcoder"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://profiles.topcoder.com/{username}/"


class PicturepushComConstants:
    NAME = "picturepush.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.picturepush.com/"


class VoicesConstants:
    NAME = "Voices"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.voices.com/actors/{username}"


class NhattaoComConstants:
    NAME = "nhattao.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.nhattao.com/members/?username={username}"


class ReplItConstants:
    NAME = "Repl.it"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://repl.it/@{username}"


class UsernamePortfolioboxNetConstants:
    NAME = "{username}.portfoliobox.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.portfoliobox.net"


class DcinsideConstants:
    NAME = "Dcinside"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gallog.dcinside.com/{username}"


class DigitalPointConstants:
    NAME = "DigitalPoint"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.digitalpoint.com/members/?username={username}"


class AsciinemaConstants:
    NAME = "Asciinema"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://asciinema.org/~{username}"


class CfdOnlineConstants:
    NAME = "cfd-online"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.cfd-online.com/Forums/members/{username}.html"


class FunnyjunkConstants:
    NAME = "Funnyjunk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://funnyjunk.com/user/{username}"


class GloriaTvConstants:
    NAME = "gloria.tv"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gloria.tv/{username}"


class FicwadConstants:
    NAME = "Ficwad"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ficwad.com/a/{username}/favorites/authors"


class TriplineConstants:
    NAME = "Tripline"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.tripline.net/{username}"


class DeepDreamGeneratorConstants:
    NAME = "DeepDreamGenerator"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://deepdreamgenerator.com/u/{username}"


class N1xConstants:
    NAME = "1x"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://1x.com/{username}"


class PokecommunityConstants:
    NAME = "Pokecommunity"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.pokecommunity.com/members/?username={username}"


class SamlibConstants:
    NAME = "Samlib"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://samlib.ru/e/{username}"


class GoodgameRuConstants:
    NAME = "goodgame.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://goodgame.ru/channel/{username}"


class PlingConstants:
    NAME = "Pling"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.pling.com/u/{username}/"


class HardforumConstants:
    NAME = "Hardforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://hardforum.com/members/?username={username}"


class N23hqConstants:
    NAME = "23hq"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.23hq.com/{username}"


class AndroidforumsConstants:
    NAME = "Androidforums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://androidforums.com/members/?username={username}"


class ComedyConstants:
    NAME = "Comedy"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.comedy.co.uk/profile/{username}/"


class YouPicConstants:
    NAME = "YouPic"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://youpic.com/photographer/{username}/"


class PolarstepsConstants:
    NAME = "Polarsteps"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://polarsteps.com/{username}"


class PlatziConstants:
    NAME = "Platzi"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://platzi.com/p/{username}/"


class WritingforumsOrgConstants:
    NAME = "writingforums.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.writingforums.org//members/?username={username}"


class ChatujmeCzConstants:
    NAME = "Chatujme.cz"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://profil.chatujme.cz/{username}"


class AntiquersConstants:
    NAME = "Antiquers"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.antiquers.com/members/?username={username}"


class BigsoccerConstants:
    NAME = "Bigsoccer"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.bigsoccer.com/members/?username={username}"


class SkyblockConstants:
    NAME = "Skyblock"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://skyblock.net/members/?username={username}"


class HiveBlogConstants:
    NAME = "Hive Blog"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://hive.blog/@{username}"


class JoyreactorCcConstants:
    NAME = "joyreactor.cc"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://joyreactor.cc/user/{username}"


class ViewBugConstants:
    NAME = "ViewBug"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.viewbug.com/member/{username}"


class ExophaseConstants:
    NAME = "Exophase"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.exophase.com/user/{username}/"


class WebdeveloperComConstants:
    NAME = "webdeveloper.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://webdeveloper.com/u/{username}"


class FediversePartyConstants:
    NAME = "fediverse.party"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://fediverse.party/en/{username}"


class WeblancerConstants:
    NAME = "Weblancer"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.weblancer.net/users/{username}/"


class SugoidesuConstants:
    NAME = "Sugoidesu"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://sugoidesu.net/members/?username={username}"


class ProfiRuConstants:
    NAME = "profi.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://profi.ru/profile/{username}/"


class ThoughtsComConstants:
    NAME = "thoughts.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://thoughts.com/members/{username}"


class GapyearConstants:
    NAME = "Gapyear"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.gapyear.com/members/{username}"


class MyinstantsConstants:
    NAME = "Myinstants"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.myinstants.com/profile/{username}/"


class SmokingmeatforumsComConstants:
    NAME = "smokingmeatforums.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://smokingmeatforums.com/members/?username={username}"


class ReibertConstants:
    NAME = "Reibert"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://reibert.info//members/?username={username}"


class FreelancehuntConstants:
    NAME = "Freelancehunt"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://freelancehunt.com/freelancer/{username}.html"


class AtcoderConstants:
    NAME = "Atcoder"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://atcoder.jp/users/{username}"


class JetpunkConstants:
    NAME = "Jetpunk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.jetpunk.com/users/{username}"


class RappadConstants:
    NAME = "Rappad"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.rappad.co/users/{username}"


class NationStatesNationConstants:
    NAME = "NationStates Nation"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://nationstates.net/nation={username}"


class EthresearConstants:
    NAME = "Ethresear"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ethresear.ch/u/{username}/summary"


class HomebrewtalkComConstants:
    NAME = "homebrewtalk.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.homebrewtalk.com/members/?username={username}"


class LemmyWorldConstants:
    NAME = "Lemmy World"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://lemmy.world/u/{username}"


class ZoomirIrConstants:
    NAME = "Zoomir.ir"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.zoomit.ir/user/{username}"


class CentConstants:
    NAME = "Cent"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://beta.cent.co/@{username}"


class VjudgeConstants:
    NAME = "Vjudge"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://VJudge.net/user/{username}"


class TheSimsResourceConstants:
    NAME = "TheSimsResource"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.thesimsresource.com/members/{username}/"


class VgtimesGamesConstants:
    NAME = "Vgtimes/Games"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://vgtimes.ru/games/{username}/forum/"


class WindowsforumConstants:
    NAME = "Windowsforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://windowsforum.com/members/?username={username}"


class WarpcastConstants:
    NAME = "Warpcast"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://warpcast.com/{username}"


class TopmateConstants:
    NAME = "Topmate"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://topmate.io/{username}"


class TyperacerConstants:
    NAME = "Typeracer"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://data.typeracer.com/pit/profile?user={username}"


class DevRantConstants:
    NAME = "devRant"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://devrant.com/users/{username}"


class RmmediaConstants:
    NAME = "Rmmedia"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://rmmedia.ru/members/?username={username}"


class HometheaterforumConstants:
    NAME = "Hometheaterforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.hometheaterforum.com/community/members/?username={username}"


class VLRConstants:
    NAME = "VLR"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.vlr.gg/user/{username}"


class HackingWithSwiftConstants:
    NAME = "HackingWithSwift"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.hackingwithswift.com/users/{username}"


class PokemonShowdownConstants:
    NAME = "Pokemon Showdown"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://pokemonshowdown.com/users/{username}"


class MynicknameComConstants:
    NAME = "mynickname.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://mynickname.com/{username}"


class EthereumMagiciansConstants:
    NAME = "Ethereum-magicians"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ethereum-magicians.org/u/{username}/summary"


class GovloopConstants:
    NAME = "Govloop"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.govloop.com/members/{username}"


class DesignspirationConstants:
    NAME = "Designspiration"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://designspiration.com/{username}/"


class PolitforumsConstants:
    NAME = "Politforums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.politforums.net/free/profile.php?showuser={username}"


class IcheckmoviesConstants:
    NAME = "Icheckmovies"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.icheckmovies.com/profiles/{username}"


class CrevadoConstants:
    NAME = "Crevado"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.crevado.com"


class MonkeytypeConstants:
    NAME = "Monkeytype"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://monkeytype.com/profile/{username}"


class E621Constants:
    NAME = "E621"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://e621.net/users/{username}"


class GvectorsConstants:
    NAME = "Gvectors"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gvectors.com/forum/profile/{username}/"


class RollitupConstants:
    NAME = "Rollitup"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.rollitup.org/members/?username={username}"


class RiveAppConstants:
    NAME = "rive.app"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://rive.app/a/{username}"


class MstdnIoConstants:
    NAME = "mstdn.io"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://mstdn.io/@{username}"


class LightstalkingComConstants:
    NAME = "lightstalking.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.lightstalking.com/author/{username}/"


class GuruShotsConstants:
    NAME = "GuruShots"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gurushots.com/{username}/photos"


class WeasylConstants:
    NAME = "Weasyl"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.weasyl.com/~{username}"


class TouristlinkConstants:
    NAME = "Touristlink"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.touristlink.com/user/{username}"


class W7forumsConstants:
    NAME = "W7forums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.w7forums.com/members/?username={username}"


class FragmentConstants:
    NAME = "Fragment"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://fragment.com/username/{username}"


class AllTheLyricsConstants:
    NAME = "AllTheLyrics"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.allthelyrics.com/forum/member.php?username={username}"


class NothingCommunityConstants:
    NAME = "Nothing Community"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://nothing.community/u/{username}"


class ClozemasterConstants:
    NAME = "Clozemaster"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.clozemaster.com/players/{username}"


class N999MdConstants:
    NAME = "999.md"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://999.md/ru/profile/{username}"


class ArrseConstants:
    NAME = "Arrse"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.arrse.co.uk//community/members/?username={username}"


class N1001tracklistsConstants:
    NAME = "1001tracklists"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.1001tracklists.com/user/{username}/index.html"


class LiviosConstants:
    NAME = "Livios"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.livios.be/nl/forum/leden/{username}"


class PronounsPageConstants:
    NAME = "Pronouns.page"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://pronouns.page/@{username}"


class AuConstants:
    NAME = "Au"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://au.ru/user/{username}/"


class ListographyConstants:
    NAME = "Listography"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://listography.com/{username}"


class Millerovo161RuConstants:
    NAME = "millerovo161.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://millerovo161.ru/index/8-0-{username}"


class RlocmanConstants:
    NAME = "Rlocman"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.rlocman.ru/forum/member.php?username={username}"


class Aminus3Constants:
    NAME = "Aminus3"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.aminus3.com/"


class ElixirforumConstants:
    NAME = "Elixirforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://elixirforum.com/u/{username}/summary"


class EGPUConstants:
    NAME = "eGPU"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://egpu.io/forums/profile/{username}/"


class VintageMustangComConstants:
    NAME = "vintage-mustang.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://vintage-mustang.com/members/?username={username}"


class ForumHrConstants:
    NAME = "forum.hr"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.forum.hr/member.php?username={username}"


class School2dobrinkaRuConstants:
    NAME = "school2dobrinka.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://school2dobrinka.ru/index/8-0-{username}"


class JigidiConstants:
    NAME = "Jigidi"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.jigidi.com/user/{username}"


class ChemportConstants:
    NAME = "Chemport"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.chemport.ru/forum/memberlist.php?username={username}"


class SnbforumsConstants:
    NAME = "Snbforums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.snbforums.com/members/?username={username}"


class RedcafeConstants:
    NAME = "Redcafe"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.redcafe.net/members/?username={username}"


class ShowmeConstants:
    NAME = "Showme"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.showme.com/{username}"


class OfficeForumsConstants:
    NAME = "Office-forums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.office-forums.com/members/?username={username}"


class SubaruoutbackOrgConstants:
    NAME = "subaruoutback.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://subaruoutback.org/members/?username={username}"


class SvtperformanceComConstants:
    NAME = "svtperformance.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://svtperformance.com/members/?username={username}"


class RailforumsCoUkConstants:
    NAME = "railforums.co.uk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.railforums.co.uk/members/?username={username}"


class SubaruforesterOrgConstants:
    NAME = "subaruforester.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://subaruforester.org/members/?username={username}"


class RubyForumConstants:
    NAME = "Ruby-forum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.ruby-forum.com/u/{username}/summary"


class BlipfotoConstants:
    NAME = "Blipfoto"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.blipfoto.com/{username}"


class NitroTypeConstants:
    NAME = "Nitro Type"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.nitrotype.com/racer/{username}"


class BlastConstants:
    NAME = "Blast"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.blast.hk/members/?username={username}"


class VishivalochkaRuConstants:
    NAME = "vishivalochka.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://vishivalochka.ru/index/8-0-{username}"


class CSLordsConstants:
    NAME = "CS-Lords"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://cs-lords.ru/index/8-0-{username}"


class NiketalkConstants:
    NAME = "Niketalk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://niketalk.com/members/?username={username}"


class ThefirearmsforumConstants:
    NAME = "Thefirearmsforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.thefirearmsforum.com/members/?username={username}"


class AffiliatefixConstants:
    NAME = "Affiliatefix"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.affiliatefix.com/members/?username={username}"


class SigtalkComConstants:
    NAME = "sigtalk.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://sigtalk.com/members/?username={username}"


class MirStalkeraRuConstants:
    NAME = "mir-stalkera.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://mir-stalkera.ru/index/8-0-{username}"


class MacHelpConstants:
    NAME = "Mac-help"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.mac-help.com/members/?username={username}"


class FlashflashrevolutionConstants:
    NAME = "Flashflashrevolution"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.flashflashrevolution.com/profile/{username}/"


class DMOJConstants:
    NAME = "DMOJ"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://dmoj.ca/user/{username}"


class LadaVestaNetConstants:
    NAME = "lada-vesta.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.lada-vesta.net/member.php?username={username}"


class SysadminsConstants:
    NAME = "Sysadmins"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://sysadmins.ru/member{username}.html"


class JeepgarageOrgConstants:
    NAME = "jeepgarage.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://jeepgarage.org/members/?username={username}"


class N4gameforumConstants:
    NAME = "4gameforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://4gameforum.com/members/?username={username}"


class Spells8Constants:
    NAME = "Spells8"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://forum.spells8.com/u/{username}"


class N101010PlConstants:
    NAME = "101010.pl"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://101010.pl/@{username}"


class CryptoHackConstants:
    NAME = "Crypto Hack"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://cryptohack.org/user/{username}/"


class PiccsyConstants:
    NAME = "Piccsy"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://{username}.piccsy.com/"


class Windows10forumsConstants:
    NAME = "Windows10forums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.windows10forums.com//members/?username={username}"


class IfishNetConstants:
    NAME = "ifish.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://ifish.net/members/?username={username}"


class SwedroidSeConstants:
    NAME = "swedroid.se"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://swedroid.se/forum/members/?username={username}"


class CSSBattleConstants:
    NAME = "CSSBattle"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://cssbattle.dev/player/{username}"


class MacosxConstants:
    NAME = "Macosx"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://macosx.com/members/?username={username}"


class ReligiousForumsConstants:
    NAME = "ReligiousForums"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.religiousforums.com/members/?username={username}"


class Not606ComConstants:
    NAME = "not606.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.not606.com//members/?username={username}"


class GpodderConstants:
    NAME = "Gpodder"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://gpodder.net/user/{username}"


class MdConstants:
    NAME = "md"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://forum.md/ru/users/{username}"


class ImoodConstants:
    NAME = "Imood"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.imood.com/users/{username}"


class ArmtorgConstants:
    NAME = "Armtorg"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://armtorg.ru//forum/memberlist.php?username={username}"


class RusspussRuConstants:
    NAME = "russpuss.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.russpuss.ru/profile/{username}/"


class VTwinforumComConstants:
    NAME = "v-twinforum.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://v-twinforum.com/members/?username={username}"


class FanficslandiaComConstants:
    NAME = "fanficslandia.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://fanficslandia.com/index.php/members/?username={username}"


class QbnConstants:
    NAME = "Qbn"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.qbn.com/{username}"


class LkforumConstants:
    NAME = "Lkforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.lkforum.ru//member.php?username={username}"


class ClubsnapComConstants:
    NAME = "clubsnap.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.clubsnap.com//members/?username={username}"


class WolpyConstants:
    NAME = "Wolpy"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://wolpy.com/{username}/profile"


class WarframeMarketConstants:
    NAME = "Warframe Market"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://warframe.market/profile/{username}"


class CubecraftNetConstants:
    NAME = "cubecraft.net"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.cubecraft.net/members/?username={username}"


class TvGamesConstants:
    NAME = "Tv-games"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://tv-games.ru//forum/member.php?username={username}"


class SniperforumsComConstants:
    NAME = "sniperforums.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://sniperforums.com/members/?username={username}"


class IzobilRuConstants:
    NAME = "izobil.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://izobil.ru/index/8-0-{username}"


class GoldroyalConstants:
    NAME = "Goldroyal"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://goldroyal.net/member.php?username={username}"


class FCRubinConstants:
    NAME = "FCRubin"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.fcrubin.ru/forum/member.php?username={username}"


class OakleyforumComConstants:
    NAME = "oakleyforum.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.oakleyforum.com/members/?username={username}"


class HuntingConstants:
    NAME = "hunting"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.hunting.ru/forum/members/?username={username}"


class UvelirConstants:
    NAME = "Uvelir"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://uvelir.net//member.php?username={username}"


class ThelionConstants:
    NAME = "Thelion"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.thelion.com/bin/profile.cgi?c=s&ru_name={username}"


class XShakerConstants:
    NAME = "XShaker"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.xshaker.net/{username}.html"


class NucastleCoUkConstants:
    NAME = "nucastle.co.uk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.nucastle.co.uk//members/?username={username}"


class RealmeyeConstants:
    NAME = "Realmeye"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.realmeye.com/player/{username}"


class HitmanforumConstants:
    NAME = "Hitmanforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.hitmanforum.com/u/{username}/summary"


class DatingRuConstants:
    NAME = "Dating.Ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://dating.ru/{username}"


class VolgogradForumConstants:
    NAME = "Volgograd Forum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.forum-volgograd.ru/members/?username={username}"


class TigerfanComConstants:
    NAME = "tigerfan.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.tigerfan.com//members/?username={username}"


class ImpalaforumsComConstants:
    NAME = "impalaforums.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://impalaforums.com/members/?username={username}"


class ForumJizniConstants:
    NAME = "ForumJizni"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.forumjizni.ru/member.php?username={username}"


class XgmGuruConstants:
    NAME = "xgm.guru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://xgm.guru/user/{username}"


class TexasguntalkConstants:
    NAME = "Texasguntalk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.texasguntalk.com/members/?username={username}"


class PolitikforumConstants:
    NAME = "Politikforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.politikforum.ru//member.php?username={username}"


class TruthbookConstants:
    NAME = "Truthbook"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://truthbook.com/forum/memberlist.php?username={username}"


class DefenceForumIndiaConstants:
    NAME = "DefenceForumIndia"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://defenceforumindia.com//members/?username={username}"


class ForumsDromRuConstants:
    NAME = "forums.drom.ru"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.forumsdrom.ru/member.php?username={username}"


class AntiqueBottlesConstants:
    NAME = "Antique-bottles"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.antique-bottles.net/members/?username={username}"


class RidemonkeyComConstants:
    NAME = "ridemonkey.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.ridemonkey.com/members/?username={username}"


class DiscussfastpitchConstants:
    NAME = "Discussfastpitch"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.discussfastpitch.com/members/?username={username}"


class AvtoForumNameConstants:
    NAME = "Avto-forum.name"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://avto-forum.name/members/?username={username}"


class SpacesConstants:
    NAME = "Spaces"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://spaces.im/mysite/index/{username}/"


class RussianFIConstants:
    NAME = "RussianFI"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.russian.fi//forum/member.php?username={username}"


class XtratimeOrgConstants:
    NAME = "xtratime.org"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.xtratime.org/members/?username={username}"


class NikoncafeComConstants:
    NAME = "nikoncafe.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.nikoncafe.com//members/?username={username}"


class CowboyszoneComConstants:
    NAME = "cowboyszone.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://cowboyszone.com/members/?username={username}"


class ThebuddyforumConstants:
    NAME = "Thebuddyforum"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.thebuddyforum.com/members/?username={username}"


class VauxhallownersnetworkCoUkConstants:
    NAME = "vauxhallownersnetwork.co.uk"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.vauxhallownersnetwork.co.uk/members/?username={username}"


class ErogenClubConstants:
    NAME = "Erogen.club"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://erogen.club/members/?username={username}"


class MineplexComConstants:
    NAME = "mineplex.com"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://www.mineplex.com/members/?username={username}"


class CodersRankConstants:
    NAME = "Coders Rank"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://profile.codersrank.io/user/{username}/"


class WorldofplayersConstants:
    NAME = "Worldofplayers"
    CRAWL_TYPE = "unverified"
    PROFILE_URL = "https://worldofplayers.ru/members/?username={username}"
