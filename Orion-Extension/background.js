const DEFAULT_SETTINGS = {
  backendUrl: "ws://127.0.0.1:8020/extensions/ws",
  authApiBaseUrl: "https://127.0.0.1:8443/api",
  authToken: "",
  sessionToken: "",
  refreshToken: "",
  authPageOrigin: "",
  authSyncBlocked: false,
  autoConnect: true,
  closeTabsAfterScrape: true
};

const AUTH_EXPIRY_SKEW_SECONDS = 30;
const RESULT_ACK_TIMEOUT_MS = 15000;
const RESULT_ACK_RETRY_COUNT = 2;

const AUTH_API_BASE_URL_CANDIDATES = [
  DEFAULT_SETTINGS.authApiBaseUrl,
  "https://localhost:8443/api",
  "http://127.0.0.1:8080/api",
  "http://localhost:8080/api",
  "http://127.0.0.1:4200/api",
  "http://localhost:4200/api"
];

const AUTH_PROXY_BASE_URL_CANDIDATES = [
  "http://127.0.0.1:8020",
  "http://localhost:8020"
];

const SUPPORTED_PLATFORMS = ["reddit", "linkedin", "x", "twitter", "instagram", "facebook", "github"];
const SCRAPER_FILES = {
  reddit: ["scrapers/common/dom.js", "scrapers/reddit.js", "content.js"],
  linkedin: ["scrapers/common/dom.js", "scrapers/linkedin.js", "content.js"],
  x: ["scrapers/common/dom.js", "scrapers/x.js", "content.js"],
  twitter: ["scrapers/common/dom.js", "scrapers/x.js", "content.js"],
  instagram: ["scrapers/common/dom.js", "scrapers/instagram.js", "content.js"],
  facebook: ["scrapers/common/dom.js", "scrapers/facebook.js", "content.js"],
  github: ["scrapers/common/dom.js", "scrapers/github.js", "content.js"]
};

let socket = null;
let reconnectTimer = null;
let heartbeatTimer = null;
let authExpiryTimer = null;
let intentionalDisconnect = false;
let activeJobId = null;
let activeJob = null;
const authExpiredJobIds = new Set();
const pendingResultAcks = new Map();
let statusSnapshot = {
  connected: false,
  state: "disconnected",
  extensionId: "",
  backendUrl: DEFAULT_SETTINGS.backendUrl,
  activeJobId: null,
  lastError: "",
  lastSeenAt: null
};

chrome.runtime.onInstalled.addListener(async () => {
  const existing = await storageGet(Object.keys(DEFAULT_SETTINGS));
  await storageSet({ ...DEFAULT_SETTINGS, ...compactSettings(existing) });
  await setStatus({ state: "installed" });
  connectIfEnabled();
});

chrome.runtime.onStartup.addListener(() => {
  connectIfEnabled();
});

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  handleRuntimeMessage(message).then(sendResponse).catch((error) => {
    sendResponse({ ok: false, error: error.message || String(error) });
  });
  return true;
});

connectIfEnabled();

