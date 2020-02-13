import os

from flask import jsonify, redirect, render_template, request, send_from_directory, url_for
from datetime import datetime

from oval import app, cache


@app.route('/')
@cache.cached()
def index():
    return redirect(url_for('event_2020'))


@app.route('/2020/')
@cache.cached()
def event_2020():
    return render_template('pages/2019/event.html')


@app.route('/hooks/cc/', methods=['GET'])
def clear_cache():
    try:
        cache.clear()
        res = {'status': 200}
    except Exception as e:
        res = {'status': 500, 'error': str(e)}

    return jsonify(res), res['status']


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
