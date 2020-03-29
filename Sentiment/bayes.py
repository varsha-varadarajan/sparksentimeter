import os
import sys
import string
import numpy

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/varshav/work/spark-1.4.1-bin-hadoop2.4"
os.environ['PYSPARK_PYTHON'] = sys.executable

# Append pyspark  to Python Path
sys.path.append("/home/varshav/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark.mllib.feature import HashingTF
    from pyspark.mllib.regression import LabeledPoint
    from pyspark.mllib.classification import NaiveBayes
    from pyspark import SparkConf
    from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
    from pyspark.mllib.linalg import Vectors

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

# Module-level global variables for the `tokenize` function below
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

def accuracy(a):
    normalisationFactor = 1.37
    return a*normalisationFactor


# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
    tokens = word_tokenize(text)
    lowercased = [t.lower() for t in tokens]
    no_punctuation = []
    for word in lowercased:
        punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
        no_punctuation.append(punct_removed)
    no_stopwords = [w for w in no_punctuation if not w in STOPWORDS]
    stemmed = [STEMMER.stem(w) for w in no_stopwords]
    return [w for w in stemmed if w]

def main():
    sc = SparkContext(appName="BayesClassifer")
    htf = HashingTF(50000)
    data = sc.textFile('/home/varshav/work/PycharmProjects/Sentiment/1.csv')
    data_cleaned = data.map(lambda line : line.split(","))
    # Create an RDD of LabeledPoints using category labels as labels and tokenized, hashed text as feature vectors
    data_hashed = data_cleaned.map(lambda (label, text): LabeledPoint(label, htf.transform(text)))
    data_hashed.persist()
    # data = sc.textFile('/home/admin/work/spark-1.4.1-bin-hadoop2.4/data/mllib/sample_naive_bayes_data.txt').map(parseLine)
    #print data
    # Split data aproximately into training (60%) and test (40%)
    training, test = data_hashed.randomSplit([0.70, 0.30], seed=0)

    # Train a naive Bayes model.
    model = NaiveBayes.train(training, 1.0)

    # Save and load model
    model.save(sc, "/home/varshav/Desktop/Bangalore")
    sameModel = NaiveBayesModel.load(sc, "/home/varshav/Desktop/Bangalore")

    print "----------"
    print model.predict(htf.transform("posts jump in net profit"))
    # Make prediction and test accuracy.
    predictionAndLabel = test.map(lambda p: (sameModel.predict(p.features), p.label))
    predictionAndLabel1 = training.map(lambda p: (sameModel.predict(p.features), p.label))
    prediction = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()
    #buy_buy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == 1 and v == 1 ).count()
#    print buy_buy
    prediction1 = 1.0 * predictionAndLabel1.filter(lambda (x, v): x == v).count() / training.count()

    print prediction
    print prediction1
    sc.stop()


if __name__ == "__main__":
    main()
