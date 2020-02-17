import os

from datetime import datetime
from flask import Flask
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_compress import Compress
from flask_talisman import Talisman


app = Flask(__name__, static_url_path="/static")

app.config.update(SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "FLASK_SECRET_KEY"),)

if "REDIS_URL" in os.environ:
    CACHE_CONFIG = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": os.environ.get("REDIS_URL"),
        "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 6,  # 6 hours
    }
else:
    CACHE_CONFIG = {"CACHE_TYPE": "null"}


# optimization & security
cache = Cache(app, config=CACHE_CONFIG)
Compress(app)
Talisman(
    app,
    content_security_policy={
        "default-src": [
            "'self'",
            "'unsafe-eval'",
            "'unsafe-inline'",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
            "localhost:8000" if app.config["DEBUG"] else "www.hipeac.net",
        ]
    },
)


# assets
assets = Environment(app)
assets.url = app.static_url_path
assets.register("base_css", Bundle("scss/base.scss", filters="pyscss", output="css/base.css"))


# jinja
app.jinja_env.globals["DEBUG"] = app.config["DEBUG"]
app.jinja_env.globals["YEAR"] = datetime.now().year
app.jinja_env.globals["HIPEAC_API_ENDPOINT"] = os.environ.get("HIPEAC_API_ENDPOINT", "https://www.hipeac.net/api/v1")


# views
import oval.views  # noqa
