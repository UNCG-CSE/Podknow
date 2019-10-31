### Progress Report 2 
 **Statistics, 9/25 to 10/31**

**Vincent Yang**
Tasks: 

**Jeremy Hudson**
Tasks: Topic modeling using bigrams and statistical analysis using bigram data

The following notebook was my first prototype that simply printed bigrams from the NLTK to excel format.
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/bigramFinder.ipynb
The following notebook was my mostly unsuccessful attempt at using LDA modeling combined with the Gensim topic modeling library. 
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/gramTopicModeling.ipynb
The following notebook was my successful result at topic modeling using bigram data from the NLTK and topic modeling using an LDA model.
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/NLTKGensimHybrid.ipynb

I would approximate that I spent around twenty hours designing, modifying and experimenting with notebooks for my first task.
My first task included topic modeling with the use of bigrams. To achieve this, I attempted to use LDA topic modeling in combination with another topic modeling library called Gensim to generate bigrams, then feed the bigrams into my LDA model to perform topic analysis. However, it would consistently generate a single topic even though my model parameters were set to generate more than that. To combat this, I attempted to generate bigrams using the Natural Language Toolkit, then generate the topics using the LDA model with these new bigrams as input data. This new approach worked successfully. 

The following notebook was a modification of my NLTKGensimHyrid notebook that prints the mean of the occurrences of the top 10 collocations for a given podcast. 
https://github.com/UNCG-CSE/Podknow/blob/master/src/notebooks/MeanOfBigramQuantity.ipynb
Since my second task used my earlier notebooks as a base, I only spent around two to three hours on my second task.
My second task included the gathering of the top 10 occurrences of certain bigrams throughout podcasts. I added up their occurrences, then divided by 10 to find the mean of the occurrences for these bigrams for each podcast. Since many topics can be more accurately represented in two or more words, this provided deeper insight into how often certain topics of discussion are mentioned in a given podcast. I found that the mean of the top 10 bigrams varies a substantial amount across many podcasts, and as such the concentration of topics discussed most likely does as well. 


**Jamie Weathers**
Tasks: 

**Christopher Edgecombe**
Tasks: 


**Harini Booravalli**
Tasks: 

