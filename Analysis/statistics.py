import numpy as np
from glob import glob
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
import matplotlib
from math import pow, sqrt, ceil
from collections import OrderedDict

from Analysis.expert import ProjectType, DatasetType

class Statistics:
    
    def __init__(self, participants):

        self.participants = participants

    def calc_statistics(self):

        data = []

        for participant in self.participants:

            ground_truth = [temp for temp in self.participants if temp.ProjectType == ProjectType.GroundTruth and temp.DatasetType == participant.DatasetType][0]

            miou = participant.calc_MIoU(ground_truth)
            data.append([participant.expert, participant.DatasetType, participant.ProjectType ,participant.total_annotations, participant.mean_seconds_to_label, miou])

        return pd.DataFrame(data, columns=['Name', 'Dataset', 'ProjectType', 'Nr. Annotations', 'Seconds', 'mIoU'])


    def get_annotations(self, image_name):

        data = []

        for participant in self.participants:
            if image_name not in participant.Images:
                continue
            image = participant.Images[image_name]

            annotations = image.Annotations

            for anno in annotations:
                data.append([participant.expert, anno.Vector, anno.Label, participant.ProjectType])

        return pd.DataFrame(data, columns=['Name', 'Vector', 'Label', 'ProjectType'])
        





