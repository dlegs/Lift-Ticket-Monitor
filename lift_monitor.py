#!/usr/bin/env python3

import os
import smtplib, ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 

GMAIL = "smtp-relay.gmail.com"
ROOT_EMAIL = "srv@legg.io"
EMAILS = "dylan@legg.io, ajw592@nyu.edu"
TICKET_URL = "https://www.huntermtn.com/plan-your-trip/lift-access/tickets.aspx?startDate=02%2F20%2F2021&numberOfDays=2&ageGroup=Adult"
RESULTS_CLASS = "liftTicketsResults"

def diff(old, new):
    if (old != new):
        return True
    return False

def get_results(driver):
    driver.get(TICKET_URL)
    results = driver.find_element_by_class_name(RESULTS_CLASS).get_attribute("innerHTML")
    return results

def email():
    message = MIMEMultipart("alternative")
    message["Subject"] = "Lift Tickets Are Available"
    message["From"] = ROOT_EMAIL
    message["To"] = EMAILS

    text = "Hey bitch buy your lift tickets"
    html = """\
<html>
  <body>
    <p>Hey bitch buy your <a href="https://www.huntermtn.com/plan-your-trip/lift-access/tickets.aspx?startDate=02%2F20%2F2021&numberOfDays=2&ageGroup=Adult">lift tickets</a> 
    </p>
  </body>
</html>
"""
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    port = 465
    pw = os.getenv('GMAIL_TOKEN')
    try:
        server = smtplib.SMTP_SSL(GMAIL, port)
        server.ehlo()
        server.login(ROOT_EMAIL, pw)
        server.sendmail(ROOT_EMAIL, EMAILS, message.as_string()) 
    except Exception as e:
        print(e)

def main():
    # Seed time and set up headless chrome.
    start = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)  

    # Grab an initial result html so we have something to diff against.
    old = get_results(driver)
    # Now check every minute.
    while True:
        time.sleep(60)
        new = get_results(driver)
        if diff(old, new):
            email()
        else:
            old = new
            print("not new")
    
if __name__ == "__main__":
    main()
