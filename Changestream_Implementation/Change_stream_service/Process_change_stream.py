import sys
import os
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Event_processing'))
from Event_processing import Processing
from Model_selection import Model_Selection

# To make predictions for the events of the test stations, the data must be processed, converted to the correct format, 
# the corresponding ML model must be loaded and the results have to be saved to be displayed later. 
# The method contained in the class performs the above steps
class Process_change_stream:

    # Event processing
    def process_event(self, change_stream_event):

        # Get EventDB Connection
        eventdb = DBConnections.get_event_db()
        col_result = eventdb["result"]

        # Get pandas dataframe
        event = pd.DataFrame(change_stream_event)

        # Process Event
        processed_event = Processing.process_events(event)

        # Because NAN are going to be deleted in the processing script, it may happen that the event is empty
        if processed_event is not None:
            if processed_event.empty == False:

                # Select matching features for the predicition
                features = Model_Selection.select_features(processed_event)

                # Load matching ML models
                models = Model_Selection.select_model(processed_event)

                # Make Prediction for each model
                for item in models:
                    
                    # Make predictions and keep result in varaible result
                    result = models[item].predict(features)

                    # Get probability of the prediciton
                    prob = models[item].predict_proba(features)

                    # Create list with all important information 
                    tmp = result.tolist()
                    processed_event['Result'] = tmp[0]
                    processed_event['Probability'] = prob[0,0]
                    error = item
                    processed_event['Error_Type'] = error[:-7]
                    subset = processed_event[['Component_ID', 'Teststation_ID', 'Product_Type' , 'Error_Type' ,  'Result' , 'Probability']]

                    # Message to corresponding reststation if Result is 1 (Error)
                    if tmp[0] == 1:
                        print('Remove following item from the production line')
                        print(subset)

                    # Create dict for storing the important information in mongodb
                    dict = subset.to_dict('records')
                    prediction = list()

                    # Encode dict values (numpy data types) to python data types
                    for i in dict:
                        input = self.encode_features(i)
                        prediction.append(input)

                    # Store Prediction in Result DB
                    col_result.insert_many(prediction)


    # Process Changestream Format
    def process_change_stream(self, change_stream_event):

        dict_event = change_stream_event["fullDocument"]
        event = pd.DataFrame(dict_event, index=[0])

        return event
    
    # Encode dict in order to store the dict in a mongodb collection
    def encode_features(self, dict):

        dict_new = {}
        for k, v in dict.items():

            if isinstance(v, np.bool_):
                v = bool(v)

            if isinstance(v, np.int64):
                v = int(v)

            if isinstance(v, np.float64):
                v = float(v)

            if isinstance(v, np.uint32):
                v = int(v)

            if isinstance(v, np.float32):
                v = float(v)

            dict_new[k] = v

        return dict_new