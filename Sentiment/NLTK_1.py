import csv
import re
import random

#start replaceTwoOrMore
import nltk
from nltk.classify import *
from nltk.classify.maxent import MaxentClassifier


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end


#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end


#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureVector:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


#Read the tweets one by one and process it
inpTweets = csv.reader(open('/home/varshav/work/PycharmProjects/Sentiment/labels1.csv', 'rb'), delimiter=',')
featureList = []

# Get tweet words
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    featureVector = getFeatureVector(tweet)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))
random.shuffle(tweets)
# Extract feature vector for all tweets in one shote
data = nltk.classify.apply_features(extract_features, tweets)

print data.__len__()
train_set, test_set = data[62345:], data[:26719]
# Train the classifier
NBClassifier = nltk.NaiveBayesClassifier.train(train_set)

# Test the classifier
testTweet = 'Bajaj puts hold on Indonesian JV with Kawasaki, to focus on KTM'
print "-------------------------------------------"
print NBClassifier.classify(extract_features(getFeatureVector(testTweet)))
print "-------------------------------------------"
print NBClassifier.show_most_informative_features(10)


print "---------------------------------------------------------"
print(nltk.classify.accuracy(NBClassifier, test_set))
print(nltk.classify.accuracy(NBClassifier, train_set))
'''
#Max Entropy Classifier
MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 10)
testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
processedTestTweet = processTweet(testTweet)
print MaxEntClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))

# Output
# =======
# positive

#print informative features
print MaxEntClassifier.show_most_informative_features(10)
'''
