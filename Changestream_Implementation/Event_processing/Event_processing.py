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
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Data_model'))
from Data_model import Data_Model


# Set of Methods to preprocess data in order to train models or make predictions
class Processing:

# Method for orchestrating event processing steps
    def process_events(event_data):

        # Clean events
        events_cl = clean_events(event_data)

        # In case the cleaning method above dropped an event and only a single event (array or pandas series) was transfered to the method, derivating and storing is not necessary
        if events_cl.empty == False:
            
            # Get additional attributes by derivating existing attributes
            events_dv = derivate_events(events_cl)

            # Store processed events
            store_events(events_dv)

            # merge events (first and last teststation events don't need to be merged)
            if event_data['Teststation_ID'].iloc[0] == 2:
                events_dv = merge_events(events_dv)

            # Return events for further processing (Last teststion doesn't need to return events)
            if event_data['Teststation_ID'].iloc[0] != 3:
                return events_dv


# Method to call all cleaning operations
def clean_events(event_data):

    # Delete rows with NAN values
    event_data = delete_nan(event_data)

    # Delete column '_id' (generated in the mongodb)
    event_data = delete_id_column(event_data)

    # Transform commas to dots
    event_data = convert_comma_to_dot(event_data)

    # Apply a regex
    event_data = apply_regex(event_data)

    # Delete unique columns
    event_data = delete_unique_columns(event_data)

    # Transform column 'Error_Message' to numeric values
    event_data = process_error_message(event_data)

    return event_data.copy()


# Method to call all derivation operations
def derivate_events(event_data):

    # Create a 'DateTime' column out of column 'Date' and 'Time'
    event_data = combine_date_time(event_data)

    # Create a cheksum feature out of the 'Time' column
    event_data = create_checksum(event_data)

    # Delete column 'Data' and 'Time' (Redundant because of column 'DateTime')
    event_data = delete_date_and_time(event_data)

    # Create day columns out of column 'DateTime'
    event_data = get_days(event_data)

    # Create week column out of column 'DateTime'
    event_data = get_week(event_data)

    # Create object of class Data_Model
    dm = Data_Model()

    # Store event_data column names in a list
    column_names = event_data.columns.tolist()

    # Check if columns of column_names are also present in the feature_list from the Data_Model
    check =  any(item in column_names for item in dm.get_features())

    # If yes, derivate events
    if check is True:
        if 'Category' in column_names:
            event_data = get_categories(event_data)

    return event_data.copy()


# In order to merge events from different teststation, the processed events have to be stored
def store_events(event_data):
    
    # Get EventDB Connection
    eventdb = DBConnections.get_event_db()

    # Check from which station the events are from and whether the event is in the speed layer or in the batch layer
    # In the Batch Layer the collection has to be cleaned before storing events. Otherwise the same events will be stored multiple times, when executing the batch training more than one time.
    # Merging events would not be possible because the Component_ID is not unqiue any longer.
    # In case the event is from the Speed layer (single event), the redundancy problem does not appear, which is why a cleaning of the collection is not necessary
    # Therefore the events from the batch layer and the events from the speed layer needs to be stored seperately

    # Check whether the input is a single event or multiple events and from which teststation
    if event_data['Teststation_ID'].iloc[0] == 1 and len(event_data) == 1:
        
        # Create a collection
        col_t1_preprocess = eventdb["processed_t1_events"]

        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)
        
        # Save processed events
        col_t1_preprocess.insert_many(dict_events)

    # Check whether the input is a single event or multiple events and from which teststation
    if event_data['Teststation_ID'].iloc[0] == 1 and len(event_data) > 1:

        # Create a collection
        col_t1_preprocess = eventdb["processed_t1_events_batch"]
        # Clear collection
        col_t1_preprocess.delete_many({})
        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)

        # Save processed events
        col_t1_preprocess.insert_many(dict_events)
        
    # Check whether the input is a single event or multiple events and from which teststation
    if event_data['Teststation_ID'].iloc[0] == 2 and len(event_data) == 1:

        # Create a collection        
        col_t2_preprocess = eventdb["processed_t2_events"]
        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)

        # Save processed events
        col_t2_preprocess.insert_many(dict_events)

    # Check whether the input is a single event or multiple events and from which teststation    
    if event_data['Teststation_ID'].iloc[0] == 2 and len(event_data) > 1:

        # Create a collection        
        col_t2_preprocess = eventdb["processed_t2_events_batch"]
        # Clear collection
        col_t2_preprocess.delete_many({})
        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)

        # Save processed events
        col_t2_preprocess.insert_many(dict_events)
        
    # Check whether the input is a single event or multiple events and from which teststation
    if event_data['Teststation_ID'].iloc[0] == 3 and len(event_data) == 1:

        # Create a collection        
        col_t3_preprocess = eventdb["processed_t3_events"]
        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)

        # Save processed events
        col_t3_preprocess.insert_many(dict_events)

    # Check whether the input is a single event or multiple events and from which teststation
    if event_data['Teststation_ID'].iloc[0] == 3 and len(event_data) > 1:

        # Create a collection
        col_t3_preprocess = eventdb["processed_t3_events_batch"]
        # Clear collection
        col_t3_preprocess.delete_many({})
        # Encode events for storing in the mongodb
        dict = event_data.to_dict('records')
        dict_events = list()
        for i in dict:
            tmp = encode_features(i)
            dict_events.append(tmp)

        # Save processed events
        col_t3_preprocess.insert_many(dict_events)
        
        
