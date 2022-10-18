# -*- coding: utf-8 -*-

"""
Creates a csv with audio features for songs from spotify.
python 2
"""

#libraries
import spotipy.oauth2
import csv
import pandas as pd
import os 

def find_song_id(song_name,artist):

    """ 
    Finds the song's spotify id in order to be able to search
    for features with the api.
    Input: the song's name and artist
    Output: the song_id

    """
    
    query="track:"+song_name+" artist:"+artist

    results = spotify.search(q=query, type='track')
    
    dict_a=results["tracks"]
    dict_b=dict_a["items"]
    song_id=dict_b[0]["id"]
    
    return song_id


def get_metadata(sid,song_name,feats):

    """
    Request audio features for a given id from the api.
    Input: the song's spotify id, the song's name and the 
           features to extract
    Output: a list starting with the song name followed by the 
            features

    """

    metadata=spotify.audio_features([sid])
   
    metadata_list=[song_name.replace(" ", "_")]
    
    for i in feats:
        metadata_list.append(metadata[0][i])
        
    return metadata_list
   
print "--Make sure to insert spotify credentials before using-- \n"
# user spotify credentials for authentication, REPLACE A and B with yout spotify credentials    
credentials = spotipy.oauth2.SpotifyClientCredentials(client_id='A',
                           client_secret='B')
spotify = spotipy.Spotify(client_credentials_manager=credentials)


# features that are extracted
spoti_feats=['energy','liveness','tempo','speechiness','acousticness','instrumentalness',
             'time_signature','danceability','key','duration_ms','loudness','valence','mode']

#read  path to output csv
rpath=raw_input("type the output csv name: ")
    
#header for the output csv
header="name,"+",".join(spoti_feats)

#write header to file
with open(rpath, 'w') as results:
    results.write(header+'\n')

"""----------------main-------------------------"""

if __name__ == '__main__':

  
    #user input
    data_file=raw_input("type the input csv path: ") #evaluation_set.csv
    while os.path.exists(data_file) is False:
            data_file=raw_input("path doesn't exist, retype path: ")

    
    #read dataset of type url,song name, artist,type
    df = pd.read_csv(data_file, delimiter=',',header=None)

    #replace _ with space in song name and artist
    df[1]=df[1].str.replace('_', ' ')
    df[2]=df[2].str.replace('_', ' ')
    
    
    for index, row in df.iterrows():
        print row[1], row[2]
	try:
            song_id=find_song_id(row[1],row[2])
            metadata=get_metadata(song_id,row[1],spoti_feats)
        except:
            print "---ERROR: check artist or song name---"
            break
        
        with open(rpath, 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(metadata)
        
        
