### Progress Report 2 
 **Statistics, 9/25 to 10/31**

**Vincent Yang**
Tasks: 
My task includes reading for all the transcripts Json generated from teammate Jamie.
Correct each one of the top 90 scripts into correct json format.
My work also include using ipython notebook to calculate the basic stats for the cost of each cost. 
Mean, variance, std, measures of spread and quantil.
Find out the best distribution based on using MOM and KDE.
Link to work :https://github.com/UNCG-CSE/Podknow/blob/master/util/scripts/VincentScripts/apiStatistics.ipynb


**Jeremy Hudson**
Tasks: Topic modeling using bigrams and statistical analysis using bigram data

The following notebook was my first prototype that simply printed bigrams from the NLTK to excel format.
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/bigramFinder.ipynb

The following notebook was my mostly unsuccessful attempt at using LDA modeling combined with the Gensim topic modeling library. 
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/gramTopicModeling.ipynb

The following notebook was my successful result at topic modeling using bigram data from the NLTK and topic modeling using an LDA model.
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/NLTKGensimHybrid.ipynb


The following notebook was my successful attempt at calculating hellinger distance between topics using LDA models:
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/HellingerCalculator.ipynb

I would approximate that I spent around twenty hours designing, modifying and experimenting with notebooks for my first task.
My first task included topic modeling with the use of bigrams. To achieve this, I attempted to use LDA topic modeling in combination with another topic modeling library called Gensim to generate bigrams, then feed the bigrams into my LDA model to perform topic analysis. However, it would consistently generate a single topic even though my model parameters were set to generate more than that. To combat this, I attempted to generate bigrams using the Natural Language Toolkit, then generate the topics using the LDA model with these new bigrams as input data. This new approach worked successfully. Finally, I computed the hellinger distance between topics after building the model.

The following notebook was a modification of my NLTKGensimHyrid notebook that prints the mean of the occurrences of the top 10 collocations for a given podcast. 
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/MeanOfBigramQuantity.ipynb

Since my second task used my earlier notebooks as a base, I only spent around two to three hours on my second task.
My second task included the gathering of the top 10 occurrences of certain bigrams throughout podcasts. I added up their occurrences, then divided by 10 to find the mean of the occurrences for these bigrams for each podcast. Since many topics can be more accurately represented in two or more words, this provided deeper insight into how often certain topics of discussion are mentioned in a given podcast. I found that the mean of the top 10 bigrams varies a substantial amount across many podcasts, and as such the concentration of topics discussed most likely does as well. 


**Jamie Weathers**
Tasks: 
Transcript Collector Application
https://github.com/UNCG-CSE/Podknow/blob/master/util/scripts/collector.py
Approx 20 hours
-The Collector app is vital for outputting valuable data points for the project.
-Many hours spent debugging and figuring out how to overcome limitations, ie. Among many issues, using pydub to convert an audio file results in memory overflow, so calling an external application such as ffmpeg to handle it received no errors
-This includes the time it takes to transcribe podcasts, the length of each podcast, the download status, file sizes before and after conversion of audio formats, and confidence scores. 
-These points are important because from a business perspective it would allow us to project and predict how much time and money is being spent on certain tasks.

Confidence Score Analysis
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/PodcastConfidenceScores.ipynb
Approx 6 hours
-An attempt was made to find an explanation for why confidence scores were higher than others.
-First clue was that I noticed many shorter phrases had a lower confidence score in the data output.
-Taking the mean of the confidence scores for each podcast and plotting them along side the length of the audio file demonstrated little relation.
-Breaking the transcripts down further and introducing a word count for each transcript with their associated confidence score produced better results.
-When this was graphed, a clear exponential relation was evident.

**Christopher Edgecombe**
Tasks: 
Title vs Content Notebook
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/titledataframe.ipynb
Time Spent: 7 hours

