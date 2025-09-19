# PiSpeed

PiSpeed is a lightweight internet speed monitor for Raspberry Pi.  
It runs periodic speed tests, stores results in SQLite, and serves a simple web dashboard at `http://<pi-ip>:1234`.

## Features
- Automatic speed tests (default every 15 minutes)
- Stores results in SQLite database
- Web dashboard with Chart.js graphs
- One-click "Run test now" button
- Easy to run as a systemd service

## Installation
```bash
git clone https://github.com/T3chieJack/PiSpeed.git
cd PiSpeed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pispeed.py
