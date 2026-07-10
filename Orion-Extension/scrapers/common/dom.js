(function () {
  const helpers = {
    text(selector, root = document) {
      const node = root.querySelector(selector);
      return helpers.cleanText(node?.textContent || "");
    },

    attr(selector, attribute, root = document) {
      const node = root.querySelector(selector);
      return node?.getAttribute(attribute) || "";
    },

    cleanText(value) {
      return String(value || "").replace(/\s+/g, " ").trim();
    },

    absoluteUrl(value) {
      if (!value) {
        return "";
      }
      try {
        return new URL(value, window.location.href).toString();
      } catch (_error) {
        return String(value);
      }
    },

    unique(items, keyFn) {
      const seen = new Set();
      return items.filter((item) => {
        const key = keyFn(item);
        if (!key || seen.has(key)) {
          return false;
        }
        seen.add(key);
        return true;
      });
    },

    meta(name) {
      return document.querySelector(`meta[property="${name}"], meta[name="${name}"]`)?.content || "";
    },

    async delay(ms) {
      await new Promise((resolve) => setTimeout(resolve, ms));
    },

    async waitForAny(selectors, timeoutMs = 12000) {
      const startedAt = Date.now();
      while (Date.now() - startedAt < timeoutMs) {
        if (selectors.some((selector) => document.querySelector(selector))) {
          return true;
        }
        await helpers.delay(350);
      }
      return false;
    },

    async settlePage(selectors = []) {
      await helpers.waitForAny(selectors, 12000);
      for (let index = 0; index < 3; index += 1) {
        window.scrollBy({ top: Math.max(500, Math.floor(window.innerHeight * 0.8)), behavior: "instant" });
        await helpers.delay(900);
      }
      window.scrollTo({ top: 0, behavior: "instant" });
      await helpers.delay(700);
    }
  };

  window.OrionScraperHelpers = helpers;
  window.OrionScrapers = window.OrionScrapers || {};
})();
