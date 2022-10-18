# -*- coding: utf-8 -*-

"""
Compares given video clips to those in the database and returns similar ones .
python 3
"""

# libraries
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
import sys


# read the database datasets
db_video = pd.read_csv('training_data/video_features.csv', sep=',')
db_music = pd.read_csv('training_data/music_features.csv', sep=',')
db_spotify = pd.read_csv("training_data/spotify_features.csv").drop(["mode", "duration_ms"], axis=1)
db_files = pd.read_csv("training_data/data.csv", sep=",", header=None, names=["url", "song", "artist", "genre"])

# join video and music features tables on song name
db = pd.merge(db_video, db_music)

# save the normalization max values in order to apply the same normalization to the evaluation data too
normalizer = db.iloc[:, 1:].values.max(axis=0)
spoti_normalizer = db_spotify.iloc[:, 1:].abs().values.max(axis=0)

# normalize the data per column
db_normed = db.iloc[:,1:].values /normalizer
db.iloc[:, 1:] = db_normed

spoti_normed = db_spotify.iloc[:, 1:].values /spoti_normalizer
db_spotify.iloc[:, 1:] = spoti_normed

# merge all features
all_feats = pd.merge(db, db_spotify)

"""----------------main-------------------------"""

if __name__ == '__main__':
    
    # number of similar videos to retrieve
    N = int(input("select the number of similar videos you want: "))
    
    while N <= 0 or N > 50:
        N = int(input("N must be between 1 and 50, retype N: "))

    # the path to the evaluation dataset
    d = input("type the dataset csv path: ")
    while os.path.exists(d) is False:
        d = input("path doesn't exist, retype path: ")
        
    # the path to evaluation music features
    m = input("type the music features csv path: ")
    while os.path.exists(m) is False:
        m = input("path doesn't exist, retype path: ")
        
    # the path to evaluation video features
    v = input("type the video features csv path: ")
    while os.path.exists(v) is False:
        v = input("path doesn't exist, retype path: ")
    
    # the path to evaluation spotify features
    s = input("type the spotify features csv path: ")
    while os.path.exists(s) is False:
        s = input("path doesn't exist, retype path: ")
    
    # read the evaluation data
    eval_data = pd.read_csv(d, sep=",", header=None, names=["url", "song", "artist", "genre"])
    eval_m = pd.read_csv(m, sep=",")
    eval_v = pd.read_csv(v, sep=",")
    eval_spotify = pd.read_csv(s, sep=",").drop(["mode", "duration_ms"], axis=1)
    eval_db = pd.merge(eval_v, eval_m)

    # normalize the datasets per column
    eval_normed = eval_db.iloc[:, 1:].values /normalizer
    eval_db.iloc[:, 1:] = eval_normed

    eval_spoti_normed = eval_spotify.iloc[:, 1:].values /spoti_normalizer
    eval_spotify.iloc[:, 1:]= eval_spoti_normed
    
    # merge all eval features
    all_eval_feats = pd.merge(eval_db, eval_spotify)

    # similarity matix based on video and audio
    a = cosine_similarity(eval_db.iloc[:, 1:].values, db.iloc[:, 1:].values)
    #  matrix based on spotify
    b = cosine_similarity(eval_spotify.iloc[:, 1:].values,db_spotify.iloc[:, 1:].values)
    # similarity matrix based on all features
    c = cosine_similarity(all_eval_feats.iloc[:, 1:].values, all_feats.iloc[:, 1:].values)
    
    # remove the above line to send output to a file
    sys.stdout = open('./RESULTS', 'w')

    print("\nRESULTS:\n")
    for i in range(a.shape[0]):
        print("\n"+str(i+1))
        print("\n---> "+eval_db["name"][i]+"   " +
               eval_data["url"].loc[eval_data['song'] == eval_db["name"][i]].iloc[0] +
              " <---\n\n*Similarity based on audio and video features:")
        for j in a[i].argsort()[-N:][::-1]:
            print("|- "+db["name"][j]+"  Score: " + str(round(a[i][j], 6))+"   " +
                  db_files["url"].loc[db_files['song'] == db["name"][j]].iloc[0])
        print("\n*Similarity based on spotify features:")
        for k in b[i].argsort()[-N:][::-1]:
            print("|- "+db["name"][k]+"  Score: " + str(round(b[i][k], 6))+"   " +
                  db_files["url"].loc[db_files['song'] == db["name"][k]].iloc[0])
        print("\n*Similarity based on all features:")
        for l in c[i].argsort()[-N:][::-1]:
            print("|- "+db["name"][l]+"  Score: " + str(round(c[i][l], 6))+"   " +
                  db_files["url"].loc[db_files['song'] == db["name"][l]].iloc[0])


