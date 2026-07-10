(function () {
  const helpers = window.OrionScraperHelpers;

  window.OrionScrapers = window.OrionScrapers || {};
  window.OrionScrapers.github = {
    selectors: [".vcard-fullname", ".avatar-user", "[itemprop='owns']", "main"],
    async run(job) {
      const username = job.username || usernameFromUrl();
      return {
        platform: "github",
        username,
        url: window.location.href,
        profile: {
          username,
          display_name: helpers.text(".vcard-fullname") || username,
          bio: helpers.text(".user-profile-bio"),
          avatar_url: helpers.absoluteUrl(document.querySelector(".avatar-user")?.getAttribute("src") || ""),
          company: helpers.text(".p-org"),
          location: helpers.text(".p-label"),
          website: helpers.absoluteUrl(document.querySelector("[data-test-selector='profile-website-url'], .vcard-detail a[rel='nofollow me']")?.getAttribute("href") || "")
        },
        posts: collectRepositories(),
        images: [],
        followers: [],
        following: []
      };
    }
  };

  function usernameFromUrl() {
    const match = window.location.pathname.match(/^\/([^/?#]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function collectRepositories() {
    return Array.from(document.querySelectorAll("[itemprop='owns'] [itemprop='name codeRepository'], .pinned-item-list-item")).slice(0, 12).map((node) => {
      const link = node.closest("a") || node.querySelector("a");
      return {
        title: helpers.cleanText(node.textContent || ""),
        url: helpers.absoluteUrl(link?.getAttribute("href") || ""),
        source: "github"
      };
    });
  }
})();
