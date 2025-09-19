# PiSpeed

**PiSpeed** is a lightweight, self-hosted internet speed monitor for Raspberry Pi.  
It runs periodic speed tests, stores the results in a SQLite database, and serves a local web dashboard.

---

## ✨ Features
- 🔁 Interval testing (default every 15 minutes, configurable)
- 💾 Stores results in `speed_results.db` (SQLite)
- 📈 Dashboard available at `http://<pi-ip>:1234`
- ⚙️ Configure via environment variables
- 🐧 Easy systemd integration for background service

---

## 📦 Installation (Raspberry Pi)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/<YOUR_GITHUB_USERNAME>/PiSpeed.git
cd PiSpeed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pispeed.py
