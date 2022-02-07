# MIT License
#
# Copyright (c) 2022 Lars Grespan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#

import sys
import os
import pandas as pd
from flask import *
from flask_restful import Resource, Api
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections

# Create Server
app = Flask(__name__ , template_folder="../Dashboard")
api = Api(app)

# REST Service functionality accessible via https://127.0.0.1:5000/event
@app.route('/result')
def showResults():

    # Get database connection
    eventdb = DBConnections.get_event_db()
    col_result = eventdb["result"]
    
    # Load data from mongodb
    results = pd.DataFrame(list(col_result.find())) 
    del results['_id']

    # Transfer the dataframe to HTML   
    return render_template('dashboard.html', table = results.to_html (header = 'true'))
                           

if __name__ == "__main__":
    app.run(debug=True)
