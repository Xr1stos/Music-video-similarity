# -*- coding: utf-8 -*-
"""
Creates a csv with video features from videos in a path.
Python 3
"""
#libraries
import numpy as np
import pandas as pd
import glob
import video_features as vf
from tqdm import tqdm
import re
import os


def video_feature_dataframe(path, folder_name, features, width=300, step_size=0.5):
    
    """
    
    Returns a dataframe with song names and video features for all files in a folder 
    Input: path to folder, folder name,features to extract in a list format,
           resize width and time step
    Output: a pandas data frame ready to be written to a csv file
    """

    
    # read video files in a directory
    files = glob.glob(path)
    
    # construct the extractor
    v = vf.VideoFeatureExtractor(features, resize_width=width, step =step_size)
    
    # use the first file to get dimensions and create a base np array
    # extract features
    features, times, labels = v.extract_features(files[0])
    
    # get the mean for each feature
    features_mean_base=np.mean(features, axis=0)
    
    # create a base numpy array to append the rest file results
    features_mean_base = np.reshape(features_mean_base, (1, features_mean_base.shape[0]))
    
    # save the names of the videos in a list
    vid_names = [re.findall("(?<="+folder_name+"/)(.*)(?=.mp4)", files[0])[0]]
    
    # del the first video used to construct the base numpy array
    del files[0]
    
    if len(files)>0:
        for file in tqdm(files): 

            # extract features from every file and prepare them
            features, times, labels = v.extract_features(file)
            features_mean = np.mean(features, axis=0)
            features_mean = np.reshape(features_mean, (1, features_mean.shape[0]))
            
            # stack the features of every video in a numpy array
            features_mean_base=np.vstack((features_mean_base, features_mean))

            vid_names.append(re.findall("(?<="+folder_name+"/)(.*)(?=.mp4)", file)[0])
    
    
    # create a dataframe with video name
    names = pd.DataFrame(vid_names, columns=["name"])
    # convert the features numpy array to a pandas dataframe
    dframe=pd.DataFrame(features_mean_base, columns=labels)
    # concatenate the above to dataframes to create the final dataframe to be exported
    fin=pd.concat([names, dframe], axis=1)
    
    return fin    


"""----------------main-------------------------"""

if __name__ == '__main__':

    # set path to output csv
    rpath = input("type the output csv name: ")
    
    # read the input path
    input_path = input("type the path to the folder containing the videos: ")
    while os.path.exists(input_path) is False:
        input_path = input("path doesn't exist, retype path: ")

    folder = os.path.basename(os.path.normpath(input_path))

    p = video_feature_dataframe(input_path+"*.mp4", folder, ["colors", "lbps"])
    
    # write the results for every video
    p.to_csv(rpath, sep=',', index=False)