# Merge Data for Predictions
# Because of multiple collections (origin in the store_events method) the merging has to be handled seperately as well
def merge_events(event_data):
    t2_pc_events = event_data

    # Get EventDB Connection
    eventdb = DBConnections.get_event_db()

    # Placeholder for storing event/events
    merged_data = []

    # Check if event is from the Speed Layer
    if len(event_data) == 1: 

        # Access the speed layer collection for the t1 events
        col_t1_preprocess = eventdb["processed_t1_events"]

        # Load processed data from teststation1
        t1_pc_events = pd.DataFrame(list(col_t1_preprocess.find()))

        # Select specific columns which are necessary for the merging
        t1_pc_events = t1_pc_events[['Component_ID','Feature1','Feature2','Green', 'Yellow', 'Red', 'Blue']]

        # Concate t2_pc_events and t1_pc_events using the Component_ID
        merged_data = pd.merge(t2_pc_events, t1_pc_events, on="Component_ID")

    # Check if event is from the Batch Layer
    if len(event_data) > 1: 

        # Access the batch layer collection for the t1 events
        col_t1_preprocess = eventdb["processed_t1_events_batch"]

        # Load processed data from teststation1
        t1_pc_events = pd.DataFrame(list(col_t1_preprocess.find()))
        t1_pc_events = t1_pc_events[['Component_ID','Feature1','Feature2','Green', 'Yellow', 'Red', 'Blue']]

        # Concate t2_pc_events and t1_pc_events using the Component_ID
        merged_data = pd.merge(t2_pc_events, t1_pc_events, on="Component_ID")

    return merged_data


# delete all rows with missing values
def delete_nan(event_data):

    event_data.dropna()

    return event_data.copy()

    
# delete Error_Message value '_id' (generated in mongodb)
def delete_id_column(event_data):
        
    if '_id' in event_data.columns:
        del event_data['_id']

    return event_data.copy()


# Replace ',' with '.' 
def convert_comma_to_dot(event_data):

    columns = list(event_data) 
    for i in columns:
        event_data[i].replace( { r"[,]+" : '' }, inplace = True, regex = True)

    return event_data.copy()


# Apply regex on columns
def apply_regex(event_data):

    columns = list(event_data) 
    for i in columns:
        event_data[i].replace( { r"[^0-9a-zA-Z\_.-:]+" : '' }, inplace = True, regex = True)

    return event_data.copy()


# Delete columns based on the droplist of the DataModel
def delete_unique_columns(event_data):

    # Create columns which are in the droplist of the Datamodel (For testing purposes. So far there are no unique columns to drop)
    event_data['Test']='Test'
    event_data['Description']='Description'

    # Create List with column names
    columns_list = event_data.columns.tolist()

    # Load DataModel and DropList
    dm = Data_Model()
    drop_list = dm.get_drop_list()


    # Delete columns which are also present in the DropList
    for column in columns_list:
        if column in drop_list:
            del event_data[column]

    return event_data.copy()

# Error_Message values were set from True/False to 1/0 and other possible values
# All missing NAN or wrong values are going to be removed
def process_error_message(event_data):
    
    # Convert all values in upper case
    event_data['Error_Message'] = event_data['Error_Message'].astype(str).str.upper()

    # Transform all possible values for OK to 1
    event_data['Error_Message'] = np.where((event_data.Error_Message=='OK'), 1,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='OKAY'), 1,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='1'), 1,event_data.Error_Message)

    # Transform all possilbe values for TemperaturTooHigh to 2
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURETOOHIGH'), 2,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURE TOO HIGH'), 2,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURE_TOO_HIGH'), 2,event_data.Error_Message)

    # Transform all possible values for TemperaturTooLow to 3
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURETOOLOW'), 3,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURE TOO LOW'), 3,event_data.Error_Message)
    event_data['Error_Message'] = np.where((event_data.Error_Message=='TEMPERATURE_TOO_LOW'), 3,event_data.Error_Message)


    # Delete all other values which haven't been processed (possible errors -> no information gain)
    event_data.drop(event_data[(event_data.Error_Message != 1) & 
    (event_data.Error_Message != 2) & 
    (event_data.Error_Message != 3 )].index, inplace=True)

    return event_data.copy()


