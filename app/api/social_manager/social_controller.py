from typing import Dict, Any, cast
from urllib.parse import urlparse

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.helper_methods.social_recon import social_recon
from api.social_manager.helper_methods.phone_recon import phone_recon
from api.social_manager.sessions.playwright_session import playwright_session
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.post_supported._instagram import _instagram as InstagramScraper
from api.social_manager.scrapers.post_supported._facebook import _facebook as FacebookScraper
from api.social_manager.scrapers.post_supported._twitter import _twitter as TwitterScraper
from api.social_manager.scrapers.post_supported._tiktok import _tiktok as TikTokScraper
from api.social_manager.scrapers.post_supported._youtube import _youtube as YoutubeScraper
from api.social_manager.scrapers.post_supported._reddit import _reddit as RedditScraper
from api.social_manager.scrapers.post_supported._mastodon import _mastodon as MastodonScraper
from api.social_manager.scrapers.post_supported._linkedin import _linkedin as LinkedInScraper
from api.social_manager.scrapers.post_supported._pastebin import _pastebin as PastebinScraper
from api.social_manager.scrapers.other._about_me import _about_me as PlatformScraper_about_me
from api.social_manager.scrapers.other._ameba_blog import _ameba_blog as PlatformScraper_ameba_blog
from api.social_manager.scrapers.other._anilist import _anilist as PlatformScraper_anilist
from api.social_manager.scrapers.other._anime_planet import _anime_planet as PlatformScraper_anime_planet
from api.social_manager.scrapers.other._aparat import _aparat as PlatformScraper_aparat
from api.social_manager.scrapers.other._archive_org import _archive_org as PlatformScraper_archive_org
from api.social_manager.scrapers.other._archiveofourown import _archiveofourown as PlatformScraper_archiveofourown
from api.social_manager.scrapers.other._artstation import _artstation as PlatformScraper_artstation
from api.social_manager.scrapers.other._audiomack import _audiomack as PlatformScraper_audiomack
from api.social_manager.scrapers.other._bandcamp import _bandcamp as PlatformScraper_bandcamp
from api.social_manager.scrapers.other._beacons import _beacons as PlatformScraper_beacons
from api.social_manager.scrapers.other._behance import _behance as PlatformScraper_behance
from api.social_manager.scrapers.other._bigo_live import _bigo_live as PlatformScraper_bigo_live
from api.social_manager.scrapers.other._bio_site import _bio_site as PlatformScraper_bio_site
from api.social_manager.scrapers.other._bitbucket import _bitbucket as PlatformScraper_bitbucket
from api.social_manager.scrapers.other._bitchute import _bitchute as PlatformScraper_bitchute
from api.social_manager.scrapers.post_supported._blogger import _blogger as PlatformScraper_blogger
from api.social_manager.scrapers.post_supported._bluesky import _bluesky as PlatformScraper_bluesky
from api.social_manager.scrapers.other._buymeacoffee import _buymeacoffee as PlatformScraper_buymeacoffee
from api.social_manager.scrapers.other._cara import _cara as PlatformScraper_cara
from api.social_manager.scrapers.other._carrd import _carrd as PlatformScraper_carrd
from api.social_manager.scrapers.other._chess_com import _chess_com as PlatformScraper_chess_com
from api.social_manager.scrapers.other._codepen import _codepen as PlatformScraper_codepen
from api.social_manager.scrapers.other._dailymotion import _dailymotion as PlatformScraper_dailymotion
from api.social_manager.scrapers.post_supported._devto import _devto as PlatformScraper_devto
from api.social_manager.scrapers.other._dlive import _dlive as PlatformScraper_dlive
from api.social_manager.scrapers.other._dockerhub import _dockerhub as PlatformScraper_dockerhub
from api.social_manager.scrapers.other._douban import _douban as PlatformScraper_douban
from api.social_manager.scrapers.other._douyin import _douyin as PlatformScraper_douyin
from api.social_manager.scrapers.other._ebay_profiles import _ebay_profiles as PlatformScraper_ebay_profiles
from api.social_manager.scrapers.other._ello import _ello as PlatformScraper_ello
from api.social_manager.scrapers.other._genius import _genius as PlatformScraper_genius
from api.social_manager.scrapers.other._gettr import _gettr as PlatformScraper_gettr
from api.social_manager.scrapers.other._giphy import _giphy as PlatformScraper_giphy
from api.social_manager.scrapers.other._gitea_public import _gitea_public as PlatformScraper_gitea_public
from api.social_manager.scrapers.other._github import _github as PlatformScraper_github
from api.social_manager.scrapers.other._github_sponsors import _github_sponsors as PlatformScraper_github_sponsors
from api.social_manager.scrapers.other._gitlab import _gitlab as PlatformScraper_gitlab
from api.social_manager.scrapers.other._goodreads import _goodreads as PlatformScraper_goodreads
from api.social_manager.scrapers.other._gumroad import _gumroad as PlatformScraper_gumroad
from api.social_manager.scrapers.post_supported._habr import _habr as PlatformScraper_habr
from api.social_manager.scrapers.post_supported._hackernoon import _hackernoon as PlatformScraper_hackernoon
from api.social_manager.scrapers.post_supported._hashnode import _hashnode as PlatformScraper_hashnode
from api.social_manager.scrapers.other._hatena_blog import _hatena_blog as PlatformScraper_hatena_blog
from api.social_manager.scrapers.other._hearthis import _hearthis as PlatformScraper_hearthis
from api.social_manager.scrapers.other._imgur import _imgur as PlatformScraper_imgur
from api.social_manager.scrapers.other._indiehackers import _indiehackers as PlatformScraper_indiehackers
from api.social_manager.scrapers.other._issuu import _issuu as PlatformScraper_issuu
from api.social_manager.scrapers.other._kakaostory import _kakaostory as PlatformScraper_kakaostory
from api.social_manager.scrapers.other._kick import _kick as PlatformScraper_kick
from api.social_manager.scrapers.other._komoot import _komoot as PlatformScraper_komoot
from api.social_manager.scrapers.other._kuaishou import _kuaishou as PlatformScraper_kuaishou
from api.social_manager.scrapers.other._lastfm import _lastfm as PlatformScraper_lastfm
from api.social_manager.scrapers.other._letterboxd import _letterboxd as PlatformScraper_letterboxd
from api.social_manager.scrapers.other._liberapay import _liberapay as PlatformScraper_liberapay
from api.social_manager.scrapers.other._librarything import _librarything as PlatformScraper_librarything
from api.social_manager.scrapers.other._lichess import _lichess as PlatformScraper_lichess
from api.social_manager.scrapers.other._likee import _likee as PlatformScraper_likee
from api.social_manager.scrapers.other._line_voom import _line_voom as PlatformScraper_line_voom
from api.social_manager.scrapers.other._linktree import _linktree as PlatformScraper_linktree
from api.social_manager.scrapers.other._livejournal import _livejournal as PlatformScraper_livejournal
from api.social_manager.scrapers.other._lnk_bio import _lnk_bio as PlatformScraper_lnk_bio
from api.social_manager.scrapers.post_supported._medium import _medium as PlatformScraper_medium
from api.social_manager.scrapers.other._mewe import _mewe as PlatformScraper_mewe
from api.social_manager.scrapers.post_supported._microblog import _microblog as PlatformScraper_microblog
from api.social_manager.scrapers.other._milkshake import _milkshake as PlatformScraper_milkshake
from api.social_manager.scrapers.post_supported._misskey import _misskey as PlatformScraper_misskey
from api.social_manager.scrapers.other._mixcloud import _mixcloud as PlatformScraper_mixcloud
from api.social_manager.scrapers.other._mixi import _mixi as PlatformScraper_mixi
from api.social_manager.scrapers.other._msha_ke import _msha_ke as PlatformScraper_msha_ke
from api.social_manager.scrapers.other._myanimelist import _myanimelist as PlatformScraper_myanimelist
from api.social_manager.scrapers.other._naver_blog import _naver_blog as PlatformScraper_naver_blog
from api.social_manager.scrapers.other._niconico import _niconico as PlatformScraper_niconico
from api.social_manager.scrapers.post_supported._nostr import _nostr as PlatformScraper_nostr
from api.social_manager.scrapers.other._npm import _npm as PlatformScraper_npm
from api.social_manager.scrapers.other._observable import _observable as PlatformScraper_observable
from api.social_manager.scrapers.other._odysee import _odysee as PlatformScraper_odysee
from api.social_manager.scrapers.other._ok_ru import _ok_ru as PlatformScraper_ok_ru
from api.social_manager.scrapers.other._opencollective import _opencollective as PlatformScraper_opencollective
from api.social_manager.scrapers.other._packagist import _packagist as PlatformScraper_packagist
from api.social_manager.scrapers.other._patreon import _patreon as PlatformScraper_patreon
from api.social_manager.scrapers.other._pinterest import _pinterest as PlatformScraper_pinterest
from api.social_manager.scrapers.other._pixnet import _pixnet as PlatformScraper_pixnet
from api.social_manager.scrapers.post_supported._pleroma import _pleroma as PlatformScraper_pleroma
from api.social_manager.scrapers.other._plurk import _plurk as PlatformScraper_plurk
from api.social_manager.scrapers.post_supported._primal import _primal as PlatformScraper_primal
from api.social_manager.scrapers.other._producthunt import _producthunt as PlatformScraper_producthunt
from api.social_manager.scrapers.other._pypi import _pypi as PlatformScraper_pypi
from api.social_manager.scrapers.other._quay import _quay as PlatformScraper_quay
from api.social_manager.scrapers.post_supported._quora import _quora as PlatformScraper_quora
from api.social_manager.scrapers.other._redbubble import _redbubble as PlatformScraper_redbubble
from api.social_manager.scrapers.other._rednote import _rednote as PlatformScraper_rednote
from api.social_manager.scrapers.other._rubygems import _rubygems as PlatformScraper_rubygems
from api.social_manager.scrapers.other._semantic_scholar import _semantic_scholar as PlatformScraper_semantic_scholar
from api.social_manager.scrapers.other._sketchfab import _sketchfab as PlatformScraper_sketchfab
from api.social_manager.scrapers.other._smugmug import _smugmug as PlatformScraper_smugmug
from api.social_manager.scrapers.other._snapchat_public import _snapchat_public as PlatformScraper_snapchat_public
from api.social_manager.scrapers.other._solo_to import _solo_to as PlatformScraper_solo_to
from api.social_manager.scrapers.other._sourceforge import _sourceforge as PlatformScraper_sourceforge
from api.social_manager.scrapers.post_supported._stackoverflow import _stackoverflow as PlatformScraper_stackoverflow
from api.social_manager.scrapers.other._steam_community import _steam_community as PlatformScraper_steam_community
from api.social_manager.scrapers.post_supported._substack import _substack as PlatformScraper_substack
from api.social_manager.scrapers.other._taplink import _taplink as PlatformScraper_taplink
from api.social_manager.scrapers.other._tencent_video import _tencent_video as PlatformScraper_tencent_video
from api.social_manager.scrapers.post_supported._threads import _threads as PlatformScraper_threads
from api.social_manager.scrapers.other._tistory import _tistory as PlatformScraper_tistory
from api.social_manager.scrapers.other._triller import _triller as PlatformScraper_triller
from api.social_manager.scrapers.other._tudou import _tudou as PlatformScraper_tudou
from api.social_manager.scrapers.other._twitch import _twitch as PlatformScraper_twitch
from api.social_manager.scrapers.other._unsplash import _unsplash as PlatformScraper_unsplash
from api.social_manager.scrapers.other._vimeo import _vimeo as PlatformScraper_vimeo
from api.social_manager.scrapers.other._vsco import _vsco as PlatformScraper_vsco
from api.social_manager.scrapers.other._weibo import _weibo as PlatformScraper_weibo
from api.social_manager.scrapers.other._write_as import _write_as as PlatformScraper_write_as
from api.social_manager.scrapers.other._xing import _xing as PlatformScraper_xing
from api.social_manager.scrapers.live_search.live_search_handler import live_search_handler
from crawler.crawler_instance.local_shared_model.rule_model import FetchProxy, SocialDataType


