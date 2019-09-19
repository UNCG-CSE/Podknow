# Podknow
**Description**

## Table of Contents

 ## People
 **SnackOverflow Team** [Harini Booravalli](https://github.com/HariniBooravalli), [Jamie Weathers](https://github.com/jwthrs), [Kun Yang](https://github.com/kunyang6), [Christopher Edgecombe](https://github.com/credgeco), [Jeremy Hudson](https://github.com/JeremyHudson43)

 **Mentor** [Dr. Aaron Beveridge](https://github.com/aabeveridge)

 **Instructor** [Dr. Somya Mohanty](https://github.com/somyamohanty)

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

 ## Terminology and Jargon
 ``.flac``
 **SST**
 **iTunes ID**

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
 - [x] Use a different platform or some other Github tool (Project tab?) for to do lists!
   - 9/15/19 Done, check projects tab.
 - [ ] Unit testing?
 - [ ] Delete this todolist and fully transition to Github projects!
