"""
convert selfback into the same format as 
head actitracker_raw.txt
33,Jogging,49105962326000,-0.6946377,12.680544,0.50395286
33,Jogging,49106062271000,5.012288,11.264028,0.95342433
group by user_id, activity, timestamp is int, x,y,z

let us try the thigh first

selfBACK
format: https://rgu-repository.worktribe.com/output/246417
"""

import os
import glob
import pandas as pd
import numpy as np

sample = 5 # 100 hz to 20hz
activities = ['downstairs',  'jogging',   'sitting',  'standing',  'upstairs', 'walk_mod']
activity_index = {'jogging': 0, 'walk_mod': 1, 'upstairs': 2, 'downstairs': 3, 'sitting': 4, 'standing': 5}

files = glob.glob('selfBACK/t/*/*.csv')
files = sorted(files, key=lambda x: x.split('/')[-1] + str(activity_index.get(x.split('/')[2], 6)))

frames = []
for f in files:
    activity = f.split('/')[2]
    if not activity in activities:
        continue
    user_id = os.path.basename(f).replace('.csv', '').split('_')[0]

    columnNames = ['timestamp1', 'x-axis', 'y-axis', 'z-axis', 'activity']
    data = pd.read_csv(f, names=columnNames, na_values=',', header=None, skiprows=[0])
    data['user_id'] = user_id
    data['timestamp'] = pd.to_datetime(data['timestamp1'], infer_datetime_format=True, format="%Y-%m-%d %H:%M:%S").values.astype(np.int64)//1000
    frames.append(data.iloc[::sample, :])
result = pd.concat(frames)

columns = ['user_id','activity','timestamp','x-axis','y-axis','z-axis']
result = result[columns]

result.to_csv('selfBACK_t.csv', header=False, index=False, line_terminator='\n')