# PiSpeed

A lightweight, self-hosted internet speed monitor for Raspberry Pi.  
It runs periodic speed tests, stores results in a local SQLite database, and serves a simple web dashboard on your LAN.

---

## ✨ Features

- **Interval testing** (default every 15 minutes; configurable)
- **Stores results** in `speed_results.db` (SQLite)
- **Local dashboard** at `http://<pi-ip>:1234`
- **Configure via environment variables** (no code changes needed)
- **Systemd unit included** for running in the background on boot (`speed-monitor.service`)

---

## 📦 Requirements

- Raspberry Pi running Raspberry Pi OS (or any Linux box)
- Python 3 + venv and pip
- Network access for speed tests

See `requirements.txt` for Python dependencies.

---

## 🚀 Installation (Raspberry Pi)

```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# Clone the repo
git clone https://github.com/T3chieJack/PiSpeed.git
cd PiSpeed

# Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run it
python3 pispeed.py
```

Now open the dashboard at `http://<pi-ip>:1234`.

---

## ⚙️ Configuration

PiSpeed can be configured via environment variables (no config file required).

| Variable           | Purpose               | Example                   |
|--------------------|----------------------|---------------------------|
| `PISPEED_INTERVAL` | Seconds between tests | `900`                     |
| `PISPEED_PORT`     | Web dashboard port    | `1234`                    |
| `PISPEED_BIND`     | Bind host             | `0.0.0.0`                 |
| `PISPEED_DB_PATH`  | SQLite database path  | `./speed_results.db`      |

> Note: Exact keys supported are defined in the code; the table above shows typical/expected keys. Adjust to match the variables used in `pispeed.py`.

Export these before launching:

```sh
export PISPEED_INTERVAL=900
export PISPEED_PORT=1234
export PISPEED_BIND=0.0.0.0
export PISPEED_DB_PATH=$PWD/speed_results.db
python3 pispeed.py
```

---

## 🛠️ Run as a service (systemd)

A ready-to-adapt unit file is provided: `speed-monitor.service`.

Edit the unit to suit your user, paths, and environment:

```sh
nano speed-monitor.service
```

Recommended tweaks:
- `User=pi` (or your user)
- `WorkingDirectory=/home/pi/PiSpeed`
- `ExecStart=/home/pi/PiSpeed/.venv/bin/python /home/pi/PiSpeed/pispeed.py`
- Add `Environment=` lines for any variables you set (see config section)

Install & enable:

```sh
sudo cp speed-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now speed-monitor.service
```

Check status & logs:

```sh
systemctl status speed-monitor.service
journalctl -u speed-monitor.service -f
```

---

## 🧰 Database

Results are stored in a local SQLite database (default: `speed_results.db`). To inspect:

```sh
sudo apt install -y sqlite3
sqlite3 speed_results.db
sqlite> .tables
sqlite> SELECT * FROM results ORDER BY timestamp DESC LIMIT 10;
```
*(Adjust table names/columns based on the schema used in `pispeed.py`.)*

---

## 🧑‍💻 Development

```sh
# In the repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python3 pispeed.py
```

Key files:

- `pispeed.py` – main application
- `requirements.txt` – Python deps
- `speed-monitor.service` – systemd unit template

---

## 🤝 Contributing

PRs and issues are welcome!  
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

---

## 📄 License

This project includes a LICENSE file — see it for details.

---

## 🗺️ Roadmap (ideas)

- CSV/JSON export of results
- Configurable test servers/providers
- Auth for dashboard (optional)
- Docker container

---

## ❓ FAQ

**Q: How often does it test by default?**  
A: Every 15 minutes by default (you can change this).

**Q: Where do I find the dashboard?**  
A: Visit `http://<pi-ip>:1234` from a device on the same network.
