(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  const scraper = {
    selectors: ["[data-testid='UserName']", "[data-testid='tweetText']", "article[data-testid='tweet']"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      const profile = {
        username,
        display_name: helpers.text("[data-testid='UserName'] span") || document.title.replace(/\s+\/\s+X$/, ""),
        bio: helpers.text("[data-testid='UserDescription']"),
        location: helpers.text("[data-testid='UserLocation']"),
        website: helpers.absoluteUrl(document.querySelector("[data-testid='UserUrl'] a")?.getAttribute("href") || ""),
        avatar_url: helpers.absoluteUrl(document.querySelector("[data-testid='UserAvatar-Container-unknown'] img, img[src*='profile_images']")?.getAttribute("src") || ""),
        cover_url: helpers.absoluteUrl(document.querySelector("[data-testid='UserProfileHeader_Items'] img, a[href*='header_photo'] img")?.getAttribute("src") || "")
      };

      return {
        platform: "x",
        username,
        url: window.location.href,
        profile,
        posts: collectPosts(job),
        images: collectImages(),
        followers: [],
        following: []
      };
    }
  };

  window.OrionScrapers.x = scraper;
  window.OrionScrapers.twitter = scraper;

  function usernameFromUrl() {
    const match = window.location.pathname.match(/^\/([^/?#]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function collectPosts(job) {
    const limit = Number(job?.limits?.max_posts || job?.max_posts || 10);
    return Array.from(document.querySelectorAll("article[data-testid='tweet']")).slice(0, limit).map((node) => {
      const link = Array.from(node.querySelectorAll("a[href*='/status/']")).pop();
      return {
        id: (link?.getAttribute("href") || "").split("/status/")[1]?.split(/[/?#]/)[0] || "",
        text: helpers.cleanText(node.querySelector("[data-testid='tweetText']")?.textContent || node.textContent || ""),
        url: helpers.absoluteUrl(link?.getAttribute("href") || ""),
        created_at: node.querySelector("time")?.getAttribute("datetime") || "",
        image_url: helpers.absoluteUrl(node.querySelector("img[src*='media']")?.getAttribute("src") || ""),
        source: "x"
      };
    }).filter((post) => post.text || post.url);
  }

  function collectImages() {
    return helpers.unique(Array.from(document.querySelectorAll("article img[src*='media']")).map((image) => ({
      image_url: helpers.absoluteUrl(image.getAttribute("src") || ""),
      title: image.getAttribute("alt") || "X media",
      source: "x"
    })), (image) => image.image_url).slice(0, 20);
  }
})();