# Merge Date and Time in one new column
def combine_date_time(event_data):

    # Combine Date and Time to DateTime
    dateTime = pd.to_datetime(event_data['Date'] + ' ' + event_data['Time'])

    # find index number of column time
    index_no = event_data.columns.get_loc('Time')

    # Using DataFrame.insert() to add the new column 
    event_data.insert(index_no +1, "DateTime", dateTime, True)

    return event_data.copy()


# Create a new field based on a convertation of time into an int value
def create_checksum(event_data):

    # Get Total Seconds from the Time column
    checkSum = event_data['Time'].astype(str).apply(total_seconds)

    # Create new column checksum and insert the column into the dataframe
    index_no = event_data.columns.get_loc('DateTime')
    event_data.insert(index_no + 1, "Checksum", checkSum, True)

    return event_data.copy()


# Calculate total seconds
def total_seconds(time):

    tmp = time.split(':')

    return (60*60*int(tmp[0])+60*int(tmp[1]))+int(tmp[2])


# Delete column Date and Time
def delete_date_and_time(event_data):

    if 'Date' in event_data.columns:
        del event_data['Date']

    if 'Time' in event_data.columns:
        del event_data['Time']

    return event_data.copy()


# Create new columns for each day
def get_days(event_data):

    # Get Day from column DateTime
    day = event_data['DateTime'].dt.dayofweek

    # find index number of column CheckSum
    index_no = event_data.columns.get_loc('Checksum')

    # Using DataFrame.insert() to add a column 
    event_data.insert(index_no +1, 'Day', day.astype(str), True)

    # If event is from Batch Layer a onehot encoding is possilbe (all possible values are present in the dataframe)
    if len(event_data) > 1:
        event_data = encode_days_events(event_data)

    # If event is from Speed Layer a onehot encoding is not possilbe which is why the columns need to be created automatically.
    else:
        event_data = encode_days_event(event_data)

    return event_data.copy()

# Encode days using onehot encoding for events from the batch layer
def encode_days_events(event_data):

    # Map numeric values to days
    event_data['Day'] = np.where((event_data.Day=='0'), 'Monday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='1'), 'Tuesday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='2'), 'Wednesday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='3'), 'Thursday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='4'), 'Friday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='5'), 'Saturday', event_data.Day)
    event_data['Day'] = np.where((event_data.Day=='6'), 'Sunday', event_data.Day)

    # Apply onehot encoing using the pandas function get_dummies()
    event_data = pd.concat([event_data,pd.get_dummies(event_data['Day'])],axis=1)

    # Drop the Day column after the onehot encoding
    event_data.drop(['Day'],axis=1, inplace=True)

    # Reorder the columns of the dataframe
    if event_data['Teststation_ID'].iloc[0] == 1:
        event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature1','Feature2','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Category', 'Product_Type' , 'Error_Message']]

    if event_data['Teststation_ID'].iloc[0] == 2:
        event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature3','Feature4','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Product_Type' , 'Error_Message']]

    if event_data['Teststation_ID'].iloc[0] == 3:
        event_data = event_data[['Component_ID', 'Teststation_ID' ,'DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Product_Type' , 'Error_Message']]

    return event_data.copy()

