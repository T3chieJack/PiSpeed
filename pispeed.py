#!/usr/bin/env python3
import os, time, sqlite3, threading, signal
from datetime import datetime
from flask import Flask, jsonify, render_template_string
import speedtest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "speed_results.db")

INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "900"))  # 15 min default
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "1234"))
MAX_POINTS = int(os.getenv("MAX_POINTS", "200"))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS speeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL,
        ping_ms REAL,
        download_mbps REAL,
        upload_mbps REAL
    )""")
    conn.commit(); conn.close()

def insert_result(ts, ping_ms, dl, ul):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO speeds (ts,ping_ms,download_mbps,upload_mbps) VALUES (?,?,?,?)",
              (ts, ping_ms, dl, ul))
    conn.commit(); conn.close()

def fetch_recent(limit):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ts,ping_ms,download_mbps,upload_mbps FROM speeds ORDER BY ts DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close()
    return list(reversed(rows))

def run_speedtest_once(timeout=60):
    try:
        st = speedtest.Speedtest(timeout=timeout)
        st.get_best_server()
        ping_ms = st.results.ping
        dl = round(st.download() / 1_000_000, 2)
        ul = round(st.upload() / 1_000_000, 2)
        ts = int(time.time())
        print(f"[{datetime.utcfromtimestamp(ts)}] ping {ping_ms} ms dl {dl} Mbps ul {ul} Mbps", flush=True)
        return ts, ping_ms, dl, ul
    except Exception as e:
        print("speedtest error:", e, flush=True)
        return None

def background_loop(stop_event):
    while not stop_event.is_set():
        r = run_speedtest_once()
        if r:
            ts, p, d, u = r
            insert_result(ts, p, d, u)
        for _ in range(INTERVAL_SECONDS):
            if stop_event.is_set(): break
            time.sleep(1)

app = Flask(__name__)

INDEX_HTML = """
<!doctype html><html><head><meta charset="utf-8"><title>PiSpeed</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>body{font-family:system-ui,Arial,sans-serif;margin:20px}canvas{max-width:100%}</style>
</head><body>
<h1>PiSpeed</h1>
<p>Interval: {{interval}} min &middot; <button id="run">Run test now</button> <small id="s"></small></p>
<canvas id="c" height="120"></canvas>
<script>
async function j(p,o){const r=await fetch(p,o);return await r.json();}
async function load(){
  const d = await j('/api/data');
  const ctx = document.getElementById('c').getContext('2d');
  new Chart(ctx,{type:'line',data:{
    labels:d.map(x=>new Date(x.ts*1000).toLocaleString()),
    datasets:[
      {label:'Download (Mbps)',data:d.map(x=>x.download_mbps)},
      {label:'Upload (Mbps)',data:d.map(x=>x.upload_mbps)},
      {label:'Ping (ms)',data:d.map(x=>x.ping_ms),yAxisID:'y1'}
    ]},
    options:{interaction:{mode:'index',intersect:false},
      scales:{y:{title:{display:true,text:'Mbps'},beginAtZero:true},
              y1:{position:'right',title:{display:true,text:'Ping (ms)'},grid:{drawOnChartArea:false}}}}
  });
}
document.getElementById('run').onclick=async()=>{
  document.getElementById('s').textContent=' running...';
  try{await j('/api/run-now',{method:'POST'}); setTimeout(()=>location.reload(),3000);}
  catch(e){document.getElementById('s').textContent=' error';}
};
load();
</script></body></html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML, interval=INTERVAL_SECONDS//60)

@app.route("/api/data")
def api_data():
    rows = fetch_recent(MAX_POINTS)
    return jsonify([{"ts":ts,"ping_ms":p,"download_mbps":d,"upload_mbps":u} for ts,p,d,u in rows])

@app.route("/api/run-now", methods=["POST"])
def api_run_now():
    r = run_speedtest_once()
    if r:
        ts, p, d, u = r
        insert_result(ts, p, d, u)
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 500

stop_event = threading.Event()
def handle_sigterm(signum, frame): stop_event.set()
signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    init_db()
    t = threading.Thread(target=background_loop, args=(stop_event,), daemon=True)
    t.start()
    app.run(host=HOST, port=PORT)
