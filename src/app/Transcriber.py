# TODO: Transcriber is responsible for selecting an API or module to acquire the transcriptions of audio files.
from api.google import CloudSpeechToText as cstt
from api.apple import iTunesPodcastRSS as itp

print (cstt.CloudSpeechToText.fetchCloudSettings())
