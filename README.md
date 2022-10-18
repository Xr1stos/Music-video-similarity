# Music video similarity
Author: Christos Platias

Predicting video clip similarity using  image and audio features, as well as  audio features from spotify.


# File descriptions:

**Database [training_data]:**  
       data.csv  
       video_features.csv  
       music_features.csv  
       spotify_features.csv  

   Notes:  
	  i  ) You can add files to the data.csv to enlarge the database.  
	  ii ) These filenames are used by default by the functions. **DO NOT**  
      	       change these names.  
	  iii) These files must be in the same folder as the functions.


**Evaluation - prediction [evaluation_data]:**  
       evaluation_dataset.csv  
       eval_video_features.csv  
       eval_music_features.csv  
       eval_spotify_features.csv  

   Notes:  
	  i) These files are for predictions and can have any name the user wants.  


**Functions:**  
       downloader.sh  
       Video_features_extraction.py  
       Music_features_extraction.py  
       Spotify_features_extraction.py  
       Similarity_calculator.py  
	
       video_features.py --- by tyiannak  
       visual_features.py --- by tyiannak  

   
# Prerequisites: 

**Python 3 with:**  

cv2  
csv  
glob  
numpy  
pandas  
pickle  
pyaudioanalysis  
scipy  
skimage  
sklearn  
tqdm  

**Python 2 with:**  

csv  
pandas  
spotipy  


# HOW TO USE:

Dowload the folder and inside the folder do the following:  


1) Create a **DATASET.csv** with the following info:

    
   url,song_name,song_artist,genre	#genre can be left blank




2) Call the **downloader.sh** , which downloads and saves the videos and extracts the audio.


   e.g.:  ./downloader.sh DATASET.csv ./path_to_save_videos/ ./path_to_save_music/

	
   Output: A folder containing the video files and a folder containing the audio files.




3) Call the **Spotify_features_extraction.py**	--PYTHON 2--


   Notes:  
	  i ) Don't forget to insert your spotify credentials  
       	  ii) If info for a song name or an artist can't be downloaded  
      	      try checking spotify's spelling in their site or avoid ' "  
      	      e.g. dont instead of don't. 

   Output: A csv file with the spotify features.


4) Call the  **Music_features_extraction.py**	--PYTHON 3--

   Output: A csv file with the music features.





5) Call the **Video_features_extraction.py**	--PYTHON 3--

   Output: A csv file with the video features.


6) Call the **Similarity_calculator.py**	--PYTHON 3--

   Notes:  
   	  i ) If you want to save the output to a log file uncomment the  
	      appropriate line inside the main function of the script.  
	  ii) You can select the number of similar objects per request,  
   	      upper limit was set to 50 but can be raised from the inside.

   Output: Prints the song names and urls of similar videos.


   **example run:**  
   python Similarity_calculator.py  
   select the number of similar videos you want: *2*  
   type the dataset csv path: *evaluation_dataset.csv*  
   type the music features csv path: *eval_music_features.csv*  
   type the video features csv path: *eval_video_features.csv*  
   type the spotify features csv path: *eval_spotify_features.csv*  






