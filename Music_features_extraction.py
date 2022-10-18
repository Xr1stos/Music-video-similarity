# -*- coding: utf-8 -*-

"""
Creates a csv with music features from videos in a folder.
python 3

"""

#libraries
from pyAudioAnalysis.audioFeatureExtraction import dirWavFeatureExtraction as dW
import pandas as pd
import re
import os


def getname(dwobject):
    """
    
    Corrects the song names in the dwobject
    Input: dwobject
    Output: dwobject with correct name   
    
    """

    j = 0
    for i in dwobject[1]:
        dwobject[1][j]=(re.findall("(?<=music/)(.*)(?=.wav)", dwobject[1][j]))
        j += 1
    
    return dwobject


def produce_final_dataframe(dwobject):
    """
    
    Makes a final dataframe with song names and feature names 
    Input: dwobject
    Output: a pandas data frame ready to be written to a csv file
    """

    df = pd.DataFrame(dwobject[0], columns=dwobject[2], index=range(0, dwobject[0].shape[0]))
    nm= pd.DataFrame(dwobject[1], columns=["name"], index=range(0, dwobject[0].shape[0]))
    fin=pd.concat([nm, df], axis=1)
    
    return fin


"""----------------main-------------------------"""

if __name__ == '__main__':
    
    # set path to output csv
    rpath = input("type the output csv name: ")
    
    # read the input path
    data_path=input("type the path to the folder containing the music: ") 
    while os.path.exists(data_path) is False:
        data_path=input("path doesn't exist, retype path: ")

    # extract features for all songs in a folder

    f1 = dW(data_path, 1, 1, 0.1, 0.1)
    
    # get the correct song names
    f1 = getname(f1)
    
    # create the final dataframe
    dataframe = produce_final_dataframe(f1)
    
    # write to csv
    dataframe.to_csv(rpath, sep=',', index=False)

