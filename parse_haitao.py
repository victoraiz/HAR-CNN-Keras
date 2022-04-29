"""
convert haitao into the same format as 
head actitracker_raw.txt
33,Jogging,49105962326000,-0.6946377,12.680544,0.50395286
33,Jogging,49106062271000,5.012288,11.264028,0.95342433
group by user_id, activity, timestamp is int, x,y,z

let us try the thigh first

selfBACK
format: https://rgu-repository.worktribe.com/output/246417
"""

import os, sys
import glob
import pandas as pd
import numpy as np
import re

output = sys.argv[1] # 'selfBACK_t.csv'
input_glob = sys.argv[2] # 'haitao2/*.txt'
sample = 1 # keep 100 hz
activities = ['downstairs',  'jogging',   'sitting',  'standing',  'upstairs', 'walking',]
activity_index = {'jogging': 0, 'walking': 1, 'upstairs': 2, 'downstairs': 3, 'sitting': 4, 'standing': 5, 'lying': 8}

files = glob.glob(input_glob)
files_activity = {}
pattern = r'^([a-zA-Z]+).*$'
for f in files:
    activity = re.search(pattern, os.path.basename(f)).group(1).lower()
    files_activity[f] = activity
files = sorted(files, key=lambda x: str(activity_index.get(files_activity[x], 9)))

frames = []
for f in files:
    activity = files_activity[f]
    print(f, activity)
    if not activity in activities:
        continue
    user_id = "1"

    columnNames = ['timestamp', 'x-axis', 'y-axis', 'z-axis', 'x1', 'y1', 'z1']
    data = pd.read_csv(f, names=columnNames, na_values=',', header=None, skiprows=None, delim_whitespace=True)
    data['user_id'] = user_id
    data['activity'] = activity
    data['x-axis'] = data['x-axis'] * 0.244 / 1000 * 9.81
    data['y-axis'] = data['y-axis'] * 0.244 / 1000 * 9.81
    data['z-axis'] = data['z-axis'] * 0.244 / 1000 * 9.81
    data = data[data.index % 5 != 0]
    frames.append(data)
result = pd.concat(frames)

columns = ['user_id','activity','timestamp','x-axis','y-axis','z-axis']
result = result[columns]

result.to_csv(output, header=False, index=False, line_terminator='\n')