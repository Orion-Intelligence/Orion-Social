from enum import Enum

class FetchConfig(str, Enum):
    PLAYRIGHT = "playright"
    REQUESTS = "requests"
    API = "api"

class SocialDataType(str, Enum):
    DEFAULT = "default"
    PROFILE = "profile_info"
    CHANNEL = "channel_info"
    POSTS = "posts"
    VIDEOS = "videos"
    SHORTS = "shorts"
    COMMENTS = "comments"
    FOLLOWERS = "followers"
    FOLLOWING = "following"

class ThreatType(str, Enum):
    DEFACEMENT = "defacement_collector"
    API = "api_collector"
    LEAK = "leak_collector"
    GENERIC = "general_collector"
    EXPLOIT = "exploit_collector"
    NEWS = "news_collector"
    TWITTER = "tweek_collector"
    REDDIT = "reddit_collector"
    SOCIAL = "social_collector"
    TIKTOK = "tiktok_collector"
    FORUM = "forum_collector"
    TRACKING = "tracking_collector"
    PASTEBIN = "pastebin_collector"
    MASTODON = "mastodon_collector"
    YOUTUBE = "youtube_collector"
    FACEBOOK = "facebook_collector"
    INSTAGRAM = "instagram_collector"
    LINKEDIN = "linkedin_collector"
    DISCORD = "discord_collector"
    WHATSAPP = "whatsapp_collector"

class RuleType(str, Enum):
    BLOGGER = "blogger"
    BLUESKY = "bluesky"
    DEVTO = "devto"
    DEFACEMENT = "defacement"
    EXPLOIT = "exploit"
    HABR = "habr"
    HACKERNOON = "hackernoon"
    HASHNODE = "hashnode"
    FORUM = "forum"
    GENERIC = "generic"
    LEAK = "leak"
    MASTODON = "mastodon"
    MEDIUM = "medium"
    MICROBLOG = "microblog"
    MISSKEY = "misskey"
    NEWS = "news"
    NOSTR = "nostr"
    PASTEBIN = "pastebin"
    PLEROMA = "pleroma"
    PRIMAL = "primal"
    QUORA = "quora"
    REDDIT = "reddit"
    STACKOVERFLOW = "stackoverflow"
    SUBSTACK = "substack"
    TRACKING = "tracking"
    THREADS = "threads"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    DISCORD = "discord"
    WHATSAPP = "whatsapp"


class FetchProxy(str, Enum):
    TOR = "tor"
    NONE = "none"

class RuleModel:
    def __init__(self, m_timeout: int = 177200, m_fetch_config: FetchConfig = FetchConfig.PLAYRIGHT, m_fetch_proxy: FetchProxy = FetchProxy.NONE, m_javascript = True, m_resoource_block = True, m_threat_type: ThreatType | None = None, m_rule_type: RuleType | None = None, m_social_data_type:SocialDataType|None=SocialDataType.DEFAULT, m_block_default_javascript = True, m_user_agent: bool = True):
        if not isinstance(m_threat_type, ThreatType):
            raise ValueError(f"RuleModel.m_threat_type must be a ThreatType, got {m_threat_type!r}")
        if m_social_data_type is not None:
            if not isinstance(m_social_data_type, SocialDataType):
                raise ValueError(f"Invalid SocialDataType: {m_social_data_type!r}"
                )
        self.m_timeout = m_timeout
        self.m_javascript = m_javascript
        self.m_block_default_javascript = m_block_default_javascript
        self.m_fetch_config = m_fetch_config
        self.m_fetch_proxy = m_fetch_proxy
        self.m_resoource_block = m_resoource_block
        self.m_threat_type = m_threat_type
        self.m_rule_type = m_rule_type
        if m_social_data_type is not None and not isinstance(m_social_data_type, list):
            self.m_social_data_types = [m_social_data_type]
        else:
            self.m_social_data_types = m_social_data_type or []
        self.m_user_agent = m_user_agent
