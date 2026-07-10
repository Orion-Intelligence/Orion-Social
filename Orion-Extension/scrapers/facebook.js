(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  window.OrionScrapers.facebook = {
    selectors: ["h1", "[role='article']", "[data-pagelet*='FeedUnit']", "[role='main']"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      return {
        platform: "facebook",
        username,
        url: window.location.href,
        profile: {
          username,
          display_name: helpers.text("h1, [role='main'] h1") || document.title,
          bio: helpers.text("[data-pagelet='ProfileTilesFeed'] span, [role='main'] span"),
          avatar_url: helpers.absoluteUrl(document.querySelector("image[href], svg image, [role='main'] img")?.getAttribute("href") || document.querySelector("[role='main'] img")?.getAttribute("src") || ""),
          cover_url: helpers.absoluteUrl(document.querySelector("img[data-imgperflogname='profileCoverPhoto'], [data-pagelet='ProfileCover'] img")?.getAttribute("src") || "")
        },
        posts: collectPosts(job),
        images: collectImages(),
        followers: [],
        following: []
      };
    }
  };

  function usernameFromUrl() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts[0] || "";
  }

  function collectPosts(job) {
    const limit = Number(job?.limits?.max_posts || job?.max_posts || 10);
    return Array.from(document.querySelectorAll("[role='article'], div[data-pagelet*='FeedUnit']")).slice(0, limit).map((node) => {
      const link = node.querySelector("a[href*='/posts/'], a[href*='story_fbid'], a[href]");
      return {
        title: helpers.cleanText(node.querySelector("strong, h2, h3")?.textContent || "Facebook post"),
        text: helpers.cleanText(node.textContent || "").slice(0, 1200),
        url: helpers.absoluteUrl(link?.getAttribute("href") || ""),
        image_url: helpers.absoluteUrl(node.querySelector("img[src]")?.getAttribute("src") || ""),
        source: "facebook"
      };
    }).filter((post) => post.text || post.url);
  }

  function collectImages() {
    return helpers.unique(Array.from(document.querySelectorAll("[role='main'] img[src], [role='article'] img[src]")).map((image) => ({
      image_url: helpers.absoluteUrl(image.getAttribute("src") || ""),
      title: image.getAttribute("alt") || "Facebook image",
      source: "facebook"
    })), (image) => image.image_url).slice(0, 30);
  }
})();
