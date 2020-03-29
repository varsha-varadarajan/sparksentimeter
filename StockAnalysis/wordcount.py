import urllib2
import bs4
import os, csv
import sys
from datetime import datetime
import fileinput, time
import re

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/varshav/work/spark-1.4.1-bin-hadoop2.4"

# Append pyspark  to Python Path/home/varshav/work/spark-1.4.1-bin-hadoop2.4
sys.path.append("/home/varshav/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

def getCompanyName():
    companies = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        words = company_name.split(" ")
        for word in words:
            if word not in companies:
                companies.append(word)
        nse_code = row.get('NSE_Symbol')
        companies.append(nse_code)
    return companies


def getExpertsname():
    experts = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/datasets/experts1.tsv', 'rb'), delimiter='\t')
    for row in reader:
        name = row.get('expert_name')
        words = name.split(" ")
        for word in words:
            if word not in experts:
                experts.append(word)
    return experts

def process(line):
    line = re.sub('[0-9]',' ',line)
    line = re.sub('-',' ',line)
    line = re.sub(',',' ',line)
    line = re.sub('\.',' ',line)
    line = re.sub("Rs",'  ',line)
    line = re.sub('%','',line)
    line = re.sub('\?',' ',line)
    line = re.sub('\'','',line)
    line = re.sub(';',' ',line)
    line = re.sub('\$',' ',line)
    line = re.sub('[\s]+', ' ', line)
    return line


def remove_company_name(word):
    companies = []
    if word not in companies:
        return True
    else:
        return False

def main():
    sc = SparkContext(appName="Test")
    text_file = sc.textFile("/home/varshav/work/PycharmProjects/StockAnalysis/comments.txt")
    d1 = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda x, y: x+y).map(lambda (x, y): (y, x)).sortByKey(False)
    print d1.count()
    d1.saveAsTextFile("/home/varshav/work/PycharmProjects/StockAnalysis/word_count.txt")
    sc.stop()


if __name__ == "__main__":
    main()