async function handleRuntimeMessage(message) {
  if (!message || typeof message !== "object") {
    return { ok: false, error: "invalid_message" };
  }

  if (message.type === "orion:getStatus") {
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:updateSettings") {
    const nextSettings = sanitizeSettings(message.settings || {});
    await storageSet(nextSettings);
    await setStatus({ backendUrl: nextSettings.backendUrl || statusSnapshot.backendUrl, lastError: "" });
    reconnectNow();
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:login") {
    const settings = await getSettings();
    const username = typeof message.username === "string" ? message.username.trim() : "";
    const password = typeof message.password === "string" ? message.password : "";
    const authApiBaseUrl = typeof message.authApiBaseUrl === "string" ? normalizeApiBaseUrl(message.authApiBaseUrl) : DEFAULT_SETTINGS.authApiBaseUrl;
    if (!username || !password) {
      return { ok: false, error: "missing_credentials" };
    }

    let loginResult;
    try {
      loginResult = await loginWithOrion(username, password, authApiBaseUrl, settings.backendUrl);
    } catch (error) {
      const message = error.message || String(error);
      await setStatus({ authState: "login_failed", lastError: message });
      return { ok: false, error: message, status: await getStatus() };
    }

    if (loginResult.twofa_required) {
      await setStatus({ authState: "twofa_required", lastError: "twofa_required" });
      return { ok: false, error: "twofa_required", status: await getStatus() };
    }
    if (!loginResult.access_token) {
      await setStatus({ authState: "login_failed", lastError: "login_failed" });
      return { ok: false, error: "login_failed", status: await getStatus() };
    }

    await storageSet({
      sessionToken: loginResult.access_token,
      refreshToken: String(loginResult.refresh_token || ""),
      authApiBaseUrl: loginResult.authApiBaseUrl || authApiBaseUrl,
      authPageOrigin: "extension_popup",
      authSyncBlocked: false,
      autoConnect: true
    });
    await setStatus({ authState: "authenticated", lastError: "" });
    await reconnectNow(true);
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:syncAuthSession") {
    const token = typeof message.token === "string" ? message.token.trim() : "";
    const authApiBaseUrl = typeof message.authApiBaseUrl === "string" ? normalizeApiBaseUrl(message.authApiBaseUrl) : "";
    const authPageOrigin = typeof message.pageOrigin === "string" ? message.pageOrigin.trim() : "";
    const settings = await getSettings();
    if (!token) {
      return { ok: false, error: "missing_token" };
    }
    if (settings.authSyncBlocked && authPageOrigin !== "extension_popup") {
      await setStatus({ authState: "unauthenticated", lastError: "Extension auth sync is disabled after logout. Log in from the extension popup." });
      return { ok: false, error: "auth_sync_blocked", status: await getStatus() };
    }
    const storedSessionToken = String(settings.sessionToken || "").trim();
    const storedAuthToken = String(settings.authToken || "").trim();
    const tokenUnchanged = token === storedSessionToken || token === storedAuthToken;
    await storageSet({
      sessionToken: token,
      ...(authApiBaseUrl ? { authApiBaseUrl } : {}),
      ...(authPageOrigin ? { authPageOrigin } : {}),
      authSyncBlocked: false,
      autoConnect: true
    });
    await setStatus({ authState: "authenticated", lastError: "" });
    if (activeJobId) {
      await setStatus({ lastError: "" });
      return { ok: true, status: await getStatus(), skippedReconnect: "active_job" };
    }
    if (tokenUnchanged && socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
      return { ok: true, status: await getStatus(), skippedReconnect: "token_unchanged" };
    }
    await reconnectNow(true);
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:clearAuthSession") {
    const authApiBaseUrl = typeof message.authApiBaseUrl === "string" ? normalizeApiBaseUrl(message.authApiBaseUrl) : "";
    const authPageOrigin = typeof message.pageOrigin === "string" ? message.pageOrigin.trim() : "";
    await storageSet({
      authToken: "",
      sessionToken: "",
      refreshToken: "",
      authSyncBlocked: true,
      ...(authApiBaseUrl ? { authApiBaseUrl } : {}),
      ...(authPageOrigin ? { authPageOrigin } : {})
    });
    await setStatus({ authState: "unauthenticated", connected: false, extensionId: "" });
    clearAuthExpiryTimer();
    disconnect("auth_session_cleared");
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:connect") {
    await reconnectNow(true);
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:disconnect") {
    disconnect("manual_disconnect");
    return { ok: true, status: await getStatus() };
  }

  if (message.type === "orion:runJob") {
    runJob(message.job).catch((error) => {
      const failedJob = normalizeJob(message.job);
      sendJobResult(failedJob, { success: false, ...normalizeJobError(error, failedJob) });
    });
    return { ok: true };
  }

  return { ok: false, error: "unknown_message_type" };
}

async function connectIfEnabled() {
  const settings = await getSettings();
  if (settings.autoConnect) {
    connect(settings);
  } else {
    await setStatus({ state: "idle", backendUrl: settings.backendUrl });
  }
}

async function reconnectNow(force = false) {
  const settings = await getSettings();
  disconnect("reconnect");
  if (force || settings.autoConnect) {
    await storageSet({ autoConnect: true });
    await connect({ ...settings, autoConnect: true });
  } else {
    await setStatus({ state: "idle", backendUrl: settings.backendUrl });
  }
}

async function connect(settings) {
  clearReconnect();
  clearHeartbeat();

  if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
    return;
  }

  const preparedAuth = await prepareAuth(settings);
  if (!preparedAuth.token) {
    const authState = preparedAuth.authState || "missing";
    const lastError = authState === "expired"
      ? "Session expired. Log in again."
      : authState === "refresh_failed"
        ? statusSnapshot.lastError || "Authentication refresh failed. Log in again."
        : "Open Orion Intelligence while logged in to authenticate the extension.";
    await setStatus({ connected: false, state: "auth_required", backendUrl: settings.backendUrl || DEFAULT_SETTINGS.backendUrl, authState, lastError });
    return;
  }

  const backendUrl = settings.backendUrl || DEFAULT_SETTINGS.backendUrl;
  scheduleAuthExpiryLogout(preparedAuth.token);
  await setStatus({ connected: false, state: "connecting", backendUrl, lastError: "", authState: preparedAuth.authState });

  try {
    intentionalDisconnect = false;
    socket = new WebSocket(backendUrl);
  } catch (error) {
    scheduleReconnect(error.message || String(error));
    return;
  }

  socket.addEventListener("open", () => {
    setStatus({ connected: false, state: "registering", extensionId: "", backendUrl, lastError: "", lastSeenAt: new Date().toISOString() });
    sendSocketMessage({
      type: "extension_online",
      auth_token: preparedAuth.token,
      auth_type: preparedAuth.authType,
      capabilities: {
        platforms: SUPPORTED_PLATFORMS,
        commands: ["profile", "posts", "videos", "shorts", "images", "followers", "following"]
      }
    });
  });

  socket.addEventListener("message", (event) => {
    handleSocketMessage(event.data).catch((error) => {
      sendSocketMessage({ type: "extension_error", error: error.message || String(error) });
    });
  });

  socket.addEventListener("close", (event) => {
    rejectAllPendingResultAcks(new Error(formatSocketCloseError(event)));
    if (intentionalDisconnect) {
      intentionalDisconnect = false;
      return;
    }
    if (isAuthCloseEvent(event)) {
      logoutExpiredSession("auth_session_expired").catch((error) => {
        setStatus({ authState: "expired", lastError: error.message || String(error) });
      });
      return;
    }
    scheduleReconnect(formatSocketCloseError(event), event.code, event.reason || "");
  });

  socket.addEventListener("error", () => {
    scheduleReconnect(`socket_error: cannot reach Orion Social at ${backendUrl}`);
  });
}

