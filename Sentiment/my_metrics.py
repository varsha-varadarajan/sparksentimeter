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
    from pyspark.mllib.evaluation import MulticlassMetrics

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)


# Module-level global variables for the `tokenize` function below
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

def normalize(a):
    normalisationFactor = 1.135
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
    data = sc.textFile('/home/varshav/work/PycharmProjects/Sentiment/cleaned_bayes_labels1.csv')
    data_cleaned = data.map(lambda line : line.split(","))
    # Create an RDD of LabeledPoints using category labels as labels and tokenized, hashed text as feature vectors
    data_hashed = data_cleaned.map(lambda (label, text): LabeledPoint(label, htf.transform(text)))
    data_hashed.persist()
    # data = sc.textFile('/home/admin/work/spark-1.4.1-bin-hadoop2.4/data/mllib/sample_naive_bayes_data.txt').map(parseLine)
    #print data
    # Split data aproximately into training (60%) and test (40%)
    training, test = data_hashed.randomSplit([0.70, 0.30], seed=0)

    sameModel = NaiveBayesModel.load(sc, "/home/varshav/work/PycharmProjects/StockAnalysis/myModel")

    print "----------"
    print sameModel.predict(htf.transform("posts jump in net profit"))

    predictionAndLabel = test.map(lambda p: (sameModel.predict(p.features), p.label))
    predictionAndLabel1 = training.map(lambda p: (sameModel.predict(p.features), p.label))
    prediction = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()
    prediction1 = 1.0 * predictionAndLabel1.filter(lambda (x, v): x == v).count() / training.count()

    buy_buy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == 1 and v ==1).count()
    sell_sell = 1.0 * predictionAndLabel.filter(lambda (x, v): x == 2 and v ==2).count()
    hold_hold = 1.0 * predictionAndLabel.filter(lambda (x, v): x == 3 and v ==3).count()

    print buy_buy
    print sell_sell
    print hold_hold


    # Statistics by class
    labels = data_hashed.map(lambda lp: lp.label).distinct().collect()
    print labels
    print type(labels[0])
    '''
    for label in sorted(labels):
        print("Class %s precision = %s" % (label, metrics.precision(label)))
        print("Class %s recall = %s" % (label, metrics.recall(label)))
        print("Class %s F1 Measure = %s" % (label, metrics.fMeasure(label, beta=1.0)))
    '''
    '''
    print("Class %s precision = %s" % (1, metrics.precision(1)))
    print("Class %s recall = %s" % (1, metrics.recall(1)))
    print("Class %s F1 Measure = %s" % (1, metrics.fMeasure()))

    print("Class %s precision = %s" % (2, metrics.precision(2)))
    print("Class %s recall = %s" % (2, metrics.recall(2)))
    print("Class %s F1 Measure = %s" % (2, metrics.fMeasure(2)))
    '''
    # Weighted stats
    '''
    print("Weighted recall = %s" % metrics.weightedRecall)
    print("Weighted precision = %s" % metrics.weightedPrecision)
    print("Weighted F(1) Score = %s" % metrics.weightedFMeasure())
    print("Weighted F(0.5) Score = %s" % metrics.weightedFMeasure(beta=0.5))
    print("Weighted false positive rate = %s" % metrics.weightedFalsePositiveRate)
    '''

    sc.stop()


if __name__ == "__main__":
    main()
