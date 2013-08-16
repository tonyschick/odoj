import urllib2
import csv
import re
import mechanize
import time
from BeautifulSoup import *

start_time = time.clock()

br = mechanize.Browser()

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)



# Creates the output file for our scrape
handle = open('complaints.csv', 'a')
outfile = csv.writer(handle)

#Creates an array with our headers
headers = ['Case Status', 'Date Open', 'Date Closed', 'Respondent', 'Address Line 1', 'Address Line 2', 'City', 'State', 'Zip', 'Business Description', 'Complaint Description', 'Closing Description', 'Reference Number']

# Appends the headers into the first row of the file, 
# which would be messy to fish out of the ridiculous single table cell (?!) 
# into whichthe agency writes its data
outfile.writerow(headers)

#Total number of records, taken from a basic check using the agency's query tool
complaint_numbers = range(64129)

casetotal = len(complaint_numbers)


list_id = [num for num in complaint_numbers]

for num in list_id:
	    
	cnum = str(num) #convert from tuple

	# The base address we'll be working from
	address = ('https://justice.oregon.gov/complaints/ComplaintsDetails.aspx?FFWebID=' + cnum)

	# Open the HTML file and turn it into a BeautifulSoup object for parsing
	html = br.open(address)

	soup = BeautifulSoup(html)
	counter = 0
	#Find the <td> tag that the data we want rests in
	for td in soup.findAll('td'):
	
	#Create an array that we'll fill with the data we scrape
		output_row = []

	# Each field of data is presented within a <span> tag, so we parse the html file for that <span>
		complaints = td.findAll('span')

	# If the length of the span is greather than zero, 
	# then append the text of all the spans to the output row array
		if len('span') > 0:
				
			for c in complaints:

				output_row.append(c.text)
				
		
	# If the length of the output row we just created is greather than zero,
	# Then append it onto the csv file we created.
			if len(output_row) > 0:
				outfile.writerow(output_row)

#Time Keeping and Process Status
	stage_time = time.clock()
	rowcount = sum(1 for line in open(r'/Users/anthonyschick/complaints.csv'))
	print (int(stage_time-start_time)/60),":",(int(stage_time-start_time)%60)," #",cnum,"/", casetotal
		
	# Pause for a second to be polite to the server 
	time.sleep(1)


### AND WE'RE DONE ###
stop_time = time.clock()
print "YOUR SCRAPE IS COMPLETE ... "
print "AND IT ONLY TOOK",(int(stop_time-start_time/60),"minutes and ", (int(stop_time-start_time)%60), "seconds")
