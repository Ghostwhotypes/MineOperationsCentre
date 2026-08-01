from flask import Flask, render_template, request
import subprocess
import platform
import re
import socket

app = Flask(__name__)


def ping(host):
    flag = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", flag, "1", host],
        capture_output=True,
        text=True
    )

    output = result.stdout

    online = result.returncode == 0
    ping_ms = None

    match = re.search(r"time[=<]\s*(\d+)", output)

    if match:
        ping_ms = int(match.group(1))

    if ping_ms is None:
        latency = "---"
    elif ping_ms <= 10:
        latency = "Excellent"
    elif ping_ms <= 30:
        latency = "Good"
    elif ping_ms <= 60:
        latency = "Fair"
    elif ping_ms <= 100:
        latency = "Poor"
    else:
        latency = "Very Poor"

    try:
        hostname = socket.gethostbyaddr(host)[0]
    except Exception:
        hostname = "---"

    return {
        "online": online,
        "ping_ms": ping_ms,
        "latency": latency,
        "hostname": hostname,
    }


@app.route("/", methods=["GET", "POST"])
def index():

    rows = [{"ip": "", "info": None}]

    if request.method == "POST":

        rows = []

        ips = request.form.getlist("ip")

        action = request.form.get("action")
        remove = request.form.get("remove")

        for ip in ips:

            ip = ip.strip()

            info = None

            if action in ("monitor", "refresh") and ip:
                info = ping(ip)

            rows.append(
                {
                    "ip": ip,
                    "info": info,
                }
            )

        if action == "add":
            rows.append(
                {
                    "ip": "",
                    "info": None,
                }
            )

        if action == "remove" and remove is not None:
            rows.pop(int(remove))

        if len(rows) == 0:
            rows.append(
                {
                    "ip": "",
                    "info": None,
                }
            )

    return render_template(
        "index.html",
        rows=rows,
    )


if __name__ == "__main__":
    app.run(debug=True)
    