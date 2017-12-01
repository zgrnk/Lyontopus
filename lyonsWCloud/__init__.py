# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from flask import current_app, Flask, redirect, url_for
from .generator import WCTopWords
from nltk import download, data
import ssl



def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Register the Bookshelf CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/wcloud')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.wcloud'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    #download nltk corpus first time ran, if needed
    try:
        data.find('tokenizers/tokenize')
    except LookupError:
        #hack due to SSL issue with downloading from wrong local location
        #obviously not the right thing to do, just to get working for now
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        download('popular')

    return app


def get_model():
    from . import model_cloudsql
    return model_cloudsql
