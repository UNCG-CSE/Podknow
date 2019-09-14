from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Jeremy\Downloads\Audio to text-b06233f3da38.json"

client = speech_v1.SpeechClient()

podcastName = 'sword and scale'

storage_uri = 'gs://audio_files47/Podcast mp3s/' + podcastName + '.flac'

sample_rate_hertz = 44100

language_code = "en-US"

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
config = {
    "sample_rate_hertz": sample_rate_hertz,
    "language_code": language_code,
    "encoding": encoding,
}
audio = {"uri": storage_uri}

operation = client.long_running_recognize(config, audio)

print(u"Waiting for operation to complete...")
response = operation.result()

for result in response.results:
    # First alternative is the most probable result
    alternative = result.alternatives[0]
    print(u"{}".format(alternative.transcript))

    f = open(podcastName + ".txt", "a+")
    f.write((u"{}".format(alternative.transcript)))
    f.close()
