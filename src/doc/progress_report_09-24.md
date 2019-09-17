### Initial Prototype
 **Data Collection, 9/11 to 9/17**

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We acquired the **names** and **ids** of the top 200 trending podcasts from the [**iTunes RSS API**](https://rss.itunes.apple.com/en-us) into a csv file on 9/11/19. To make processing easier on the group, each member assumed partial responsibility for acquiring the transcriptions of the 200 podcasts. Luckily, each **iTunes ID** for the podcast is associated accordingly with their **ids** on [podbay.fm](https://www.podbay.fm). Upon this discovery, a **webscraper tool** was made that automatically downloads the latest episode from podbay.fm into each team members local machines. 

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During the weekend, we figured out how to use **Google Cloud Speech to Text API** and the process to set it up and made a **transcriber tool**. Each team member used **Audacity** to convert each audio file into a **mono-track** ``*.flac`` format. This step is required because **Google Cloud Speech To Text API** can operate on larger files that are only hosted on their buckets, and **SST** requires them to be in a mono-track ``*.flac`` format. With close to 66% of data collection completion, an **audio conversion tool** was made to convert audio files to mono-track and ``*.flac`` format to bypass the cumbersome use of mass importing and mass processing and exporting in Audacity. After audio files were converted by team members, the audio files were processed by the transcriber tool and output was stored in ``/data/transcripts/``.

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Some transcripts were acquired through other means while the tools were being programmed. These methods span from collecting transcripts of podcasts from **YouTube**, official podcast websites, and directly feeding audio to **Google Documents** speech to text overnight with stereo mix enabled. In the data folder these methods are separated accordingly:

 - ``data/yt/`` - Acquired by downloading the podcast transcript from YouTube
 - ``data/gdocs/`` - Acquired by feeding audio through speech to text in Google docs.
 - ``data/official/`` - Acquired from the podcasts official site.
 - ``data/gcsst/`` - Acquired by sending the audio files to Google Cloud Speech to Text API.

 There are two folders in each of these directories called ``/raw`` and ``/scrubbed``. The ``/raw`` folder contains original transcripts as it was acquired by its method. The ``/scrubbed`` folder contains transcripts with stopping words removed.

 **Next steps**

TBA