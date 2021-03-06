# sparksentimeter
Sentiment analysis project

![High level design](https://github.com/varsha-varadarajan/sparksentimeter-images/blob/master/overall-architecture.png)

## Folders
1. Folder StockAnalysis - all data acquisition and data pre-processing code.

2. Folder Sentiment - Sentiment analysis and sentiment classification code.

3. Folder rating - code for Analyst credibility module.


## StockAnalysis

1. scrape.py : Distributed scraping

2. preprocess.py : Data pre-processing

3. match.py : Named Entity Recognition

4. clean.py : Handle negation

5. featurelist.py : Generate list of features

6. label.py : Perform sentiment labelling

7. dictionary.txt : File containing financial dictionary words

8. stopwords.txt : File containing stopwords

## Sentiment
1. bayes_clean.py : Code to clean data for Bayes module

2. bayes.py : Bayes code

3. my_metrics.py : Calculate metrics of system

4. NLTK.py : NLTK Bayes code

![Architecture](https://github.com/varsha-varadarajan/sparksentimeter-images/blob/master/architecture.png)

## StockAnalysis/myModel
This is where the Bayes prediction model is stored. New incoming comments are classified based on this saved model.
