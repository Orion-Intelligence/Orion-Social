(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  window.OrionScrapers.instagram = {
    selectors: ["header", "main", "article img", "a[href*='/p/']", "a[href*='/reel/']"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      const command = getJobCommand(job);
      assertCanScrape(username);
      const description = helpers.meta("description");
      const profileStats = parseProfileStats();
      const result = {
        platform: "instagram",
        username,
        url: window.location.href,
        profile: {
          username,
          display_name: helpers.text("header section h1, header h2") || document.title,
          bio: collectBio() || description,
          avatar_url: helpers.absoluteUrl(document.querySelector("header img, img[alt*='profile picture']")?.getAttribute("src") || ""),
          description,
          posts_count: profileStats.posts,
          followers_count: profileStats.followers,
          following_count: profileStats.following,
          total_posts: profileStats.posts,
          total_followers: profileStats.followers,
          total_following: profileStats.following
        },
        posts: [],
        images: [],
        followers: [],
        following: [],
        partial: false,
        errors: []
      };
      rememberPartialResult(result);

      if (shouldCollectFollowers(command)) {
        try {
          result.followers = await collectConnectionList(job, "followers", username);
          rememberPartialResult(result);
        } catch (error) {
          if (isAuthRequiredError(error)) {
            throw error;
          }
          addPartialError(result, "followers", error);
        }
      }

      if (shouldCollectFollowing(command)) {
        try {
          result.following = await collectConnectionList(job, "following", username);
          rememberPartialResult(result);
        } catch (error) {
          if (isAuthRequiredError(error)) {
            throw error;
          }
          addPartialError(result, "following", error);
        }
      }

      if (shouldCollectPosts(command)) {
        try {
          result.posts = await collectPosts(job, result);
          result.images = collectImages(result.posts);
          rememberPartialResult(result);
        } catch (error) {
          if (isAuthRequiredError(error)) {
            throw error;
          }
          addPartialError(result, "posts", error);
          result.images = collectImages(result.posts);
        }
      }

      return result;
    }
  };

  function usernameFromUrl() {
    const match = window.location.pathname.match(/^\/([^/?#]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function getJobCommand(job) {
    return String(job?.command || job?.social_data_type || "profile").toLowerCase();
  }

  function assertCanScrape(username) {
    const authState = detectAuthRequired(username);
    if (!authState.required) {
      return;
    }
    throw createAuthRequiredError(authState);
  }

  function detectAuthRequired(username) {
    const path = window.location.pathname.toLowerCase();
    const bodyText = helpers.cleanText(document.body?.innerText || document.body?.textContent || "");
    const dialogText = helpers.cleanText(Array.from(document.querySelectorAll("div[role='dialog'], [role='dialog']"))
      .map((dialog) => dialog.textContent || "")
      .join(" "));
    const hasLoginRoute = /\/accounts\/(?:login|signup)|\/challenge|\/checkpoint/i.test(path);
    const hasCredentialForm = !!document.querySelector("form[action*='/accounts/login'], input[name='password'], input[name='username']");
    const hasBlockingDialog = !!dialogText
      && /\b(log in|login|sign up)\b/i.test(dialogText)
      && /\b(instagram|account|continue|see|view)\b/i.test(dialogText);
    const hasProfileSignals = hasInstagramProfileSignals(username);
    const hasLoginCopy = /\b(log in|login|sign up)\b/i.test(bodyText)
      && /\b(password|username|instagram|account)\b/i.test(bodyText);
    return {
      required: hasLoginRoute || hasBlockingDialog || (hasCredentialForm && !hasProfileSignals) || (!hasProfileSignals && hasLoginCopy),
      platform: "instagram",
      login_url: buildInstagramLoginUrl()
    };
  }

  function hasInstagramProfileSignals(username) {
    const headerText = helpers.cleanText(document.querySelector("header")?.textContent || "");
    if (document.querySelector("header img, header h1, header h2, article img, a[href*='/p/'], a[href*='/reel/'], a[href*='/tv/']")) {
      return true;
    }
    return !!username && headerText.toLowerCase().includes(String(username).toLowerCase());
  }

  function buildInstagramLoginUrl() {
    const next = `${window.location.pathname}${window.location.search || ""}`;
    return `https://www.instagram.com/accounts/login/?next=${encodeURIComponent(next || "/")}`;
  }

  function createAuthRequiredError(authState) {
    const error = new Error("Instagram login required in this browser.");
    error.code = "AUTH_REQUIRED";
    error.error_code = "AUTH_REQUIRED";
    error.platform = authState.platform || "instagram";
    error.login_url = authState.login_url || buildInstagramLoginUrl();
    return error;
  }

  function isAuthRequiredError(error) {
    return error?.error_code === "AUTH_REQUIRED" || error?.code === "AUTH_REQUIRED";
  }

  function shouldCollectPosts(command) {
    return !["followers", "following"].includes(command);
  }

  function shouldCollectFollowers(command) {
    return ["profile", "profile_info", "followers"].includes(command);
  }

  function shouldCollectFollowing(command) {
    return ["profile", "profile_info", "following"].includes(command);
  }

  async function collectConnectionList(job, type, username) {
    const limitKey = type === "followers" ? "max_followers" : "max_following";
    const limit = Number(job?.limits?.[limitKey] || job?.[limitKey] || 1000);
    const profileUrl = window.location.href;
    const link = findConnectionLink(type, username);
    if (!link || limit <= 0) {
      return [];
    }
    try {
      window.scrollTo({ top: 0, behavior: "instant" });
      await randomSleep(700, 1300);
      const root = await openConnectionSurface(link, type);
      if (!root) {
        return [];
      }
      const users = await collectConnectionUsers(root, type, username, limit);
      await closeConnectionSurface(profileUrl);
      await randomSleep(700, 1300);
      return users;
    } catch (error) {
      await closeConnectionSurface(profileUrl);
      if (isAuthRequiredError(error)) {
        throw error;
      }
      return [];
    }
  }

  function findConnectionLink(type, username) {
    const normalizedUsername = normalizeInstagramUsername(username || usernameFromUrl()).toLowerCase();
    const roots = [document.querySelector("header"), document.querySelector("main"), document].filter(Boolean);
    const candidates = helpers.unique(
      roots.flatMap((root) => Array.from(root.querySelectorAll("a[href], button, [role='link'], [role='button']"))),
      (node) => node
    );
    return candidates.find((link) => {
      const path = pathFromHref(link.getAttribute("href") || "").toLowerCase();
      return path === `${normalizedUsername}/${type}` || path.endsWith(`/${type}`);
    }) || candidates.find((link) => {
      const text = helpers.cleanText(link.textContent || link.getAttribute("aria-label") || link.getAttribute("href") || "");
      return new RegExp(`\\b${type}\\b`, "i").test(text);
    });
  }

  async function openConnectionSurface(trigger, type) {
    const clickable = trigger.closest?.("a, button, [role='link'], [role='button']") || trigger;
    for (let attempt = 0; attempt < 3; attempt += 1) {
      clickable.scrollIntoView({ block: "center", inline: "center" });
      await randomSleep(600, 1100);
      clickLikeUser(clickable);
      assertCanScrape(usernameFromUrl());
      const root = await waitForConnectionRoot(type, 4500);
      if (root) {
        return root;
      }
    }
    return null;
  }

  function clickLikeUser(element) {
    const options = { bubbles: true, cancelable: true, composed: true, view: window, button: 0, buttons: 1 };
    try {
      element.focus?.();
    } catch (_error) {
      // Ignore focus failures from non-focusable elements.
    }
    try {
      if (typeof PointerEvent !== "undefined") {
        element.dispatchEvent(new PointerEvent("pointerover", { ...options, pointerType: "mouse", pointerId: 1 }));
        element.dispatchEvent(new PointerEvent("pointerenter", { ...options, pointerType: "mouse", pointerId: 1 }));
        element.dispatchEvent(new PointerEvent("pointerdown", { ...options, pointerType: "mouse", pointerId: 1 }));
        element.dispatchEvent(new PointerEvent("pointerup", { ...options, pointerType: "mouse", pointerId: 1, buttons: 0 }));
      }
      element.dispatchEvent(new MouseEvent("mouseover", options));
      element.dispatchEvent(new MouseEvent("mousedown", options));
      element.dispatchEvent(new MouseEvent("mouseup", { ...options, buttons: 0 }));
      element.click?.();
      element.dispatchEvent(new MouseEvent("click", { ...options, buttons: 0 }));
    } catch (_error) {
      element.click?.();
    }
  }

  async function waitForConnectionRoot(type, timeoutMs = 9000) {
    const startedAt = Date.now();
    while (Date.now() - startedAt < timeoutMs) {
      const dialog = Array.from(document.querySelectorAll("div[role='dialog']")).find((node) => {
        const text = helpers.cleanText(node.textContent || "");
        return new RegExp(type, "i").test(text) || extractConnectionUsernames(node, usernameFromUrl(), 3).length > 0;
      });
      if (dialog) {
        return dialog;
      }
      if (new RegExp(`/${type}/?$`, "i").test(window.location.pathname)) {
        return document.querySelector("main") || document;
      }
      await helpers.delay(300);
    }
    return null;
  }

  function pathFromHref(href) {
    if (!href) {
      return "";
    }
    try {
      return new URL(href, window.location.href).pathname.replace(/^\/+|\/+$/g, "");
    } catch (_error) {
      return String(href).split("?")[0].replace(/^\/+|\/+$/g, "");
    }
  }

  async function collectConnectionUsers(root, type, username, limit) {
    const users = [];
    const seen = new Set();
    const addUsers = (items) => {
      for (const item of items) {
        const key = item.toLowerCase();
        if (!item || seen.has(key) || users.length >= limit) {
          continue;
        }
        seen.add(key);
        users.push(item);
      }
    };
    addUsers(extractConnectionUsernames(root, username, limit));
    let previousCount = users.length;
    let stalled = 0;
    for (let index = 0; index < 28 && users.length < limit; index += 1) {
      clickConnectionControls(root, type);
      for (let step = 0; step < 3; step += 1) {
        scrollConnectionContainers(root);
        await randomSleep(650, 1150);
      }
      addUsers(extractConnectionUsernames(root, username, limit));
      if (users.length <= previousCount) {
        stalled += 1;
      } else {
        stalled = 0;
      }
      previousCount = users.length;
      if (stalled >= 6) {
        break;
      }
    }
    return users.slice(0, limit);
  }

  function clickConnectionControls(root, type) {
    const controls = Array.from(root.querySelectorAll("button, div[role='button'], span[role='button']"))
      .filter((button) => /see all|show more|load more|more/i.test(helpers.cleanText(button.textContent || button.getAttribute("aria-label") || "")))
      .slice(0, 4);
    for (const control of controls) {
      try {
        control.scrollIntoView({ block: "center", inline: "center" });
        control.click();
      } catch (_error) {
        // Ignore non-clickable Instagram controls.
      }
    }
  }

  function scrollConnectionContainers(root) {
    const target = findConnectionScrollContainer(root);
    const lastProfileLink = Array.from(root.querySelectorAll("a[href]"))
      .map((anchor) => ({ anchor, username: usernameFromProfileAnchor(anchor) }))
      .filter((item) => item.username)
      .pop()?.anchor;
    if (target) {
      const delta = Math.max(700, Math.floor(target.clientHeight * 0.95));
      const nextScrollTop = Math.min(target.scrollTop + delta, Math.max(0, target.scrollHeight - target.clientHeight));
      target.scrollTop = nextScrollTop;
      target.scrollTo?.({ top: nextScrollTop, behavior: "instant" });
      target.scrollBy?.({ top: delta, behavior: "instant" });
      lastProfileLink?.scrollIntoView({ block: "end", inline: "nearest" });
      dispatchScrollEvent(target);
      dispatchScrollWheel(target, delta);
      dispatchScrollWheel(root, delta);
      dispatchScrollWheel(document, delta);
      return;
    }
    lastProfileLink?.scrollIntoView({ block: "end", inline: "nearest" });
    window.scrollBy({ top: Math.floor(window.innerHeight * 0.5), behavior: "instant" });
    dispatchScrollWheel(document, 950);
  }

  function findConnectionScrollContainer(root) {
    const dialog = root?.closest?.("div[role='dialog']") || document.querySelector("div[role='dialog']");
    const scope = dialog || root || document;
    const explicitSelectors = [
      "div[style*='overflow: hidden auto']",
      "div[style*='overflow:hidden auto']",
      "div[style*='overflow-y: auto']",
      "div[style*='overflow-y:auto']",
      "div[style*='overflow: auto']",
      "div[style*='overflow:auto']",
      "div[style*='overflow: scroll']",
      "div[style*='overflow:scroll']"
    ];
    const candidates = helpers.unique([
      ...explicitSelectors.flatMap((selector) => Array.from(scope.querySelectorAll?.(selector) || [])),
      root,
      root?.parentElement,
      document.scrollingElement,
      ...Array.from(scope.querySelectorAll?.("div, ul, section") || [])
    ].filter(Boolean), (node) => node);

    return candidates
      .filter(isConnectionScrollableNode)
      .sort((left, right) => scoreConnectionScrollNode(right) - scoreConnectionScrollNode(left))[0] || null;
  }

  function isConnectionScrollableNode(node) {
    if (!node || !node.querySelectorAll || node.clientHeight <= 0) {
      return false;
    }
    const profileLinks = Array.from(node.querySelectorAll("a[href]")).filter((anchor) => usernameFromProfileAnchor(anchor));
    if (profileLinks.length === 0) {
      return false;
    }
    return node.scrollHeight > node.clientHeight + 10;
  }

  function scoreConnectionScrollNode(node) {
    const inlineStyle = String(node.getAttribute?.("style") || "").toLowerCase();
    let computedOverflow = "";
    try {
      const style = window.getComputedStyle(node);
      computedOverflow = `${style.overflow} ${style.overflowY}`.toLowerCase();
    } catch (_error) {
      computedOverflow = "";
    }
    const profileCount = Array.from(node.querySelectorAll?.("a[href]") || []).filter((anchor) => usernameFromProfileAnchor(anchor)).length;
    const explicitOverflowScore = /overflow\s*:\s*hidden\s+auto|overflow-y\s*:\s*auto|overflow\s*:\s*(auto|scroll)/i.test(inlineStyle) ? 2000 : 0;
    const computedOverflowScore = /(auto|scroll|overlay)/i.test(computedOverflow) ? 1000 : 0;
    const dialogPenalty = node.getAttribute?.("role") === "dialog" ? 400 : 0;
    return explicitOverflowScore + computedOverflowScore + (profileCount * 25) + Math.min(node.clientHeight, 900) - dialogPenalty;
  }

  function dispatchScrollEvent(target) {
    try {
      target.dispatchEvent(new Event("scroll", { bubbles: true, cancelable: false }));
    } catch (_error) {
      // Ignore nodes that cannot receive scroll events.
    }
  }

  function dispatchScrollWheel(target, deltaY) {
    try {
      target.dispatchEvent(new WheelEvent("wheel", { bubbles: true, cancelable: true, deltaY }));
    } catch (_error) {
      // Ignore nodes that cannot receive wheel events.
    }
  }

  function extractConnectionUsernames(root, currentUsername, limit) {
    const current = normalizeInstagramUsername(currentUsername || usernameFromUrl()).toLowerCase();
    const users = Array.from(root.querySelectorAll("a[href]"))
      .map((anchor) => usernameFromProfileAnchor(anchor))
      .filter((username) => username && username.toLowerCase() !== current);
    return helpers.unique(users, (username) => username.toLowerCase()).slice(0, limit);
  }

  function usernameFromProfileAnchor(anchor) {
    try {
      const path = new URL(anchor.getAttribute("href") || "", window.location.href).pathname.split("/").filter(Boolean);
      if (path.length !== 1 || !isProfilePathSegment(path[0])) {
        return "";
      }
      return normalizeInstagramUsername(path[0] || anchor.textContent || "");
    } catch (_error) {
      return "";
    }
  }

  function isProfilePathSegment(value) {
    return /^[A-Za-z0-9._]{1,30}$/.test(value || "") && !/^(p|reel|tv|explore|accounts|stories|direct|about|developer|privacy)$/i.test(value || "");
  }

  async function closeConnectionSurface(profileUrl) {
    const closeButton = document.querySelector("div[role='dialog'] button[aria-label='Close'], div[role='dialog'] svg[aria-label='Close']")?.closest("button");
    if (closeButton) {
      closeButton.click();
      await helpers.delay(600);
      return;
    }
    if (window.location.href !== profileUrl) {
      history.back();
      await helpers.delay(900);
      return;
    }
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", bubbles: true }));
    await helpers.delay(500);
  }

  async function collectPosts(job, partialResult) {
    if (getJobCommand(job) === "comments") {
      return collectCommentsForCursorPost(job, partialResult);
    }
    const limit = Number(job?.limits?.max_posts || job?.max_posts || 20);
    const offset = Number(job?.limits?.post_offset || job?.post_offset || job?.cursor?.post_offset || 0);
    const existingPostsCount = Number(job?.limits?.existing_posts_count || job?.existing_posts_count || 0);
    const maxComments = Number(job?.limits?.max_comments || job?.max_comments || 25);
    const existingPostKeys = getExistingPostKeys(job);
    const skipCount = Math.max(0, offset, existingPostsCount, existingPostKeys.size);
    const targetCount = skipCount + limit + existingPostKeys.size;
    const links = await collectPostLinks(targetCount);
    const candidates = links.filter((link, index) => {
      if (index < skipCount) {
        return false;
      }
      return !existingPostKeys.has(postKeyFromUrl(helpers.absoluteUrl(link.getAttribute("href") || "")));
    });
    const posts = [];
    for (const link of candidates.slice(0, limit)) {
      try {
        const activeLink = resolvePostLink(link) || link;
        const fallbackPost = collectPostPreview(activeLink);
        const fullPost = await collectPostFromModal(activeLink, fallbackPost, maxComments);
        posts.push(fullPost || fallbackPost);
        if (partialResult && typeof partialResult === "object") {
          partialResult.posts = helpers.unique([...(partialResult.posts || []), ...posts], (post) => post.url || post.id);
          partialResult.images = collectImages(partialResult.posts);
          rememberPartialResult(partialResult);
        }
      } catch (error) {
        if (isAuthRequiredError(error)) {
          throw error;
        }
        const partial = window.__orionLastPartialResult;
        if (partial && Array.isArray(partial.errors)) {
          partial.partial = true;
          partial.errors.push({ step: "post", message: error?.message || String(error) });
        }
      }
      await randomSleep(1700, 2700);
    }
    return helpers.unique(posts, (post) => post.url || post.id);
  }

  async function collectCommentsForCursorPost(job, partialResult) {
    const maxComments = Number(job?.limits?.max_comments || job?.max_comments || 25);
    const cursorUrl = job?.cursor?.hash_id || job?.hash_id || window.location.href;
    const postUrl = helpers.absoluteUrl(cursorUrl || window.location.href);
    const fallbackPost = {
      id: idFromUrl(postUrl),
      title: "Instagram post",
      text: "",
      caption: "",
      url: postUrl,
      post_url: postUrl,
      source: "instagram",
      comment_items: [],
      comment_details: []
    };
    const directRoot = await waitForPostRoot(postUrl);
    if (directRoot) {
      assertCanScrape(usernameFromUrl());
      await loadComments(directRoot, maxComments);
      const post = extractPost(directRoot, fallbackPost);
      if (partialResult && typeof partialResult === "object") {
        partialResult.posts = [post];
        partialResult.images = collectImages(partialResult.posts);
        rememberPartialResult(partialResult);
      }
      return [post];
    }
    const link = getPostLinks().find((candidate) => postKeyFromUrl(candidate.getAttribute("href") || "") === postKeyFromUrl(postUrl));
    if (!link) {
      return [fallbackPost];
    }
    const post = await collectPostFromModal(link, collectPostPreview(link), maxComments);
    return [post || fallbackPost];
  }

  function getExistingPostKeys(job) {
    const urls = [
      ...(Array.isArray(job?.existing_post_urls) ? job.existing_post_urls : []),
      ...(Array.isArray(job?.cursor?.existing_post_urls) ? job.cursor.existing_post_urls : [])
    ];
    return new Set(urls.map((url) => postKeyFromUrl(url)).filter(Boolean));
  }

  function postKeyFromUrl(url) {
    const absoluteUrl = helpers.absoluteUrl(url || "");
    return idFromUrl(absoluteUrl) || normalizePostUrl(absoluteUrl);
  }

  function normalizePostUrl(url) {
    try {
      const parsed = new URL(url, window.location.href);
      return `${parsed.origin}${parsed.pathname.replace(/\/+$/, "")}`.toLowerCase();
    } catch (_error) {
      return String(url || "").split("?")[0].replace(/\/+$/, "").toLowerCase();
    }
  }

  async function collectPostLinks(targetCount) {
    const seen = new Map();
    addVisiblePostLinks(seen);
    let previousCount = seen.size;
    let stalled = 0;
    for (let index = 0; index < 22 && seen.size < targetCount; index += 1) {
      window.scrollBy({ top: Math.max(600, Math.floor(window.innerHeight * 0.85)), behavior: "instant" });
      await randomSleep(900, 1700);
      addVisiblePostLinks(seen);
      if (seen.size <= previousCount) {
        stalled += 1;
      } else {
        stalled = 0;
      }
      previousCount = seen.size;
      if (stalled >= 5) {
        break;
      }
    }
    return Array.from(seen.values());
  }

  function getPostLinks() {
    return helpers.unique(
      Array.from(document.querySelectorAll("a[href*='/p/'], a[href*='/reel/'], a[href*='/tv/']")),
      (link) => idFromUrl(helpers.absoluteUrl(link.getAttribute("href") || "")) || link.getAttribute("href")
    );
  }

  function addVisiblePostLinks(seen) {
    for (const link of getPostLinks()) {
      const key = postKeyFromUrl(link.getAttribute("href") || "");
      if (key && !seen.has(key)) {
        seen.set(key, link);
      }
    }
  }

  function resolvePostLink(link) {
    const key = postKeyFromUrl(link?.getAttribute?.("href") || "");
    if (!key) {
      return link;
    }
    return getPostLinks().find((candidate) => postKeyFromUrl(candidate.getAttribute("href") || "") === key) || link;
  }

  function collectPostPreview(link) {
      const container = link.closest("article, div") || link;
      const media = collectPostMedia(link, container);
      const url = helpers.absoluteUrl(link.getAttribute("href") || "");
      const caption = media.alt || textNear(container);
      const counts = parseCounts(container);
      return {
        id: idFromUrl(url),
        title: caption || "Instagram post",
        text: caption,
        caption,
        url,
        post_url: url,
        datetime: findTime(container),
        likes: counts.likes,
        comments: counts.comments,
        views: counts.views,
        shares: counts.shares,
        comments_count: counts.comments,
        likes_count: counts.likes,
        views_count: counts.views,
        media_type: media.media_type,
        media_url: media.media_url,
        image_url: media.image_url,
        thumbnail: media.thumbnail,
        source: "instagram",
        comment_items: collectVisibleComments(container),
        comment_details: collectVisibleCommentDetails(container)
      };
  }

  async function collectPostFromModal(link, fallbackPost, maxComments) {
    const profileUrl = window.location.href;
    const postUrl = fallbackPost.url || helpers.absoluteUrl(link.getAttribute("href") || "");
    try {
      link.scrollIntoView({ block: "center", inline: "center" });
      await randomSleep(900, 1700);
      link.click();
      link.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
      await randomSleep(1700, 2700);
      assertCanScrape(usernameFromUrl());

      const root = await waitForPostRoot(postUrl);
      if (!root) {
        return fallbackPost;
      }
      assertCanScrape(usernameFromUrl());
      await loadComments(root, maxComments);
      const post = extractPost(root, fallbackPost);
      await closePostSurface(profileUrl);
      await randomSleep(900, 1700);
      return post;
    } catch (error) {
      await closePostSurface(profileUrl);
      if (isAuthRequiredError(error)) {
        throw error;
      }
      return fallbackPost;
    }
  }

  async function waitForPostRoot(postUrl) {
    const startedAt = Date.now();
    const postId = idFromUrl(postUrl);
    while (Date.now() - startedAt < 9000) {
      const dialogArticle = document.querySelector("div[role='dialog'] article");
      if (dialogArticle) {
        return dialogArticle;
      }
      const dialog = document.querySelector("div[role='dialog']");
      if (dialog) {
        return dialog;
      }
      const article = Array.from(document.querySelectorAll("article")).find((node) => {
        const link = node.querySelector("a[href*='/p/'], a[href*='/reel/'], a[href*='/tv/']");
        return !postId || link?.getAttribute("href")?.includes(postId);
      });
      if (article) {
        return article;
      }
      if (postId && window.location.href.includes(postId)) {
        return document.querySelector("article") || document.querySelector("main");
      }
      await helpers.delay(300);
    }
    return null;
  }

  async function loadComments(root, maxComments) {
    let previousCount = 0;
    let stalled = 0;
    for (let index = 0; index < 20; index += 1) {
      await clickCommentControls(root);
      scrollCommentContainers(root);
      await randomSleep(1700, 2700);
      await clickCommentControls(root);
      const currentCount = collectVisibleCommentDetails(root).length;
      if (currentCount >= maxComments) {
        break;
      }
      if (currentCount <= previousCount) {
        stalled += 1;
      } else {
        stalled = 0;
      }
      previousCount = currentCount;
      if (stalled >= 4) {
        break;
      }
    }
  }

  async function clickCommentControls(root) {
    const searchRoot = getPostSearchRoot(root);
    const controls = Array.from(searchRoot.querySelectorAll("button, div[role='button'], span[role='button'], a[role='link']"))
      .filter((button) => {
      const text = helpers.cleanText(button.textContent || button.getAttribute("aria-label") || "");
        return /view\s+(?:all\s+)?(?:\d+\s+)?(?:more\s+)?(?:comments?|replies)|load more|more comments|show more/i.test(text)
          && !/hide replies|reply$/i.test(text);
      })
      .slice(0, 8);
    for (const control of controls) {
      try {
        control.scrollIntoView({ block: "center", inline: "center" });
        await randomSleep(450, 900);
        control.click();
      } catch (_error) {
        // Ignore controls that Instagram blocks.
      }
    }
  }

  function scrollCommentContainers(root) {
    const searchRoot = getPostSearchRoot(root);
    const containers = [searchRoot, root, root?.parentElement, ...Array.from(searchRoot.querySelectorAll("div, ul, section"))]
      .filter(Boolean)
      .filter((node) => node.scrollHeight > node.clientHeight + 20);
    const target = containers.sort((left, right) => right.scrollHeight - left.scrollHeight)[0];
    if (target) {
      target.scrollTop = target.scrollHeight;
      target.scrollBy?.({ top: Math.max(500, Math.floor(target.clientHeight * 0.85)), behavior: "instant" });
      target.dispatchEvent(new WheelEvent("wheel", { bubbles: true, cancelable: true, deltaY: 900 }));
    }
    window.scrollBy({ top: Math.floor(window.innerHeight * 0.45), behavior: "instant" });
  }

  function extractPost(root, fallbackPost) {
    const media = collectPostMedia(root, root, fallbackPost);
    const comments = collectVisibleCommentDetails(root);
    const counts = parseCounts(root);
    const caption = findCaption(root, fallbackPost);
    return {
      ...fallbackPost,
      title: caption || fallbackPost.title || "Instagram post",
      text: caption || fallbackPost.text || "",
      caption: caption || fallbackPost.caption || "",
      datetime: findTime(root) || fallbackPost.datetime || "",
      likes: counts.likes || fallbackPost.likes || "",
      comments: counts.comments || String(comments.length || fallbackPost.comment_details?.length || ""),
      views: counts.views || fallbackPost.views || "",
      shares: counts.shares || fallbackPost.shares || "",
      comments_count: counts.comments || String(comments.length || ""),
      likes_count: counts.likes || fallbackPost.likes_count || "",
      views_count: counts.views || fallbackPost.views_count || "",
      media_type: media.media_type,
      media_url: media.media_url,
      image_url: media.image_url,
      thumbnail: media.thumbnail,
      comment_items: comments.map((comment) => comment.text),
      comment_details: comments
    };
  }

  function findCaption(root, fallbackPost) {
    const comments = collectVisibleCommentDetails(root);
    const ownerComment = comments.find((comment) => comment.sender_name && comment.sender_name.toLowerCase() === usernameFromUrl().toLowerCase());
    return ownerComment?.text || root.querySelector("h1")?.textContent?.trim() || fallbackPost.caption || fallbackPost.text || "";
  }

  async function closePostSurface(profileUrl) {
    const closeButton = document.querySelector("div[role='dialog'] button[aria-label='Close'], div[role='dialog'] svg[aria-label='Close']")?.closest("button");
    if (closeButton) {
      closeButton.click();
      await helpers.delay(500);
      return;
    }
    if (window.location.href !== profileUrl && /\/(p|reel|tv)\//i.test(window.location.pathname)) {
      history.back();
      await helpers.delay(900);
      return;
    }
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", bubbles: true }));
  }

  function collectImages(posts) {
    const postImages = posts.filter((post) => isCollectableInstagramImage(post.image_url, post.title || post.caption)).map((post) => ({
      image_url: post.image_url,
      thumbnail: post.thumbnail || post.image_url,
      title: post.caption || post.title || "Instagram image",
      source_url: post.url,
      source: "instagram"
    }));
    const pageImages = Array.from(document.querySelectorAll("article img[src], main img[src]"))
      .map((image) => ({
        image_url: helpers.absoluteUrl(image.getAttribute("src") || ""),
        thumbnail: helpers.absoluteUrl(image.getAttribute("src") || ""),
        title: image.getAttribute("alt") || "Instagram image",
        source: "instagram"
      }))
      .filter((image) => isCollectableInstagramImage(image.image_url, image.title));
    return helpers.unique([...postImages, ...pageImages], (image) => image.image_url).slice(0, 30);
  }

  function collectBio() {
    const header = document.querySelector("header");
    if (!header) {
      return "";
    }
    const candidates = Array.from(header.querySelectorAll("span, div"))
      .map((node) => helpers.cleanText(node.textContent || ""))
      .filter((text) => text && !/^\d/.test(text) && !/followers|following|posts/i.test(text));
    return candidates.slice(0, 4).join(" ");
  }

  function parseProfileStats() {
    const text = helpers.cleanText(document.querySelector("header")?.textContent || "");
    return {
      posts: findCount(text, /([\d.,]+[KMB]?)\s+posts?/i),
      followers: findCount(text, /([\d.,]+[KMB]?)\s+followers?/i),
      following: findCount(text, /([\d.,]+[KMB]?)\s+following/i)
    };
  }

  function parseCounts(root) {
    const text = helpers.cleanText(root?.textContent || "");
    return {
      likes: findCount(text, /([\d.,]+[KMB]?)\s+likes?/i) || findCount(text, /liked by.*?and\s+([\d.,]+[KMB]?)\s+others/i),
      comments: findCount(text, /view all\s+([\d.,]+[KMB]?)\s+comments?/i) || findCount(text, /([\d.,]+[KMB]?)\s+comments?/i),
      views: findCount(text, /([\d.,]+[KMB]?)\s+views?/i),
      shares: findCount(text, /([\d.,]+[KMB]?)\s+shares?/i)
    };
  }

  function findCount(text, pattern) {
    const match = String(text || "").match(pattern);
    return match ? match[1] : "";
  }

  function findTime(root) {
    return root?.querySelector("time")?.getAttribute("datetime") || "";
  }

  function textNear(root) {
    const candidates = Array.from(root?.querySelectorAll("span, h1, h2, div") || [])
      .map((node) => helpers.cleanText(node.textContent || ""))
      .filter((text) => text.length > 8 && !/likes?|comments?|followers?|following|posts?/i.test(text));
    return candidates[0] || "";
  }

  function collectVisibleComments(root) {
    return collectVisibleCommentDetails(root).map((comment) => comment.text);
  }

  function collectVisibleCommentDetails(root) {
    const searchRoot = getPostSearchRoot(root);
    const candidates = helpers.unique(
      Array.from(searchRoot?.querySelectorAll("ul li, article ul li") || []),
      (node) => node
    );
    const comments = candidates.map((node) => {
      const username = extractCommentUsername(node);
      const text = extractCommentText(node, username);
      if (!username || !text || isCommentChromeText(text)) {
        return null;
      }
      return {
        sender_name: username,
        text,
        date: node.querySelector("time")?.getAttribute("datetime") || "",
        likes: extractCommentLikes(node)
      };
    }).filter(Boolean);
    return helpers.unique(comments, (comment) => [comment.sender_name, comment.date, comment.text].join("|"));
  }

  function collectPostMedia(primaryRoot, fallbackRoot, fallbackPost = {}) {
    const roots = [primaryRoot, fallbackRoot].filter(Boolean);
    const video = roots.map((root) => root.querySelector("video")).find(Boolean);
    const image = findBestImage(roots);
    const videoUrl = getPlayableVideoUrl(video);
    const imageUrl = getImageUrl(image, video) || fallbackPost.image_url || fallbackPost.thumbnail || fallbackPost.media_url || "";
    const fallbackImageUrl = helpers.absoluteUrl(imageUrl || "");
    return {
      media_type: videoUrl ? "video" : "image",
      media_url: videoUrl || fallbackImageUrl,
      image_url: fallbackImageUrl,
      thumbnail: fallbackImageUrl || helpers.absoluteUrl(fallbackPost.thumbnail || ""),
      alt: image?.getAttribute("alt") || ""
    };
  }

  function findBestImage(roots) {
    const images = roots.flatMap((root) => Array.from(root.querySelectorAll?.("img[src], img[srcset]") || []));
    return images
      .filter((image) => isCollectableInstagramImage(getImageUrl(image), image.getAttribute("alt") || ""))
      .sort((left, right) => imageScore(right) - imageScore(left))[0] || null;
  }

  function imageScore(image) {
    const rect = image.getBoundingClientRect?.();
    const area = rect ? rect.width * rect.height : 0;
    const src = getImageUrl(image);
    const altBoost = image.getAttribute("alt") ? 5000 : 0;
    const cdnBoost = /cdninstagram|fbcdn/i.test(src) ? 3000 : 0;
    return area + altBoost + cdnBoost;
  }

  function getPlayableVideoUrl(video) {
    if (!video) {
      return "";
    }
    const candidates = [
      video.currentSrc,
      video.src,
      video.getAttribute("src"),
      ...Array.from(video.querySelectorAll("source[src]")).map((source) => source.getAttribute("src"))
    ];
    return candidates
      .map((value) => helpers.absoluteUrl(value || ""))
      .find((value) => isPlayableVideoUrl(value)) || "";
  }

  function isPlayableVideoUrl(value) {
    const url = String(value || "").trim();
    if (!url || /^(blob|data|about|javascript):/i.test(url)) {
      return false;
    }
    try {
      const parsed = new URL(url, window.location.href);
      if (!/^https?:$/i.test(parsed.protocol)) {
        return false;
      }
    } catch (_error) {
      return false;
    }
    return /\.(mp4|m4v|webm|mov)(?:[?#]|$)/i.test(url) || /\/video\//i.test(url);
  }

  function getImageUrl(image, video) {
    const srcsetUrl = firstSrcsetUrl(image?.getAttribute("srcset") || "");
    const candidates = [
      video?.poster,
      video?.getAttribute("poster"),
      image?.currentSrc,
      image?.src,
      image?.getAttribute("src"),
      srcsetUrl
    ];
    return candidates
      .map((value) => helpers.absoluteUrl(value || ""))
      .find((value) => isUsableImageUrl(value)) || "";
  }

  function firstSrcsetUrl(srcset) {
    return String(srcset || "").split(",").map((entry) => entry.trim().split(/\s+/)[0]).find(Boolean) || "";
  }

  function isUsableImageUrl(value) {
    const url = String(value || "").trim();
    return !!url && !/^(blob|about|javascript):/i.test(url);
  }

  function isCollectableInstagramImage(value, title = "") {
    const url = String(value || "").trim();
    const label = String(title || "");
    if (!isUsableImageUrl(url)) {
      return false;
    }
    return !/profile picture/i.test(label)
      && !/\/t51\.[^/]+-19\//i.test(url)
      && !/[?&]efg=[^&]*profile/i.test(url)
      && !/profile_pic/i.test(url);
  }

  function getPostSearchRoot(root) {
    return root?.closest?.("div[role='dialog']") || document.querySelector("div[role='dialog']") || root || document;
  }

  function extractCommentUsername(node) {
    const anchors = Array.from(node.querySelectorAll("h3 a[href^='/'], a[href^='/']"));
    for (const anchor of anchors) {
      const href = anchor.getAttribute("href") || "";
      const username = normalizeInstagramUsername(anchor.textContent || "");
      if (username && isProfileHref(href)) {
        return username;
      }
    }
    return normalizeInstagramUsername(node.querySelector("h3")?.textContent || "");
  }

  function extractCommentText(node, username) {
    const values = Array.from(node.querySelectorAll("span[dir='auto'], div[dir='auto'], span"))
      .filter((element) => {
        const ownerLi = element.closest("li");
        return (!ownerLi || ownerLi === node) && !element.closest("h3, time, button");
      })
      .map((element) => helpers.cleanText(element.textContent || ""))
      .filter((value) => isCommentTextCandidate(value, username));
    if (values.length) {
      return helpers.unique(values, (value) => value).join(" ").trim();
    }
    const clone = node.cloneNode(true);
    clone.querySelectorAll("li, h3, time, button, svg").forEach((item) => item.remove());
    return stripCommentChrome(helpers.cleanText(clone.textContent || ""), username);
  }

  function isCommentTextCandidate(value, username) {
    const text = helpers.cleanText(value || "");
    return !!text
      && text !== username
      && normalizeInstagramUsername(text) !== username
      && !isCommentChromeText(text);
  }

  function stripCommentChrome(value, username) {
    let text = helpers.cleanText(value || "");
    if (username && text.startsWith(username)) {
      text = text.slice(username.length).trim();
    }
    return text.replace(/^(like|reply|see translation)\b/i, "").trim();
  }

  function isCommentChromeText(value) {
    const text = helpers.cleanText(value || "");
    return /^(like|reply|see translation|view replies|hide replies|view all comments|load more comments|more comments|show more)$/i.test(text)
      || /^view\s+\d+\s+(?:replies|comments)$/i.test(text)
      || /^\d+[smhdw]$/i.test(text)
      || /^[\d.,]+[KMB]?\s+(?:likes?|replies|comments?|views?)$/i.test(text)
      || /^liked by\b/i.test(text);
  }

  function extractCommentLikes(node) {
    const text = Array.from(node.querySelectorAll("span, button, div"))
      .map((item) => helpers.cleanText(item.textContent || ""))
      .find((value) => /^[\d.,]+[KMB]?\s+likes?$/i.test(value));
    return findCount(text || "", /^([\d.,]+[KMB]?)\s+likes?$/i);
  }

  function normalizeInstagramUsername(value) {
    const match = helpers.cleanText(value || "").replace(/^@/, "").match(/[A-Za-z0-9._]{1,30}/);
    return match ? match[0] : "";
  }

  function isProfileHref(href) {
    try {
      const path = new URL(href, window.location.href).pathname.split("/").filter(Boolean);
      return path.length === 1 && !/^(p|reel|tv|explore|accounts|stories)$/i.test(path[0]);
    } catch (_error) {
      return false;
    }
  }

  function rememberPartialResult(result) {
    window.__orionLastPartialResult = {
      ...result,
      posts: Array.isArray(result.posts) ? [...result.posts] : [],
      images: Array.isArray(result.images) ? [...result.images] : [],
      followers: Array.isArray(result.followers) ? [...result.followers] : [],
      following: Array.isArray(result.following) ? [...result.following] : [],
      errors: Array.isArray(result.errors) ? [...result.errors] : []
    };
  }

  function addPartialError(result, step, error) {
    result.partial = true;
    result.errors = Array.isArray(result.errors) ? result.errors : [];
    result.errors.push({ step, message: error?.message || String(error) });
    rememberPartialResult(result);
  }

  async function randomSleep(minMs = 1700, maxMs = 2700) {
    const duration = Math.floor(minMs + Math.random() * (maxMs - minMs));
    await helpers.delay(duration);
  }

  function idFromUrl(url) {
    const match = String(url || "").match(/\/(?:p|reel|tv)\/([^/?#]+)/i);
    return match ? match[1] : "";
  }
})();
