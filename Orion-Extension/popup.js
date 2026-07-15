const loginPanel = document.getElementById("loginPanel");
const connectionPanel = document.getElementById("connectionPanel");
const authForm = document.getElementById("authForm");
const loginUsernameInput = document.getElementById("loginUsername");
const loginPasswordInput = document.getElementById("loginPassword");
const loginButton = document.getElementById("loginButton");
const loginError = document.getElementById("loginError");
const statusLabel = document.getElementById("statusLabel");
const connectionValue = document.getElementById("connectionValue");
const stateValue = document.getElementById("stateValue");
const authValue = document.getElementById("authValue");
const jobValue = document.getElementById("jobValue");
const errorValue = document.getElementById("errorValue");
const resultValue = document.getElementById("resultValue");
const connectButton = document.getElementById("connectButton");
const clearAuthButton = document.getElementById("clearAuthButton");
const MESSAGE_TIMEOUT_MS = 2500;

let currentStatus = {};

renderStatus({ authState: "loading", state: "loading", lastError: "" });

document.addEventListener("DOMContentLoaded", () => {
  refresh();
});

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setLoginBusy(true);
  loginError.textContent = "";
  statusLabel.textContent = "Logging in";

  const response = await sendMessage({
    type: "orion:login",
    username: loginUsernameInput.value,
    password: loginPasswordInput.value,
    authApiBaseUrl: currentStatus.authApiBaseUrl
  });

  loginPasswordInput.value = "";
  setLoginBusy(false);

  if (!response?.ok) {
    loginError.textContent = formatLoginError(response?.error);
    if (response?.status) {
      renderStatus(response.status);
    } else {
      statusLabel.textContent = "Login failed";
    }
    return;
  }

  if (response.status) {
    renderStatus(response.status);
  }
  await refresh();
});

connectButton.addEventListener("click", async () => {
  await sendMessage({ type: "orion:connect" });
  await refresh();
});

clearAuthButton.addEventListener("click", async () => {
  await sendMessage({
    type: "orion:clearAuthSession",
    authApiBaseUrl: currentStatus.authApiBaseUrl,
    pageOrigin: "extension_popup"
  });
  loginPasswordInput.value = "";
  loginUsernameInput.focus();
  await refresh();
});

chrome.runtime.onMessage.addListener((message) => {
  if (message?.type === "orion:statusChanged") {
    renderStatus(message.status);
  }
});

async function refresh() {
  const response = await sendMessage({ type: "orion:getStatus" });
  if (response?.ok) {
    renderStatus(response.status);
    return;
  }
  renderStatus({ authState: "unknown", state: "loading", lastError: response?.error || "Starting extension..." });
}

function renderStatus(status) {
  currentStatus = status || {};
  const hasAuth = Boolean(currentStatus.hasSessionToken || currentStatus.hasAuthToken || currentStatus.authState === "authenticated" || currentStatus.connected);
  loginPanel.hidden = hasAuth;
  connectionPanel.hidden = !hasAuth;

  if (!hasAuth) {
    statusLabel.textContent = authRequiredLabel(currentStatus);
    loginError.textContent = currentStatus.authState === "expired" ? currentStatus.lastError || "Session expired. Log in again." : "";
    return;
  }

  const connectionText = connectionLabel(currentStatus);
  statusLabel.textContent = connectionText;
  connectionValue.textContent = connectionText;
  stateValue.textContent = currentStatus.state || "unknown";
  authValue.textContent = currentStatus.authState || "authenticated";
  jobValue.textContent = currentStatus.activeJobId || "none";
  errorValue.textContent = currentStatus.lastError || "none";
  resultValue.textContent = formatLastResult(currentStatus);
}

function authRequiredLabel(status) {
  if (status.authState === "loading") {
    return "Loading";
  }
  if (status.state === "loading") {
    return "Starting extension";
  }
  if (status.authState === "login_failed") {
    return "Login failed";
  }
  if (status.authState === "expired") {
    return "Session expired";
  }
  return "Login required";
}

function connectionLabel(status) {
  if (status.connected) {
    return "Connected";
  }
  if (["connecting", "registering"].includes(status.state)) {
    return "Connecting";
  }
  return "Not connected";
}

function formatLastResult(status) {
  const summary = status.lastResultSummary || {};
  if (!status.lastResultAt && !Object.keys(summary).length) {
    return "none";
  }
  const parts = [];
  if (status.lastResultAck) {
    parts.push(status.lastResultAck);
  }
  if (summary.posts !== undefined) {
    parts.push(`${summary.posts || 0} posts`);
  }
  if (summary.images) {
    parts.push(`${summary.images} images`);
  }
  if (summary.followers) {
    parts.push(`${summary.followers} followers`);
  }
  if (summary.following) {
    parts.push(`${summary.following} following`);
  }
  if (summary.partial) {
    parts.push("partial");
  }
  if (summary.errors) {
    parts.push(`${summary.errors} scrape errors`);
  }
  return parts.length ? parts.join(" · ") : "ready";
}

function setLoginBusy(isBusy) {
  loginButton.disabled = isBusy;
  loginUsernameInput.disabled = isBusy;
  loginPasswordInput.disabled = isBusy;
}

function formatLoginError(error) {
  const message = String(error || "login_failed");
  const normalized = message.toLowerCase();
  if (normalized.includes("networkerror") || normalized.includes("failed to fetch") || normalized.includes("load failed") || normalized.includes("unreachable")) {
    return "Orion Intelligence API not reachable. Open http://127.0.0.1:8080 or https://127.0.0.1:8443 in the browser, then reload the extension.";
  }
  return message;
}

function sendMessage(message) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = (response) => {
      if (settled) {
        return;
      }
      settled = true;
      clearTimeout(timeout);
      resolve(response);
    };
    const timeout = setTimeout(() => {
      finish({ ok: false, error: "Extension is starting. Try again in a moment." });
    }, MESSAGE_TIMEOUT_MS);
    try {
      chrome.runtime.sendMessage(message, (response) => {
        const error = chrome.runtime.lastError;
        if (error) {
          finish({ ok: false, error: error.message || String(error) });
          return;
        }
        finish(response);
      });
    } catch (error) {
      finish({ ok: false, error: error.message || String(error) });
    }
  });
}