PUBLIC_SOCIAL_SCRAPERS = {
    "about_me": PlatformScraper_about_me,
    "ameba_blog": PlatformScraper_ameba_blog,
    "anilist": PlatformScraper_anilist,
    "anime_planet": PlatformScraper_anime_planet,
    "aparat": PlatformScraper_aparat,
    "archive_org": PlatformScraper_archive_org,
    "archiveofourown": PlatformScraper_archiveofourown,
    "artstation": PlatformScraper_artstation,
    "audiomack": PlatformScraper_audiomack,
    "bandcamp": PlatformScraper_bandcamp,
    "beacons": PlatformScraper_beacons,
    "behance": PlatformScraper_behance,
    "bigo_live": PlatformScraper_bigo_live,
    "bio_site": PlatformScraper_bio_site,
    "bitbucket": PlatformScraper_bitbucket,
    "bitchute": PlatformScraper_bitchute,
    "blogger": PlatformScraper_blogger,
    "bluesky": PlatformScraper_bluesky,
    "buymeacoffee": PlatformScraper_buymeacoffee,
    "cara": PlatformScraper_cara,
    "carrd": PlatformScraper_carrd,
    "chess_com": PlatformScraper_chess_com,
    "codepen": PlatformScraper_codepen,
    "dailymotion": PlatformScraper_dailymotion,
    "devto": PlatformScraper_devto,
    "dlive": PlatformScraper_dlive,
    "dockerhub": PlatformScraper_dockerhub,
    "douban": PlatformScraper_douban,
    "douyin": PlatformScraper_douyin,
    "ebay_profiles": PlatformScraper_ebay_profiles,
    "ello": PlatformScraper_ello,
    "genius": PlatformScraper_genius,
    "gettr": PlatformScraper_gettr,
    "giphy": PlatformScraper_giphy,
    "gitea_public": PlatformScraper_gitea_public,
    "github": PlatformScraper_github,
    "github_sponsors": PlatformScraper_github_sponsors,
    "gitlab": PlatformScraper_gitlab,
    "goodreads": PlatformScraper_goodreads,
    "gumroad": PlatformScraper_gumroad,
    "habr": PlatformScraper_habr,
    "hackernoon": PlatformScraper_hackernoon,
    "hashnode": PlatformScraper_hashnode,
    "hatena_blog": PlatformScraper_hatena_blog,
    "hearthis": PlatformScraper_hearthis,
    "imgur": PlatformScraper_imgur,
    "indiehackers": PlatformScraper_indiehackers,
    "issuu": PlatformScraper_issuu,
    "kakaostory": PlatformScraper_kakaostory,
    "kick": PlatformScraper_kick,
    "komoot": PlatformScraper_komoot,
    "kuaishou": PlatformScraper_kuaishou,
    "lastfm": PlatformScraper_lastfm,
    "letterboxd": PlatformScraper_letterboxd,
    "liberapay": PlatformScraper_liberapay,
    "librarything": PlatformScraper_librarything,
    "lichess": PlatformScraper_lichess,
    "likee": PlatformScraper_likee,
    "line_voom": PlatformScraper_line_voom,
    "linktree": PlatformScraper_linktree,
    "livejournal": PlatformScraper_livejournal,
    "lnk_bio": PlatformScraper_lnk_bio,
    "medium": PlatformScraper_medium,
    "mewe": PlatformScraper_mewe,
    "microblog": PlatformScraper_microblog,
    "milkshake": PlatformScraper_milkshake,
    "misskey": PlatformScraper_misskey,
    "mixcloud": PlatformScraper_mixcloud,
    "mixi": PlatformScraper_mixi,
    "msha_ke": PlatformScraper_msha_ke,
    "myanimelist": PlatformScraper_myanimelist,
    "naver_blog": PlatformScraper_naver_blog,
    "niconico": PlatformScraper_niconico,
    "nostr": PlatformScraper_nostr,
    "npm": PlatformScraper_npm,
    "observable": PlatformScraper_observable,
    "odysee": PlatformScraper_odysee,
    "ok_ru": PlatformScraper_ok_ru,
    "opencollective": PlatformScraper_opencollective,
    "packagist": PlatformScraper_packagist,
    "patreon": PlatformScraper_patreon,
    "pinterest": PlatformScraper_pinterest,
    "pixnet": PlatformScraper_pixnet,
    "pleroma": PlatformScraper_pleroma,
    "plurk": PlatformScraper_plurk,
    "primal": PlatformScraper_primal,
    "producthunt": PlatformScraper_producthunt,
    "pypi": PlatformScraper_pypi,
    "quay": PlatformScraper_quay,
    "quora": PlatformScraper_quora,
    "redbubble": PlatformScraper_redbubble,
    "rednote": PlatformScraper_rednote,
    "rubygems": PlatformScraper_rubygems,
    "semantic_scholar": PlatformScraper_semantic_scholar,
    "sketchfab": PlatformScraper_sketchfab,
    "smugmug": PlatformScraper_smugmug,
    "snapchat_public": PlatformScraper_snapchat_public,
    "solo_to": PlatformScraper_solo_to,
    "sourceforge": PlatformScraper_sourceforge,
    "stackoverflow": PlatformScraper_stackoverflow,
    "steam_community": PlatformScraper_steam_community,
    "substack": PlatformScraper_substack,
    "taplink": PlatformScraper_taplink,
    "tencent_video": PlatformScraper_tencent_video,
    "threads": PlatformScraper_threads,
    "tistory": PlatformScraper_tistory,
    "triller": PlatformScraper_triller,
    "tudou": PlatformScraper_tudou,
    "twitch": PlatformScraper_twitch,
    "unsplash": PlatformScraper_unsplash,
    "vimeo": PlatformScraper_vimeo,
    "vsco": PlatformScraper_vsco,
    "weibo": PlatformScraper_weibo,
    "write_as": PlatformScraper_write_as,
    "xing": PlatformScraper_xing,
}


