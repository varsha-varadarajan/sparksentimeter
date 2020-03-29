import urllib2
import bs4
import os, csv
import sys
from datetime import datetime
import workdays

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/varshav/work/spark-1.4.1-bin-hadoop2.4"

# Append pyspark  to Python Path
sys.path.append("/home/varshav/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)
# from pyspark.sql import SQLContext

pg_no = 1


def scrape():
    x = 0
    global pg_no
    # Page

    URL = "http://www.moneycontrol.com/elite/section/technical-experts/2-9-"+str(pg_no)+".html"
    # Download the page data and create a BeautitulSoup object
    Page = urllib2.urlopen(URL)
    Text = Page.read()
    soup = bs4.BeautifulSoup(Text, "html.parser")

    letters = soup.find_all("div", "expcontent")
    # expert1 = soup.find("a", "bl16")
    # expert = expert1.get_text()
    for element in letters:
        # ---- date -----
        date = element.find("p", "gry_11")
        dt_str = date.get_text()
        dt_obj = datetime.strptime(dt_str, '%I:%M %p | %d %b %Y |').date()
        date1 = dt_obj.__str__()
        td = datetime.now().date()
        prev_day = workdays.workday(td,-4)

        if dt_obj >= prev_day:
            x = 1

            comment1 = element.a.get_text()
            comment2 = comment1.encode('utf-8')
            formattedComment = comment2.__str__()
            if ";" in formattedComment:
                formattedComment1 , rest1 = formattedComment.split(";", 1)
            else:
                formattedComment1 = formattedComment
            print formattedComment1

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
            csvFile = open('/home/varshav/django-projects/stock_website/stock/static/stock/csvs/comments.csv', 'a')
            csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n')
            csvWriter.writerow([formattedName,date1,formattedComment1])
            print formattedName+"    "+date1+"   "+formattedComment1
            # s = formattedName + "\t" + formattedComment + "\t" + date1 + "\n"
            # f.write(s)

        else:
            x = 0
            break

    if x == 1:
        pg_no += 1
    return x


def scr_call():
    if os.path.exists('/home/varshav/django-projects/stock_website/stock/static/stock/csvs/comments.csv'):
        os.remove('/home/varshav/django-projects/stock_website/stock/static/stock/csvs/comments.csv')
    page = 1
    #sc = SparkContext(appName="Test")
    x = 1
    while x:
        x = scrape()
    pg_no=1
    #sc.stop()


def main():
    scr_call()


if __name__ == "__main__":
    main()