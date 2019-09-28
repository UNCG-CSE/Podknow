# TODO: Transcriber is responsible for selecting an API or module to acquire the transcriptions of audio files.
from controllers.api.google import CloudSpeechToText as cstt
from controllers.api.apple import iTunesPodcastRSS as itp

print (cstt.fetchCloudSettings())
