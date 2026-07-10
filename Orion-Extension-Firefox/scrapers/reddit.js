(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  window.OrionScrapers.reddit = {
    selectors: ["shreddit-post", "article", "[data-testid='post-container']", "h1"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      const posts = collectPosts(job);
      const profile = {
        display_name: helpers.meta("og:title").replace(/\s+-\s+Reddit$/, "") || username,
        username,
        bio: helpers.meta("description"),
        url: window.location.href,
        avatar_url: findAvatar(),
        cover_url: helpers.meta("og:image")
      };

      return {
        platform: "reddit",
        username,
        url: window.location.href,
        profile,
        posts,
        images: collectImages(posts),
        followers: [],
        following: []
      };
    }
  };

  function usernameFromUrl() {
    const match = window.location.pathname.match(/\/user\/([^/]+)/i);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function collectPosts(job) {
    const limit = Number(job?.limits?.max_posts || job?.max_posts || 25);
    const candidates = Array.from(document.querySelectorAll("shreddit-post, article, [data-testid='post-container']"));
    const posts = candidates.slice(0, limit).map((node) => {
      const title = helpers.cleanText(node.getAttribute("post-title") || node.querySelector("h1, h2, h3, a[slot='title']")?.textContent || "");
      const linkNode = node.querySelector("a[href*='/comments/'], a[slot='title'], a[href]");
      const imageNode = node.querySelector("img[src]");
      return {
        id: node.getAttribute("id") || node.getAttribute("post-id") || "",
        title,
        text: helpers.cleanText(node.querySelector("[slot='text-body'], div[slot='text-body'], p")?.textContent || ""),
        url: helpers.absoluteUrl(linkNode?.getAttribute("href") || window.location.href),
        created_at: node.getAttribute("created-timestamp") || node.querySelector("time")?.getAttribute("datetime") || "",
        score: node.getAttribute("score") || "",
        comments_count: node.getAttribute("comment-count") || "",
        image_url: helpers.absoluteUrl(imageNode?.getAttribute("src") || "")
      };
    });

    return helpers.unique(posts, (post) => post.url || post.title);
  }

  function collectImages(posts) {
    return helpers.unique(
      posts.filter((post) => post.image_url).map((post) => ({
        image_url: post.image_url,
        source_url: post.url,
        title: post.title,
        source: "reddit"
      })),
      (image) => image.image_url
    );
  }

  function findAvatar() {
    const selectors = [
      "img[alt*='Avatar']",
      "img[src*='styles.redditmedia.com']",
      "img[src*='redditstatic.com/avatars']"
    ];
    for (const selector of selectors) {
      const value = document.querySelector(selector)?.getAttribute("src");
      if (value) {
        return helpers.absoluteUrl(value);
      }
    }
    return "";
  }
})();
