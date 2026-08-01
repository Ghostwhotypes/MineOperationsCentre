from flask import Flask, render_template, request
import subprocess
import platform

app = Flask(__name__)


def ping(host):
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(
        ["ping", flag, "1", host],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


@app.route("/", methods=["GET", "POST"])
def index():

    rows = [{"ip": "", "status": None}]

    if request.method == "POST":

        rows = []

        ips = request.form.getlist("ip")

        action = request.form.get("action")

        remove = request.form.get("remove")

        for ip in ips:
            ip = ip.strip()

            status = None

            if action == "monitor" and ip:
                status = ping(ip)

            rows.append(
                {
                    "ip": ip,
                    "status": status
                }
            )

        if action == "add":
            rows.append(
                {
                    "ip": "",
                    "status": None
                }
            )

        if action == "remove" and remove is not None:
            rows.pop(int(remove))

        if len(rows) == 0:
            rows.append(
                {
                    "ip": "",
                    "status": None
                }
            )

    return render_template(
        "index.html",
        rows=rows
    )


if __name__ == "__main__":
    app.run(debug=True)