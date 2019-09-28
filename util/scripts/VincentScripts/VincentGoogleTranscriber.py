import io 
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\vince\Desktop\\MyGoogleCloudService\\linear-equator-253121-2b458fe691e7.json"

podcastNames = glob.glob("../../data/audio/*.flac")

podcastTranscriptOutputPath = "../../data/transcripts/vince/raw/"
client = speech.SpeechClient()

config = speech.types.RecognitionConfig(
    encoding = speech.enums.RecognitionConfig.AudioEncoding.FLAC,
    language_code = 'en-US',
    sample_rate_hertz = 44100,
)

for fileName in podcastNames:
    with io.open(fileName,'rb') as stream:
        content = stream.read()
        audio = types.RecognitionAudio(content = content)
    