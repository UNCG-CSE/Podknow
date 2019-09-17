# from glob import glob
# from pydub import AudioSegment
# import os
# path = glob("..\\data\\audio\\*.mp3")

# for src in path:
#     dis = src.replace(".mp3",".flac")
#     song = AudioSegment.from_mp3(src)
#     song.set_channels(1)
#     song.export(dis,format="flac")
#     os.remove(src)    
#     print(dis+"\nCompleted")
import google
print(google.__path__)