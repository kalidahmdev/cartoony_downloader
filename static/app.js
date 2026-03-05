const logsContainer = document.getElementById("logs");
const startBtn = document.getElementById("startBtn");
const cancelBtn = document.getElementById("cancelBtn");
const confirmModal = document.getElementById("confirmModal");
const confirmYes = document.getElementById("confirmYes");
const confirmNo = document.getElementById("confirmNo");
const browseBtn = document.getElementById("browseBtn");
const fetchBtn = document.getElementById("fetchBtn");
const episodeSection = document.getElementById("episodeSection");
const episodeList = document.getElementById("episodeList");
const episodeCount = document.getElementById("episodeCount");
const selectAllBtn = document.getElementById("selectAll");
const deselectAllBtn = document.getElementById("deselectAll");
const copyLogsBtn = document.getElementById("copyLogsBtn");

const seasonIdInput = document.getElementById("seasonId");
const downloadPathInput = document.getElementById("downloadPath");

let eventSource = null;
let fetchedEpisodes = [];
let currentSeasonId = "";

// Sync Start Button visibility / state
function updateStartBtn() {
  const selected = getSelectedIds();
  const hasEpisodes = fetchedEpisodes.length > 0;
  const isCorrectSeason = seasonIdInput.value === currentSeasonId;

  // If season ID changed after fetch, disable start until RE-FETCHED
  const canStart = hasEpisodes && isCorrectSeason && selected.length > 0;

  startBtn.disabled = !canStart;

  if (!isCorrectSeason && hasEpisodes) {
    startBtn.title = "Season ID changed. Please re-fetch episodes.";
  } else {
    startBtn.title = "";
  }

  startBtn.textContent =
    selected.length > 0
      ? `Start Automation (${selected.length})`
      : "Start Automation";
}

// Watch for Season ID changes to invalidate current fetch
seasonIdInput.addEventListener("input", updateStartBtn);

// Browse folder picker
browseBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/browse");
    const data = await res.json();
    if (data.path) {
      downloadPathInput.value = data.path;
    }
  } catch (e) {
    console.error("Browse error:", e);
  }
});

// Fetch episodes
fetchBtn.addEventListener("click", async () => {
  const seasonId = seasonIdInput.value;
  if (!seasonId) {
    alert("Please enter a Season ID.");
    return;
  }

  fetchBtn.disabled = true;
  fetchBtn.textContent = "🔄 Fetching...";
  episodeList.innerHTML =
    '<div class="log-entry system">Scraping season page...</div>';
  episodeSection.style.display = "block";

  try {
    const res = await fetch(`/fetch?season_id=${seasonId}`);
    const data = await res.json();

    if (data.error) {
      episodeList.innerHTML = `<div class="log-entry error">❌ ${data.error}</div>`;
      fetchedEpisodes = [];
      currentSeasonId = "";
      updateStartBtn();
      return;
    }

    fetchedEpisodes = data.episodes;
    currentSeasonId = seasonId;
    renderEpisodes();
  } catch (e) {
    episodeList.innerHTML = `<div class="log-entry error">❌ Connection error: ${e.message}</div>`;
    fetchedEpisodes = [];
    currentSeasonId = "";
    updateStartBtn();
  } finally {
    fetchBtn.disabled = false;
    fetchBtn.textContent = "🔍 Fetch Episodes";
  }
});

function renderEpisodes() {
  if (fetchedEpisodes.length === 0) {
    episodeList.innerHTML =
      '<div class="log-entry system">No episodes found.</div>';
    episodeCount.textContent = "0 episodes found";
    updateStartBtn();
    return;
  }

  episodeCount.textContent = `${fetchedEpisodes.length} episodes found`;
  episodeList.innerHTML = fetchedEpisodes
    .map(
      (ep, i) =>
        `<label class="episode-item">
          <input type="checkbox" class="ep-checkbox" data-id="${ep.id}" checked>
          <span class="ep-num">${i + 1}.</span>
          <span class="ep-name">${ep.name || "Episode " + (i + 1)}</span>
          <span class="ep-id">ID: ${ep.id}</span>
        </label>`,
    )
    .join("");
  updateStartBtn();
}

function getSelectedIds() {
  return Array.from(document.querySelectorAll(".ep-checkbox:checked")).map(
    (cb) => cb.dataset.id,
  );
}

// Shift+click range selection
let lastCheckedIndex = null;

