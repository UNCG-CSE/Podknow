# Podknow
**Description**

## Table of Contents

 ## People
 **SnackOverflow Team** [Harini Booravalli](https://github.com/HariniBooravalli), [Jamie Weathers](https://github.com/jwthrs), [Kun Yang](https://github.com/kunyang6), [Christopher Edgecombe](https://github.com/credgeco), [Jeremy Hudson](https://github.com/JeremyHudson43)

 **Mentor** [Dr. Aaron Beveridge](https://github.com/aabeveridge)

 **Instructor** [Dr. Somya Mohanty](https://github.com/somyamohanty)

 ## Goals
- Determine what topics are popular within the top 200 podcasts on iTunes 
- Acquire the raw text of the podcast
- Performing natural language processing on the text
- Determine best method of topic modeling
     
 ## Tasks
  - ``Jeremy Hudson``
     - 
  - ``Jamie Weathers``
     - 
  - ``Kun Yang``
     -
  - ``Christopher Edgecombe``
     - 
  - ``Harini Booravalli``
     - 
     
 ## Results Obtained 


     
 ## Software Requirements
**Required modules:**
  - ``pip install pandas``
     - Useful for various data scrubbing functionality.
  - ``pip install pydub``
     - Used to get the sampling rate of an audio file to be wrapped in a config file sent to Google Speech To Text API.
     - Dependent upon FFmpeg library.
  - ``pip install nltk``
     - Used to provide text analysis.
     - All NLTK data will also need to be imported.
     - Data Install guide: https://www.nltk.org/data.html     
     
 **Required libraries:**
  - FFmpeg
     - This library is an audio encoder/decoder that's needed for the operation of the pydub module.
     - Windows Setup guide: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

 ## Terminology and Jargon
  - ``.flac`` : Common audio extension used in Google Cloud speech to text
  - **SST** : Speech to text
  - **iTunes ID** : An ID associated to many podcast authors from iTunes API
