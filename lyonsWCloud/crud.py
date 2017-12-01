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

from lyonsWCloud import get_model, WCTopWords
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START wcloud]
@crud.route("/", methods=['GET', 'POST'])
def wcloud():
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        url = form_data['url']
        if url != '':
            mywcloud = WCTopWords(url)
            mywcloud.generate_wc()
            ewords = mywcloud.encr_words
            for word in ewords:
                get_model().create(word)

            return render_template('wcloud.html', wcloud_url=url, form_url=url)
        else:
            return render_template("wcloud.html", form_url='')

    return render_template("wcloud.html", form_url='')
# [END wcloud]

# [START admin]
@crud.route("/admin")
def admin():
    # try:
    #     words = get_model().adminRead()
    # except Exception:
    #     words = {}

    # return render_template("admin.html", words=words)
    return render_template("admin.html")
# [END admin]
