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

import pandas as pd
import sys
import os
import requests
import json
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections


class Rest:

    def __init__(self, teststation, product_type):

        self.start_sending(teststation, product_type)

        
    def start_sending(self, teststation, product_type):

        # Get EventDB Connection
        eventdb = DBConnections.get_event_db()
        ts_col = eventdb["teststations"]

        # Load data from the mongo collections
        ts_events = pd.DataFrame(list(ts_col.changestream.find()))

        # Group by Teststations
        grouped_df = ts_events.groupby('Teststation_ID')
        t1_events = grouped_df.get_group(1).copy()
        t1_events.drop(columns =['Feature3', 'Feature4'], axis=1, inplace = True)
        t2_events = grouped_df.get_group(2).copy()
        t2_events.drop(['Feature1', 'Feature2', 'Category'], axis = 1, inplace = True)
        t3_events = grouped_df.get_group(3).copy()
        t3_events.drop(['Feature1', 'Feature2','Feature3', 'Feature4', 'Category'], axis=1, inplace = True)

        # Group by Product Type
        pt_t1_events = t1_events.groupby('Product_Type')
        pt1_t1_events = pt_t1_events.get_group('PT1')
        pt2_t1_events = pt_t1_events.get_group('PT2')

        pt_t2_events = t2_events.groupby('Product_Type')
        pt1_t2_events = pt_t2_events.get_group('PT1')
        pt2_t2_events = pt_t2_events.get_group('PT2')


        # Sent all events to the REST Server
        if teststation == 'All' and product_type == 'All':
            self.send_events(t1_events, 1)
            self.send_events(t2_events, 2)
        
        if teststation == 'T1' and product_type == 'All':
            self.send_events(t1_events, 1)
        
        if teststation == 'T1' and product_type == 'PT1':
            self.send_events(pt1_t1_events, 1)

        if teststation == 'T1' and product_type == 'PT2':
            self.send_events(pt2_t1_events, 1)
        
        if teststation == 'T2' and product_type == 'PT1':
            self.send_events(pt1_t1_events, 1)
            self.send_events(pt1_t2_events,2)

        if teststation == 'T2' and product_type == 'PT2':
            self.send_events(pt2_t1_events, 1)
            self.send_events(pt2_t2_events,2)
            


    # Method for sending events to the REST Server
    def send_events(self, event , teststation):
    
        # Information for sending events
        url = 'http://127.0.0.1:5000/event'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # Iterate over the t1_events
        if teststation == 1: 
            for column,row in event.iterrows():

                # Extract features
                id = row['_id']
                component_id = row['Component_ID']
                teststation_id = row['Teststation_ID']
                feature1 = row['Feature1']
                feature2 = row['Feature2']
                date = row['Date']
                time = row['Time']
                category = row['Category']
                product_type = row['Product_Type']
                error_Message = row['Error_Message']

                # Store the features in a dict
                data = {'_id': id, 
                    'Component_ID' : component_id,
                    'Teststation_ID' : teststation_id,
                    'Feature1': feature1, 
                    'Feature2': feature2, 
                    'Date': date, 
                    'Time': time, 
                    'Category': category,
                    'Product_Type' : product_type,
                    'Error_Message': error_Message,
                    } 
                    
                # Convert the dict to a json file and sent it to the REST server
                requests.post(url, data=json.dumps(data, default=str), headers=headers)

        # Iterate over the t2_events
        if teststation == 2:
            for column,row in event.iterrows():

                # Extracting features
                id = row['_id']
                component_id = row['Component_ID']
                teststation_id = row['Teststation_ID']
                feature3 = row['Feature3']
                feature4 = row['Feature4']
                date = row['Date']
                time = row['Time']
                product_type = row['Product_Type']
                error_Message = row['Error_Message']

                # Store the features in a dict
                data = {'_id': id, 
                    'Component_ID' : component_id,
                    'Teststation_ID' : teststation_id,
                    'Feature3': feature3, 
                    'Feature4': feature4, 
                    'Date': date, 
                    'Time': time, 
                    'Product_Type' : product_type,
                    'Error_Message': error_Message,
                    } 
                    
                # Convert the dict to a json file and sent it to the REST server
                requests.post(url, data=json.dumps(data, default=str), headers=headers)
