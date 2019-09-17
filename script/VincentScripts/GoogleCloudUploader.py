from gcloud import storage
from glob import glob
import os
import time
from multiprocessing import Process
#method for posting audio files onto google cloud
def upload(tup,bucket):
    time.sleep(2)
    print(tup)
    fileNameGoogleCloud = tup[0]
    pathName = tup[1]
    blob = bucket.blob(fileNameGoogleCloud)#save the disered name
    startingTime = time.time()
    print("\nStarting to upload " + fileNameGoogleCloud)
    with open(pathName,'rb') as f:
        blob.upload_from_file(f)#write the audio into google cloud
        f.close()
    endingTime = time.time()
    return pathName+"\nUploaded\nTimelaspe: "+str(endingTime-startingTime)

#creating threadpool for 4 workers

def printResult(result):
    print(result)

def start():
    #change this for the credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\vince\Desktop\\MyGoogleCloudService\\linear-equator-253121-2b458fe691e7.json"

    #instantiating a client with a corresponded bucket
    client = storage.Client()
    bucketName = input("Enter Your Bucket:")
    try:
        bucket = client.get_bucket(bucketName)
    except Exception as e:
        print(e)
    bucketPath = input("Enter Your disired Bucket Path(Format= \'[path]/\')\nIf no path, press Enter: ")
    #path for all the aduio files
    path = glob("../../data/audio/*.flac")
    #file name for google cloud
    fileNameGC = [bucketPath+name.replace("../../data/audio\\","") for name in path]

    #creating a tuple for the threadpool
    tuples = []
    for i in range(len(path)):
        tup =(fileNameGC[i],path[i])
        tuples.append(tup)
    for tup in tuples:
        printResult(upload(tup,bucket))
    print("All uploads are finished")

if __name__ == '__main__':
    start()