function disconnect(reason) {
  clearReconnect();
  clearHeartbeat();
  rejectAllPendingResultAcks(new Error(reason || "disconnect"));
  intentionalDisconnect = true;
  if (socket) {
    try {
      socket.close(1000, reason || "disconnect");
    } catch (_error) {
      // Ignore close errors from already-closed sockets.
    }
  }
  socket = null;
  activeJobId = null;
  setStatus({ connected: false, state: "disconnected", extensionId: "", activeJobId: null });
}

async function logoutExpiredSession(reason = "auth_session_expired") {
  clearReconnect();
  clearHeartbeat();
  clearAuthExpiryTimer();
  try {
    await failActiveJobForAuthExpiry(reason);
  } catch (error) {
    await setStatus({ lastError: error.message || String(error) });
  }
  intentionalDisconnect = true;
  const updates = {
    authToken: "",
    sessionToken: "",
    refreshToken: "",
    authSyncBlocked: true
  };
  await storageSet(updates);
  if (socket) {
    try {
      socket.close(1000, reason);
    } catch (_error) {
      // Ignore close errors from already-closed sockets.
    }
  }
  socket = null;
  activeJobId = null;
  activeJob = null;
  await setStatus({
    connected: false,
    state: "auth_required",
    extensionId: "",
    activeJobId: null,
    authState: "expired",
    lastError: "Session expired. Log in again."
  });
}

function scheduleReconnect(error, closeCode = null, closeReason = "") {
  clearHeartbeat();
  rejectAllPendingResultAcks(new Error(error || "socket_disconnected"));
  if (socket) {
    try {
      socket.close();
    } catch (_error) {
      // Ignore close errors from already-closed sockets.
    }
  }
  socket = null;
  setStatus({
    connected: false,
    state: "disconnected",
    extensionId: "",
    lastError: error || "disconnected",
    lastCloseCode: closeCode,
    lastCloseReason: closeReason,
    activeJobId: activeJobId || null
  });
  clearReconnect();
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    connectIfEnabled();
  }, 5000);
}

function isAuthCloseEvent(event) {
  const reason = String(event?.reason || "").toLowerCase();
  return event?.code === 1008 && /invalid_orion_session|missing_extension_auth|invalid_extension_token|auth|token|session/.test(reason);
}

function formatSocketCloseError(event) {
  const code = event?.code || 0;
  const reason = String(event?.reason || "").trim();
  if (reason) {
    return `ws_closed_${code}: ${reason}`;
  }
  if (code === 1006) {
    return "ws_closed_1006: Orion Social websocket is unreachable";
  }
  return `ws_closed_${code || "unknown"}`;
}

async function handleSocketMessage(rawData) {
  const message = parseJson(rawData);
  if (!message || typeof message !== "object") {
    return;
  }

  if (message.type === "job" || message.type === "scrape_job") {
    await runJob(message.job || message);
  }

  if (message.type === "extension_registered") {
    await setStatus({
      connected: true,
      state: "online",
      extensionId: String(message.extension_id || ""),
      lastError: "",
      lastSeenAt: new Date().toISOString()
    });
    clearHeartbeat();
    heartbeatTimer = setInterval(() => {
      sendSocketMessage({ type: "heartbeat", active_job_id: activeJobId, at: new Date().toISOString() });
    }, 25000);
  }

  if (message.type === "ping") {
    sendSocketMessage({ type: "pong", at: new Date().toISOString() });
  }

  if (message.type === "job_result_ack") {
    resolveResultAck(message);
    if (message.accepted === false) {
      await setStatus({ lastError: String(message.error || "job_result_not_accepted") });
    }
  }
}

