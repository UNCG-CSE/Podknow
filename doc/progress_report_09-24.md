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
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During data collection, I helped organize the repo. I advised that we all store our transcriptions by order of the method that they were acquired, since some transcripts were acquired through other means while the tools were being programmed. These methods span from collecting transcripts of podcasts from **YouTube**, official podcast websites, and directly feeding audio to **Google Documents** speech to text overnight with stereo mix enabled. In the data folder these methods are separated accordingly:
 - ``data/yt/`` - Acquired by downloading the podcast transcript from YouTube
 - ``data/gdocs/`` - Acquired by feeding audio through speech to text in Google docs.
 - ``data/official/`` - Acquired from the podcasts official site.
 - ``data/gcsst/`` - Acquired by sending the audio files to Google Cloud Speech to Text API.

 There are two folders in each of these directories called ``/raw`` and ``/scrubbed``. The ``/raw`` folder contains original transcripts as it was acquired by its method. The ``/scrubbed`` folder contains transcripts with stopping words removed.

**Harini Booravalli**

**Christopher Edgecomb**

 **Next steps**

TBA