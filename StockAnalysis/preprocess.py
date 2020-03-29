import os,sys
import csv
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

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
    m=0
    text = "Bajaj Hindusthan may touch Rs 188"
for company in companies:
    value=fuzz.token_set_ratio(text, company)
    print str(value)+" "+company
    if(value>=m):
        m=value
        match=company
print "-----------------------------------------------"
print match + str(m)

nse=""
flag = ""
if company_list.__contains__(match):
    flag= "company"
    with open("/home/admin/PycharmProjects/nse_mapping.csv", 'r') as file:
        reader = csv.reader(file)
        nse = [line[2] for line in reader if line[0] == match]
        final_nse = nse[0]
else:
    if codes_list.__contains__(match):
        flag = "code"
        nse = match
        final_nse = nse

print str(final_nse)
print str(match)
n=0
match1=""
words = text.split()
for word in words:
        similarity = SequenceMatcher(None, word, match)
        print word + " "+ match +" "+str(similarity.ratio())
        if(similarity.ratio()>=n):
            n=similarity
            match1 = word
print str(n)
print match1

words = text.split()
match_words = str(match).split()
print match_words

print len(words)-len(match_words)

matched=""

x=0
for i in range(0,len(words)-len(match_words)+1,1):
    str1=""
    for j in range(0,len(match_words),1):
        str1=str1+" "+words[i+j]
    print str1
    #str1=words[i]+" "+words[i+1]
    sim = SequenceMatcher(None, str1.lower(), match.lower())
    if(sim.ratio()>=x):
        x=sim.ratio()
        matched=str1
    i+=1

print "--------------------------------------"
print matched
print "--------------------------------------"
