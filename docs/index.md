# PiSpeed

**PiSpeed** is a minimal internet speed tracker for Raspberry Pi.

- Dashboard: `http://<pi-ip>:1234`
- Config via env vars: `PORT`, `INTERVAL_SECONDS`, `HOST`, `MAX_POINTS`.

## Install

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/T3chieJack/PiSpeed.git
cd PiSpeed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pispeed.py