episodeList.addEventListener("click", (e) => {
  const checkbox = e.target.closest(".ep-checkbox");
  if (!checkbox) return;

  const allCheckboxes = Array.from(document.querySelectorAll(".ep-checkbox"));
  const currentIndex = allCheckboxes.indexOf(checkbox);

  if (
    e.shiftKey &&
    lastCheckedIndex !== null &&
    lastCheckedIndex !== currentIndex
  ) {
    const start = Math.min(lastCheckedIndex, currentIndex);
    const end = Math.max(lastCheckedIndex, currentIndex);
    const newState = checkbox.checked;

    for (let i = start; i <= end; i++) {
      allCheckboxes[i].checked = newState;
    }
  }

  lastCheckedIndex = currentIndex;
  updateStartBtn();
});

// Also update on direct change (keyboard toggle)
episodeList.addEventListener("change", updateStartBtn);

selectAllBtn.addEventListener("click", () => {
  document
    .querySelectorAll(".ep-checkbox")
    .forEach((cb) => (cb.checked = true));
  updateStartBtn();
});

deselectAllBtn.addEventListener("click", () => {
  document
    .querySelectorAll(".ep-checkbox")
    .forEach((cb) => (cb.checked = false));
  updateStartBtn();
});

function addLog(message) {
  const entry = document.createElement("div");
  entry.className = "log-entry";

  if (message.includes("✅")) entry.classList.add("success");
  else if (message.includes("❌") || message.includes("🛑"))
    entry.classList.add("error");
  else if (
    message.includes("---") ||
    message.includes("EP") ||
    message.includes("🚀")
  )
    entry.classList.add("process");
  else entry.classList.add("system");

  entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  logsContainer.appendChild(entry);
  logsContainer.scrollTop = logsContainer.scrollHeight;
}

function setRunning(isRunning) {
  startBtn.disabled = isRunning;
  fetchBtn.disabled = isRunning;
  cancelBtn.style.display = isRunning ? "flex" : "none";
  if (!isRunning) {
    cancelBtn.disabled = false;
    cancelBtn.textContent = "Cancel";
    updateStartBtn();
  }
}

startBtn.addEventListener("click", async () => {
  const seasonId = document.getElementById("seasonId").value;
  const tabCount = document.getElementById("tabCount").value || "5";
  const downloadPath = document.getElementById("downloadPath").value;
  const selectedIds = getSelectedIds();

  if (!seasonId || selectedIds.length === 0) {
    alert("Please fetch episodes and select at least one.");
    return;
  }

  // Request notification permission if not already granted
  if (Notification.permission === "default") {
    Notification.requestPermission();
  }

  setRunning(true);
  logsContainer.innerHTML = "";
  addLog("Initializing batch process...");

  let url = `/run?season_id=${seasonId}&episode_ids=${selectedIds.join(",")}&tabs=${tabCount}`;
  if (downloadPath) {
    url += `&download_path=${encodeURIComponent(downloadPath)}`;
  }
  eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    if (event.data === "[DONE]") {
      eventSource.close();
      eventSource = null;
      setRunning(false);
      addLog("Batch process completed.");

      // Trigger Desktop Notification
      if (Notification.permission === "granted") {
        new Notification("Cartoony Downloader Pro", {
          body: "🎉 All downloads have finished successfully!",
          icon: "/static/logo.webp",
        });
      }
    } else {
      addLog(event.data);
    }
  };

  eventSource.onerror = (err) => {
    console.error("SSE Error:", err);
    addLog("❌ Connection lost or server error.");
    if (eventSource) eventSource.close();
    eventSource = null;
    setRunning(false);
  };
});

// Cancel flow: show confirmation modal
cancelBtn.addEventListener("click", () => {
  confirmModal.style.display = "flex";
});

confirmNo.addEventListener("click", () => {
  confirmModal.style.display = "none";
});

confirmYes.addEventListener("click", async () => {
  confirmModal.style.display = "none";
  addLog("🛑 Cancelling all downloads immediately...");
  cancelBtn.disabled = true;
  cancelBtn.textContent = "Cancelling...";

  try {
    await fetch("/cancel", { method: "POST" });
  } catch (e) {
    console.error("Cancel error:", e);
  }
});

// Copy logs logic
copyLogsBtn.addEventListener("click", () => {
  const logText = Array.from(logsContainer.querySelectorAll(".log-entry"))
    .map((entry) => entry.textContent)
    .join("\n");

  navigator.clipboard.writeText(logText).then(() => {
    const originalText = copyLogsBtn.textContent;
    copyLogsBtn.textContent = "✅ Copied!";
    copyLogsBtn.classList.add("success");
    setTimeout(() => {
      copyLogsBtn.textContent = originalText;
      copyLogsBtn.classList.remove("success");
    }, 2000);
  });
});
