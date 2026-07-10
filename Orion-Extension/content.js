(function () {
  window.__orionRunScraper = async function (job) {
    try {
      const platform = String(job.platform || "").toLowerCase();
      const registry = window.OrionScrapers || {};
      const scraper = registry[platform] || registry[platform === "twitter" ? "x" : platform];
      if (!scraper || typeof scraper.run !== "function") {
        return { success: false, error: `scraper_not_found:${platform}`, message: `scraper_not_found:${platform}`, error_code: "SCRAPER_NOT_FOUND", platform };
      }
      const helpers = window.OrionScraperHelpers;
      if (helpers?.settlePage) {
        await helpers.settlePage(scraper.selectors || []);
      }
      const data = await scraper.run(job);
      return { success: true, data };
    } catch (error) {
      const normalizedError = normalizeScraperError(error, job);
      if (normalizedError.error_code === "AUTH_REQUIRED") {
        return { success: false, ...normalizedError };
      }
      if (window.__orionLastPartialResult && typeof window.__orionLastPartialResult === "object") {
        return {
          success: true,
          data: {
            ...window.__orionLastPartialResult,
            partial: true,
            error: normalizedError.message || normalizedError.error
          }
        };
      }
      return { success: false, ...normalizedError };
    }
  };

  function normalizeScraperError(error, job) {
    const message = error?.message || error?.error || String(error || "scraper_failed");
    return {
      error: message,
      message,
      error_code: String(error?.error_code || error?.code || "").trim() || null,
      platform: String(error?.platform || job?.platform || "").trim().toLowerCase() || null,
      login_url: isSafeHttpUrl(error?.login_url) ? String(error.login_url) : null
    };
  }

  function isSafeHttpUrl(value) {
    try {
      const parsed = new URL(String(value || ""));
      return parsed.protocol === "http:" || parsed.protocol === "https:";
    } catch (_error) {
      return false;
    }
  }
})();
