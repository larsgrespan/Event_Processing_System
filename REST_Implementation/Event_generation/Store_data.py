import pandas as pd
from Create_dependencies import Create_Dependencies
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Database'))
from Connection import DBConnections


# Convert CSV files to pandas dataframe
t1_events = pd.read_csv('./teststation1.csv', header = 0)
t2_events = pd.read_csv('./teststation2.csv', header = 0)
t3_events = pd.read_csv('./teststation3.csv', header = 0)

# Create Dependencies among the dataframes
# Delete rows in the following dataframe that do not have the value "Ok" in the column "Error_Message" in the present dataframe
t1_not_ok = Create_Dependencies.get_not_oks(t1_events)
t2_events = Create_Dependencies.drop_not_oks(t1_not_ok, t2_events)
t2_not_ok = Create_Dependencies.get_not_oks(t2_events)
t1_2_not_ok = t2_not_ok + t1_not_ok
t3_events = Create_Dependencies.drop_not_oks(t1_2_not_ok, t3_events)

# Per Component_ID, the product types must be the same across the records.
pt1_list = Create_Dependencies.get_pt(t1_events, 'PT1')
pt2_list = Create_Dependencies.get_pt(t1_events, 'PT2')
t2_events = Create_Dependencies.correct_pt(t2_events, pt1_list, 'PT1')
t2_events = Create_Dependencies.correct_pt(t2_events, pt2_list, 'PT2')
t3_events = Create_Dependencies.correct_pt(t3_events, pt1_list, 'PT1')
t3_events = Create_Dependencies.correct_pt(t3_events, pt2_list, 'PT2')

# Sort values by ID
t1_events = Create_Dependencies.sort_by_component_id(t1_events)
t2_events = Create_Dependencies.sort_by_component_id(t2_events)
t3_events = Create_Dependencies.sort_by_component_id(t3_events)

# Get EventDB Connection
eventdb = DBConnections.get_event_db()
ts_col = eventdb["teststations"]

# Store events in the Database
ts_col.changestream.insert_many(t1_events.to_dict('records'))
ts_col.changestream.insert_many(t2_events.to_dict('records'))
ts_col.changestream.insert_many(t3_events.to_dict('records'))
