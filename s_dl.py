import urllib.request
import urllib.parse
import re
import subprocess #for running a bash command within the python script
import sys
import glob
import os
from mutagen.easyid3 import EasyID3 #for changing the tags

song= sys.argv[1] + " " + sys.argv[2] #storing the user entry

query_string = urllib.parse.urlencode({"search_query" : song}) #creating the youtube search query
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

link_to_video= "http://www.youtube.com/watch?v=" + search_results[0]
subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--output", "%(uploader)s%(title)s.%(ext)s", link_to_video]) #downloading it through youtube-dl


#I could not get any other way of getting the path of the downloaded  filename  to work properly, so I thought of grabbing the last created file using glob
newest = max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime) #getting the newest file that was created

audio = EasyID3(newest) #changing the tags
audio["title"] = sys.argv[1]
audio["artist"] = sys.argv[2]
audio["album"] = sys.argv[3]
audio.save()

os.rename(newest, sys.argv[1]+".mp3") #changing the file name

#THINGS TO BE DONE
'''
0. Convert it to a shell script
1. Get album cover art
2. Refactor the code to get more accurate search results
3. Make it work faster
4. send the downloaded file to your android device using Telegram API
'''







