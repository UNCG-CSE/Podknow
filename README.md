# Podknow
---

 ## Purpose
 ---

 ## Data
 ---
 ## Requirements
#### Required modules:
  - Pandas

#### Required libraries:
  - FFmpeg
     - Windows Setup guide: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

 ## To Do
 ---
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