# Encode days manually for a event from the speed layer
def encode_days_event(event_data):

    # Create Day columns with. Initialize with value 0.
    event_data.loc[:,"Monday"] = 0
    event_data.loc[:,"Tuesday"] = 0
    event_data.loc[:,"Wednesday"] = 0
    event_data.loc[:,"Thursday"] = 0
    event_data.loc[:,"Friday"] = 0
    event_data.loc[:,"Saturday"] = 0
    event_data.loc[:,"Sunday"] = 0

    # If column 'Day' is Monday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '0':
        event_data.loc[0,'Monday'] = 1

    # If column 'Day' is Tuesday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '1':
        event_data.loc[0,'Tuesday'] = 1

    # If column 'Day' is Wednesday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '2':
        event_data.loc[0,'Wednesday'] = 1

    # If column 'Day' is Thursday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '3':
        event_data.loc[0,'Thursday'] = 1

    # If column 'Day' is Friday - change the value from column 'Monday' to 1    
    if event_data['Day'].iloc[0] == '4':
        event_data.loc[0,'Friday'] = 1

    # If column 'Day' is Saturday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '5':
        event_data.loc[0,'Saturday'] = 1

    # If column 'Day' is Sunday - change the value from column 'Monday' to 1
    if event_data['Day'].iloc[0] == '6':
        event_data.loc[0,'Sunday'] = 1

    # Drop the Day column after the onehot encoding
    event_data.drop(['Day'],axis=1, inplace=True)

    # Reorder the columns of the dataframe
    if event_data['Teststation_ID'].iloc[0] == 1:
        event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature1','Feature2','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Category', 'Product_Type' , 'Error_Message']]

    if event_data['Teststation_ID'].iloc[0] == 2:
        event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature3','Feature4','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Product_Type' , 'Error_Message']]

    if event_data['Teststation_ID'].iloc[0] == 3:
        event_data = event_data[['Component_ID', 'Teststation_ID' ,'DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
        'Thursday', 'Friday' , 'Saturday' , 'Sunday' , 'Product_Type' , 'Error_Message']]

    return event_data.copy()


# Get Weeks from the colukns 'DateTime'
def get_week(event_data):

    week = event_data['DateTime'].dt.isocalendar().week
    index_no = event_data.columns.get_loc('Sunday')
    event_data.insert(index_no +1, 'Week', week, True)


    return event_data.copy()

# Method for applying a oneHot encoding on the attribute category
def get_categories(event_data):

    # If event is from Batch Layer a onehot encoding is possilbe (all possible values are present in the dataframe)
    if len(event_data) > 1:
        event_data_categories = encode_categories(event_data)

    # If event is from Speed Layer a onehot encoding is not possilbe which is why the columns need to be created automatically.
    else:
    
        # Feature Category is not present in every event (Feature DateTime is availalbe in all events independently from which teststation the event is from)
        # DataModel has to be loaded in order to get the value of feature Category
        dm = Data_Model()
        category_columns = dm.get_values('Category')

        # Create dict with Category values as key and 0 as value
        category_dict = { i : 0 for i in category_columns }

        # Convert dict to dataframe
        categories = pd.DataFrame(category_dict, index=[0])
        
        # Combine event with category dataframe
        event = pd.concat([event_data, categories], axis=1)

        # Execute Onehot encoding manually using the encode_category method
        event_data_categories = encode_category(event)

    return event_data_categories


# Onehot encoding (automatically) for feature 'Category'
def encode_categories(event_data):

    # Create new category columns by using onehotencoding
    event_data = pd.concat([event_data,pd.get_dummies(event_data['Category'])],axis=1)

    # Drop the Day column after the onehot encoding
    event_data.drop(['Category'],axis=1, inplace=True)

    # Reorder dataframe
    event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature1','Feature2','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
    'Thursday', 'Friday' , 'Saturday' , 'Sunday', 'Week','Green', 'Yellow', 'Red', 'Blue' ,'Product_Type' , 'Error_Message']]

    return event_data.copy()


# Onehot encoding (manually) for feature 'Category'
def encode_category(event_data):

    # If column 'Category' is Green - change the value from column 'Green' to 1
    if event_data['Category'].iloc[0] == 'Green':
        event_data.loc[0,'Green'] = 1

    if event_data['Category'].iloc[0] == 'Yellow':
        event_data.loc[0,'Yellow'] = 1

    if event_data['Category'].iloc[0] == 'Red':
        event_data.loc[0,'Red'] = 1

    if event_data['Category'].iloc[0] == 'Blue':
        event_data.loc[0,'Blue'] = 1

    # Drop the Day column after the onehot encoding
    event_data.drop(['Category'],axis=1, inplace=True)

    # Reorder dataframe
    event_data = event_data[['Component_ID', 'Teststation_ID', 'Feature1','Feature2','DateTime', 'Checksum', 'Monday', 'Tuesday' , 'Wednesday', 
    'Thursday', 'Friday' , 'Saturday' , 'Sunday', 'Week','Green', 'Yellow', 'Red', 'Blue' ,'Product_Type' , 'Error_Message']]

    return event_data.copy()


# The events may have been transformed to Numpy data types when applying Numpy methods. 
# MongoDB does not accept these data types, which is why the events must be transformed back into python data types.
def encode_features(dict):

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

