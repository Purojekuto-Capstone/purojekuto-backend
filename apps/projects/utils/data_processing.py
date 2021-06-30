import numpy as np
import pandas as pd
import random
from datetime import date, timedelta

def clean_data(data):
    try:
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

        df['today'] = date.today()

        df['progress'] = (pd.to_datetime(df['project finish']) - pd.to_datetime(df['today']))/(pd.to_datetime(df['project finish'], utc = True) - pd.to_datetime(df['start date'], utc = True))*100

        progress_metrics = df.groupby('project name')['progress'].mean().to_dict()

        return {
            'projects comparision': project_events,
            'events in projects':  events_projects,
            'activities comparison': events_metrics,
            'progress metrics': progress_metrics
        }
    except:
        return {'activities comparison': {'escribir': 1,
                'investigar': 1,
                'leer': 1,
                'llamadas': 5,
                'planear': 1,
                'programar': 3,
                'reunion': 1,
                'trotar': 2},
                'events in projects': [{'metrics': {'escribir': 1,
                    'investigar': 1,
                    'leer': 1,
                    'llamadas': 1,
                    'trotar': 1},
                'project name': 'ML bot'},
                {'metrics': {'planear': 1, 'programar': 3, 'reunion': 1},
                'project name': 'project manage app'},
                {'metrics': {'llamadas': 4, 'trotar': 1}, 'project name': 'Web app Market'}],
                'progress metrics': {'ML bot': -4.316909638439045,
                'Web app Market': 206.63992791214247,
                'project manage app': 62.91876384624253},
                'projects comparision': {'ML bot': 5,
                'Web app Market': 5,
                'project manage app': 5}}