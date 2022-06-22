import os
import sys
import pytube
import subprocess
import pychorus
import time

os.chdir(os.path.dirname(sys.argv[0]))

playlist = pytube.Playlist('https://www.youtube.com/playlist?list=PLwxh-CuoGZ_1NgdfTPjTkWAmG-g8DNEGv')
for url in playlist.video_urls:
    video = pytube.YouTube(url)
    video = video.streams.get_highest_resolution().download('download')

files = os.listdir('download')
i = 0

for file in files:
    os.rename('download/'+file, 'download/test_'+str(i)+'.mp4')
    i = i+1

for k in range(i):
    command = "ffmpeg -loglevel quiet -i ./download/"+'test_'+str(k)+".mp4 -ab 160k -ac 1 -ar 22050 -vn ./download/"+'test_'+str(k)+".wav"
    subprocess.call(command, shell=True)
    chroma = pychorus.create_chroma('download/test_'+str(k)+'.wav')
    chorus_start_sec = pychorus.find_chorus(chroma[0], chroma[2], chroma[3], 15)
    if chorus_start_sec == None:
        chorus_start_sec = pychorus.find_chorus(chroma[0], chroma[2], chroma[3], 10)
    if chorus_start_sec == None:
        chorus_start_sec = pychorus.find_chorus(chroma[0], chroma[2], chroma[3], 5)
    if chorus_start_sec == None:
        chorus_start_sec = pychorus.find_chorus(chroma[0], chroma[2], chroma[3], 1)
    start = time.strftime('%H:%M:%S', time.gmtime(chorus_start_sec))
    end = time.strftime('%H:%M:%S', time.gmtime(chorus_start_sec+30))
    command = "ffmpeg -loglevel quiet -ss "+start+" -to "+end+" -i ./download/"+'test_'+str(k)+".wav -c copy ./download/"+'jpop.'+str(k)+".wav"
    subprocess.call(command, shell=True)

files = os.listdir('download')
to_del = [file for file in files if file.endswith(".mp4") or file.startswith("test")]
for file in to_del:
    os.remove(os.path.join('download', file))
