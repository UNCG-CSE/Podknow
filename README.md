# Podknow


 ## Purpose



 ## People
 **The Team** [Harini Booravalli](), [Jamie Weathers](https://github.com/jwthrs), [Kun Yang](https://github.com), [Christopher Edgecombe](https://github.com), [Jeremy Hudson]()
 **Mentor** [Dr. Aaron Beveridge](https://github.com/)

 **Instructor** [Dr. Somya Mohanty](https://github.com/)

 ## Data

 ## Requirements
**Required modules:**
  - pandas
  - pydub

**Required libraries:**
  - FFmpeg
     - This library is needed for the operation of pydub, which is used to get the sampling rate of an audio file to be wrapped in a config file sent to Google Speech To Text API.
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
   - [ ] Grab audio files from podbay if no transcripts exist
      - At this time, store audio data locally.
      - [ ] Run TTS on audio files to convert to textual data
   - [ ] Run NLP on text to find top mentioned terms
   - [ ] From all scraped data, generate csv files.
