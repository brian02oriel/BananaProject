import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from LocalBinaryPattern import LocalBinaryPatterns
from joblib import dump
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score, roc_curve
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score

def creating_dataset(data_path, label, Training_Data, Labels):
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    
    # Preparing the radius and the no. of points of the LBP descriptor
    radius = 3
    no_points = 8 * radius

    desc = LocalBinaryPatterns(no_points, radius)

    for files in onlyfiles:
        image_path = data_path + files
        images = cv2.imread(image_path, 0)
        images = cv2.resize(images, (150,150))
        hist = desc.describe(images)
        Training_Data.append(hist)
        Labels.append(label)
    return Training_Data, Labels

Training_Data, Labels = [], []
Training_Data, Labels = creating_dataset('../Captured images/Third Try Dataset (green segment)/', 1, Training_Data, Labels)
Training_Data, Labels = creating_dataset('../Captured images/Second Try Dataset (green banana)/', 1, Training_Data, Labels)
Training_Data, Labels = creating_dataset('../Captured images/Fifth Try (green segment without ventilation)/', 1, Training_Data, Labels)
Training_Data, Labels = creating_dataset('./Negatives/', 0, Training_Data, Labels)

print(len(Training_Data))
print(len(Labels))