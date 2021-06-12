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
            

