# PiSpeed

Lightweight, self-hosted internet speed monitor for Raspberry Pi. Runs periodic tests, stores results in SQLite, and serves a local web dashboard.

- 🔁 Interval testing (default every 15 minutes)
- 💾 Stores to `speed_results.db` (SQLite)
- 📈 Dashboard at `http://<pi-ip>:1234`
- ⚙️ Configure via environment variables

## Quick start (Raspberry Pi)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/T3chieJack/PiSpeed.git
cd PiSpeed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pispeed.py
