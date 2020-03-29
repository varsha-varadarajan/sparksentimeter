import os,sys
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print fuzz.ratio("ACME Factory", "ACME Factory Inc.")
# 83
print fuzz.partial_ratio("ACME Factory", "ACME Factory Inc.")
# 100

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

# Generate experts list from train data


def main():
    print "------------------------------"
    sc = SparkContext(appName="Test")
    num = 1
    companies = []
    company_list = []
    codes_list = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/admin/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        company_list.append(company_name)
        nse_code = row.get('NSE_Symbol')
        codes_list.append(nse_code)
        companies.append(nse_code)
        #name = name.lstrip().rstrip()
        companies.append(company_name)

    # print companies

    '''
    query = 'K M Mills stretched: Tulsian'
    #choices = ['Barack H Obama', 'Barack H. Obama', 'B. Obama']
    # Get a list of matches ordered by score, default limit to 5
    print process.extract(query, companies)
    # [('Barack H Obama', 95), ('Barack H. Obama', 95), ('B. Obama', 85)]

    # If we want only the top one
    print process.extractOne(query, companies)
    # ('Barack H Obama', 95)
    '''
    reader1 = csv.DictReader(open('/home/admin/PycharmProjects/StockAnalysis/train/train1.tsv','rb'),delimiter='\t')
    for row in reader1:
        # print row
        comment_id = row.get('comment_id')
        comment = row.get('comment')
        m = 0
        for company in companies:
            value=fuzz.token_set_ratio(comment, company)
            # print company+ "-- "+str(value)
            if(value>=m):
                m=value
                match=company
        # print "--------------------------------------------"
        nse=""
        if company_list.__contains__(match):
            with open("/home/admin/PycharmProjects/nse_mapping.csv", 'r') as file:
                reader = csv.reader(file)
                nse = [line[2] for line in reader if line[0] == match]
                final_nse = nse[0]
        else:
            if codes_list.__contains__(match):
                nse = match
                final_nse = nse

        csvFile = open('/home/admin/PycharmProjects/StockAnalysis/datasets/comment_tags1.csv', 'a')
        csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
        csvWriter.writerow([comment_id,final_nse])
        print comment + ":"+ match + "-->" + str(final_nse)
        sc.stop()


if __name__ == '__main__':
    main()