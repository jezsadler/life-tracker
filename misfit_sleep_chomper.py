# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:03:56 2019

@author: jezsadler

This script takes the sleep log from a Misfit tracking device, as exported via
IFTTT, and calculates average total sleep and restful sleep in hours per week.
First we sum sleep sessions per day, then average per week.
"""

import pandas as pd
from dateutil.parser import parse
from datetime import timedelta

def schomp(infile,outfile):

    # Read in the sleep data.
    sleep_data = pd.read_csv(infile)
    
    # Turn the sleep end times into datetimes so we can work with them.
    sleep_data['End'] = sleep_data['End'].apply(parse)
    
    # Count any sleep that ends after 10pm as belonging to the next day.
    sleep_data['End'] = sleep_data['End'].apply(lambda x: x + timedelta(hours=2))
    
    # Convert to dates so that we can total per day.
    sleep_data['End'] = sleep_data['End'].dt.date
    
    # Total daily.
    sleep_daily = sleep_data.groupby(by='End').sum()[[
            'Total sleep (secs)','Restful sleep (secs)']].reset_index()
    
    # Convert index to datetime so that we can average weekly.
    sleep_daily.index = pd.to_datetime(sleep_daily['End'])
    
    # Average weekly.
    sleep_weekly = sleep_daily.groupby(
            pd.Grouper(freq='W-MON')).mean().reset_index()
    
    # Convert End column back to dates.
    sleep_weekly['End'] = sleep_weekly['End'].dt.date
    
    # Label columns and convert seconds -> hours.
    sleep_weekly.columns = ['Week start','Total sleep','Restful sleep']
    sleep_weekly['Total sleep'] = sleep_weekly['Total sleep']/3600
    sleep_weekly['Restful sleep'] = sleep_weekly['Restful sleep']/3600

    # Write to CSV.
    sleep_weekly.to_csv(outfile,header=True)

    return sleep_weekly