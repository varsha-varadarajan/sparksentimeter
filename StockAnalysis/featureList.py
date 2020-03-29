# Extract comments list from train data

import csv
import re


def getCompanyName():
    companies = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        words = company_name.lower().split(" ")
        for word in words:
            if word not in companies:
                companies.append(word)
        nse_code = row.get('NSE_Symbol')
        companies.append(nse_code.lower())
    return companies


def getExpertsname():
    experts = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/datasets/experts1.tsv', 'rb'), delimiter='\t')
    for row in reader:
        name = row.get('expert_name')
        words = name.lower().split(" ")
        for word in words:
            if word not in experts:
                experts.append(word)
    return experts


def getStopwords():
    stopwords = []
    f = open('/home/varshav/work/PycharmProjects/StockAnalysis/stopwords.txt', 'r')
    ys = f.readlines()
    for y in ys:
        stopwords.append(y[:-1])
    return stopwords


def process(line, stopwords):
    line= line.lower()
    line = re.sub('[0-9]', ' ', line)
    line = re.sub(' - ', ' ', line)
    line = re.sub(',', ' ', line)
    line = re.sub('\.', ' ', line)
    line = re.sub(" rs ", '  ', line)
    line = re.sub("says", '  ', line)
    line = re.sub("Says", '  ', line)
    line = re.sub("advices", ' ', line)
    line = re.sub("advises", ' ', line)
    line = re.sub(" q ", ' ', line)
    line = re.sub('%', ' ', line)
    line = re.sub('\?', ' ', line)
    line = re.sub('\'', '', line)
    line = re.sub(';', ' ', line)
    line = re.sub(':', ' ', line)
    line = re.sub('!', ' ', line)
    line = re.sub('@', ' ', line)
    line = re.sub('/', ' ', line)
    line = re.sub('"', ' ', line)
    line = re.sub('\$', ' ', line)
    line = re.sub('[\s]+', ' ', line)

    newline = []

    words = line.split(" ")
    #words = [w for w in words if not w in stopwords]
    #print words
    for word in words:
        if word not in stopwords:
            newline.append(word + " ")
    return ''.join(newline)


def main():
    comments = []
    stopwords = []
    exclude = []
    #companies = []
    #experts = []
    stopwords = getStopwords()
    #companies = getCompanyName()
    experts = getExpertsname()
    for s in stopwords:
        exclude.append(s)
    for e in experts:
        exclude.append(e)
    print exclude
    print exclude.__len__()
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/train/train1.tsv', 'rb'), delimiter='\t')
    for row in reader:
        comment = row.get('comment')
        new_comm = process(comment, exclude)
        comments.append(new_comm)

    print comments.__len__()
    for x in comments:
        print x

    num=1
    for x in comments:
        csvFile = open('/home/varshav/work/PycharmProjects/StockAnalysis/comments.csv', 'a')
        csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
        csvWriter.writerow([num,x])
        num += 1
    '''
    f = open('/home/varshav/work/PycharmProjects/StockAnalysis/comments.txt', 'a')

    for x in comments:
        f.write(str(num))
        f.write(",")
        f.write(x)
        f.write("\n")
    '''
if __name__ == '__main__':
    main()