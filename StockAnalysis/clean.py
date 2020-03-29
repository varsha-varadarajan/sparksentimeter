# handle negation

import csv

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


def process(line, stopwords):
    newline = []
    neg = ["dont", "not","no"]
    words = line.split(" ")
    #words = [w for w in words if not w in stopwords]
    #print words
    for word in words:
        if word not in stopwords:
            newline.append(word + " ")
    line = ''.join(newline)

    f = []
    words = line.split(" ")
    for word in words:
        if word in neg:
            pos = words.index(word)
            if pos>0 and pos<(len(words)-1):
                words[pos-1] = "!"+words[pos-1]
                words[pos+1] = "!"+words[pos+1]
            else:
                if pos==0:
                    words[pos+1] = "!"+words[pos+1]
                else:
                    if pos==len(words):
                        words[pos-1] = "!"+words[pos-1]
    new_words = []
    for word in words:
        new_words.append(word+" ")
    return ''.join(new_words)


def main():
    comp = []
    comp = getCompanyName()
    print comp
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/labels.csv', 'rb'), delimiter=',')
    csvFile = open('/home/varshav/work/PycharmProjects/Sentiment/cleaned_labels1.csv', 'a')
    csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    for row in reader:
        comment_id = row.get('comment_id')
        comment = row.get('comment')
        text_label = row.get('label')
        new_comm = process(comment,str(comp))
        csvWriter.writerow([text_label, str(new_comm)])

if __name__ == '__main__':
    main()
