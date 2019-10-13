from api.google import CloudSpeechToText as cstt

transcriptionMethodList = ["google_cloud", "sphinx"]

def transcribe(method, targetAudioPath, resultPath):

    # Make sure resultPath is OK and transcription doesn't already exist.
    if method == transcriptionMethodList[0]:
        print("Google cloud transcription")
        # Make sure targetAudioPath is a valid GC path.
        # Get cloud settings.
        # Transcribe.
    elif method == transcriptionMethodList[1]:
        print("Sphinx Transcription")
        # Make sure targetAudioPath is valid local file path to an audio file.
        # Transcribe
    else:
        raise Exception("Invalid transcription method.\nAvailable methods:" + str(transcriptionMethodList))

    # Return a statistics report. ConfScore, PodcastAudioMinutes, TranscriptionRunTime

def transcribeSphinx(targetAudioPath, resultPath):
    print("Not implemented")

def transcribeGoogleCloud(targetAudioPath, resultPath):
    print("Not implemented")


def report(content):
    print("not implemented")