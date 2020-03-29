from nsepy import get_history
from datetime import datetime
from datetime import date
import pandas as pd
import workdays
import numpy as np
#import quandl
import re
import csv

def main():
	reader = csv.DictReader(open('/home/varshav/Desktop/final_train1.tsv', 'rb'), delimiter='\t')
	for row in reader:
		csvFile = open('/home/varshav/Desktop/final_train_with_rating.tsv', 'a')
        	csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n')
		total_rating = 0
		prediction = -1
		tgt = -1
		comment_id = row.get('comment_id')
		expert_id = row.get('expert_id')
		comment = row.get('comment')
		date_text = row.get('date')
		sentiment = row.get('sentiment')
		code = row.get('company')
		y,m,d = date_text.split("-")
		y = int(y)
		m = int(m)
		d = int(d)
		today = enddate = date(y,m,d)
		#print today	

		comment = re.sub('-', ' ', comment)
		words = comment.lower().split(" ")

		for i,word in enumerate(words):
    			if word == "rs":
				try:
					num = float(words[i+1])
	        			tgt = float(words[i+1])
        				break
				except:
					continue
    			try:
         			num=float(word)
         			tgt = float(word)
         			break
    			except:
         			continue

		print "Comment id: %s  code: %s sentiment: %s Target: %s" %(comment_id,code,sentiment,str(tgt))
		
		if code == 'NIFTY':
			'''
			for i,word in enumerate(words):
				try:
         				num=int(word)
         				tgt = int(word)
         				break
    				except:
         				continue
         		'''	
			todays_price = current = get_history(symbol=code,start=today,end=today,index=True)
		        final_today = today
			#print "Todays value: %s" %(str(todays_value))
			
			tries = 0
			while todays_price.empty and tries<5:
				tries+=1
        			prev_day = workdays.workday(today,-1)
        			todays_price = get_history(symbol=code,start=prev_day, end=prev_day,index=True)
        			final_today = prev_day	
			if tries == 5:
				prediction = 1
				total_rating = 80
				csvWriter.writerow([comment_id,expert_id,date_text,comment,code,sentiment,tgt,prediction,total_rating])
				continue
    			#print todays_price
    			todays_value = float(np.max(todays_price['Close']))
			#todays_low = float(todays_price['Low'])
			print "code: %s sentiment: %s Target: %s Todays value: %s" %(code,sentiment,str(tgt),str(todays_value))

			tries = 0
    			while current.empty and tries<5:
        			tries+=1
        			enddate = workdays.workday(enddate,1)
        			current = get_history(symbol=code,start=enddate, end=enddate,index=True)

    			if tries == 5:
				prediction = 1
				total_rating = 80
				csvWriter.writerow([comment_id,expert_id,date_text,comment,code,sentiment,tgt,prediction,total_rating])
				continue
    			w = workdays.workday(enddate,2)   # next 2 working days
    			valid_till = w
    			values = get_history(symbol=code,start=enddate, end=w,index=True)
    			#print values
    			max_in_next_5_days = float(np.max(values ['High']))
    			min_in_next_5_days = float(np.max(values ['Low']))
			print "code: %s sentiment: %s Target: %s Todays value: %s Max:%s Min:%s" %(code,sentiment,str(tgt),str(todays_value),str(max_in_next_5_days),str(min_in_next_5_days))
		else:
			'''
			for i,word in enumerate(words):
    				if word == "rs":
        				tgt = float(words[i+1])
        				break
			'''
			#print code
			todays_price = current = get_history(symbol=code,start=today,end=today)
			#print todays_price
    			final_today = today
			#print "Todays value: %s" %(str(todays_value))

			tries = 0
			while todays_price.empty and tries<5:
        			tries+=1
				prev_day = workdays.workday(today,-1)
				todays_price = get_history(symbol=code,start=prev_day, end=prev_day)
			        final_today = prev_day

    			if tries == 5:
				prediction = 1
				total_rating = 80
				csvWriter.writerow([comment_id,expert_id,date_text,comment,code,sentiment,tgt,prediction,total_rating])
				continue
    			#print todays_price
    			todays_value = float(np.max(todays_price['Close']))
    			#print todays_value
			print "code: %s sentiment: %s Target: %s Todays value: %s" %(code,sentiment,str(tgt),str(todays_value))

			tries = 0
    			while current.empty and tries<5:
        			tries+=1
        			enddate = workdays.workday(enddate,1)
        			current = get_history(symbol=code,start=enddate, end=enddate)

    			if tries == 5:
				prediction = 1
				total_rating = 80
				csvWriter.writerow([comment_id,expert_id,date_text,comment,code,sentiment,tgt,prediction,total_rating])
				continue

    			w = workdays.workday(enddate,4)   # next 5 working days
    			valid_till = w

    			values = get_history(symbol=code,start=enddate, end=w)
    			#print values
    			max_in_next_5_days = float(np.max(values ['High']))
    			min_in_next_5_days = float(np.max(values ['Low']))
			print "code: %s sentiment: %s Target: %s Todays value: %s Max:%s Min:%s" %(code,sentiment,str(tgt),str(todays_value),str(max_in_next_5_days),str(min_in_next_5_days))
		c=0
		if sentiment == "buy" or sentiment == "hold":
			if max_in_next_5_days < todays_value:
				base_rating = 0
				c =1
    				rating = 0
				prediction = 0
			else:
				prediction = 1
				base_rating = 60
				if tgt == -1:
					c=2
					rating = 0
				else:
    					if max_in_next_5_days >= tgt:
						c=3
        					rating = 40
    					else:
						c=4
						num = abs(tgt - todays_value)
						denom = float(num) + abs(float(tgt) - float(max_in_next_5_days))
						rating = (num/denom) * 40
						'''
					        ran = abs(tgt - todays_value)
					        diff = float(max_in_next_5_days)- float(todays_value)
					        rating = (diff/float(ran))*100
						if rating == 0:
							rating = 50
						'''
			total_rating = base_rating + rating
		#end if
		else:
			if sentiment == "sell":
				if min_in_next_5_days >= todays_value:
					base_rating = 0
					c = 10
    					rating = 0
					prediction = 0
				else:
					prediction = 1
					base_rating = 60
					if tgt == -1:
						c=20
						rating = 0
					else:
    						if min_in_next_5_days <= tgt:
							c=30
        						rating = 40
    						else:
							c=40
							num = abs(todays_value - tgt)
							denom = float(num) + abs(float(min_in_next_5_days) - float(tgt))
							rating = (num/denom) * 40
							
							'''
					        	ran = abs(tgt - todays_value)
					        	diff = float(todays_value) - float(max_in_next_5_days)
					        	rating = (diff/float(ran))*100
							if rating == 0:
								rating = 50					
							'''
				total_rating = base_rating + rating
		print "code: %s sentiment: %s Target: %s Todays value: %s Max:%s Min:%s C:%s" %(code,sentiment,str(tgt),str(todays_value),str(max_in_next_5_days),str(min_in_next_5_days),str(c))
        	csvWriter.writerow([comment_id,expert_id,date_text,comment,code,sentiment,tgt,prediction,total_rating])
		
		
if __name__ == '__main__':
    main()
