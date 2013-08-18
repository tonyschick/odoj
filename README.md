oregon consumer complaints
====

Python scraper for Oregon Department of Justice Consumer Complaints  
[https://justice.oregon.gov/complaints/](https://justice.oregon.gov/complaints/)


## How to use 

1. Clone the repo or download the files. 

2. Make sure Python and the libraries used here are installed on your computer  
[http://www.python.org/download/](http://www.python.org/download/)

* Install [mechanize](http://wwwsearch.sourceforge.net/mechanize/)
* Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

3. Open your terminal/command line

4. Navigate to the folder containing the files  

		$ cd ~/myfolder/myotherfolder

5. Run the script  

		$ python complaint.py

6. The script will count the number of lines in the complaint.csv file in your directory. It will also query the ODOJ database to determine the total number of records online, then compare the two. It will look like this on the command line:

		According to our count, you have already scraped 64128 records.
		The database has a total of 64146 records.
		Do you wish to scrape the rest? (type 'yes' or 'no') yes

7. Tell the scraper you whether you want the rest of the records. Type yes and it will start. It will keep track of each record and when it was scraped.

		Do you wish to scrape the rest? (type 'yes' or 'no') yes

		0 : 0  # 1 / 64129 scraped
		0 : 0  # 2 / 64129 scraped
		0 : 0  # 3 / 64129 scraped
		0 : 0  # 4 / 64129 scraped
