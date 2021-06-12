# class DataModel as bridge between Speed and Batch Layer
# Information about categorical features and features to drop...
class Data_Model:

    # drop_list contains all columns which are not necessary 
    drop_list = ['Test','Description']

    # contains all categorical features and its values
    feature_dict = {
        'Category' : ['Green', 'Yellow', 'Red', 'Blue']
    }

    # Get Drop_List
    def get_drop_list(self): 

        return self.drop_list

    # Get Categorical Features from the Teststations
    def get_features(self):

        self.feature_list = list(self.feature_dict.keys())

        return self.feature_list

    # Return values for specific categorical values
    def get_values(self, feature_name):

        feature_values = self.feature_dict[feature_name]

        return feature_values