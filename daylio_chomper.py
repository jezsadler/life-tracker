# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:20:33 2019

@author: cheek
"""

import pandas as pd

infile = "C:\\Users\\cheek\\Documents\\daylio_export20190902.csv"
outfile = "C:\\Users\\cheek\\Documents\\daylio_weeklyavg20190902.csv"

def mchomp (infile,outfile):
    mood_data = pd.read_csv(infile)
    
    mood_dict = {'rad':4,'good':3,'meh':2,'fugly':1,'awful':0}
    
    mood_data = mood_data.replace({"mood":mood_dict})
    
    mood_data = mood_data[["full_date","mood"]]
    
    mood_data.index = pd.to_datetime(mood_data['full_date'])
    
    mood_weekly = mood_data.groupby(
                pd.Grouper(freq='W-MON')).mean().reset_index()
    
    mood_weekly.columns = ["Week start","Mood"]
    mood_weekly['Week start'] = mood_weekly['Week start'].dt.date
    
    mood_weekly.to_csv(outfile,header=True)

    return mood_weekly