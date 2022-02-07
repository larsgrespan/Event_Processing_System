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
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections

# In order to train the ML models using supervised learning techniques such as RandomForest, it is necessary 
# that the error(label) is also input for the training. 
# The errors may only be displayed at the following test station, which is why the 'Error_Message' of the following test stations are loaded. 
# This class provides a method for loading the Column 'Error_Message' from the subsequent test station.
class Load_Label:

    # Method for loading the Column 'Error_Message' from the subsequent test station
    def load_label(event_data):
        
        # Get EventDb Connection
        eventdb = DBConnections.get_event_db()
        event_data_label = event_data
        # Get Teststation_ID
        teststation_id = event_data['Teststation_ID'].iloc[0]

        # Load Label for Teststation1
        if teststation_id == 1:

            # Access corresponding collection
            col_t2_preprocess = eventdb["processed_t2_events_batch"]

            # Load Label 
            label = pd.DataFrame(list(col_t2_preprocess.find()))
            label = label[['Component_ID','Error_Message']]
            label.columns = ['Component_ID', 'Future_Error_Message']

            # Concate t1_events and label using the Component_ID
            event_data_label = pd.merge(event_data, label, on="Component_ID")

        # Load Label for Teststation2
        if teststation_id == 2:
            
            # Access corresponding collection
            col_t3_preprocess = eventdb["processed_t3_events_batch"]

            # Load Label 
            label = pd.DataFrame(list(col_t3_preprocess.find()))
            label = label[['Component_ID','Error_Message']]
            label.columns = ['Component_ID', 'Future_Error_Message']

            # Concate t2events and label using the Component_ID
            event_data_label = pd.merge(event_data, label, on="Component_ID")

        return event_data_label
