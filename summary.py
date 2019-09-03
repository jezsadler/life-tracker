# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:29:05 2019

@author: cheek
"""
import pandas as pd
from datetime import timedelta


from trello_chomper import tchomp
from calendar_chomper import cchomp
from misfit_sleep_chomper import schomp
from daylio_chomper import mchomp

start_date = "2019-04-01"
end_date = "2019-09-01"

weekly_trello = tchomp(
        "C:\\Users\\cheek\\Documents\\trello-20190902.json",
        "C:\\Users\\cheek\\Documents\\tasks-20190902.csv")

weekly_events = cchomp(
        'C:\\Users\\cheek\\Documents\\cheeky.jez@gmail.com.ics',
        'C:\\Users\\cheek\\Documents\\cal_events-20190501.csv',
        '2018-12-01')

weekly_sleep = schomp(
        "C:\\Users\\cheek\\Documents\\Sleep-20190902.csv",
        "C:\\Users\\cheek\\Documents\\SleepSummary-20190902.csv"
        )

weekly_mood = mchomp(
        "C:\\Users\\cheek\\Documents\\daylio_export20190902.csv",
        "C:\\Users\\cheek\\Documents\\daylio_weeklyavg20190902.csv"
        )

all_data = pd.merge(weekly_trello,weekly_events,how="outer",on="Week start")
all_data = pd.merge(all_data,weekly_sleep,how="outer",on="Week start")
all_data = pd.merge(all_data,weekly_mood,how="outer",on="Week start")

all_data["Week end"] = all_data["Week start"] + timedelta(days=6)

all_data["Week"] = all_data["Week start"].astype(str) + "-" + all_data["Week end"].astype(str)

period_data = all_data[(all_data["Week end"] > pd.to_datetime(start_date))
    & (all_data["Week start"] < pd.to_datetime(end_date))]

period_data.plot(x="Week start",rot=60)

