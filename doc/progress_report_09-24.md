### Initial Prototype
 **Data Collection, 9/11 to 9/17**

!--VINCENT'S PART--! Add or recycle this.
**Vincent Yang**
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We acquired the **names** and **ids** of the top 200 trending podcasts from the [**iTunes RSS API**](https://rss.itunes.apple.com/en-us) into a csv file on 9/11/19. To make processing easier on the group, each member assumed partial responsibility for acquiring the transcriptions of the 200 podcasts. 

**Jeremy Hudson**

**Jamie Weathers**

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Luckily, each **iTunes ID** for the podcast is associated accordingly with their **ids** on [podbay.fm](https://www.podbay.fm). Upon this discovery, I programmed a **webscraper tool** that automatically downloads the latest episode from podbay.fm into each team members local machines. All members then had to group import these audio files into **Audacity** to convert stereo audio files to mono-track, .flac formats for use by Google Cloud Speech to Text API.

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Once Jeremy figured out how to use the Google Cloud Speech to Text API, I used his program as a base for the **transcriber tool** which scans the users audio folder for .flac files to transcribe all at one time. I couldn't find a way to upload the .flac files to the user's Google Cloud Bucket, so I required users to upload their .flac files manually to their Bucket with the assumption they didn't change file names.
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Later, Vincent found a way to programmatically convert audio files to .flac and upload those files to Google Cloud Bucket.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During data collection, I helped organize the repo. I advised that we all store our transcriptions by order of the method that they were acquired, since some transcripts were acquired through other means while the tools were being programmed. These methods span from collecting transcripts of podcasts from **YouTube**, official podcast websites, and directly feeding audio to **Google Documents** speech to text overnight with stereo mix enabled. 

**Harini Booravalli**

**Christopher Edgecombe**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using the Natural Language Toolkit (NLTK) the goal is to analyze the raw text files and output a file that can be used in "pandas".

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The current implementation of the NLTK program pulls the raw data from a local directory and runs it through a simple stop word removal. The main goal of this implementation is to get a framework for how the data will be moved throughout the system. The output file for the current program is a "pickle" file. This file type was selected so it could help streamline our process of reading text data in the future.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the future, we will potentially be pulling the raw data from Google Cloud Platforms, and running more advanced text analysis on the text files. We will be working in conjunction with Dr. Beveridge to explore future implementations of text analysis.

 **Next steps**

TBA
