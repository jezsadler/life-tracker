# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 08:39:30 2018

@author: jezsadler

This script opens the JSON export from a trello board and counts tasks 
accomplished each week. The assumption is that a list is created for each week,
Monday - Sunday, tasks are added to that list as they are completed, and the
list is archived at some point during the next week. 
"""

import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta,SU,MO
import json

def tchomp(infile, outfile):

    # Open the trello output, put into a dataframe, and close the file.
    f = open(infile,'rb')
    trello_in =  json.load(f)
    f.close()
    
    # Pull out relevant aspects of the tasks and lists.
    actions = pd.DataFrame(trello_in['actions'])
    cards = pd.DataFrame(trello_in['cards'])
    lists = pd.DataFrame(trello_in['lists'])
    
    cards = cards[['dateLastActivity','idList','name']]
    lists = lists[['id','name']]
    
    # Get the close actions on lists.
    listacts = pd.concat([actions[actions['type'] == 'updateList']['date'],
                          actions[actions['type'] == 'updateList']['data'].apply(
                                  pd.Series)['list'].apply(pd.Series)],axis=1)
    
    listclosed = listacts[listacts['closed']==True][['date','name','id']]
    
    # Turn closed date string into a date.
    listclosed['date'] = listclosed['date'].apply(parse)
    listclosed['date'] = listclosed['date'].dt.date
    
    # Set the week from the Monday to Sunday before the list was closed.
    listclosed['wkend'] = listclosed['date'].apply(
            lambda x: x + relativedelta(weekday=SU(-1)))
    listclosed['wkstrt'] = listclosed['wkend'].apply(
            lambda x: x + relativedelta(weekday=MO(-1)))
    
    # Map tasks to lists.
    tasks_complete = pd.merge(cards,lists,left_on='idList',right_on='id')
    
    # Map lists to close dates.
    tasks_complete = pd.merge(tasks_complete,listclosed,left_on='idList',
                              right_on='id')
    
    # Group by weekly list.
    wtasks = tasks_complete.groupby(
            by=['wkstrt']).count()['name_x'].reset_index()
    
    # Label columns.
    wtasks.columns = ['Week start','Tasks completed']
    
    # Write to CSV.
    wtasks.to_csv(outfile,header=True)
    
    return wtasks