async function runJob(job) {
  const normalizedJob = normalizeJob(job);
  if (!normalizedJob.job_id) {
    throw new Error("job_id_required");
  }

  activeJobId = normalizedJob.job_id;
  activeJob = normalizedJob;
  await setStatus({ state: "running", activeJobId });
  sendProgress(normalizedJob, "job_received", 20);

  let tabId = null;
  try {
    sendProgress(normalizedJob, "opening_tab", 25);
    const tab = await createTab({ url: normalizedJob.url, active: false });
    tabId = tab.id;
    await waitForTabComplete(tabId, 45000);

    sendProgress(normalizedJob, "waiting_for_dom", 35);
    const result = await executeScraper(tabId, normalizedJob);
    if (authExpiredJobIds.has(normalizedJob.job_id)) {
      throw createAuthExpiredError();
    }
    await setStatus({
      state: "result_ready",
      activeJobId,
      lastResultSummary: summarizeResultData(result),
      lastResultAt: new Date().toISOString(),
      lastError: ""
    });
    sendProgress(normalizedJob, scraperStep(normalizedJob), 85);
    sendProgress(normalizedJob, "complete", 100);
    const ack = await sendJobResult(normalizedJob, { success: true, data: result });
    await setStatus({
      state: "result_delivered",
      activeJobId,
      lastResultAck: ack?.accepted === false ? "rejected" : "accepted",
      lastResultAt: new Date().toISOString(),
      lastError: ack?.accepted === false ? String(ack.error || "job_result_not_accepted") : ""
    });
  } catch (error) {
    const normalizedError = normalizeJobError(error, normalizedJob);
    if (normalizedError.error_code === "AUTH_REQUIRED") {
      sendProgress(normalizedJob, "auth_required", 45);
    }
    await setStatus({ lastError: normalizedError.message || normalizedError.error });
    if (!authExpiredJobIds.has(normalizedJob.job_id)) {
      try {
        await sendJobResult(normalizedJob, { success: false, ...normalizedError });
      } catch (sendError) {
        await setStatus({ lastError: `job_result_send_failed: ${sendError.message || String(sendError)}` });
      }
    }
  } finally {
    if (tabId !== null) {
      try {
        await removeTab(tabId);
      } catch (_error) {
        // The user may have closed the tab manually.
      }
    }
    if (activeJob?.job_id === normalizedJob.job_id) {
      activeJob = null;
    }
    activeJobId = null;
    const expired = authExpiredJobIds.has(normalizedJob.job_id) || statusSnapshot.authState === "expired";
    authExpiredJobIds.delete(normalizedJob.job_id);
    await setStatus({ state: expired ? "auth_required" : socket?.readyState === WebSocket.OPEN ? "online" : "disconnected", activeJobId: null });
  }
}

async function failActiveJobForAuthExpiry(reason = "auth_session_expired") {
  if (!activeJob?.job_id || authExpiredJobIds.has(activeJob.job_id)) {
    return false;
  }
  authExpiredJobIds.add(activeJob.job_id);
  sendProgress(activeJob, "auth_expired", 90);
  await sendJobResult(activeJob, {
    success: false,
    error: "Extension session expired. Log in again and retry.",
    message: "Extension session expired while scraping. Log in again and retry.",
    error_code: "AUTH_EXPIRED",
    platform: activeJob.platform,
    details: { reason }
  });
  return true;
}

function createAuthExpiredError() {
  const error = new Error("Extension session expired while scraping. Log in again and retry.");
  error.code = "AUTH_EXPIRED";
  error.error_code = "AUTH_EXPIRED";
  return error;
}

async function executeScraper(tabId, job) {
  const files = SCRAPER_FILES[job.platform];
  if (!files) {
    throw new Error(`unsupported_platform:${job.platform}`);
  }

  await executeFiles(tabId, files);
  const execution = await executeFunction(tabId, (scrapeJob) => window.__orionRunScraper(scrapeJob), [job]);

  if (!execution || !execution.result) {
    throw new Error("empty_scraper_result");
  }
  if (execution.result.success === false) {
    const scraperError = new Error(execution.result.message || execution.result.error || "scraper_failed");
    Object.assign(scraperError, normalizeJobError(execution.result, job));
    throw scraperError;
  }
  return execution.result.data || execution.result;
}

async function executeFiles(tabId, files) {
  if (chrome.scripting?.executeScript) {
    await chrome.scripting.executeScript({ target: { tabId }, files });
    return;
  }
  for (const file of files) {
    await new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tabId, { file }, () => {
        const error = chrome.runtime.lastError;
        if (error) {
          reject(new Error(error.message));
          return;
        }
        resolve();
      });
    });
  }
}

async function executeFunction(tabId, func, args) {
  if (chrome.scripting?.executeScript) {
    const [execution] = await chrome.scripting.executeScript({ target: { tabId }, func, args });
    return execution;
  }
  const code = `(${func.toString()})(${args.map((value) => JSON.stringify(value)).join(",")});`;
  const [result] = await new Promise((resolve, reject) => {
    chrome.tabs.executeScript(tabId, { code }, (values) => {
      const error = chrome.runtime.lastError;
      if (error) {
        reject(new Error(error.message));
        return;
      }
      resolve(values || []);
    });
  });
  return { result };
}

function waitForTabComplete(tabId, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      chrome.tabs.onUpdated.removeListener(listener);
      reject(new Error("tab_load_timeout"));
    }, timeoutMs);

    const listener = (updatedTabId, changeInfo) => {
      if (updatedTabId === tabId && changeInfo.status === "complete") {
        clearTimeout(timeout);
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    };

    chrome.tabs.onUpdated.addListener(listener);
    getTab(tabId).then((tab) => {
      if (tab.status === "complete") {
        clearTimeout(timeout);
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    }).catch((error) => {
      clearTimeout(timeout);
      chrome.tabs.onUpdated.removeListener(listener);
      reject(error);
    });
  });
}

