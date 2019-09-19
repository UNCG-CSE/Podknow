from glob import glob
from pydub import AudioSegment
import os
path = glob("..\\..\\data\\audio\\*.mp3")

print(path)

for src in path:
    dis = src.replace(".mp3",".flac")
    song = AudioSegment.from_mp3(src)
    print(song.channels)
    newsong = song.set_channels(1)
    print(newsong.channels)
    newsong.export(dis,format="flac")
    os.remove(src)    
    print(dis+"\nCompleted")
