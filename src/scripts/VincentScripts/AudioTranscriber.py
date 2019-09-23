from glob import glob
from pydub import AudioSegment
import os
path = glob("..\\..\\data\\audio\\*.mp3")

print(path)

for src in path:
    left = src.replace(".mp3","_left.flac")
    right = src.replace(".mp3", "_right.flac")
    song = AudioSegment.from_mp3(src)
    tracks = song.split_to_mono()
    for i in range(len(tracks)):
        newsong = tracks[i].set_channels(1)
        print(newsong.channels)
        dis = ""
        if i == 0:
            newsong.export(left,format="flac")
            dis = left
        else:
            newsong.export(right,format="flac")
            dis = right
            os.remove(src)    
        print(dis+"\nCompleted")
