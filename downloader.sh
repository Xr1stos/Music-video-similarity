#!/bin/bash

#----USAGE:  ./downloader.sh evaluation_set.csv ./eval_videos/ ./eval_music/   ----


#reads from a csv with columns: url,song_name,artist,genre

#downloads videos in .mp4 format (640 x 360) and saves in a given videos folder
#also transforms videos to wavs (16000) and saves them in a given music folder

echo -e "-----USAGE:  ./downloader.sh dataset_path.csv ./save_videos_path/ ./save_music_path/ \n" 

echo
pip install --upgrade youtube_dl


input=$1

mkdir -p $3

# Set "," as the field separator using $IFS 
# and read line by line using while read combo 
while IFS=',' read -r f1 f2 f3 f4 
do 
  echo "$f2"
   youtube-dl -f 18 --default-search "ytsearch" -o "$2$f2.%(ext)s" "$f1"
   ffmpeg -i "$2$f2.mp4"  -ar 16000 "$3$f2.wav"

done < "$input"

