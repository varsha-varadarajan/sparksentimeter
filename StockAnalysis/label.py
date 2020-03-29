import csv
import re

def main():
    comment_nums = []
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/comments.csv', 'rb'), delimiter=',')
    csvFile = open('/home/varshav/work/PycharmProjects/StockAnalysis/labels.csv', 'a')
    csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    label = "buy"
    for row in reader:
        comment_id = row.get('comment_id')
        comment = row.get('comment')
        new_comm = str(comment)
        obj = re.search(r'uncertain',new_comm)
        if obj:
            print comment_id
            print new_comm
            comment_nums.append(comment_id)
            csvWriter.writerow([comment_id, label, str(new_comm)])
    print comment_nums

    reader1 = csv.DictReader(open('/home/varshav/work/PycharmProjects/StockAnalysis/labels/comments.csv', 'rb'), delimiter=',')
    csvFile1 = open('/home/varshav/work/PycharmProjects/StockAnalysis/labels/comments1.csv', 'a')
    csvWriter1 = csv.writer(csvFile1, delimiter=',', lineterminator='\n')
    for row in reader1:
        comment_id1=row.get('comment_id')
        new_comm_id = str(comment_id1)
        comment1 = row.get('comment')
        if new_comm_id not in comment_nums:
            csvWriter1.writerow([new_comm_id, comment1])

if __name__ == '__main__':
    main()