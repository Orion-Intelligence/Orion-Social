(function () {
  window.dispatchEvent(new CustomEvent("orion-extension-ready", {
    detail: {
      source: "orion-extension",
      at: new Date().toISOString()
    }
  }));
})();
