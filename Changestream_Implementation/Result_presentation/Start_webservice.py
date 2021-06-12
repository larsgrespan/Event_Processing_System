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
