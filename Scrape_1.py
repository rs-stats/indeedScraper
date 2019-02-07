"""
This module scrapes the web www.indeed.es to download job postings. 
It stores the job title and the employer in a table. Then, it copies 
the whole job posting in a separated file and references the file name in the 
table. 

You are welcome to modify it to scrape other jobs postings of any country in 
which indeed operates :-)

"""


# import python libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import sys

# Some job postings contain characters not encoded in ASCII. Thats why 
# I set the encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

# Create a list of webs to scrape. There are only 7 pages of information when
# requesting Data Scientist jobs in www.indeed.es Barcelona. Therefore I just
# copied the  webs to scrape. As you can see there is a clear pattern for all these 
# pages. In case your target job/city has more pages with offers, you just have to
# create a for loop building the name for each page

a = 'https://www.indeed.es/ofertas?q=%22data+scientist%22&l=Barcelona+provincia'
b = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=10'
c = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=20'
d = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=30'
e = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=40'
f = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=50'
g = 'https://www.indeed.es/jobs?q=%22data+scientist%22&l=Barcelona+provincia&start=60'

url = [a,b,c,d,e,f,g]

# Create the file where we will store the resulting dataframe
count = 0
f= open("results.csv","w")
f.write('job_Name, job_Company, job_Description_File\n')
f.close()

# For loop to scrape the web
for udx in url:
    # Open driver 
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    
	# Get the web
    driver.get(udx)
    driver0 = driver
	
	# Scrape the web with beautifulsoup
    soup = BeautifulSoup(driver.page_source)
    
	# Get the number of jobs in the page 
    jobTitles = driver.find_elements_by_class_name("jobtitle")

    print("Length found Links :", len(jobTitles))
    print("*** LOOP ***")

    # For every job obtained in the page, scrape its information
    for idx in range(0,len(jobTitles)-1):
        print("index :", idx)

        driver.execute_script("arguments[0].click();", jobTitles[idx])
       
	    sleep(2) # The response of the browser is too slow, we wait 2 seconds to get the info
        soup = BeautifulSoup(driver.page_source)
        sleep(2)

        print(soup.find("div", {"id": "vjs-jobtitle"}).get_text())
        
		# We get the basic info of the jobs displayed in the web
        jobName = soup.find("div", {"id": "vjs-jobtitle"}).get_text()
        jobCompany = soup.find("span", {"id": "vjs-cn"}).get_text()
        jobDescription = soup.find("div", {"id": "vjs-desc"}).get_text()
        FileDesc = "File_" + str(count) + ".txt"
        
		# Save the results in a CSV file
        f= open("results.csv","a")
        f.write(jobName + "," + jobCompany + "," + FileDesc + "\n")
        f.close()
        
		# Save the job description in a separated file
        f2= open(FileDesc,"w")
        f2.write(jobDescription)
        f2.close()
        
		# update driver
        driver = driver0
        del soup
		
		# increase the counter
        count = count + 1



