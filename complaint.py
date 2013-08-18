import urllib2
import csv
import re
import mechanize
import time
import datetime
from BeautifulSoup import *

start_time = time.clock()

br = mechanize.Browser()

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)

### SETTING UP ### 

# Use Pyton's datetime module to get today's date
now = datetime.datetime.now()

today = '%s/%s/%s' %(now.month, now.day, now.year)

# Creates the output file for our scrape
handle = open('complaints.csv', 'a')
outfile = csv.writer(handle)

# Counts the number of records in our CSV file
startingpoint = sum(1 for line in open(r'complaints.csv'))

# Check whether our CSV is empty. If it is, let's add headers.
if startingpoint == 0: 

#Creates an array with our headers
	headers = ['Case Status', 'Date Open', 'Date Closed', 'Respondent', 'Address Line 1', 'Address Line 2', 'City', 'State', 'Zip', 'Business Description', 'Complaint Description', 'Closing Description', 'Reference Number']

	# Appends the headers into the first row of the file, 
	# which would be messy to fish out of the single <td> 
	# into which the agency writes its data (<---- ?!)
	outfile.writerow(headers)


# Open the main page with search prompts
startpage = br.open('https://justice.oregon.gov/complaints/')

# Enter a start date of 1/1/1990, an arbitrary date that predates the first record ...
# to ensure the total returned is the full database.
start_date = '1/1/1990'

#Select Form
br.form = list(br.forms())[0]

#Set controls to writeable
br.form.set_all_readonly(False)

# Enter the start date into the start date field on the odoj search form
br["ctl00$ContentPlaceHolder_main$start_date_InputTextBox"] = start_date

# Enter the today's date into the end date field on the odoj search form
br["ctl00$ContentPlaceHolder_main$end_date_InputTextBox"] = today

response = br.submit("ctl00$ContentPlaceHolder_main$search_consumer_complaints")

response_read = response.read()

response_soup = BeautifulSoup(response_read)

response_text = response_soup.find("span", {'id': 'ctl00_ContentPlaceHolder_main_lblDisplaying'}).text

response_parsed = re.findall('(?<=of)(.*?)(?=items)', response_text)

endingpoint = int(response_parsed[0])+1


### LET'S GET STARTED ###

print "According to our count, you have already scraped", startingpoint-1, "records."

print "The database has a total of", endingpoint-1, "records."

please_continue = raw_input("Do you wish to scrape the rest? (type 'yes' or 'no') ")

if please_continue == "yes" or please_continue == "YES" or please_continue == "Yes" :

	#Total number of records, taken from a basic check using the agency's query tool
	complaint_numbers = range(startingpoint, endingpoint)

	casetotal = len(complaint_numbers)


	list_id = [num for num in complaint_numbers]

	for num in list_id:
		    
		cnum = str(num) #convert from tuple

		# The base address we'll be working from
		address = ('https://justice.oregon.gov/complaints/ComplaintsDetails.aspx?FFWebID=' + cnum)

		# Open the HTML file and turn it into a BeautifulSoup object for parsing
		html = br.open(address)

		soup = BeautifulSoup(html)

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

	# Normally we would subtract one to account for row headers, but have to add one anyway
	# because we need to start the scrape at 1 after the row count
		rowcount = sum(1 for line in open(r'complaints.csv'))
		print (int(stage_time-start_time)/60),":",(int(stage_time-start_time)%60)," #",cnum,"/", casetotal, " scraped"
			
		# Pause for a second to be polite to the server 
		time.sleep(1)


	### AND WE'RE DONE ###
	stop_time = time.clock()
	print "YOUR SCRAPE IS COMPLETE ... "
	print "AND IT ONLY TOOK",(int(stop_time-start_time/60),"minutes and ", (int(stop_time-start_time)%60), "seconds")
