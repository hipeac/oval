The OVAL Europe website uses [Flask][flask].

Application dependencies
------------------------

The application uses [Pipenv][pipenv] to manage Python packages. While in development, you will need to install
all dependencies (includes packages like `debug_toolbar`):

    $ pipenv shell
    $ pipenv install --dev

Update dependencies (and manually update `requirements.txt`):

    $ pipenv update --dev && pipenv lock -r

Running the server
------------------

    $ flask run

There is an environment variable called `FLASK_ENV` that has to be set to `development`
if you want to run Flask in debug mode with auto-reload.

Running tests
-------------

    $ pytest --cov=oval

Style guide
-----------

Tab size is 4 spaces. Max line length is 120. You should run `black` before committing any change.

    $ black oval


[flask]: https://flask.pocoo.org/
[pipenv]: https://docs.pipenv.org/#install-pipenv-today
