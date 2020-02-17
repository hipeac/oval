import json
import os

from flask import jsonify, redirect, render_template, send_from_directory, url_for

from oval import app, cache


EVENT_CODES = json.loads(os.environ.get("HIPEAC_EVENT_CODES", "{}"))


@app.route("/")
@cache.cached()
def index():
    return redirect(url_for("event", year=2020))


@app.route("/admin/<event_secret>/<year>/")
@cache.cached()
def admin(year, event_secret):
    return render_template("admin/dashboard.html", year=year, event_code=EVENT_CODES[year], event_secret=event_secret)


@app.route("/<year>/")
@cache.cached()
def event(year):
    return render_template(f"events/{year}/event.html", event_code=EVENT_CODES[year])


@app.route("/hooks/cc/", methods=["GET"])
def clear_cache():
    try:
        cache.clear()
        res = {"status": 200}
    except Exception as e:
        res = {"status": 500, "error": str(e)}

    return jsonify(res), res["status"]


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")
