### Initial Prototype
 **Data Collection, 9/11 to 9/17**

**Vincent Yang**
Tasks: Download top 200 podcast list on itunes, created tools to convert mp3 files into flac files, and created tools to upload audio files onto the google cloud bucket.
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We acquired the **names** and **ids** of the top 200 trending podcasts from the [**iTunes RSS API**](https://rss.itunes.apple.com/en-us) into a csv file on 9/11/19. To make processing easier on the group, each member assumed partial responsibility for acquiring the transcriptions of the 200 podcasts.
 Turning .mp3 files into .flac files using pydub, essentially convert the stereo .mp3 files into a mono .flac files. Once the .flac files are created, the old .mp3 files will be deleted.
 Created a python script to upload all the .flac files onto the google cloud, so Jeremy's script can utilize the speech to text api.

**Jeremy Hudson**
Tasks: Speech to Text API
Since many podcasts were not accompanied by official transcripts, I looked into several methods to procure transcripts for podcasts that didn’t have any. These included finding the automatically generated YouTube transcripts, having speech recognition done in real time by having the podcast play in the background while being transcribed by Google Docs speech recognition, and our final solution that we intend to use from now on: the Google Speech to Text API. We settled on this API because it supported Python, and given the work that many of my other teammates are doing it would be possible to use it as a part of a fully automated system that acquires Podcast IDs, downloads them, converts them to a necessary audio file type (in our case .FLAC) and automatically writes the resulting transcript from the API to a text file. To set the API up I had to pip install the Google Cloud module, which I imported to my initial GoogleRequest.py file. For our initial test run, I manually converted all podcast mp3 files to FLAC files for API transcription. After this I setup my Google Cloud storage and uploaded the converted FLAC files to my cloud storage and successfully transcribed the bulk of my assigned thirty-three podcasts this way.

**Jamie Weathers**
Tasks: Web Scraping, Optimization, initial Github organization and management
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Each **iTunes ID** for the podcast is associated accordingly with their **ids** on [podbay.fm](https://www.podbay.fm). I programmed a [webscraper tool](https://github.com/UNCG-CSE/Podknow/blob/master/src/scripts/webscrapers/podbay_webscraper.py) that automatically downloads the latest episode from podbay.fm. All members then had to group import these audio files into **Audacity** to convert stereo audio files to mono-track, .flac formats for use by Google Cloud Speech to Text API.

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I used Jeremy's transcription program as a base for the [transcriber tool](https://github.com/UNCG-CSE/Podknow/blob/master/src/scripts/transcriber.py) which scans the users audio folder for .flac files to transcribe all at one time. Users were required to upload their .flac files manually to their Google Cloud Bucket. Vincent later was able to solve this problem programmatically.

**Harini Booravalli**

**Christopher Edgecombe**
Tasks: Scrubbing Transcriptions

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using the Natural Language Toolkit (NLTK) the goal is to analyze the raw text files and output a file that can be used in "pandas".

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The current implementation of the NLTK program pulls the raw data from a local directory and runs it through a simple stop word removal. The main goal of this implementation is to get a framework for how the data will be moved throughout the system. The output file for the current program is a "pickle" file. This file type was selected so it could help streamline our process of reading text data in the future.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the future, we will potentially be pulling the raw data from Google Cloud Platforms, and running more advanced text analysis on the text files. We will be working in conjunction with Dr. Beveridge to explore future implementations of text analysis.

 **Next steps**

TBA
=======
We're going to start textmining the scrubbed transcriptions, and work on a data collection console application that will make future data collection tasks much faster and easier.
