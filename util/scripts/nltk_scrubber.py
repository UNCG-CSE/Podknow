from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import glob
import os
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#TODO Need to make this able to pull and push files to the Google Cloud.
#TODO Create some documentation for this program.
#TODO Find out how else we want to manipulate the text files other than stop words.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Chris\Desktop\My First Project-ebb89ddda148.json"

def main():

    stopWords = set(stopwords.words('english'))
    myPath = 'data/transcripts/gcsst/raw'
    print ("myPath", myPath)
    files = os.listdir(myPath) # Creates a list of all things in the directory. 
    print("files: ", files)

    saveLocation = 'data/transcripts/gcsst/scrubbed' #Relative path

    for eachFile in files:
        fileLocation = myPath+'/{0}'.format(eachFile) 
        # print("fileLocation: ", fileLocation)
        with open(fileLocation, 'r') as f:
            data = f.read()
            print("data: ", data)
            tokenizedWords = word_tokenize(data)
            print ("tokenizedWords: ", tokenizedWords)

        cleanWords = []
        for eachWord in tokenizedWords:
            if eachWord not in stopWords:
                cleanWords.append(eachWord)
        fileSaveName = saveLocation + '/{0}_scrubbed'.format(eachFile)
        with open(fileSaveName, 'wb') as f:
            pickle.dump(cleanWords, f)      # Serialize the object

if __name__ == '__main__':
    main()

#Load Pickle. Created the file as a python object so you dont have to read a csv everytime. 
# with open(fileSaveName, 'rb') as f:
#   data = pickle.load(f)
# print("data: ", data)