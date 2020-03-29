# prepare input for bayes file

import csv

reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/Sentiment/labels.csv', 'rb'), delimiter=',')
csvFile = open('/home/varshav/work/PycharmProjects/Sentiment/1.csv', 'a')
csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
for row in reader:
    comment = row.get('comment')
    text_label = row.get('label')
    new_comm = str(comment)
    if text_label == "buy":
        label = 1
    else :
        if text_label == "sell":
            label = 2
        else:
            if text_label == "hold":
                label = 3
    csvWriter.writerow([label, str(new_comm)])
