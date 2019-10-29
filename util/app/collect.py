import sys
import pandas as pd
import controllers.Transcriber as tsbr
import controllers.PodcastListProducer as plp

miscArgList = ["help"]
typeList = ["latest"]
trendingSourceList = ["itunes"]
transcribeList = ["google_cloud", "sphinx"]

expectedArgsTemplate = ("(type):\t\t\t<latest>\n"
"(source):\t\t<itunes>\n"
"(transcribe_method):\t<google_cloud\sphinx>\n"
)
expectedArgsExample = "collect -trending -itunes -sphinx"
expectedArgCount = 4

currentlyDownloading = 0
downloadAudioCount = 0
downloadConcurrencyMax = 3
downloadAttempts = 0
downloadAttemptMax = 200

def areArgsValid(args):
    return args[1].lower() in typeList and args[2].lower() in trendingSourceList and args[3].lower() in transcribeList

def validateArguments():
    expectedArgCount = 4
    args = sys.argv
    argsCount = len(args)
    if argsCount < 2:
        print("Error: No arguments given. Type \"collect.py help\" for template")
        return False
    elif (argsCount is 2 and args[1].lower() in miscArgList) or (argsCount == expectedArgCount and areArgsValid(args)):
        return True
    else:
        print("Error: Requires the expected arguments\n" + expectedArgsTemplate)
        return False

def helpCmd():
    print("Expected arguments:\n" + expectedArgsExample + "Example Useage:\n" + expectedArgsExample)

def transcribe():
    print("Not implemented")

def downloadTranscribeProcess():
    print("Not implemented")

def collectionProcess():
    
    df_podcasts = pd.DataFrame()

    # Get list of podcasts


    # Download audio from webpages. 3 at a time.
    # once finished downloading

    print("Not implemented")


def executeArgs():
    args = sys.argv
    if args[1] == (miscArgList[0]):
        print("Help")
        helpCmd()
    else:
        print("Collection process")
        collectionProcess()
    
    sys.exit(0)


def main():
    argsValid = validateArguments()

    if argsValid:
        print("Parsing and executing arguments...")
        executeArgs()
    else:
        print("Application not executed.")

main()