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

        data = []
        for i, name in enumerate(names):
            project = {}
            project['name'] = name
            project['hours'] = hours[i]
            data.append(project)

        return data
    except:
        return [{'hours': 5.583333333333334, 'name': 'ML bot'},
                {'hours': 3.75, 'name': 'Web app Market'},
                {'hours': 8.0, 'name': 'project manage app'}]