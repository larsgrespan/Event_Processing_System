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

import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Event_processing'))
from Event_processing import Processing
from Load_label import Load_Label
from ML_model_training import Train_Models

# Class for processing data and training the ML-Models
class Batch_Training:

    # Get command line arguments
    def __init__(self, teststation, product_type):

        # start processing and training
        self.start_batch_training(teststation, product_type)

    # Method to Initiate Data Processing and ML-Model Training    
    def start_batch_training(self, teststation, product_type):

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

        pt_t3_events = t3_events.groupby('Product_Type')
        pt1_t3_events = pt_t3_events.get_group('PT1')
        pt2_t3_events = pt_t3_events.get_group('PT2')


        # Based on comannd line arguments, process and train models with all data or with specific data
        if teststation == 'All' and product_type == 'All':

            # Preprocess data in order to train the models.
            t1_events_pr = Processing.process_events(t1_events)
            t2_events_pr = Processing.process_events(t2_events)
            Processing.process_events(t3_events)
            
            # Get Labels for t1_events_pr and t2_events_pr
            t1_events_label = Load_Label.load_label(t1_events_pr)
            t2_events_label = Load_Label.load_label(t2_events_pr)

            # Train and save Models
            Train_Models.train_models(t1_events_label)
            Train_Models.train_models(t2_events_label)

        # Based on comannd line arguments, process and train models with all data or with specific data
        if teststation == 'T1' and product_type == 'All':

            t1_events_pr = Processing.process_events(t1_events)
            Processing.process_events(t2_events)

            t1_events_label = Load_Label.load_label(t1_events_pr)
            Train_Models.train_models(t1_events_label)

        # Based on comannd line arguments, process and train models with all data or with specific data
        if teststation == 'T1' and product_type == 'PT1':
            
            t1_events_pr = Processing.process_events(pt1_t1_events)
            Processing.process_events(pt1_t2_events)

            t1_events_label = Load_Label.load_label(t1_events_pr)
            Train_Models.train_models(t1_events_label)

        # Based on comannd line arguments, process and train models with all data or with specific data
        if teststation == 'T1' and product_type == 'PT2':

            t1_events_pr = Processing.process_events(pt2_t1_events)
            Processing.process_events(pt2_t2_events)

            t1_events_label = Load_Label.load_label(t1_events_pr)
            Train_Models.train_models(t1_events_label)


        # Based on comannd line arguments, process and train models with all data or with specific data     
        if teststation == 'T2' and product_type == 'PT1':
            
            t1_events_pr = Processing.process_events(pt1_t1_events)
            t2_events_pr = Processing.process_events(pt1_t2_events)
            Processing.process_events(pt1_t3_events)
            
            t1_events_label = Load_Label.load_label(t1_events_pr)
            t2_events_label = Load_Label.load_abel(t2_events_pr)

            Train_Models.train_models(t1_events_label)
            Train_Models.train_models(t2_events_label)

        # Based on comannd line arguments, process and train models with all data or with specific data
        if teststation == 'T2' and product_type == 'PT2':
            
            t1_events_pr = Processing.process_events(pt2_t1_events)
            t2_events_pr = Processing.process_events(pt2_t2_events)
            Processing.process_events(pt2_t3_events)
            
            t1_events_label = Load_Label.load_label(t1_events_pr)
            t2_events_label = Load_Label.load_label(t2_events_pr)

            Train_Models.train_models(t1_events_label)
            Train_Models.train_models(t2_events_label)
