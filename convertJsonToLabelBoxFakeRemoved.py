from glob import glob
from pathlib import Path
from datetime import datetime
import json
import numpy as np


fake_path = "Results/Mitosen/FirstRound/GT/removedMitoticFigures.json"
group_0 = []
group_1 = []
group_2 = []

data = None
with open(fake_path) as json_file:
    data = json.load(json_file)

for annotation in data:

    file_name = annotation['file']
    group = annotation['group']

    bbox = (annotation['x1'] - 25,  annotation['y1'] - 25, annotation['x1'] + 25,  annotation['y1'] + 25)
    box_dict = json.dumps({"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3]})

    row = "{0}|{1}|{2}||2019-12-18 12:46:46.366235||2020-01-12 10:28:28.279911||False|10000|10000".format(file_name, "mitotic figure", box_dict) + "\n"

    if group == 0:
        group_0.append(row)
    elif group == 1:
        group_1.append(row)
    else:
        group_2.append(row)

with open('Results//Mitosen//FirstRound/GT//RemovedMitoticFigures_G0.txt', 'w') as f:
    f.writelines(group_0)

with open('Results//Mitosen//FirstRound/GT//RemovedMitoticFigures_G1.txt', 'w') as f:
    f.writelines(group_1)

with open('Results//Mitosen//FirstRound/GT//RemovedMitoticFigures_G2.txt', 'w') as f:
    f.writelines(group_2)