function createTab(options) {
  return new Promise((resolve, reject) => {
    try {
      const result = chrome.tabs.create(options, (tab) => {
        const error = chrome.runtime.lastError;
        if (error) {
          reject(new Error(error.message));
          return;
        }
        if (!tab?.id) {
          reject(new Error("tab_create_failed"));
          return;
        }
        resolve(tab);
      });
      if (result && typeof result.then === "function") {
        result.then(resolve).catch(reject);
      }
    } catch (error) {
      reject(error);
    }
  });
}

function getTab(tabId) {
  return new Promise((resolve, reject) => {
    try {
      const result = chrome.tabs.get(tabId, (tab) => {
        const error = chrome.runtime.lastError;
        if (error) {
          reject(new Error(error.message));
          return;
        }
        resolve(tab);
      });
      if (result && typeof result.then === "function") {
        result.then(resolve).catch(reject);
      }
    } catch (error) {
      reject(error);
    }
  });
}

function removeTab(tabId) {
  return new Promise((resolve, reject) => {
    try {
      const result = chrome.tabs.remove(tabId, () => {
        const error = chrome.runtime.lastError;
        if (error) {
          reject(new Error(error.message));
          return;
        }
        resolve();
      });
      if (result && typeof result.then === "function") {
        result.then(resolve).catch(reject);
      }
    } catch (error) {
      reject(error);
    }
  });
}

function sendProgress(job, step, progress) {
  return sendSocketMessage({
    type: "job_progress",
    job_id: job.job_id,
    status: "pending",
    step,
    progress
  });
}

async function sendJobResult(job, outcome) {
  const normalizedError = outcome.success ? {} : normalizeJobError(outcome, job);
  const payload = {
    type: "job_result",
    job_id: job.job_id,
    status: outcome.success ? "done" : "error",
    success: Boolean(outcome.success),
    data: outcome.data || null,
    error: normalizedError.error || outcome.error || null,
    message: normalizedError.message || outcome.message || outcome.error || null,
    error_code: normalizedError.error_code || null,
    platform: normalizedError.platform || job.platform || null,
    login_url: normalizedError.login_url || null
  };
  const ack = await sendSocketMessageWithResultAck(payload);
  return ack || payload;
}

async function sendSocketMessageWithResultAck(payload) {
  let lastError = null;
  for (let attempt = 0; attempt <= RESULT_ACK_RETRY_COUNT; attempt += 1) {
    const ackId = createAckId(payload.job_id);
    const payloadWithAck = { ...payload, ack_id: ackId };
    const ackPromise = waitForResultAck(ackId, payload.job_id);
    if (!sendSocketMessage(payloadWithAck)) {
      clearPendingResultAck(ackId);
      throw new Error("job_result_socket_closed");
    }
    try {
      return await ackPromise;
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error("job_result_ack_timeout");
}

function waitForResultAck(ackId, jobId) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      pendingResultAcks.delete(ackId);
      reject(new Error(`job_result_ack_timeout:${jobId || ""}`));
    }, RESULT_ACK_TIMEOUT_MS);
    pendingResultAcks.set(ackId, { jobId, resolve, reject, timeout });
  });
}

function resolveResultAck(message) {
  const ackId = String(message?.ack_id || "");
  const pending = pendingResultAcks.get(ackId);
  if (!pending) {
    return false;
  }
  clearTimeout(pending.timeout);
  pendingResultAcks.delete(ackId);
  pending.resolve(message);
  return true;
}

function clearPendingResultAck(ackId) {
  const pending = pendingResultAcks.get(ackId);
  if (!pending) {
    return;
  }
  clearTimeout(pending.timeout);
  pendingResultAcks.delete(ackId);
}

function rejectAllPendingResultAcks(error) {
  for (const [ackId, pending] of pendingResultAcks.entries()) {
    clearTimeout(pending.timeout);
    pending.reject(error);
    pendingResultAcks.delete(ackId);
  }
}

function createAckId(jobId) {
  return `${jobId || "job"}:${Date.now()}:${Math.random().toString(36).slice(2)}`;
}

function summarizeResultData(data) {
  const source = data && typeof data === "object" ? data : {};
  return {
    platform: source.platform || "",
    username: source.username || "",
    posts: Array.isArray(source.posts) ? source.posts.length : 0,
    images: Array.isArray(source.images) ? source.images.length : 0,
    followers: Array.isArray(source.followers) ? source.followers.length : 0,
    following: Array.isArray(source.following) ? source.following.length : 0,
    partial: Boolean(source.partial),
    errors: Array.isArray(source.errors) ? source.errors.length : 0
  };
}

