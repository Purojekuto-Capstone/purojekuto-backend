import numpy as np
import pandas as pd
import random
from datetime import date, timedelta

def clean_data(data):
    try:
        df = pd.DataFrame(data)
        df['start date'] = pd.to_datetime(df['start date'])
        df['end date'] = pd.to_datetime(df['end date'])
        df['project start'] = pd.to_datetime(df['project start'])
        df['project finish'] = pd.to_datetime(df['project finish'])
        df['one'] = 1
        df['today'] = date.today()

        df['hours']= pd.to_timedelta(df['end date']- df['start date'], unit='hr')
        df['hours'] = df['hours'].astype('timedelta64[m]').astype('float').apply(lambda x: x/60)

        project = df.groupby('project name')['hours'].sum()
        hours = list(project.values)
        names = list(project.index)

        df['progress'] = (pd.to_datetime(df['project finish']) - pd.to_datetime(df['today']))/(pd.to_datetime(df['project finish'], utc = True) - pd.to_datetime(df['start date'], utc = True))*100

        df['progress'] = df['progress'].apply(lambda x: x if x >= 0 else 100)
        df['progress'] = df['progress'].apply(lambda x: x if x < 100 else 0)

        progress  =  df.groupby('project name')['progress'].mean()
        progress = list(progress.values)

        data = []
        for i, name in enumerate(names):
            project = {}
            project['name'] = name
            project['hours'] = hours[i]
            project['progress'] = progress[i]
            data.append(project)

        return data
    except:
        return []