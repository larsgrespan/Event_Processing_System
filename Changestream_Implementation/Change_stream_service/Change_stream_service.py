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
#
#from Changestream_Implementation.Change_stream_service.Process_change_stream import Process_change_stream
import pandas as pd
from joblib import load
from Process_change_stream import Process_change_stream
from bson.json_util import dumps
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections


class Changestream:

    def __init__(self, teststation, product_type):

        self.start_changestream(teststation, product_type)

        
    def start_changestream(self, teststation, product_type):
        # Get EventDB Connection
        eventdb = DBConnections.get_event_db()
        ts_col = eventdb["teststations"]

        # Configure Changestream
        change_stream_ts = ts_col.changestream.watch([{
        '$match': {
            'operationType': { '$in': ['insert'] }
        }
        }])

        # Create Class for the data processing
        ep = Process_change_stream()

        # Listen on EventDB
        for insert in change_stream_ts:
            event = ep.process_change_stream(insert)

            if teststation == 'All' and product_type == 'All':
                ep.process_event(event)
            
            if teststation == 'T1' and product_type == 'All':
                if event['Teststation_ID'].iloc[0] == 1:
                    ep.process_event(event)
            
            if teststation == 'T1' and product_type == 'PT1':
                if event['Teststation_ID'].iloc[0] == 1 and event['Product_Type'].iloc[0] == 'PT1':
                    ep.process_event(event)

            if teststation == 'T1' and product_type == 'PT2':
                if event['Teststation_ID'].iloc[0] == 1 and event['Product_Type'].iloc[0] == 'PT2':
                    ep.process_event(event)
            
            if teststation == 'T2' and product_type == 'PT1':
                if (event['Teststation_ID'].iloc[0] == 2 or event['Teststation_ID'].iloc[0] == 1) and event['Product_Type'].iloc[0] == 'PT1':
                    ep.process_event(event)

            if teststation == 'T2' and product_type == 'PT2':
                if (event['Teststation_ID'].iloc[0] == 2 or event['Teststation_ID'].iloc[0] == 1) and event['Product_Type'].iloc[0] == 'PT2':
                    ep.process_event(event)
            

