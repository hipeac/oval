import os

from datetime import datetime
from flask import Flask
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_compress import Compress
from flask_talisman import Talisman


app = Flask(__name__, static_url_path='/static')

app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'FLASK_SECRET_KEY'),
)

if 'REDIS_URL' in os.environ:
    app.config['DEBUG'] = False
    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL'),
        'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 6,  # 6 hours
    }
else:
    app.config['DEBUG'] = True
    CACHE_CONFIG = {'CACHE_TYPE': 'null'}


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
            "images.unsplash.com",
            "www.hipeac.net"
        ]
    },
)


# assets
assets = Environment(app)
assets.url = app.static_url_path
assets.register('base_css', Bundle('scss/base.scss', filters='pyscss', output='css/base.css'))


# jinja
app.jinja_env.globals['DEBUG'] = app.config['DEBUG']
app.jinja_env.globals['YEAR'] = datetime.now().year
app.jinja_env.globals['HIPEAC_API_ENDPOINT'] = os.environ.get('HIPEAC_API_ENDPOINT', 'https://www.hipeac.net/api/v1')
app.jinja_env.globals['HIPEAC_EVENT_UUID'] = os.environ.get('HIPEAC_EVENT_UUID')


# views
import oval.views  # noqa
