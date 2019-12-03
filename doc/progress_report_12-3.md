### Progress Report 3 
 **Machine Learning, 11/1 to 12/3**

**Vincent Yang**
Tasks: 

**Jeremy Hudson**
Tasks: LDA model using bigrams – Compare and contrast results of bigram models with models built using the entire corpus 

Ask the question: “How do bigram models compare with models built from the whole corpus?” to determine nuances and greater details in topics.

To answer this question, I built an LDA model from exclusively bigram input to provide a greater clarity into the topics discussed, as many topics can be more accurately represented using word pairs. 

The outcome provided greater insight into the topics discussed by giving additional nuance that single words did not provide. 
The implications of these results will allow us to more accurately determine topics discussed by analyzing bigrams. 


**Jamie Weathers**
Tasks: Random Forest Regression Model - Predict outcome of confidence scores of a transcript based on it's word count.

The question: Can we predict the confidence score of a transcription based on the word count?

I trained a random forest regression model using 1600 samples of word count : confidence score data. Testing the word counts with the remaining 400 samples, we can see a clear trend that resembles the original plotted output. It's hard to predict confidence scores lower than 0.80 and we cannot predict that samples with lower word count can also produce very high confidence scores. A different methodology may be required.

**Christopher Edgecombe**
Tasks: LDA Model for Words - LDA Model for Words Using SciKit - Categorization of Topics (In Progress)

The question "What are the topics of each podcast?" was asked due to the goal of the project being to find the content of each podcast based on things other than genre. 

In order to solve this question LDA models were created in order to give us an understanding of the topics in each podcast as well as the words that make up those topics.

The outcomes of these LDA models are more apparent in the slides of Progress Report 3, however we were able to visualize the data from the topic model as well as find the most dominant topics from each podcast among other things. 

The outcome for the categorization will be to have each of the topics labeled based on the words that are found within them. This will allow us to better understand the topics in each podcast as well as lead to better visualization. 

**Harini Booravalli**
Tasks: Topic modelling ofr words using LSA

The question "to extract the topics in all the podcasts"? " to find similarity between any 2 topics", which would further lead us to know what is the trending topic

Latent Semantic Analysis (LSA) is a framework for analyzing text using matrices.It finds  relationships between documents and terms within documents. scikit learn , a  Python library for doing machine learning, feature selection, etcA simple way to add structure to text is to use a document-term matrix.Once we have the document term matrix, we apply lsa(Combination of Countvectorizer/Tf-IDF +SVD).The result gives us the topics . Once we receive the document term matrix we use LSa and set the topics count to 160 based on coherence scores.
Hence we have 160 topics . our final output is matrix of 193 podcast * 160 topics. this matrix can be further utilized as input for clustering ,getting similarity between the podcasts.
In this case i have applied the result to get the similairty between the podcasts.
Further the same matrix will give us information about  each podcasts and the the topics in the podcasts.

The corresponding code can be found at:-'
"https://github.com/UNCG-CSE/Podknow/blob/0b30975c7445d6f38d4f6273f8aa8f9006d09cb6/src/notebooks/lsamodel_final.ipynb"

Few points here:- LSA model does not do a great job due to few reasons, doc term matrix is a large but sparse matrix where as the once the model is applied the model becomes dense. SO when the data is huge the space taken is much more and makes the system slower.
secondly , couldn't find great material  on visualization of lsa. Most people prefer doing  LDA or word embedding.
Thridly, Bag of words , it doesnt take into consideration  about the position of the word in the sentence hence context goes missing.
Having said that  inspite of all the disavantages mentioned, its defintely a decent model for getting topics in this case. 

One important observation here , is SVD acts similar to PCA, by reducing the dimentinality of the matrix . 

Result :- 160 topics obtained , a topic similarity matrix was produced.(Working on clustering and improving this model)




