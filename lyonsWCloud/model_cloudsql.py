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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['salt_hash'] = row.salt_hash
    data.pop('_sa_instance_state')
    return data


# [START model]
class WCloudModel(db.Model):
    __tablename__ = 'wordcloud'

    salt_hash = db.Column(db.String(255), primary_key=True)
    encr_word = db.Column(db.String(255))
    freq = db.Column(db.Integer)
# [END model]


# [START admin]
def adminRead():
    query = (WCloudModel.query
             .order_by(WCloudModel.freq.desc()))
    words = builtin_list(map(from_sql, query.all()))
    return words
# [END admin]


# [START create]
def create(data):
    wcloudmodel = WCloudModel(**data)
    db.session.add(wcloudmodel)
    db.session.commit()
    return from_sql(wcloudmodel)
# [END create]


# [START update]
def update(data, url):
    wcloudmodel = WCloudModel.query.all()
    for k, v in data.items():
        setattr(wcloudmodel, k, v)
    db.session.commit()
    return from_sql(wcloudmodel)
# [END update]


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