class social_controller:

    def __init__(self):
        self._recon = social_recon()
        self._phone_recon = phone_recon()
        self._progress = progress_controller.get_instance()
        self.job_id = None
        self.command = None
        self._ddg = live_search_handler()

    def init_job(self, job_id: str, command):
        self.job_id = job_id
        self._progress.init(job_id)
        self.command = command
        self._progress.update(job_id, 0, "starting")

    @staticmethod
    def _clean_str(value: Any, default: str = "") -> str:
        if value is None:
            return default
        return str(value).strip()

    @staticmethod
    def _clean_lower(value: Any, default: str = "") -> str:
        return social_controller._clean_str(value, default).lower()

    @staticmethod
    def _int_value(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _bytes_value(value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        return b""

    @staticmethod
    def _list_str_value(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    @staticmethod
    def _safe_direct_url(value: str) -> str | None:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None
        if parsed.scheme == "https":
            return value
        return parsed._replace(scheme="https").geturl()

    @staticmethod
    def _scraper_name(scraper: Any) -> str:
        return getattr(scraper, "name", scraper.__class__.__name__.lstrip("_") or "scraper")

    @staticmethod
    def _social_data_type_for_command(command: int | None) -> SocialDataType:
        if command == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
            return SocialDataType.PROFILE
        if command == SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY:
            return SocialDataType.FOLLOWERS
        if command == SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY:
            return SocialDataType.FOLLOWING
        if command == SOCIAL_REQUEST_COMMANDS.S_POSTS:
            return SocialDataType.POSTS
        if command == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
            return SocialDataType.VIDEOS
        if command == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
            return SocialDataType.SHORTS
        return SocialDataType.DEFAULT

    @staticmethod
    def _social_seed_url(platform: str, username: str, target_type: str | None = None) -> str:
        username = (username or "").strip()
        target_type = (target_type or "profile").strip().lower()
        direct_url = social_controller._safe_direct_url(username)
        if direct_url:
            return direct_url
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            return f"https://www.instagram.com/{username.lstrip('@').strip('/')}/"
        if platform == SOCIAL_PLATFORMS.FACEBOOK:
            if target_type == "group":
                return f"https://www.facebook.com/groups/{username.strip().strip('/')}"
            return f"https://www.facebook.com/{username.strip().strip('/')}"
        if platform == SOCIAL_PLATFORMS.TWITTER:
            return f"https://x.com/{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.TIKTOK:
            return f"https://www.tiktok.com/@{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.YOUTUBE:
            return f"https://www.youtube.com/@{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.REDDIT:
            handle = username.strip().strip("/")
            reddit_path = handle
            if handle.startswith(("r/", "u/", "user/")):
                reddit_path = handle
            elif target_type == "profile":
                reddit_path = f"user/{handle}"
            else:
                reddit_path = f"r/{handle}"
            return RedditScraper._to_reddit_url(f"https://old.reddit.com/{reddit_path}/")
        if platform == SOCIAL_PLATFORMS.MASTODON:
            handle = username.lstrip("@")
            if "@" in handle:
                account, host = handle.split("@", 1)
                return f"https://{host}/@{account}"
            return f"https://mastodon.social/@{handle}"
        if platform == SOCIAL_PLATFORMS.LINKEDIN:
            return LinkedInScraper.build_seed_url(username, SocialDataType.POSTS, target_type)
        if platform == SOCIAL_PLATFORMS.PASTEBIN:
            return f"https://pastebin.com/u/{username.lstrip('@').strip('/')}"
        scraper_class = PUBLIC_SOCIAL_SCRAPERS.get(platform)
        if scraper_class and hasattr(scraper_class, "build_seed_url"):
            return scraper_class.build_seed_url(username, target_type=target_type)
        return username

    @staticmethod
    def _session_for_scraper(scraper: Any):
        import os
        proxy = None
        if hasattr(scraper, 'rule_config') and getattr(scraper.rule_config, 'm_fetch_proxy', None) == FetchProxy.TOR:
            tor_url = os.getenv("TOR_PROXY_URL") or "socks5://trusted-social_tor_instace_1:9552"
            tor_url = tor_url.replace("socks5h://", "socks5://")
            proxy = {"server": tor_url}
            
        data_type = getattr(scraper, "m_social_data_type", None)
        profile_data_types = {
            SocialDataType.PROFILE,
            SocialDataType.CHANNEL,
            SocialDataType.FOLLOWERS,
            SocialDataType.FOLLOWING,
        }
        if data_type in profile_data_types:
            return playwright_session(headless=True, blocked_resources=set(), proxy=proxy)

        if isinstance(scraper, (InstagramScraper, TwitterScraper, YoutubeScraper)):
            return playwright_session(headless=True, blocked_resources=set(), proxy=proxy)
        return playwright_session(headless=True, proxy=proxy)

    def _get_scraper(self, platform: str, username: str, max_followers: int, max_following: int, target_type: str | None = None) -> Any | None:
        platform = (platform or "").strip().lower()
        scraper_class = {
            SOCIAL_PLATFORMS.INSTAGRAM: InstagramScraper,
            SOCIAL_PLATFORMS.FACEBOOK: FacebookScraper,
            SOCIAL_PLATFORMS.TWITTER: TwitterScraper,
            SOCIAL_PLATFORMS.TIKTOK: TikTokScraper,
            SOCIAL_PLATFORMS.YOUTUBE: YoutubeScraper,
            SOCIAL_PLATFORMS.REDDIT: RedditScraper,
            SOCIAL_PLATFORMS.MASTODON: MastodonScraper,
            SOCIAL_PLATFORMS.LINKEDIN: LinkedInScraper,
            SOCIAL_PLATFORMS.PASTEBIN: PastebinScraper,
        }.get(platform) or PUBLIC_SOCIAL_SCRAPERS.get(platform)
        if not scraper_class:
            return None
        if platform == SOCIAL_PLATFORMS.LINKEDIN and self.command != SOCIAL_REQUEST_COMMANDS.S_POSTS:
            return None

        scraper = cast(Any, scraper_class)()
        if hasattr(scraper, "_card_data"):
            scraper._card_data = []
        if hasattr(scraper, "_entity_data"):
            scraper._entity_data = []
        scraper.m_social_data_type = self._social_data_type_for_command(self.command)
        scraper.m_target_type = (target_type or "profile").strip().lower()
        if platform in PUBLIC_SOCIAL_SCRAPERS and hasattr(scraper, "build_seed_url"):
            scraper.m_seed_url = scraper.build_seed_url(username, scraper.m_social_data_type, scraper.m_target_type)
        else:
            scraper.m_seed_url = self._social_seed_url(platform, username, scraper.m_target_type)
        scraper.m_followers_limit = max_followers
        scraper.m_following_limit = max_following
        scraper.m_max_followers = max_followers
        scraper.m_max_following = max_following
        return scraper

    @staticmethod
    def _parse_scraper(scraper: Any, page: Any) -> Any:
        result = scraper.parse_leak_data(page)
        if result is None or isinstance(result, bool):
            return getattr(scraper, "card_data", [])
        return result

    @staticmethod
    def _goto_seed(page: Any, url: str) -> None:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
        except Exception:
            pass

    def _run_scraper(self, scraper: Any, page: Any) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": self._scraper_name(scraper)}
            self._goto_seed(page, scraper.seed_url)
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded", timeout=25000)
        else:
            self._goto_seed(page, scraper.seed_url)
        return {"status": "success", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_posts_scraper(self, scraper: Any, page: Any, max_posts: int) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": self._scraper_name(scraper)}
            self._goto_seed(page, scraper.seed_url)
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded", timeout=25000)
        else:
            self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_posts, 10), 100))
        scraper.m_social_data_type = SocialDataType.POSTS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_videos_scraper(self, scraper: Any, page: Any, max_videos: int) -> Dict[str, Any]:
        self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_videos, 10), 100))
        scraper.m_social_data_type = SocialDataType.VIDEOS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_shorts_scraper(self, scraper: Any, page: Any, max_shorts: int) -> Dict[str, Any]:
        self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_shorts, 10), 100))
        scraper.m_social_data_type = SocialDataType.SHORTS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _scrape_user(self, platform, username, max_followers, max_following, target_type: str | None = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, max_followers, max_following, target_type)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_scraper(scraper, s.page)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_posts(self, platform, username, max_posts: int, target_type: str | None = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0, target_type)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_posts_scraper(scraper, s.page, max_posts)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_videos(self, platform, username, max_videos: int, target_type: str | None = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0, target_type)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_videos_scraper(scraper, s.page, max_videos)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_shorts(self, platform, username, max_shorts: int, target_type: str | None = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0, target_type)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_shorts_scraper(scraper, s.page, max_shorts)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def invoke_trigger(self, command: int, data: Any = None) -> Any:
        data = data if isinstance(data, dict) else {}
        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_USER:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                mode = self._clean_str(data.get("mode"), "default")
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(username, mode, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_PHONE:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                phone = self._clean_str(data.get("phone"))
                if not phone:
                    result = {"status": "error", "message": "phone_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                mode = self._clean_str(data.get("mode"), "default")
                result = {"status": "success", "platform": "recon_phone", "data": self._phone_recon.parse_phone(phone, mode, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command in {
            SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY,
        }:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                target_type = self._clean_lower(data.get("target_type") or data.get("source_type") or data.get("profile_type"), "profile")
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result

                followers_following_supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.PASTEBIN,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.BEHANCE,
                    SOCIAL_PLATFORMS.VIMEO,
                ]

                if command in {SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY} and platform not in followers_following_supported_platforms:
                    result = {"status": "error", "message": f"{platform}_followers_following_not_supported", "data": None}
                    self._progress.done(self.job_id, result)
                    return result

                supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.PASTEBIN,
                ]
                if command == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY and platform not in supported_platforms and platform not in PUBLIC_SOCIAL_SCRAPERS:
                    ddg_result = self._ddg.scrape_profile(username, platform)
                    result = {"status": "suggested", "data": ddg_result}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_user(
                    platform,
                    username,
                    self._int_value(data.get("max_followers"), 0),
                    self._int_value(data.get("max_following"), 0),
                    target_type,
                )
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                target_type = self._clean_lower(data.get("target_type") or data.get("source_type") or data.get("profile_type"), "profile")
                max_videos = self._int_value(data.get("max_videos"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_videos(platform, username, max_videos, target_type)
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                target_type = self._clean_lower(data.get("target_type") or data.get("source_type") or data.get("profile_type"), "profile")
                max_shorts = self._int_value(data.get("max_shorts"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_shorts(platform, username, max_shorts, target_type)
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                file_bytes = self._bytes_value(data.get("file_bytes"))
                filename = self._clean_str(data.get("filename"))
                if not file_bytes:
                    result = {"status": "error", "message": "image_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "recon_image", "data": self._recon.parse_image(file_bytes, filename=filename, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_POSTS:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                target_type = self._clean_lower(data.get("target_type") or data.get("source_type") or data.get("profile_type"), "profile")
                max_posts = self._int_value(data.get("max_posts"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                native_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.LINKEDIN,
                    SOCIAL_PLATFORMS.PASTEBIN,
                ]
                if platform in native_platforms or platform in PUBLIC_SOCIAL_SCRAPERS:
                    result = self._scrape_posts(platform, username, max_posts, target_type)
                    self._progress.done(self.job_id, result)
                    return result
                ddg_result = self._ddg.scrape_posts_search(username, platform, max_posts)
                result = {
                    "status": "suggested",
                    "platform": platform,
                    "data": ddg_result.get("posts", []),
                }
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                platform = self._clean_str(data.get("platform"))
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.collect_social_handles(username, platform or None)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_str(data.get("platform"))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.scrape_images(username, platform or "", limit=10)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA:   
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                tokens = self._list_str_value(data.get("tokens"))
                username = self._clean_str(data.get("username")) or None
                platform = self._clean_str(data.get("platform")) or None
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.search_web(tokens, username, platform)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        return None

    def get_scrape_status(self, job_id: str) -> Dict[str, Any]:
        return self._progress.get(job_id)

    def clear_scrape_status(self, job_id: str) -> None:
        self._progress.error(job_id, "cleared")
