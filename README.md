# Podknow
**Description**

## Table of Contents

 ## People
 **SnackOverflow Team** [Harini Booravalli](https://github.com/HariniBooravalli), [Jamie Weathers](https://github.com/jwthrs), [Kun Yang](https://github.com/kunyang6), [Christopher Edgecombe](https://github.com), [Jeremy Hudson](https://github.com/JeremyHudson43)

 **Mentor** [Dr. Aaron Beveridge](https://github.com/aabeveridge)

 **Instructor** [Dr. Somya Mohanty](https://github.com/somyamohanty)

 ## Data

### Initial Prototype
 **Data Collection, 9/11 to 9/17**

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We acquired the **names** and **ids** of the top 200 trending podcasts from the **iTunes RSS API** into a csv file. To make processing easier on the group, each member assumed partial responsibility for acquiring the transcriptions of the 200 podcasts. Luckily, each **iTunes ID** for the podcast is associated accordingly with their **ids** on podbay.fm. Upon this discovery, a **webscraper tool** was made that automatically downloads the latest episode from podbay.fm into each team members local machines. 

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During the weekend, we figured out how to use **Google Cloud Speech to Text API** and the process to set it up and made a **transcriber tool**. Each team member used **Audacity** to convert each audio file into a **mono-track** ``*.flac`` format. This step is required because **Google Cloud Speech To Text API** can operate on larger files that are only hosted on their buckets, and **SST** requires them to be in a mono-track ``*.flac`` format. Close to 66% of data collection completion, an **audio conversion tool** was made to convert audio files to mono-track and ``*.flac`` format to bypass the cumbersome use of mass importing and mass processing and exporting in Audacity. After audio files were be converted by team members, the transcriber tool was ran on the flac files and transcribed to ``/data/transcripts/``.

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Some transcripts were acquired through other means while the tools were being programmed. These methods span from collecting transcripts of podcasts from **YouTube**, official podcast websites, and directly feeding audio to **Google Documents** speech to text overnight with stereo mix enabled. In the data folder these methods are separated accordingly:

 - ``data/yt/`` - Acquired by downloading the podcast transcript from YouTube
 - ``data/gdocs/`` - Acquired by feeding audio through speech to text in Google docs.
 - ``data/official/`` - Acquired from the podcasts official site.
 - ``data/gcsst/`` - Acquired by sending the audio files to Google Cloud Speech to Text API.

 There are two folders in each of these directories called ``/raw`` and ``/scrubbed``. The ``/raw`` folder contains original transcripts as it was acquired by its method. The ``/scrubbed`` folder contains transcripts with stopping words removed.

 **Next steps**

TBA

 ## Requirements
**Required modules:**
  - ``pip install pandas``
  - ``pip install pydub``
     - Used to get the sampling rate of an audio file to be wrapped in a config file sent to Google Speech To Text API.
     - Transcription will not occur without inclusion.
     - Dependent upon FFmpeg library.

**Required libraries:**
  - FFmpeg
     - This library is an audio encoder/decoder that's needed for the operation of the pydub module.
     - Windows Setup guide: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

 ## To Do
 - [x] Meet with Dr. Aaron Beveridge to discuss details
    - 9/11/19
 - [ ] Scalability of Data Collection
   - [x] Get list of top trending podcasts
    - 9/11/19 updated
   - [ ] Grab textual data from transcripts of the latest episodes from aforementioned podcasts if available
   - [x] Webscrape tool for Podbay
    - 9/14/19
   - [x] Google cloud Speech to Text transcriber tool
    - 9/14/19
   - [ ] Grab audio files from podbay if no transcripts exist
      - At this time, store audio data locally.
      - [ ] Run TTS on audio files to convert to textual data
   - [ ] Run NLP on text to find top mentioned terms
   - [ ] From all scraped data, generate csv files.
 - [ ] Cleanup this readme and make it look more presentable.
 - [ ] Use a different platform or some other Github tool (Project tab?) for to do lists!
 - [ ] Unit testing?
