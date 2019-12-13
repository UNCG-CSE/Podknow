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
     - Setup Google Speech To Text API
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
**Results by Person:**
  - ``Jeremy Hudson``
  
     - Successfully acquired data from Google Speech to Text API 
     - Successfully implemented Gensim LDA models for topic modeling using data from NLTK tokenization  
     - Successfully designed a notebook to find similarity between topics in Gensim LDA models using Hellinger distance
     - Successfully built LDA models from NLTK bigram data and performed statistical analysis on them 
     
  - ``Jamie Weathers``
     - Developed Podbay.fm web scraper
     - Developed data collection tool which downloads, converts and transcribes audio in one cohesive flow.
     - Performed analytics on Audio Length and Confidence Scores associated with transcript segments.
     - Trained a random forest regression on confidence scores explained by word count of transcript segments.

     
  - ``Kun Yang``
     - Generated top 200 podcasts list from iTunes.
     - Created stereo track splitter to mono tracks.
     - Analyzed audio length vs. Cost.
     - Preformed machine learning on trending words based on bag of words


      
  - ``Christopher Edgecombe``
     - LDA Models for words using SciKit.
     - Visualization of these models using pyLDAvis as well as other visulization techniques.
     - Basic statistics on Title vs. Podcast Content.

     
  - ``Harini Booravalli``
- As a part of statistical analysis I was able to fit in the poisson’s distribution to the podcast data .
- Successfully able to apply LSA model on the podcasts data and 160 topics were obtained.
- Explored Tf and Tf-IDF methods on few of the single podcasts and on all the podcasts.
- Successfully able to determine the Similarity between the podcasts using the results of LSA model.


     
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