function normalizeJobError(error, job) {
  const details = error?.details && typeof error.details === "object" ? error.details : {};
  const message = error?.message || error?.error || details.message || details.error || String(error || "extension_job_failed");
  return {
    error: message,
    message,
    error_code: String(error?.error_code || error?.code || details.error_code || details.code || "").trim() || null,
    platform: String(error?.platform || details.platform || job?.platform || "").trim().toLowerCase() || null,
    login_url: isSafeHttpUrl(error?.login_url || details.login_url) ? String(error?.login_url || details.login_url) : null
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

function sendSocketMessage(payload) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    return false;
  }
  socket.send(JSON.stringify(payload));
  return true;
}

function normalizeJob(job) {
  const source = job && typeof job === "object" ? job : {};
  const platform = normalizePlatform(source.platform);
  const username = String(source.username || "").replace(/^@+/, "");
  return {
    ...source,
    job_id: String(source.job_id || source.jobId || source.id || ""),
    command: String(source.command || source.social_data_type || "profile").toLowerCase(),
    platform,
    username,
    url: String(source.url || buildProfileUrl(platform, username)),
    social_data_type: String(source.social_data_type || source.command || "profile_info"),
    limits: source.limits || {},
    cursor: source.cursor || { hash_id: source.hash_id || "" }
  };
}

function normalizePlatform(platform) {
  const value = String(platform || "").trim().toLowerCase();
  return value === "twitter" ? "x" : value;
}

function buildProfileUrl(platform, username) {
  const encoded = encodeURIComponent(username || "");
  const urls = {
    reddit: `https://www.reddit.com/user/${encoded}/`,
    linkedin: `https://www.linkedin.com/in/${encoded}/`,
    x: `https://x.com/${encoded}`,
    twitter: `https://x.com/${encoded}`,
    instagram: `https://www.instagram.com/${encoded}/`,
    facebook: `https://www.facebook.com/${encoded}`,
    github: `https://github.com/${encoded}`
  };
  return urls[platform] || "";
}

function scraperStep(job) {
  if (job.command.includes("image")) {
    return "collecting_images";
  }
  if (["posts", "videos", "shorts"].some((value) => job.command.includes(value))) {
    return "collecting_posts";
  }
  return "collecting_profile";
}

async function getSettings() {
  const values = await storageGet(Object.keys(DEFAULT_SETTINGS));
  return { ...DEFAULT_SETTINGS, ...compactSettings(values) };
}

function sanitizeSettings(settings) {
  const next = {};
  if (typeof settings.backendUrl === "string" && settings.backendUrl.trim()) {
    next.backendUrl = settings.backendUrl.trim();
  }
  if (typeof settings.authApiBaseUrl === "string" && settings.authApiBaseUrl.trim()) {
    next.authApiBaseUrl = normalizeApiBaseUrl(settings.authApiBaseUrl);
  }
  if (typeof settings.authToken === "string") {
    next.authToken = settings.authToken.trim();
  }
  if (typeof settings.autoConnect === "boolean") {
    next.autoConnect = settings.autoConnect;
  }
  if (typeof settings.closeTabsAfterScrape === "boolean") {
    next.closeTabsAfterScrape = settings.closeTabsAfterScrape;
  }
  return next;
}

async function prepareAuth(settings) {
  const manualToken = String(settings.authToken || "").trim();
  const sessionToken = String(settings.sessionToken || "").trim();
  if (manualToken && !looksLikeJwt(manualToken)) {
    return { token: manualToken, authType: "static", authState: "static_token" };
  }
  const token = sessionToken || manualToken;
  if (!token) {
    return { token: "", authType: "", authState: "missing" };
  }
  if (looksLikeJwt(token) && isJwtExpired(token, AUTH_EXPIRY_SKEW_SECONDS)) {
    await logoutExpiredSession("auth_token_expired");
    return { token: "", authType: "orion_jwt", authState: "expired" };
  }
  const refreshResult = await refreshOrionToken(token, settings.authApiBaseUrl, settings.backendUrl);
  if (!refreshResult.token) {
    if (refreshResult.shouldLogout) {
      await logoutExpiredSession(refreshResult.reason || "auth_session_expired");
      return { token: "", authType: "orion_jwt", authState: "expired" };
    }
    if (looksLikeJwt(token) && refreshResult.networkError && !isJwtExpired(token, AUTH_EXPIRY_SKEW_SECONDS)) {
      await setStatus({ authState: "refresh_failed", lastError: refreshResult.reason || "auth_refresh_unreachable" });
      return { token, authType: "orion_jwt", authState: "refresh_failed" };
    }
    return { token: "", authType: "orion_jwt", authState: "refresh_failed" };
  }
  await storageSet({
    sessionToken: refreshResult.token,
    ...(refreshResult.authApiBaseUrl ? { authApiBaseUrl: refreshResult.authApiBaseUrl } : {})
  });
  return { token: refreshResult.token, authType: "orion_jwt", authState: "authenticated" };
}

