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
 
   **Task by Person:**
  - ``Jeremy Hudson``
     - Acquired data from Google Speech to Text API 
     - Experimented with different speech to text engines (PocketSphinx and Google Speech to Text API)
     - Topic modeling using Gensim LDA models 
     - Determined similarity between topics using Hellinger distance
     - Built LDA models from bigrams and performed statistical analysis on them 
     
  - ``Jamie Weathers``
     - Developed a program using Google Speech to Text API to transcribe all podcasts at once 
     - Developed a web scraper to download latest episode audio from PodBay.fm
     - Performed statistical analysis from Transcription Data
     - Generated a random forest regression from sample podcast data 
     
  - ``Kun Yang``
     - Acquired data from Google Speech to Text API 
     - Acquired data from iTunes RSS API to get current top 200 podcasts 
     - Developed an automated audio converter and an automated file uploader to Google Cloud
     - Performed statistical analysis on Google Speech to Text pricing 
     - Used linear regression to find trending words 
     
      
  - ``Christopher Edgecombe``
     - Acquired data from Google Speech to Text API 
     - Used the Natural Language Toolkit to remove stopwords and generate pickled output files for language processing 
     - Used SciKit and Gensim LDA models to perform topic modeling for the entire corpus
     - Determined frequency of topic discussion vs content in podcast title 
     
  - ``Harini Booravalli``
     - Acquired data from Google Speech to Text API 
     - Data analysis and preprocessing 
     - Used LSA for Topic Modeling
     - Analyzed statistics for LSA models with single words 
     - Formed a Topic Similarity Matrix from LSA results 
     
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
