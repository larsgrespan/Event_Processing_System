from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from joblib import dump
import numpy as np
from pathlib import Path
import os

# Class Train_Models provides methods for training and saving random forest models
class Train_Models:

    # Train RF-Models
    def train_models(event_data):

        # Split data by 'Product_Type'
        splitted_events = split_by_product_type(event_data)

        # Adapt column 'Future_Error_Message' for training 
        adaptedLabels_list = list()
        for item in splitted_events:
            adaptedLabels = adapt_label(item)
            adaptedLabels_list.append(adaptedLabels)
        
        # Merge sublists
        adaptedLabels_list = [j for i in adaptedLabels_list for j in i]

        # Train and save Models
        for item in adaptedLabels_list:
            train_model(item)


# Group by column 'Product_Type' and extract different groups
def split_by_product_type(event_data):

    # Empty List for storing splitted events
    splitted_events = list()
    different_values = event_data.Product_Type.unique()
    grouped = event_data.groupby(event_data.Product_Type)   

    for item in different_values:
        splitted = grouped.get_group(item)
        splitted_events.append(splitted)

    return splitted_events


# Adapte label
def adapt_label(splitted_events):

    # Empty List for storing different list with adapted label
    adaptedLabels_list = list()

    # List which contains all different values of the column 'Future_Error_Message'
    different_values = splitted_events.Future_Error_Message.unique()
    
    # Adapt values and store results in adaptedLabels_list
    for item in different_values:

        tmp_list = different_values.tolist()
        tmp_events = splitted_events.copy()
        tmp_events['Label'] = tmp_events['Future_Error_Message']

        if item != 1:
            tmp_list.remove(item)
            for element in tmp_list:
                tmp_events['Label'] = np.where((tmp_events.Label== element), 0, tmp_events.Label)
            tmp_events['Label'] = np.where((tmp_events.Label== item), 1, tmp_events.Label)
            adaptedLabels_list.append(tmp_events)

    return adaptedLabels_list


# Train RF-model
def train_model(adapted_label):

    # Split data in test and train set
    features = adapted_label.copy()
    features = features.drop(columns =['Component_ID', 'Teststation_ID', 'DateTime' , 'Product_Type' , 'Error_Message' , 'Future_Error_Message' , 'Label'])
    X =  features
    y = adapted_label['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Meta information for creating the name of the Classifier
    teststation_id = adapted_label['Teststation_ID'].iloc[0]
    product_type = adapted_label['Product_Type'].iloc[0]
    error_list = adapted_label.loc[adapted_label['Label'] == 1, 'Future_Error_Message']
    error = error_list.iloc[0]

    # Create directory for storing the classifier
    path_name = f"../Database/Models/Teststation_ID_{teststation_id}/Product_Type_{product_type}/Error_Type_{error}.joblib"
    parent_directory = Path().resolve().parent
    path = str(parent_directory) + f"/Database/Models/Teststation_ID_{teststation_id}/Product_Type_{product_type}"

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)
    
    # Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)

    # print Accuracy of the model
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # Save Model
    dump(clf, path_name)

    # print Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print (cm)