-We obtained many useful results from this notebook. To begin with, we have the pandas dataframe columns for size of the title as well as the unique words that were mentioned in the podcasts. We also have the basic statistics on the list of values which was obtained via a simple describe function. This notebook also graphs the number of times we found a certain number of words in the content of the podcast and fits a normal distribution to this graph. We also test a hypothesis related to the mean number of words found in both the title and the podcast, and receive a p-value for a one sample z-test. Correlation between title length and words from the title being present in the content is also obtained. 

LDA Topic Modeling (Words)
Time Spent: 15 Hours (Still in Progress)

-The goal of this notebook is to find the overarching word topics of the scrubbed text and visualize them for the user. This notebook uses pyLDAvis in order to display each topic with the relevant keywords that makeup this topic. The data is cleaned before being placed into an LDA model. Coherence score is also checked to find the most accurate number of topics for the scrubbed text data. I would like to integrate this with the aforementioned notebook so that the titles can be checked against key topics/words instead of scrubbed text as a whole.
 

**Harini Booravalli**
Harini Booravalli Suresh
Tasks:-
1)Statistics and patterns observed/ word modelling
2)LSA on the podcast
The main goal for this part of my project is to link the statistic and patterns observed with the topic model i am applying.
Task #1
Hours spent :- more than 10 hours
Statistics and patterns observed/ word modelling:
1)frequency distribution of words across all podcasts.
2)frequency distributions of word across each of the podcasts.
3)Fitting zipf law( zeta distribution for the frequency of words). 
This distribtution has generally been used for all the word modelling and word frequnecy analysis. 
Results showed it fits the zeta distribution.
Trying to perform hypothesis testing with respect to this distribution which is still in progress.
4) fitting the poisson's distribution:-
Looking at the graph and looking at my values i have decided to use the poisson distribution as  both word freuency and count of words is discrete hence using this distribution.Poisson distribution nearly fits my data.
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/statistics%20visualization%20word%20modelling%20-1.ipynb

Results:-
Observations Made:-
The mean and frequency is around 3 in most of the cases(may vary at times).
Hence i have considered few podcasts and looked into the words with that have highest word frequency.
I have also considered the tail end of the poisson distribtuion and looked into few words.
Observation made is most of the  words whose frequency is high or near the mean, are common across other podcasts.
Hence this does not help us differentiate the  podcast wiht one other , or give us any particualr topic.
On the other hand the words after standard deviation seems to give soem context when compared with other podcasts.
This leads us to TF-IDF which is the core logic of LSA,leading me to my next task LSA.



Task #2:-
Number of hours spent:- more than 15 hours
LSA or Latent Semantic analysis is  one of the most foundation methods of topic modelling.
Procedure followed in the following:-
1)LSAappliedOnAllPodcasts :- this file shows the LSA model applied on all the podcasts.
2)coherence score vs number of topics which plays an important part in lsa. 
3)working on visualization of result

https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/TfIDf_SVD.ipynb
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/LSAappliedOnAllPodcasts.ipynb

Results:-
Observation made:-
1)LSA is combination of tf-idf + SVD, where a document matrix is formed and we set the number of topics  we want the result to appear.This can be determined by the coherence graph.
2) there are 2 ways  of getting the document term matrix and they are count vectorization and tf-idf vectorization. Count vectorizer is just the count of words and  is too basic and doesn't give proper results due to the fact that there can be many words across all podcasts with high frequency. our goal is to find the words which differentiates the topic.
TF-IDF considers the word with high frequency in the particualr document and low frequency in other documents, thus giving us the words which make the difference.
3) Visualization is a huge problem and making sense of result is tough, as result contains words with its tf-idf scores.
4)one  major disdavantage i have noticed in lsa is each topic is made of words with its absolute value, this leads to common words wiht different topics.
for examples:-
if we had word called apple and tf-idf score of apple in topic1 is +0.8 and in topic2 -0.7, then apple clearly can be used to differentiate between the topic1 and topic2, but when we form the lsa model , apple might appear in both topic1 and topic2, as the model counts the absolute value of apple.
5)Overall i find the LSA model , not very efficient , as it doesn't give clarity , and does a very poor job in seperating the  topic by looking at the sample results.
Though i understand the LSA topic modelling, i would defintely like to look into other efficient models for topic modelling.


