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
