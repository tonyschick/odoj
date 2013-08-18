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

response_total = int(response_parsed[0])

print response_total


