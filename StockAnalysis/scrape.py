import urllib2
import bs4
import os, csv
import sys
from datetime import datetime
import fileinput, time

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/admin/work/spark-1.4.1-bin-hadoop2.4"

# Append pyspark  to Python Path
sys.path.append("/home/admin/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)


# from pyspark.sql import SQLContext

def scrape(str):
    sentence = []
    # Page
    URL = str
    # Download the page data and create a BeautitulSoup object
    Page = urllib2.urlopen(URL)
    Text = Page.read()
    soup = bs4.BeautifulSoup(Text, "html.parser")

    letters = soup.find_all("div", "expcontent")
    # expert1 = soup.find("a", "bl16")
    # expert = expert1.get_text()
    for element in letters:
        comment1 = element.a.get_text()
        comment2 = comment1.encode('utf-8')
        formattedComment = comment2.__str__()
        # if ":" in comment:
        #  formattedComment , rest1 = comment.split(":", 1)
        # else:
        # formattedComment = comment
        print formattedComment
        date = element.find("p", "gry_11")
        dt_str = date.get_text()
        dt_obj = datetime.strptime(dt_str, '%I:%M %p | %d %b %Y |')
        date1 = dt_obj.__str__()
        print date1
        expert = element.find("p", "gry_13")
        expertName1 = expert.get_text()
        expertName2 = expertName1.encode('utf-8')
        expertName = expertName2.__str__()
        if "," in expertName:
            formattedName , rest2 = expertName.split(",", 1)
        else:
            formattedName = expertName
        print formattedName
        # f = open("/home/admin/work/newtrain.txt", 'a')
        l = formattedName+"\t"+date1+"\t"+formattedComment+"\n"
        sentence.append(l)
        #li = sc.parallelize([l]).collect()
        #li.saveAsTextFile("/home/admin/PycharmProjects/StockAnalysis/train/brokerage_train1.tsv")
        # s = formattedName + "\t" + formattedComment + "\t" + date1 + "\n"
        # f.write(s)
    return sentence


def main():
    sc = SparkContext(appName="distributed")
    links = sc.textFile("/home/admin/PycharmProjects/StockAnalysis/links/results.txt")
    print links.count()
    text = links.flatMap(scrape)
    text.count()
    sc.stop()


if __name__ == "__main__":
    main()
