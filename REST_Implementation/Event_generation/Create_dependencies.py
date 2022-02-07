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

# Class with functions that create dependencies across the different test stations records
class Create_Dependencies:

# Get list of Component_IDs where the Error_Message is 'TemperatureTooHigh' or 'TemperatureTooLow'
    def get_not_oks(events):

        temp_hi = events[events.Error_Message == 'TemperatureTooHigh']
        temp_lo = events[events.Error_Message == 'TemperatureTooLow']

        tmp = temp_hi['Component_ID'].tolist()
        tmp2 = temp_lo['Component_ID'].tolist()
        not_ok_list = tmp + tmp2

        return not_ok_list

# Drop rows from events dataframe. Drop when list values are in the Component_IDs values from the events dataframe
    def drop_not_oks(not_ok_list,events):

        events = events[~events['Component_ID'].isin(not_ok_list)]

        return events

# Get List of Component_IDs where Product_Type is PT1
    def get_pt(events, pt):

        tmp = events[events.Product_Type == pt]
        pt_list = tmp['Component_ID'].tolist()

        return pt_list

# Correct Product_Type when the corresponding Component_ID is in the pt_list
    def correct_pt(events, pt_list, pt):

        events['Product_Type'] = np.where(events['Component_ID'].isin(pt_list), pt, events.Product_Type)

        return events

# Sort dataframe by Component_ID
    def sort_by_component_id(events):

        events = events.sort_values(by=['Component_ID'])

        return events
