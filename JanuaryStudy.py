from glob import glob
from pathlib import Path
from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pow, sqrt, ceil, cos, sin, pi


from sklearn.neighbors import KDTree
from PIL import Image as PILImage
import matplotlib.patches as patches
from collections import OrderedDict

from Analysis.annotations import Annotation
from Analysis.image import Image
from Analysis.expert import Expert, DatasetType, ProjectType
from Analysis.statistics import Statistics

from utils import *



path = Path("Results/*/*")
files = glob(str(path)+"/Participants/*.txt")

users_first_round = []

for file_name in files:
    participant = "Participant_" + Path(file_name).stem.split("_")[-1]
    dataset_type = DatasetType.Asthma
    project_type = ProjectType.Annotation if "FirstRound" in file_name else ProjectType.ExpertAlgorithm
    
    if "EIPH" in file_name:
        dataset_type = DatasetType.EIPH_Exact
    elif "Mitosen" in file_name:
        dataset_type = DatasetType.MitoticFigure
    
    
    expert = Expert(participant, BBType.Detected, dataset_type, project_type)
    expert.add_file(file_name)

    users_first_round.append(expert)


files_gt = glob(str(path)+"/GT/ground truth.txt")

gt_results = []
for file_name in files_gt:
    
    participant = Path(file_name).stem.split("_")[-1]
    dataset_type = DatasetType.Asthma
    project_type = ProjectType.GroundTruth
    
    if "EIPH" in file_name:
        dataset_type = DatasetType.EIPH_Exact
    elif "Mitosen" in file_name:
        dataset_type = DatasetType.MitoticFigure
        
    gt = Expert(participant, BBType.GroundTruth, dataset_type, project_type)
    gt.add_file(file_name)

    users_first_round.append(gt)


statistics = Statistics(users_first_round)
annotations = statistics.get_annotations()

annotations.to_pickle("StudyAnnotations.pkl")

mitotic_figures_algo = annotations[(annotations['ProjectType']=='ExpertAlgorithm') & (annotations['DatasetType']=='MitoticFigure')]
for fileName in mitotic_figures_algo.FileName.unique():
    file_annos = mitotic_figures_algo[mitotic_figures_algo['FileName']==fileName]


    centers = []
    results = {}
    for _, name, vector, label, _, _ in file_annos.values.tolist():
        center = (vector[0] + (vector[2] - vector[0]) / 2, vector[1] + (vector[3] - vector[1]) / 2)

        if len(centers) > 0:
            tree = KDTree(centers)
            index_per_point = tree.query_radius([center], r=25)[0]

            if len(index_per_point) == 0:
                results["{}:{}".format(int(center[0]), int(center[1]))] = {'Vector': vector, 'Label': label, 'Users': [name]}
                centers.append(center)
            else:
                center = centers[index_per_point[0]]
                results["{}:{}".format(int(center[0]), int(center[1]))]['Users'].append(name)
        else:
            results["{}:{}".format(int(center[0]), int(center[1]))] = {'Vector': vector, 'Label': label, 'Users': [name]}
            centers.append(center)

    print()
