# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 15:14:38 2018

@author: jezsadler

This script opens an ical file and counts the number of events each week from
Monday to Sunday.
"""

import icalendar
import pandas as pd
import datetime

def cchomp (infile,outfile,startdate):
    
    # Set up data structures to hold the events.
    events_cal = pd.DataFrame(columns=['Event','Start'])
    this_event = pd.Series(['',''],index=['Event','Start'])
    
    # Open the calendar file, put events in the data structures.
    g = open(infile,'rb')
    gcal = icalendar.Calendar.from_ical(g.read())
    for component in gcal.walk('vevent'):
        this_event[0]=component.get('summary')
        this_event[1]=component.get('dtstart').dt
        events_cal=events_cal.append(this_event,ignore_index=True)
    g.close()

    events_cal['Start'] = pd.to_datetime(
            events_cal['Start'],utc=True).dt.tz_convert('US/Pacific')
    
    # Take events 
    recent = events_cal[events_cal['Start'] > pd.to_datetime(
            startdate).tz_localize('US/Pacific')].reset_index()[['Event','Start']]
    recent = recent[recent['Start'].dt.date < datetime.date.today()]
    
    recent.index = recent['Start']
    
    weekly = recent.groupby(
            pd.Grouper(freq='W-MON')).count()['Event'].reset_index()
    
        
    # Group by weekly list.
    weekly.columns = ['Week start','Events']
    
    weekly['Week start'] = weekly['Week start'].dt.date
    
    # Write to CSV.
    weekly.to_csv(outfile,header=True)
    
    return weekly
