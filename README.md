<p align="center">
  <img src="static/logo.webp" alt="Cartoony Logo" width="120">
</p>

<h1 align="center">🎬 Cartoony Downloader Pro</h1>

<p align="center">
  <strong>Professional Bulk Video Automation for Cartoony.net</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License">
</p>

---

## 📝 Overview

**Cartoony Downloader Pro** is a high-performance automation tool designed for bulk video downloading from `cartoony.net`. It combines **Playwright** for robust browser automation with a **FastAPI** backend and a premium glassmorphic web interface.

---

## ✨ Features

- **🚀 8-Strategy Play Engine**: Advanced detection to bypass complex play overlays.
- **📦 Parallel Batch Processing**: Download multiple episodes simultaneously.
- **📊 Real-time Progress**: Live logs and segment assembly tracking via SSE.
- **💎 Premium UI**: Modern dark-mode interface with range selection.
- **🔄 Auto-Retry**: Built-in failure detection and automatic retry logic.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Playwright (Chromium).
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+).
- **Configuration**: `python-dotenv` for environment management.

---

## Project Structure 📁

```bash
cartoony_downloader/
├── src/                 # 🧠 Backend Logic
│   ├── api.py           # 🌐 Fast-API Endpoints & SSE
│   ├── engine.py        # ⚙️ Automation Engine (Playwright)
│   └── utils.py         # 🔍 Scraping Utilities
├── static/              # 🎨 Frontend Assets
├── scripts/             # �️ Launch & Setup Scripts
│   ├── setup.bat
│   └── start.bat
├── config/              # ⚙️ Project Configuration
│   ├── requirements.txt
│   └── .env.example
└── .env                 # � Environment Variables (Git-ignored)
```

---

## Configuration & Environment 🔑

| Variable        | Description                            | Default      |
| :-------------- | :------------------------------------- | :----------- |
| `DOWNLOAD_PATH` | Destination folder for `.mp4` files.   | `downloads/` |
| `MAX_RETRIES`   | Number of retries for failed episodes. | `3`          |

---

## ⚡ Quick Start (Windows)

1.  **Run `scripts\setup.bat`**: Creates virtual environment and installs dependencies.
2.  **Run `scripts\start.bat`**: Launches the server and Auto-Opens in browser.

---

## 🔍 How to find Season ID

1.  Go to [cartoony.net](https://cartoony.net) and find your series.
2.  Select a season.
3.  Copy the **number** at the end of the URL (e.g., `570` from `.../watch/570`).
4.  Paste it into the app and click **Fetch Episodes**.

---

## 🚀 Getting Started (Manual)

### 🐍 Installing Python

Ensure you have **Python 3.10+** installed and checked **"Add Python to PATH"** during installation.

### Manual Setup

```bash
git clone https://github.com/kalidahmdev/cartoony_downloader.git
cd cartoony-downloader
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r config/requirements.txt
python -m playwright install chromium
cp config/.env.example .env
python src/api.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

<p align="center">
  <strong>Cartoony Downloader Pro</strong> — Built for speed, designed for style.
</p>
