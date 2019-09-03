# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:20:33 2019

@author: jezsadler

This script takes the CSV output from Daylio, a daily mood tracking app, and calculates
weekly average mood.
"""

import pandas as pd

infile = "C:\\Users\\cheek\\Documents\\daylio_export20190902.csv"
outfile = "C:\\Users\\cheek\\Documents\\daylio_weeklyavg20190902.csv"

def mchomp (infile,outfile):
    # Read in the daylio export file.
    mood_data = pd.read_csv(infile)
    
    # Translate mood descriptions to a 0-4 scale.
    mood_dict = {'rad':4,'good':3,'meh':2,'fugly':1,'awful':0}
    mood_data = mood_data.replace({"mood":mood_dict})
    
    # Select just the date and mood columns.
    mood_data = mood_data[["full_date","mood"]]
    
    # Set the index to be the date, for grouping purposes.
    mood_data.index = pd.to_datetime(mood_data['full_date'])
    
    # Take weekly averages of mood.
    mood_weekly = mood_data.groupby(
                pd.Grouper(freq='W-MON')).mean().reset_index()
    
    # Retitle the columns and convert datetime to date.
    mood_weekly.columns = ["Week start","Mood"]
    mood_weekly['Week start'] = mood_weekly['Week start'].dt.date
    
    # Write out the summary.
    mood_weekly.to_csv(outfile,header=True)

    return mood_weekly
