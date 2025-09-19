# PiSpeed Internet Speed Monitor

**PiSpeed** is a lightweight, self-hosted internet speed monitor designed for Raspberry Pi and Linux systems.  
It periodically tests your internet speed, stores results in a local SQLite database, and provides a simple web dashboard accessible on your local network.

---

## Features

- Runs interval-based speed tests (default: every 15 minutes; configurable)
- Stores results in `speed_results.db` (SQLite)
- Local dashboard at `http://<pi-ip>:1234`
- Easy configuration via environment variables (no code changes needed)
- Bundled systemd unit for auto-start at boot (`speed-monitor.service`)

---

## Requirements

- Raspberry Pi (Raspberry Pi OS recommended, but any Linux box works)
- Python 3, venv, pip
- Network access for speed tests
- Python dependencies listed in `requirements.txt`

---

## Quick Start

1. **Install dependencies:**

    ```sh
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip git
    ```

2. **Clone and set up:**

    ```sh
    git clone https://github.com/T3chieJack/PiSpeed.git
    cd PiSpeed
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 pispeed.py
    ```

3. **Open the dashboard:**  
   Visit `http://<pi-ip>:1234` in your browser (replace `<pi-ip>` with your Pi’s IP).

---

## Configuration

Set environment variables to customize behavior:

| Variable           | Purpose               | Example                   |
|--------------------|----------------------|---------------------------|
| `PISPEED_INTERVAL` | Seconds between tests | `900`                     |
| `PISPEED_PORT`     | Web dashboard port    | `1234`                    |
| `PISPEED_BIND`     | Bind host             | `0.0.0.0`                 |
| `PISPEED_DB_PATH`  | SQLite database path  | `./speed_results.db`      |

Example usage:

```sh
export PISPEED_INTERVAL=900
export PISPEED_PORT=1234
export PISPEED_BIND=0.0.0.0
export PISPEED_DB_PATH=$PWD/speed_results.db
python3 pispeed.py
```

---

## Run as a Service

A template systemd unit (`speed-monitor.service`) is provided.  
Edit paths and environment as needed, then install and enable:

```sh
sudo cp speed-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now speed-monitor.service
```

Status & logs:

```sh
systemctl status speed-monitor.service
journalctl -u speed-monitor.service -f
```

---

## Database Usage

Inspect results with sqlite3:

```sh
sqlite3 speed_results.db
sqlite> .tables
sqlite> SELECT * FROM results ORDER BY timestamp DESC LIMIT 10;
```
*(Adjust table/column names as needed.)*

---

## Development

- Main app: `pispeed.py`
- Dependencies: `requirements.txt`
- Systemd unit template: `speed-monitor.service`

Setup:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pispeed.py
```

---

## Contributing

Pull requests and issues welcome!  
See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

---

## License

See `LICENSE` for details.

---

## Roadmap Ideas

- CSV/JSON export
- Configurable speed test servers/providers
- Dashboard authentication (optional)
- Docker container support

---

## FAQ

**Q:** How often are tests run by default?  
**A:** Every 15 minutes (configurable).

**Q:** Where is the dashboard?  
**A:** Visit `http://<pi-ip>:1234` from your LAN.

## Current Release

**V1** is now available! This initial release of PiSpeed marks the start of the project.

