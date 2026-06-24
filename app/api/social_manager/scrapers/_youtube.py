import re
from abc import ABC
from typing import List, Optional
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import urllib.request

from crawler.crawler_instance.local_interface_model.leak.leak_extractor_interface import leak_extractor_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType,RuleType, SocialDataType
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class YoutubeScraper(leak_extractor_interface, ABC):
    _instance = None

    def __init__(self, username: str = "", callback=None):
        if callable(username) and callback is None:
            callback = username
            username = ""
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._initialized = None
        self._username = (username or "").strip()
        self._scope = SOCIAL_REQUEST_COMMANDS.S_POSTS
        self.m_seed_url = self._channel_url_from_username(self._username)
        self.m_extract_info_only = False
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._requested_videos_limit = None
        self._requested_shorts_limit = None

    def init_callback(self, callback=None):
        self.callback = callback

    def set_scope(self, scope: int):
        self._scope = scope

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @staticmethod
    def _channel_url_from_username(username: str) -> str:
        username = (username or "").strip()
        if not username:
            return "https://www.youtube.com"
        if username.startswith("http://") or username.startswith("https://"):
            return username.rstrip("/")
        if username.startswith("@"):
            return f"https://www.youtube.com/{username}"
        return f"https://www.youtube.com/@{username}"

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def name(self) -> str:
        return "YouTube"

    @property
    def developer_signature(self) -> str:
        return "Dilshad Ghauri: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jL82"

    @property
    def base_url(self) -> str:
        return "https://www.youtube.com"

    @property
    def rule_config(self) -> RuleModel:
        rule = RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.SOCIAL,
            m_rule_type=RuleType.YOUTUBE,
            m_social_data_type=SocialDataType.VIDEOS
        )
        rule.m_resoource_block = False
        rule.m_resource_block = False
        return rule

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return "https://www.youtube.com/t/contact_us"

    def append_leak_data(self, leak: social_model, entity: entity_model):
        self._card_data.append(leak)
        self._entity_data.append(entity)
        if self.callback:
            if self.callback():
                self._card_data.clear()
                self._entity_data.clear()

    @staticmethod
    def _parse_counts(text: str) -> int:
        if not text: return 0
        text = text.upper().replace(' VIEWS', '').replace(' SUBSCRIBERS', '').strip()
        text = re.sub(r'[^\x00-\x7F]+', '', text).strip()

        try:
            if 'K' in text: return int(float(text.replace('K', '').strip()) * 1000)
            if 'M' in text: return int(float(text.replace('M', '').strip()) * 1000000)
            if 'B' in text: return int(float(text.replace('B', '').strip()) * 1000000000)
            return int(re.sub(r'[^0-9]', '', text))
        except (ValueError, TypeError, AttributeError):
            return 0

    def _unshorten_urls(self, text: str) -> List[str]:
        short_domains = ['bit.ly', 'tinyurl.com', 't.co', 'cutt.ly', 'is.gd', 'rb.gy', 'buff.ly']
        found_urls = re.findall(r'(https?://[^\s]+)', text)
        unmasked = []

        for url in found_urls:
            if any(sd in url for sd in short_domains):
                try:
                    req = urllib.request.Request(url, method='HEAD')
                    with urllib.request.urlopen(req, timeout=5) as response:
                        final_url = response.url
                        if final_url and final_url != url:
                            unmasked.append(f"{url} -> {final_url}")
                except Exception:
                    pass
        return list(set(unmasked))

    def _fetch_channel_info(self, page, channel_url):
        # try:
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

            channel_url = self.seed_url
            if not channel_url:
                channel_url = "https://www.youtube.com/@CarryisLive"

            channel_url = channel_url.split("?")[0].rstrip("/")
            if channel_url.endswith("/videos"):
                channel_url = channel_url[:-7]
            if channel_url.endswith("/shorts"):
                channel_url = channel_url[:-7]

            channel_country = "Unknown"
            channel_joined = "Unknown"
            channel_description = "Unknown"
            channel_avatar = "Unknown"
            channel_banner = "Unknown"
            social_profiles = []

            try:
                page.goto(channel_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)

                try:
                    images_data = page.evaluate("""() => {
                        let avatarEl = document.querySelector('yt-decorated-avatar-view-model img') || document.querySelector('yt-avatar-shape img') || document.querySelector('#avatar img');
                        let bannerEl = document.querySelector('yt-image-banner-view-model img') || document.querySelector('#page-header-banner img');
                        return {
                            avatar: avatarEl ? avatarEl.src : 'Unknown',
                            banner: bannerEl ? bannerEl.src : 'Unknown'
                        };
                    }""")
                    channel_avatar = images_data.get('avatar', 'Unknown')
                    channel_banner = images_data.get('banner', 'Unknown')
                except Exception:
                    pass

                page.keyboard.press("Escape")
                page.wait_for_timeout(1000)

                page.evaluate("""() => {
                    let descBtn = document.querySelector('yt-description-preview-view-model') || 
                                  document.querySelector('#page-header-description') ||
                                  document.querySelector('page-header-view-model span[role="button"]');
                    if(descBtn) descBtn.click();
                }""")
                page.wait_for_timeout(2000)

                modal_data = page.evaluate("""() => {
                    let dialog = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-about-this-channel"]') || 
                                 document.querySelector('tp-yt-paper-dialog') || 
                                 document.querySelector('#about-container');
                    let links = [];
                    if(dialog) {
                        dialog.querySelectorAll('a').forEach(a => links.push(a.href));
                        return { text: dialog.innerText, links: links };
                    }
                    return { text: "", links: [] };
                }""")

                raw_text = modal_data.get('text', '')
                raw_links = modal_data.get('links', [])

                if raw_text:
                    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
                    for idx, line in enumerate(lines):
                        if line.lower().startswith("joined "):
                            channel_joined = line[7:].strip()
                            if idx > 0:
                                prev_line = lines[idx - 1]
                                if "youtube.com" not in prev_line and "email address" not in prev_line.lower() and "more info" not in prev_line.lower():
                                    channel_country = prev_line

                    if "Description" in lines:
                        desc_start = lines.index("Description") + 1
                        desc_end = len(lines)
                        if "Links" in lines:
                            desc_end = lines.index("Links")
                        elif "More info" in lines:
                            desc_end = lines.index("More info")

                        channel_description = " ".join(lines[desc_start:desc_end])

                clean_profiles = []
                for url in raw_links:
                    if 'redirect?' in url and 'q=' in url:
                        try:
                            parsed = parse_qs(urlparse(url).query)
                            if 'q' in parsed:
                                clean_profiles.append(parsed['q'][0])
                        except Exception:
                            clean_profiles.append(url)
                    else:
                        clean_profiles.append(url)
                social_profiles = list(set(clean_profiles))

            except Exception:
                pass

            channel_name = page.evaluate(
                "() => { let el = document.querySelector('meta[property=\"og:title\"]'); return el ? el.content : 'Unknown'; }")

            combined_content = f"CHANNEL NAME: {channel_name}\nCHANNEL URL: {channel_url}\nCOUNTRY: {channel_country}\nJOINED: {channel_joined}\nAVATAR URL: {channel_avatar}\nBANNER URL: {channel_banner}\n"
            if channel_description != "Unknown":
                combined_content += f"\nCHANNEL DESCRIPTION:\n{channel_description}"

            card_data = social_model(
                m_title=channel_name,
                m_channel_url=channel_url,
                m_sender_name=channel_name,
                m_bio=channel_description,
                m_platform_joined=channel_joined,
                m_profile_pic_url=channel_avatar,
                m_profile_cover_pic_url=channel_banner,
                m_message_sharable_link=channel_url,
                m_weblink=social_profiles,
                m_content=combined_content,
                m_content_type=["social_collector", "youtube_channel_info"],
                m_network="clearnet",
                m_message_date=datetime.now().date(),
                m_message_id=channel_url.split("@")[-1],
                m_platform="youtube",
                m_likes="0",
                m_comment_count="0",
                m_retweets="0",
                m_views="0",
            )

            entity = entity_model(
                m_scrap_file=self.__class__.__name__,
                m_name=channel_name,
            )

            try:
                if channel_country != "Unknown":
                    entity.m_country = [channel_country]
                if social_profiles:
                    entity.m_social_media_profiles = social_profiles
            except Exception:
                pass

            self.append_leak_data(card_data, entity)


    def _fetch_videos(self, page, channel_url, include_shorts=True, max_videos: Optional[int] = None):
        valid_video_links = []

        channel_country = "Unknown"
        channel_name = "Unknown"
        channel_joined = "Unknown"
        channel_description = "Unknown"
        channel_avatar = "Unknown"
        channel_banner = "Unknown"
        has_shorts = False
        social_profiles = []

        videos_tab_url = channel_url + "/videos"
        try:
            page.goto(videos_tab_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            page.evaluate("""() => {
                      let chips = document.querySelectorAll('yt-chip-cloud-chip-renderer');
                      for (let chip of chips) {
                          if (chip.innerText.trim().toLowerCase() === 'latest') {
                              if (!chip.classList.contains('selected')) {
                                  chip.click();
                              }
                              break;
                          }
                      }
                  }""")
            page.wait_for_timeout(2000)

            stop_videos_scrolling = False
            for _ in range(20):
                if stop_videos_scrolling: break

                video_elements = page.evaluate("""() => {
                          let results = [];
                          let items = document.querySelectorAll('ytd-rich-item-renderer');
                          for (let item of items) {
                              if (item.offsetParent === null) continue; 

                              let a = item.querySelector('a.ytLockupMetadataViewModelTitle') || 
                                      item.querySelector('a#video-title-link') || 
                                      item.querySelector('a#video-title') ||
                                      item.querySelector('h3 a');

                              if (!a || a.href.includes('/shorts/')) continue;

                              let timeText = "";
                              let metaSpans = item.querySelectorAll('.inline-metadata-item');
                              for (let span of metaSpans) {
                                  let txt = span.innerText.toLowerCase();
                                  if (txt.includes('ago') || txt.includes('streamed') || txt.includes('premiered')) {
                                      timeText = txt;
                                      break;
                                  }
                              }
                              if (!timeText) {
                                  let match = item.innerText.toLowerCase().match(/[0-9]+\\s*(second|minute|hour|day|week|month|year|s|m|h|d|w|mo|y)s?\\s*ago/);
                                  if (match) timeText = match[0];
                              }
                              results.push({href: a.href, time: timeText});
                          }
                          return results;
                      }""")

                for vid in video_elements:
                    href = vid.get('href', '')
                    time_text = vid.get('time', '').lower()

                    if not href or href in valid_video_links:
                        continue

                    if max_videos is not None and len(valid_video_links) >= max_videos:
                        stop_videos_scrolling = True
                        break

                    if not time_text:
                        valid_video_links.append(href)
                        continue

                    if re.search(r'\d+\s*(year|years|y)\b', time_text):
                        stop_videos_scrolling = True
                        break
                    elif re.search(r'\d+\s*(month|months|mo)\b', time_text):
                        if re.search(r'\b1\s*(month|mo)\b', time_text):
                            valid_video_links.append(href)
                        else:
                            stop_videos_scrolling = True
                            break
                    else:
                        valid_video_links.append(href)

                if not stop_videos_scrolling:
                    page.mouse.wheel(0, 3000)
                    page.wait_for_timeout(1500)
        except Exception:
            pass

        valid_media_links = valid_video_links

        if not valid_media_links:
            return

        btc_pattern = re.compile(r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})\b')
        eth_pattern = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
        tg_pattern = re.compile(r'(?:https?://)?(?:www\.)?t\.me/([a-zA-Z0-9_]+)')
        discord_pattern = re.compile(r'(?:https?://)?(?:www\.)?discord\.(?:gg|com/invite)/([a-zA-Z0-9]+)')
        onion_pattern = re.compile(r'\b([a-z2-7]{16,56}\.onion)\b')

        parsed_video_links = valid_media_links if max_videos is None else valid_media_links[:max_videos]

        for video_idx, original_video_url in enumerate(parsed_video_links, 1):
            print(f"currently parsing index : {video_idx}")
            try:
                is_short_media = "/shorts/" in original_video_url

                visit_url = original_video_url
                if is_short_media:
                    visit_url = original_video_url.replace("/shorts/", "/watch?v=")

                page.goto(visit_url, wait_until="domcontentloaded", timeout=30000)

                try:
                    page.evaluate(
                        "() => { document.querySelectorAll('video').forEach(v => { v.pause(); v.removeAttribute('autoplay'); }); }")
                except Exception:
                    pass

                page.wait_for_selector("h1.ytd-watch-metadata", state="visible", timeout=15000)

                exact_date_str = page.evaluate("""() => {
                                let meta = document.querySelector('meta[itemprop="datePublished"]');
                                return meta ? meta.getAttribute('content') : '';
                            }""")

                if exact_date_str:
                    try:
                        exact_date = datetime.strptime(exact_date_str[:10], "%Y-%m-%d").date()
                    except Exception:
                        exact_date = datetime.now().date()
                else:
                    exact_date = datetime.now().date()

                title = "Unknown"
                title_elem = page.locator("h1.ytd-watch-metadata yt-formatted-string").first
                if title_elem.count() > 0: title = title_elem.inner_text(timeout=2000)

                views_count = 0
                views_elem = page.locator("yt-formatted-string#info span").nth(0)
                views_text = views_elem.inner_text(timeout=2000) if views_elem.count() > 0 else "0"
                views_count = self._parse_counts(views_text)

                likes_count = 0
                try:
                    likes_text = page.evaluate("""() => {
                                    let btn = document.querySelector('like-button-view-model button');
                                    if (!btn) return '0';
                                    let aria = btn.getAttribute('aria-label');
                                    if (aria) {
                                        let match = aria.match(/with\\s+([\\d,]+)\\s+other/i) || aria.match(/([\\d,]+)\\s+likes/i);
                                        if (match) return match[1];
                                    }
                                    let textDiv = btn.querySelector('.ytSpecButtonShapeNextButtonTextContent');
                                    return textDiv ? textDiv.innerText : btn.innerText;
                                }""")
                    likes_count = self._parse_counts(likes_text)
                except Exception:
                    pass

                subs_count = 0
                try:
                    subs_elem = page.locator("ytd-video-owner-renderer #owner-sub-count").first
                    subs_text = subs_elem.inner_text(timeout=2000) if subs_elem.count() > 0 else "0"
                    subs_count = self._parse_counts(subs_text)
                except Exception:
                    pass

                viral_ratio = (views_count / subs_count) if subs_count > 0 else 0
                is_viral = viral_ratio > 0.20

                top_comments = []
                try:
                    for _ in range(4):
                        page.keyboard.press("PageDown")
                        page.wait_for_timeout(1000)

                    page.wait_for_selector("ytd-comment-thread-renderer", state="visible", timeout=10000)

                    prev_count = 0
                    same_count_rounds = 0
                    for scroll_idx in range(40):
                        current_count = page.evaluate(
                            "document.querySelectorAll('ytd-comment-thread-renderer').length")
                        if current_count >= 200: break

                        if current_count == prev_count:
                            same_count_rounds += 1
                            if same_count_rounds >= 3:
                                break
                        else:
                            same_count_rounds = 0

                        prev_count = current_count
                        page.evaluate(
                            "() => { let scroller = document.querySelector('#comments') || window; scroller.scrollBy(0, 1500); }")
                        page.wait_for_timeout(1500)

                    extracted_comments = page.evaluate("""() => {
                                    let elems = document.querySelectorAll('ytd-comment-thread-renderer #content-text');
                                    let texts = [];
                                    for(let i=0; i<elems.length && i<200; i++) {
                                        let txt = elems[i].innerText.trim();
                                        if(txt) texts.push(txt);
                                    }
                                    return texts;
                                }""")
                    top_comments.extend(extracted_comments)
                except Exception:
                    pass

                iocs = []
                unmasked_links = []
                try:
                    page_text = page.evaluate("document.body.innerText")
                    desc_text = channel_description if channel_description != "Unknown" else ""
                    unmasked_links = self._unshorten_urls(page_text + desc_text)

                    for match in btc_pattern.findall(page_text): iocs.append(f"BTC Wallet: {match}")
                    for match in eth_pattern.findall(page_text): iocs.append(f"ETH Wallet: {match}")
                    for match in onion_pattern.findall(page_text): iocs.append(f"DarkWeb Link: {match}")
                    for match in tg_pattern.findall(page_text): iocs.append(f"Telegram: t.me/{match}")
                    for match in discord_pattern.findall(page_text): iocs.append(f"Discord: discord.gg/{match}")

                    iocs = list(set(iocs))
                except Exception:
                    pass

                media_type_label = "SHORT" if is_short_media else "VIDEO"
                combined_content = f"TITLE: {title} [{media_type_label}]\nEXACT DATE: {exact_date}\nVIEWS: {views_count:,}\nLIKES: {likes_count:,}\nCHANNEL: {channel_name}\nSUBSCRIBERS: {subs_count:,}\nCOUNTRY: {channel_country}\nJOINED: {channel_joined}\nAVATAR URL: {channel_avatar}\nBANNER URL: {channel_banner}\nVIRAL RATIO: {viral_ratio:.2f}x\nIS VIRAL: {'YES' if is_viral else 'NO'}\nCHANNEL HAS SHORTS: {has_shorts}"

                if channel_description != "Unknown":
                    combined_content += f"\n\nCHANNEL DESCRIPTION:\n{channel_description[:250]}..."

                if unmasked_links:
                    combined_content += "\n\n⚠️ UNMASKED URLs (POTENTIAL THREATS):\n"
                    for ul in unmasked_links:
                        combined_content += f"- {ul}\n"

                if iocs:
                    combined_content += "\n\n⚠️ THREAT IOCs FOUND:\n"
                    for ioc in iocs:
                        combined_content += f"- {ioc}\n"

                if top_comments:
                    combined_content += "\n\nTOP COMMENTS:\n"
                    for idx, comment in enumerate(top_comments, 1):
                        combined_content += f"{idx}. {comment[:100]}...\n"

                card_data = social_model(
                    m_title=title,
                    m_channel_url=channel_url,
                    m_sender_name=channel_name,
                    m_message_sharable_link=original_video_url,
                    m_weblink=[],
                    m_content=combined_content,
                    m_content_type=["social_collector", "youtube_video", media_type_label.lower()],
                    m_network="clearnet",
                    m_message_date=exact_date,
                    m_message_id=original_video_url.split("/")[-1].split("?")[0],
                    m_platform="youtube",
                    m_likes=str(likes_count),
                    m_comment_count=str(len(top_comments)),
                    m_retweets="0",
                    m_views=str(views_count),
                    m_commenters=top_comments,
                )

                entity = entity_model(
                    m_scrap_file=self.__class__.__name__,
                    m_name=channel_name
                )

                try:
                    if channel_country != "Unknown":
                        entity.m_country = channel_country
                    if social_profiles:
                        entity.m_social_media_profiles = social_profiles
                    if channel_avatar != "Unknown":
                        entity.m_avatar = channel_avatar
                    if channel_banner != "Unknown":
                        entity.m_banner = channel_banner
                except Exception:
                    pass

                self.append_leak_data(card_data, entity)

            except Exception:
                continue

    def _fetch_posts(self, page, channel_url):

        channel_country = "Unknown"
        channel_name = "Unknown"
        channel_avatar = "Unknown"
        channel_banner = "Unknown"
        social_profiles = []

        btc_pattern = re.compile(r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})\b')
        eth_pattern = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
        tg_pattern = re.compile(r'(?:https?://)?(?:www\.)?t\.me/([a-zA-Z0-9_]+)')
        discord_pattern = re.compile(r'(?:https?://)?(?:www\.)?discord\.(?:gg|com/invite)/([a-zA-Z0-9]+)')
        onion_pattern = re.compile(r'\b([a-z2-7]{16,56}\.onion)\b')

        has_posts = "No"
        try:
            tabs_info = page.evaluate("""() => {
                                const tabs = Array.from(document.querySelectorAll('yt-tab-shape'));
                                return {
                                    posts: tabs.some(tab => tab.getAttribute('tab-title') === 'Posts' || tab.getAttribute('tab-title') === 'Community' || tab.innerText.includes('Posts') || tab.innerText.includes('Community')) ? 'Yes' : 'No'
                                };
                            }""")
            has_posts = tabs_info.get('posts', 'No')
        except Exception:
            pass

        if has_posts == "Yes":
            posts_tab_url = channel_url + "/posts"
            try:
                page.goto(posts_tab_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)

                stop_posts_scrolling = False
                for _ in range(50):
                    if stop_posts_scrolling: break

                    last_time = page.evaluate("""() => {
                        let times = document.querySelectorAll('ytd-backstage-post-renderer #published-time-text');
                        if (times.length === 0) return "";
                        return times[times.length - 1].innerText.toLowerCase();
                    }""")

                    if not last_time:
                        break

                    match = re.search(r'(\d+)\s*(year|years|y)\b', last_time)
                    if match and int(match.group(1)) >= 1:
                        stop_posts_scrolling = True
                        break

                    page.mouse.wheel(0, 4000)
                    page.wait_for_timeout(1500)

                page.evaluate(
                    "() => { document.querySelectorAll('tp-yt-paper-button#more').forEach(b => b.click()); }")
                page.wait_for_timeout(1500)

                extracted_posts = page.evaluate("""() => {
                    let results = [];
                    let items = document.querySelectorAll('ytd-backstage-post-renderer');
                    for (let item of items) {
                        if (item.offsetParent === null) continue;

                        let timeEl = item.querySelector('#published-time-text a');
                        let timeText = timeEl ? timeEl.innerText.trim() : "";
                        let url = timeEl ? timeEl.href : "";

                        let textEl = item.querySelector('#content-text');
                        let postText = textEl ? textEl.innerText.trim() : "";

                        let likesEl = item.querySelector('#vote-count-middle');
                        let likes = likesEl ? likesEl.innerText.trim() : "0";

                        let commentEl = item.querySelector('ytd-comment-action-buttons-renderer #reply-button-end span, ytd-comment-action-buttons-renderer #text');
                        let comments = commentEl ? commentEl.innerText.trim() : "0";

                        let imgEls = item.querySelectorAll('ytd-backstage-image-renderer img');
                        let images = [];
                        for(let img of imgEls){
                            if(img.src && img.src.includes('http')) images.push(img.src);
                        }

                        results.push({
                            url: url,
                            time: timeText,
                            text: postText,
                            likes: likes,
                            comments: comments,
                            images: images
                        });
                    }
                    return results;
                }""")

                for p in extracted_posts:
                    post_time = p.get('time', '').lower()
                    match = re.search(r'(\d+)\s*(year|years|y)\b', post_time)
                    if match and int(match.group(1)) > 1:
                        continue

                    post_text = p.get('text', '')
                    post_url = p.get('url', channel_url)
                    post_likes = str(self._parse_counts(p.get('likes', '0')))
                    post_comments = str(self._parse_counts(p.get('comments', '0')))
                    post_images = p.get('images', [])

                    post_iocs = []
                    post_unmasked_links = self._unshorten_urls(post_text)

                    for m in btc_pattern.findall(post_text): post_iocs.append(f"BTC Wallet: {m}")
                    for m in eth_pattern.findall(post_text): post_iocs.append(f"ETH Wallet: {m}")
                    for m in onion_pattern.findall(post_text): post_iocs.append(f"DarkWeb Link: {m}")
                    for m in tg_pattern.findall(post_text): post_iocs.append(f"Telegram: t.me/{m}")
                    for m in discord_pattern.findall(post_text): post_iocs.append(f"Discord: discord.gg/{m}")
                    post_iocs = list(set(post_iocs))

                    combined_content = f"TITLE: Community Post [{channel_name}]\nPOSTED: {post_time}\nLIKES: {post_likes}\nCOMMENTS: {post_comments}\nCHANNEL: {channel_name}\n\nPOST TEXT:\n{post_text}"

                    if post_images:
                        combined_content += "\n\nATTACHED IMAGES:\n"
                        for img in post_images:
                            combined_content += f"- {img}\n"

                    if post_unmasked_links:
                        combined_content += "\n\n⚠️ UNMASKED URLs (POTENTIAL THREATS):\n"
                        for ul in post_unmasked_links:
                            combined_content += f"- {ul}\n"

                    if post_iocs:
                        combined_content += "\n\n⚠️ THREAT IOCs FOUND:\n"
                        for ioc in post_iocs:
                            combined_content += f"- {ioc}\n"

                    card_data = social_model(
                        m_title=post_text,
                        m_channel_url=channel_url,
                        m_sender_name=channel_name,
                        m_message_sharable_link=post_url,
                        m_post_pic_url=post_images,
                        m_post_time=post_time,
                        m_post_url=post_url,
                        m_weblink=post_images,
                        m_content=combined_content,
                        m_content_type=["social_collector", "youtube_post"],
                        m_network="clearnet",
                        m_message_date=datetime.now().date(),
                        m_message_id=post_url.split("/")[-1] if post_url else str(hash(post_text)),
                        m_platform="youtube",
                        m_likes=post_likes,
                        m_commenters=[post_comments],
                        m_retweets="0",
                        m_views="0",
                    )

                    entity = entity_model(
                        m_scrap_file=self.__class__.__name__,
                        m_name=channel_name
                    )

                    try:
                        if channel_country != "Unknown":
                            entity.m_country = channel_country
                        if social_profiles:
                            entity.m_social_media_profiles = social_profiles
                        if channel_avatar != "Unknown":
                            entity.m_avatar = channel_avatar
                        if channel_banner != "Unknown":
                            entity.m_banner = channel_banner
                    except Exception:
                        pass

                    self.append_leak_data(card_data, entity)

            except Exception:
                pass

    def _fetch_shorts(self, page, channel_url, max_shorts: Optional[int] = None):
        btc_pattern = re.compile(r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})\b')
        eth_pattern = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
        tg_pattern = re.compile(r'(?:https?://)?(?:www\.)?t\.me/([a-zA-Z0-9_]+)')
        discord_pattern = re.compile(r'(?:https?://)?(?:www\.)?discord\.(?:gg|com/invite)/([a-zA-Z0-9]+)')
        onion_pattern = re.compile(r'\b([a-z2-7]{16,56}\.onion)\b')

        channel_country = "Unknown"
        channel_name = "Unknown"
        channel_avatar = "Unknown"
        channel_banner = "Unknown"
        channel_description = "Unknown"
        channel_joined = "Unknown"

        social_profiles = []

        valid_shorts_links = []
        has_shorts = "No"
        try:
            tabs_info = page.evaluate("""() => {
                                const tabs = Array.from(document.querySelectorAll('yt-tab-shape'));
                                return {
                                    shorts: tabs.some(tab => tab.getAttribute('tab-title') === 'Shorts' || tab.innerText.includes('Shorts')) ? 'Yes' : 'No',
                                };
                            }""")
            has_shorts = tabs_info.get('shorts', 'No')
        except Exception:
            pass

        if has_shorts == "Yes":
            shorts_tab_url = channel_url + "/shorts"
            try:
                page.goto(shorts_tab_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)

                page.evaluate("""() => {
                    let chips = document.querySelectorAll('yt-chip-cloud-chip-renderer');
                    for (let chip of chips) {
                        if (chip.innerText.trim().toLowerCase() === 'latest') {
                            if (!chip.classList.contains('selected')) {
                                chip.click();
                            }
                            break;
                        }
                    }
                }""")
                page.wait_for_timeout(2000)

                stop_shorts_scrolling = False
                for _ in range(15):
                    if stop_shorts_scrolling: break

                    shorts_elements = page.evaluate("""() => {
                        let results = [];
                        let items = document.querySelectorAll('ytd-rich-item-renderer');
                        for (let item of items) {
                            if (item.offsetParent === null) continue;
                            let a = item.querySelector('a');
                            if (!a || !a.href.includes('/shorts/')) continue;

                            let aria = a.getAttribute('aria-label') || "";
                            let title = a.innerText.split('\\n')[0];

                            let timeMatch = aria.match(/[0-9]+\\s*(second|minute|hour|day|week|month|year|s|m|h|d|w|mo|y)s?\\s*ago/i);
                            let timeText = timeMatch ? timeMatch[0] : "";

                            results.push({href: a.href, time: timeText, title: title});
                        }
                        return results;
                    }""")

                    for s_vid in shorts_elements:
                        href = s_vid.get('href', '')
                        time_text = s_vid.get('time', '').lower()

                        if not href or href in valid_shorts_links:
                            continue

                        if max_shorts is not None and len(valid_shorts_links) >= max_shorts:
                            stop_shorts_scrolling = True
                            break

                        if not time_text:
                            valid_shorts_links.append(href)
                            continue

                        if re.search(r'\d+\s*(year|years|y)\b', time_text):
                            stop_shorts_scrolling = True
                            break
                        elif re.search(r'\d+\s*(month|months|mo)\b', time_text):
                            if re.search(r'\b1\s*(month|mo)\b', time_text):
                                valid_shorts_links.append(href)
                            else:
                                stop_shorts_scrolling = True
                                break
                        else:
                            valid_shorts_links.append(href)

                    if not stop_shorts_scrolling:
                        page.mouse.wheel(0, 2000)
                        page.wait_for_timeout(1500)
            except Exception:
                pass

            valid_media_links =  valid_shorts_links

            if not valid_media_links:
                return

            parsed_shorts_links = valid_media_links if max_shorts is None else valid_media_links[:max_shorts]

            for video_idx, original_video_url in enumerate(parsed_shorts_links, 1):
                print(f"currently parsing index : {video_idx}")
                try:
                    is_short_media = "/shorts/" in original_video_url

                    visit_url = original_video_url
                    if is_short_media:
                        visit_url = original_video_url.replace("/shorts/", "/watch?v=")

                    page.goto(visit_url, wait_until="domcontentloaded", timeout=30000)

                    try:
                        page.evaluate(
                            "() => { document.querySelectorAll('video').forEach(v => { v.pause(); v.removeAttribute('autoplay'); }); }")
                    except Exception:
                        pass

                    page.wait_for_selector("h1.ytd-watch-metadata", state="visible", timeout=15000)

                    exact_date_str = page.evaluate("""() => {
                                    let meta = document.querySelector('meta[itemprop="datePublished"]');
                                    return meta ? meta.getAttribute('content') : '';
                                }""")

                    if exact_date_str:
                        try:
                            exact_date = datetime.strptime(exact_date_str[:10], "%Y-%m-%d").date()
                        except Exception:
                            exact_date = datetime.now().date()
                    else:
                        exact_date = datetime.now().date()

                    title = "Unknown"
                    title_elem = page.locator("h1.ytd-watch-metadata yt-formatted-string").first
                    if title_elem.count() > 0: title = title_elem.inner_text(timeout=2000)

                    views_count = 0
                    views_elem = page.locator("yt-formatted-string#info span").nth(0)
                    views_text = views_elem.inner_text(timeout=2000) if views_elem.count() > 0 else "0"
                    views_count = self._parse_counts(views_text)

                    likes_count = 0
                    try:
                        likes_text = page.evaluate("""() => {
                                        let btn = document.querySelector('like-button-view-model button');
                                        if (!btn) return '0';
                                        let aria = btn.getAttribute('aria-label');
                                        if (aria) {
                                            let match = aria.match(/with\\s+([\\d,]+)\\s+other/i) || aria.match(/([\\d,]+)\\s+likes/i);
                                            if (match) return match[1];
                                        }
                                        let textDiv = btn.querySelector('.ytSpecButtonShapeNextButtonTextContent');
                                        return textDiv ? textDiv.innerText : btn.innerText;
                                    }""")
                        likes_count = self._parse_counts(likes_text)
                    except Exception:
                        pass

                    subs_count = 0
                    try:
                        subs_elem = page.locator("ytd-video-owner-renderer #owner-sub-count").first
                        subs_text = subs_elem.inner_text(timeout=2000) if subs_elem.count() > 0 else "0"
                        subs_count = self._parse_counts(subs_text)
                    except Exception:
                        pass

                    viral_ratio = (views_count / subs_count) if subs_count > 0 else 0
                    is_viral = viral_ratio > 0.20

                    top_comments = []
                    try:
                        for _ in range(4):
                            page.keyboard.press("PageDown")
                            page.wait_for_timeout(1000)

                        page.wait_for_selector("ytd-comment-thread-renderer", state="visible", timeout=10000)

                        prev_count = 0
                        same_count_rounds = 0
                        for scroll_idx in range(40):
                            current_count = page.evaluate(
                                "document.querySelectorAll('ytd-comment-thread-renderer').length")
                            if current_count >= 200: break

                            if current_count == prev_count:
                                same_count_rounds += 1
                                if same_count_rounds >= 3:
                                    break
                            else:
                                same_count_rounds = 0

                            prev_count = current_count
                            page.evaluate(
                                "() => { let scroller = document.querySelector('#comments') || window; scroller.scrollBy(0, 1500); }")
                            page.wait_for_timeout(1500)

                        extracted_comments = page.evaluate("""() => {
                                        let elems = document.querySelectorAll('ytd-comment-thread-renderer #content-text');
                                        let texts = [];
                                        for(let i=0; i<elems.length && i<200; i++) {
                                            let txt = elems[i].innerText.trim();
                                            if(txt) texts.push(txt);
                                        }
                                        return texts;
                                    }""")
                        top_comments.extend(extracted_comments)
                    except Exception:
                        pass

                    iocs = []
                    unmasked_links = []
                    try:
                        page_text = page.evaluate("document.body.innerText")
                        desc_text = channel_description if channel_description != "Unknown" else ""
                        unmasked_links = self._unshorten_urls(page_text + desc_text)

                        for match in btc_pattern.findall(page_text): iocs.append(f"BTC Wallet: {match}")
                        for match in eth_pattern.findall(page_text): iocs.append(f"ETH Wallet: {match}")
                        for match in onion_pattern.findall(page_text): iocs.append(f"DarkWeb Link: {match}")
                        for match in tg_pattern.findall(page_text): iocs.append(f"Telegram: t.me/{match}")
                        for match in discord_pattern.findall(page_text): iocs.append(f"Discord: discord.gg/{match}")

                        iocs = list(set(iocs))
                    except Exception:
                        pass

                    media_type_label = "SHORT" if is_short_media else "VIDEO"
                    combined_content = f"TITLE: {title} [{media_type_label}]\nEXACT DATE: {exact_date}\nVIEWS: {views_count:,}\nLIKES: {likes_count:,}\nCHANNEL: {channel_name}\nSUBSCRIBERS: {subs_count:,}\nCOUNTRY: {channel_country}\nJOINED: {channel_joined}\nAVATAR URL: {channel_avatar}\nBANNER URL: {channel_banner}\nVIRAL RATIO: {viral_ratio:.2f}x\nIS VIRAL: {'YES' if is_viral else 'NO'}\nCHANNEL HAS SHORTS: {has_shorts}"

                    if channel_description != "Unknown":
                        combined_content += f"\n\nCHANNEL DESCRIPTION:\n{channel_description[:250]}..."

                    if unmasked_links:
                        combined_content += "\n\n⚠️ UNMASKED URLs (POTENTIAL THREATS):\n"
                        for ul in unmasked_links:
                            combined_content += f"- {ul}\n"

                    if iocs:
                        combined_content += "\n\n⚠️ THREAT IOCs FOUND:\n"
                        for ioc in iocs:
                            combined_content += f"- {ioc}\n"

                    if top_comments:
                        combined_content += "\n\nTOP COMMENTS:\n"
                        for idx, comment in enumerate(top_comments, 1):
                            combined_content += f"{idx}. {comment[:100]}...\n"

                    card_data = social_model(
                        m_title=title,
                        m_channel_url=channel_url,
                        m_sender_name=channel_name,
                        m_subscriber=subs_count,
                        m_message_sharable_link=original_video_url,
                        m_message_date=exact_date,
                        m_commenters=top_comments,
                        m_weblink=[],
                        m_content=combined_content,
                        m_content_type=["social_collector", "youtube_video", media_type_label.lower()],
                        m_network="clearnet",
                        m_message_id=original_video_url.split("/")[-1].split("?")[0],
                        m_platform="youtube",
                        m_likes=str(likes_count),
                        m_comment_count=str(len(top_comments)),
                        m_retweets="0",
                        m_views=str(views_count),
                    )

                    entity = entity_model(
                        m_scrap_file=self.__class__.__name__,
                        m_name=channel_name
                    )

                    try:
                        if channel_country != "Unknown":
                            entity.m_country = channel_country
                        if social_profiles:
                            entity.m_social_media_profiles = social_profiles
                        if channel_avatar != "Unknown":
                            entity.m_avatar = channel_avatar
                        if channel_banner != "Unknown":
                            entity.m_banner = channel_banner
                    except Exception:
                        pass

                    self.append_leak_data(card_data, entity)

                except Exception:
                    continue

    def parse_page(self, page):
        self._card_data = []
        self._entity_data = []
        self.parse_leak_data(page)
        return {
            "username": self._username,
            "profile_url": self.seed_url,
            "platform": "youtube",
            "cards": [card.model_dump(mode="json") for card in self._card_data],
            "entities": [entity.model_dump(mode="json") for entity in self._entity_data],
            "followers": [],
            "following": [],
            "mutual": [],
        }

    def scrape_posts(self, page, max_posts: int = 5):
        data = self.parse_page(page)
        return data.get("cards", [])[:max_posts]

    def scrape_videos(self, page, max_videos: int):
        self._requested_videos_limit = max_videos
        self.set_scope(SOCIAL_REQUEST_COMMANDS.S_VIDEOS)
        data = self.parse_page(page)
        return data.get("cards", [])[:max_videos]

    def scrape_shorts(self, page, max_shorts: int):
        self._requested_shorts_limit = max_shorts
        self.set_scope(SOCIAL_REQUEST_COMMANDS.S_SHORTS)
        data = self.parse_page(page)
        return data.get("cards", [])[:max_shorts]

    def parse_leak_data(self, page):
        try:
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

            channel_url = self.seed_url
            page.goto(channel_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            if self._scope == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
                self._fetch_channel_info(page, channel_url)
                return

            if self._scope == SOCIAL_REQUEST_COMMANDS.S_POSTS:
                self._fetch_posts(page, channel_url)
                return

            if self._scope == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
                self._fetch_videos(page,channel_url,include_shorts=False,max_videos=self._requested_videos_limit,)
                return

            if self._scope == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
                self._fetch_shorts(page, channel_url, max_shorts=self._requested_shorts_limit)
                return

        except Exception as e:
            raise e