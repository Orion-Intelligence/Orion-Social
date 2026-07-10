(function () {
  const chromeRuntime = globalThis.chrome?.runtime;
  const browserRuntime = globalThis.browser?.runtime;
  const runtime = chromeRuntime || browserRuntime;
  const TOKEN_KEY = "token";
  let lastToken = null;

  if (!runtime?.sendMessage) {
    return;
  }

  function sendMessage(message) {
    try {
      if (chromeRuntime?.sendMessage) {
        const result = chromeRuntime.sendMessage(message, () => {
          void chromeRuntime.lastError;
        });
        if (result?.catch) {
          result.catch(() => undefined);
        }
        return;
      }
      const result = browserRuntime.sendMessage(message);
      if (result?.catch) {
        result.catch(() => undefined);
      }
    } catch (_error) {
      // The background worker may be sleeping or the extension may be reloading.
    }
  }

  function syncSession() {
    const token = localStorage.getItem(TOKEN_KEY) || "";
    if (token === lastToken) {
      return;
    }
    lastToken = token;
    const authApiBaseUrl = `${window.location.origin}/api`;
    if (token) {
      sendMessage({
        type: "orion:syncAuthSession",
        token,
        authApiBaseUrl,
        pageOrigin: window.location.origin
      });
      return;
    }
    sendMessage({
      type: "orion:clearAuthSession",
      authApiBaseUrl,
      pageOrigin: window.location.origin
    });
  }

  syncSession();
  window.addEventListener("storage", syncSession);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      syncSession();
    }
  });
  window.setInterval(syncSession, 30000);
})();
