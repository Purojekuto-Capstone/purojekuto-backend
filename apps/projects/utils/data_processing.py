import numpy as np
import pandas as pd
import random
from datetime import date, timedelta

def clean_data(data):

    df = pd.DataFrame(data)
    df['one'] = 1

    project_events = df.groupby('project name')['one'].count().to_dict()

    cols = list(df['project name'].value_counts().index)

    events_projects = []
    for col in cols:
        event_project = dict()
        event_project['project name'] = col
        event_project['metrics'] = df[df['project name'] == col]['activity category'].value_counts().to_dict()
        events_projects.append(event_project)

    events_metrics = df.groupby('activity category')['one'].count().to_dict()
    print(events_metrics)
    df['today'] = date.today()

    df['progress'] = (pd.to_datetime(df['project finish']) - pd.to_datetime(df['today']))/(pd.to_datetime(df['project finish'], utc = True) - pd.to_datetime(df['start date'], utc = True))*100

    progress_metrics = df.groupby('project name')['progress'].mean().to_dict()

    return {
        'projects comparision': project_events,
        'events in projects':  events_projects,
        'activities comparison': events_metrics,
        'progress metrics': progress_metrics
    }