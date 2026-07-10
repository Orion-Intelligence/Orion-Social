(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  window.OrionScrapers.linkedin = {
    selectors: ["h1", ".text-heading-xlarge", ".feed-shared-update-v2", "[data-urn*='activity']"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      const profile = {
        username,
        display_name: firstText(["h1", ".text-heading-xlarge", ".pv-text-details__left-panel h1"]) || document.title,
        headline: firstText([".text-body-medium", ".pv-text-details__left-panel .text-body-medium"]),
        bio: firstText([".pv-shared-text-with-see-more", ".display-flex.ph5.pv3 .visually-hidden"]),
        location: firstText([".text-body-small.inline.t-black--light.break-words", ".pv-text-details__left-panel .text-body-small"]),
        avatar_url: helpers.absoluteUrl(document.querySelector(".pv-top-card-profile-picture__image--show, img.profile-photo-edit__preview, img[alt*='profile']")?.getAttribute("src") || ""),
        cover_url: helpers.absoluteUrl(document.querySelector(".profile-background-image__image-container img, .profile-background-image img")?.getAttribute("src") || "")
      };

      return {
        platform: "linkedin",
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

  function usernameFromUrl() {
    const match = window.location.pathname.match(/\/(?:in|company|school)\/([^/?#]+)/i);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function firstText(selectors) {
    for (const selector of selectors) {
      const value = helpers.text(selector);
      if (value) {
        return value;
      }
    }
    return "";
  }

  function collectPosts(job) {
    const limit = Number(job?.limits?.max_posts || job?.max_posts || 10);
    return Array.from(document.querySelectorAll(".feed-shared-update-v2, article, [data-urn*='activity']"))
      .slice(0, limit)
      .map((node) => {
        const link = node.querySelector("a[href*='activity'], a[href*='feed/update'], a[href]");
        return {
          title: helpers.cleanText(node.querySelector(".feed-shared-update-v2__description, .update-components-text, span[dir='ltr']")?.textContent || ""),
          text: helpers.cleanText(node.textContent || "").slice(0, 1200),
          url: helpers.absoluteUrl(link?.getAttribute("href") || ""),
          image_url: helpers.absoluteUrl(node.querySelector("img[src]")?.getAttribute("src") || ""),
          source: "linkedin"
        };
      })
      .filter((post) => post.text || post.url);
  }

  function collectImages() {
    return helpers.unique(Array.from(document.querySelectorAll("img[src]")).map((image) => ({
      image_url: helpers.absoluteUrl(image.getAttribute("src") || ""),
      title: image.getAttribute("alt") || "LinkedIn image",
      source: "linkedin"
    })), (image) => image.image_url).slice(0, 20);
  }
})();