async function refreshOrionToken(token, authApiBaseUrl, backendUrl) {
  let lastNetworkError = "";
  for (const proxyBaseUrl of getAuthProxyBaseUrlCandidates(backendUrl)) {
    try {
      const response = await fetch(`${proxyBaseUrl}/extensions/auth/refresh`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ token })
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        const reason = authRefreshFailureReason(response.status, payload);
        await setStatus({ authState: shouldLogoutForRefreshStatus(response.status) ? "expired" : "refresh_failed", lastError: reason });
        return { token: "", shouldLogout: shouldLogoutForRefreshStatus(response.status), reason };
      }
      const accessToken = String(payload?.access_token || "").trim();
      if (!accessToken) {
        await setStatus({ authState: "refresh_failed", lastError: "auth_refresh_empty_token" });
        return { token: "", shouldLogout: true, reason: "auth_refresh_empty_token" };
      }
      await setStatus({ authState: "authenticated", lastError: "" });
      return { token: accessToken };
    } catch (error) {
      lastNetworkError = error.message || String(error);
    }
  }

  for (const apiBaseUrl of getAuthApiBaseUrlCandidates(authApiBaseUrl)) {
    try {
      const response = await fetch(`${apiBaseUrl}/token/refresh`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ token })
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        const reason = authRefreshFailureReason(response.status, payload);
        await setStatus({ authState: shouldLogoutForRefreshStatus(response.status) ? "expired" : "refresh_failed", lastError: reason });
        return { token: "", shouldLogout: shouldLogoutForRefreshStatus(response.status), reason };
      }
      const accessToken = String(payload?.access_token || "").trim();
      if (!accessToken) {
        await setStatus({ authState: "refresh_failed", lastError: "auth_refresh_empty_token" });
        return { token: "", shouldLogout: true, reason: "auth_refresh_empty_token" };
      }
      await setStatus({ authState: "authenticated", lastError: "" });
      return { token: accessToken, authApiBaseUrl: apiBaseUrl };
    } catch (error) {
      lastNetworkError = error.message || String(error);
    }
  }
  const reason = formatAuthNetworkError(lastNetworkError);
  await setStatus({ authState: "refresh_failed", lastError: reason });
  return { token: "", networkError: true, reason };
}

async function loginWithOrion(username, password, authApiBaseUrl, backendUrl) {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  form.set("scope", "orion_extension");

  let lastNetworkError = "";
  for (const proxyBaseUrl of getAuthProxyBaseUrlCandidates(backendUrl)) {
    try {
      const response = await fetch(`${proxyBaseUrl}/extensions/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload?.detail || `login_${response.status}`);
      }
      return { ...(payload || {}), authApiBaseUrl };
    } catch (error) {
      const message = error.message || String(error);
      if (!isNetworkFetchError(message)) {
        throw error;
      }
      lastNetworkError = message;
    }
  }

  for (const apiBaseUrl of getAuthApiBaseUrlCandidates(authApiBaseUrl)) {
    try {
      const response = await fetch(`${apiBaseUrl}/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: form.toString()
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload?.detail || `login_${response.status}`);
      }
      return { ...(payload || {}), authApiBaseUrl: apiBaseUrl };
    } catch (error) {
      const message = error.message || String(error);
      if (!isNetworkFetchError(message)) {
        throw error;
      }
      lastNetworkError = message;
    }
  }
  throw new Error(formatAuthNetworkError(lastNetworkError));
}

function normalizeApiBaseUrl(value) {
  return String(value || DEFAULT_SETTINGS.authApiBaseUrl).trim().replace(/\/+$/, "");
}

function getAuthApiBaseUrlCandidates(preferred) {
  const values = [preferred, ...AUTH_API_BASE_URL_CANDIDATES]
    .filter((value) => typeof value === "string" && value.trim())
    .map(normalizeApiBaseUrl);
  return [...new Set(values)];
}

function getAuthProxyBaseUrlCandidates(backendUrl) {
  const values = [backendUrlToHttpBaseUrl(backendUrl), ...AUTH_PROXY_BASE_URL_CANDIDATES]
    .filter((value) => typeof value === "string" && value.trim())
    .map((value) => String(value).trim().replace(/\/+$/, ""));
  return [...new Set(values)];
}

function backendUrlToHttpBaseUrl(backendUrl) {
  try {
    const url = new URL(backendUrl || DEFAULT_SETTINGS.backendUrl);
    url.protocol = url.protocol === "wss:" ? "https:" : "http:";
    url.pathname = "";
    url.search = "";
    url.hash = "";
    return url.toString().replace(/\/+$/, "");
  } catch (_error) {
    return "";
  }
}

function isNetworkFetchError(message) {
  const value = String(message || "").toLowerCase();
  return value.includes("failed to fetch")
    || value.includes("networkerror")
    || value.includes("load failed")
    || value.includes("could not connect")
    || value.includes("unreachable")
    || value.includes("fetch");
}

function formatAuthNetworkError(detail) {
  const suffix = detail ? ` (${detail})` : "";
  return `Orion Intelligence API not reachable. Start Orion Intelligence or open its HTTPS URL once to trust the local certificate.${suffix}`;
}

