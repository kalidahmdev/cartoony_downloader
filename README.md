<p align="center">
  <img src="static/logo.webp" alt="Cartoony Logo" width="160">
</p>

<h1 align="center">🎬 Cartoony Downloader Pro</h1>

<p align="center">
  <strong>The Ultimate High-Performance Bulk Video Automation for Cartoony.net</strong>
</p>

<p align="center">
  <a href="#✨-features">Features</a> •
  <a href="#🛠️-tech-stack--architecture">Tech Stack</a> •
  <a href="#🚀-getting-started">Getting Started</a> •
  <a href="#🎨-design-system">Design System</a> •
  <a href="#🤝-contributing--community">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License">
</p>

---

---

## 📖 Overview

**Cartoony Downloader Pro** is an enterprise-grade automation solution built for mass-archiving content from `cartoony.net`. By leveraging a multi-threaded **Playwright** engine and a sleek **FastAPI** backbone, it transforms complex browser interactions into a seamless, high-velocity downloading experience. Wrapped in a stunning **Liquid Glass** UI, it’s not just a tool—it’s a production-ready media pipeline.

---

## ✨ Features

### ⚙️ Automation Engine (The Heart)

| Feature                       | Description                                                                                                     |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| **8-Strategy Play Engine**    | Exhaustive click detection system using JS injection, pointer events, and API calls to bypass any play overlay. |
| **Parallel Batch Processing** | Highly efficient multi-tab architecture powered by `asyncio` for simultaneous episode downloads.                |
| **Intelligent Auto-Retry**    | Built-in fault tolerance that automatically re-queues failed segments up to `MAX_RETRIES`.                      |
| **SSE Log Streaming**         | Real-time, server-sent events for transparent progress tracking of the automation's inner workings.             |

### 🎨 Frontend Experience

| Feature                        | Description                                                                                    |
| :----------------------------- | :--------------------------------------------------------------------------------------------- |
| **Liquid Glass UI**            | A premium, responsive interface featuring dynamic ambient orbs and high-blur glassmorphism.    |
| **Smart Range Selection**      | Shift+click support and multi-select toggles for rapid episode batching.                       |
| **Live Desktop Notifications** | Push notifications for batch completion, ensuring you're alerted even when the tab is blurred. |
| **Native Folder Picker**       | Tight OS integration via `tkinter` for selecting download destinations without typing paths.   |

---

## 🛠️ Tech Stack & Architecture

### Core Philosophy

The project follows a **Feature-Isolated Architecture**, separating the scraping logic (`utils.py`), the stateful automation engine (`engine.py`), and the communication layer (`api.py`). This ensures high maintainability and ease of scaling.

| Layer             | Technology        | Role                                                    |
| :---------------- | :---------------- | :------------------------------------------------------ |
| **Backend**       | Python 3.10+      | Core logic and process orchestration.                   |
| **Web Framework** | FastAPI           | High-performance API and SSE streaming.                 |
| **Automation**    | Playwright        | Headless/Headed browser control.                        |
| **Frontend**      | Vanilla JS / CSS3 | Zero-dependency, lightweight UI with modern aesthetics. |
| **Environment**   | Dotenv            | Secure configuration management.                        |

---

## 🔑 Configuration & Environment

| Variable        | Description                             | Default      | Required |
| :-------------- | :-------------------------------------- | :----------- | :------- |
| `DOWNLOAD_PATH` | Base directory for saved `.mp4` files.  | `downloads/` | Yes      |
| `MAX_RETRIES`   | Number of attempts for failed episodes. | `3`          | No       |
| `HEADLESS`      | Whether to hide the automation browser. | `False`      | No       |

---

## 📁 Project Structure

```bash
cartoony_downloader/
├── config/              # ⚙️ Environment and Dependencies
│   ├── .env.example     # Template for local secrets
│   └── requirements.txt # Python package manifest
├── src/                 # 🧠 Core Intelligence
│   ├── api.py           # FastAPI endpoints & SSE logic
│   ├── engine.py        # Playwright automation & retry logic
│   └── utils.py         # Static scraping & episode extraction
├── static/              # 🎨 Visual Assets & Frontend
│   ├── app.js           # Frontend logic & SSE listener
│   ├── style.css        # Premium Glassmorphism design system
│   ├── index.html       # Semantic HTML5 entry point
│   └── logo.webp        # Brand assets
├── scripts/             # 🛠️ One-click Launchers
│   ├── setup.bat        # VENV initialization & dependency install
│   └── start.bat        # Production server startup
├── docker-compose.yml   # 🐳 Container orchestration
└── Dockerfile           # 🏗️ Container blueprints
```

---

## 🚀 Getting Started

### ⚡ One-Click (Windows)

1. **Run `scripts\setup.bat`**: Initializes the environment.
2. **Run `scripts\start.bat`**: Launches the app at [localhost:8000](http://localhost:8000).

### 🐳 Docker Deployment

```bash
docker-compose up -d --build
```

**Note**: The container runs as a non-root user (`pwuser`) for enhanced security.

### 🐍 Manual Setup

```bash
# Clone & Enter
git clone https://github.com/kalidahmdev/cartoony_downloader.git
cd cartoony_downloader

# Environment Setup
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r config/requirements.txt
python -m playwright install chromium

# Launch
python src/api.py
```

---

## 🎨 Design System

The UI is built on a custom **Liquid Glass** design system, defined in `static/style.css`.

| Token          | Value                    | Description                    |
| :------------- | :----------------------- | :----------------------------- |
| **Primary**    | `#ff4d4d`                | Action buttons & branding.     |
| **Secondary**  | `#f9d423`                | Warnings & highlight accents.  |
| **Glass BG**   | `rgba(20, 20, 25, 0.45)` | Core component transparency.   |
| **Blur**       | `blur(20px)`             | Depth creation for overlays.   |
| **Typography** | `"Outfit", sans-serif`   | Modern, geometric font family. |

---

---

## 🤝 Contributing & Community

We celebrate open-source! Whether you're fixing a bug, suggesting a feature, or improving documentation, your contributions make **Cartoony Downloader Pro** better for everyone.

### 🛠️ How to Contribute

1.  **Fork the Repository**: Create your own branch from `main`.
2.  **Setup Environment**: Follow the [Getting Started](#🚀-getting-started) guide.
3.  **Draft a Feature/Bug Report**: Opening an Issue before starting work ensures alignment.
4.  **Submit a Pull Request**: Provide a detailed description of your changes.

### 🛡️ Open Source Standards

| Requirement         | Description                                                                          |
| :------------------ | :----------------------------------------------------------------------------------- |
| **Code Quality**    | Ensure all Python code is linted with `Flake8` and JS follows `ESLint` standards.    |
| **Commit Messages** | Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`) for clear version history. |
| **Branching**       | Use descriptive branch names like `feature/new-engine` or `bugfix/connection-leak`.  |

---

## 🔒 Security & Privacy

We take security seriously. Since this tool handles browser automation:

- **No Data Harvesting**: Your download history and Season IDs never leave your machine.
- **Credential Safety**: Always use `.env` for configuration; never hardcode paths or sensitive settings.
- **Reporting Vulnerabilities**: If you find a security flaw, please open an Issue with the `security` label.

---

<p align="center">
  <strong>Cartoony Downloader Pro</strong> — Built with ❤️ by <a href="https://github.com/kalidahmdev">kalidahmdev</a>
</p>

<p align="center">
  <a href="https://github.com/kalidahmdev/cartoony-downloader">View on GitHub</a>
</p>
