from joblib import load
from pathlib import Path
import numpy as np
import os

# To make predictions for the event the correct models have to be loaded. 
# This class provides a method to select the matching models
# Additionally, the loaded ML models require a specific input for making predictions.
# Therefore some columns have to be dropped. A method for selecting the matching features is provided in this class as well
class Model_Selection:

    # Select which models hav to be loaded.
    # Selection is based on meta information
    def select_model(event):

        # Dict for storing 
        models = dict()

        # Get information about the event
        teststation_id = event['Teststation_ID'].iloc[0]
        product_type = event['Product_Type'].iloc[0]

        # Get models which match to the information extracted above
        path_name = f"/Database/Models/Teststation_ID_{teststation_id}/Product_Type_{product_type}"
        parent_directory = Path().resolve().parent
        directory = os.fsencode(str(parent_directory) + path_name)

        # Load models and store them in the models dict
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".joblib"): 
                models[filename] = load(f"..{path_name}/{filename}")

        return models

    # Select features which are required for making predictions
    def select_features(event):

        # Drop unnecessary columns
        features = event.copy()
        features = features.drop(columns =['Component_ID', 'Teststation_ID', 'DateTime' , 'Product_Type' , 'Error_Message'])

        return features