function authRefreshFailureReason(status, payload) {
  const detail = payload?.detail || payload?.message || "";
  return detail ? `auth_refresh_${status}: ${detail}` : `auth_refresh_${status}`;
}

function shouldLogoutForRefreshStatus(status) {
  return [401, 403, 419, 440].includes(Number(status));
}

function looksLikeJwt(value) {
  return /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(String(value || ""));
}

function isJwtExpired(token, skewSeconds = 0) {
  const exp = jwtExpirySeconds(token);
  return exp !== null && Date.now() / 1000 >= exp - Number(skewSeconds || 0);
}

function jwtExpirySeconds(token) {
  const payload = decodeJwtPayload(token);
  const exp = Number(payload?.exp);
  return Number.isFinite(exp) && exp > 0 ? exp : null;
}

function decodeJwtPayload(token) {
  try {
    const payload = String(token || "").split(".")[1] || "";
    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized + "=".repeat((4 - normalized.length % 4) % 4);
    return JSON.parse(globalThis.atob(padded));
  } catch (_error) {
    return null;
  }
}

function scheduleAuthExpiryLogout(token) {
  clearAuthExpiryTimer();
  if (!looksLikeJwt(token)) {
    return;
  }
  const exp = jwtExpirySeconds(token);
  if (exp === null) {
    return;
  }
  const delayMs = Math.max(0, Math.floor((exp - Date.now() / 1000 - AUTH_EXPIRY_SKEW_SECONDS) * 1000));
  authExpiryTimer = setTimeout(() => {
    authExpiryTimer = null;
    logoutExpiredSession("auth_token_expired").catch((error) => {
      setStatus({ authState: "expired", lastError: error.message || String(error) });
    });
  }, Math.min(delayMs, 2147483647));
}

function clearAuthExpiryTimer() {
  if (authExpiryTimer) {
    clearTimeout(authExpiryTimer);
    authExpiryTimer = null;
  }
}

function compactSettings(values) {
  return Object.fromEntries(Object.entries(values || {}).filter(([, value]) => value !== undefined && value !== null));
}

async function getStatus() {
  const values = await storageGet([...Object.keys(DEFAULT_SETTINGS), "statusSnapshot"]);
  const settings = { ...DEFAULT_SETTINGS, ...compactSettings(values) };
  const storedToken = settings.sessionToken || (looksLikeJwt(settings.authToken) ? settings.authToken : "");
  if (storedToken && isJwtExpired(storedToken, AUTH_EXPIRY_SKEW_SECONDS)) {
    await logoutExpiredSession("auth_token_expired");
    return getStatus();
  }
  const storedStatus = values.statusSnapshot && typeof values.statusSnapshot === "object" ? values.statusSnapshot : {};
  return {
    ...storedStatus,
    ...statusSnapshot,
    backendUrl: settings.backendUrl,
    authApiBaseUrl: settings.authApiBaseUrl,
    authPageOrigin: settings.authPageOrigin,
    autoConnect: settings.autoConnect,
    closeTabsAfterScrape: settings.closeTabsAfterScrape,
    hasAuthToken: Boolean(settings.authToken),
    hasSessionToken: Boolean(settings.sessionToken),
    hasRefreshToken: Boolean(settings.refreshToken),
    authSyncBlocked: Boolean(settings.authSyncBlocked)
  };
}

async function setStatus(patch) {
  statusSnapshot = { ...statusSnapshot, ...patch };
  await storageSet({ statusSnapshot });
  safeRuntimeSendMessage({ type: "orion:statusChanged", status: statusSnapshot });
}

function storageGet(keys) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = (value) => {
      if (settled) {
        return;
      }
      settled = true;
      resolve(value && typeof value === "object" ? value : {});
    };
    try {
      const result = chrome.storage.local.get(keys, (value) => {
        const error = chrome.runtime.lastError;
        finish(error ? {} : value);
      });
      if (result && typeof result.then === "function") {
        result.then(finish).catch(() => finish({}));
      }
    } catch (_error) {
      finish({});
    }
  });
}

function storageSet(values) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const finish = (error) => {
      if (settled) {
        return;
      }
      settled = true;
      if (error) {
        reject(new Error(error.message || String(error)));
        return;
      }
      resolve();
    };
    try {
      const result = chrome.storage.local.set(values, () => {
        finish(chrome.runtime.lastError || null);
      });
      if (result && typeof result.then === "function") {
        result.then(() => finish(null)).catch(finish);
      }
    } catch (error) {
      finish(error);
    }
  });
}

function safeRuntimeSendMessage(message) {
  try {
    const result = chrome.runtime.sendMessage(message, () => {
      void chrome.runtime.lastError;
    });
    if (result && typeof result.catch === "function") {
      result.catch(() => undefined);
    }
  } catch (_error) {
    // No popup/listener is open. Status is still persisted in storage.
  }
}

function clearReconnect() {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
}

function clearHeartbeat() {
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer);
    heartbeatTimer = null;
  }
}

function parseJson(rawData) {
  try {
    return JSON.parse(rawData);
  } catch (_error) {
    return null;
  }
}
