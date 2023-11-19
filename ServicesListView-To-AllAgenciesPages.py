import time, json, csv, pandas as pd
from os import path
from unittest import result
from termcolor import colored
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import validators


chrome_options = webdriver.ChromeOptions()
#'''
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#'''
browser = webdriver.Chrome(executable_path=f'chromedriver.exe' ,chrome_options=chrome_options)
browser.maximize_window()

def getTheNumberOfMaxPaggitation(url):
    global browser
    browser.get(url)
    pagginationButtons = browser.find_elements(By.CLASS_NAME, "layout-row.layout-align-center-center.bg-primary-300.text-primary-500.small.mr-8.css-7iu4hk.e17n8fp31")
    lastpagginationButton = pagginationButtons[len(pagginationButtons)-1]
    lastpagginationButtonLink = lastpagginationButton.get_attribute("href")
    # 👇️ {'page': ['43'], 'limit': ['0']}
    dict_result = parse_qs(urlparse(lastpagginationButtonLink).query)
    lastPageNumber = int(dict_result['page'][0])
    return lastPageNumber
    


def getThePageElementsLength(page_id):
    browser.get(f"https://www.sortlist.com/web-development?page={str(page_id)}")
    buttons = browser.find_elements(By.CLASS_NAME, "flex.text-primary-500.py-12.rounded-sm.eqsdnxo0.css-srvo19.e1835u7s1")
    return len(buttons)
    

def sortListScrapeArticleById(article_id:int, page_id:int,browser):
    buttons = browser.find_elements(By.CLASS_NAME, "flex.text-primary-500.py-12.rounded-sm.eqsdnxo0.css-srvo19.e1835u7s1")
    time.sleep(2)
    buttons[int(article_id)-1].click() # -1 Because the list starts with 0
    browser.switch_to.window(browser.window_handles[1])
    scraped_url = browser.current_url
    browser.close()
    # Switch Back To 0
    browser.switch_to.window(browser.window_handles[0])
    # Storing the url to csv
    data = [page_id, article_id, scraped_url, 1]
    with open('SiteDetails.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(data)
    

def main():
    # Get The number of pages from the paggination
    numberOfMaxPaggitation = getTheNumberOfMaxPaggitation("https://www.sortlist.com/web-development")
    print(colored(f'Max Paggination is : {numberOfMaxPaggitation}', 'red'))

    this_page_buttons = 0
    for page_id in range(1,numberOfMaxPaggitation+1):
        if this_page_buttons == 0:
            this_page_buttons_len = getThePageElementsLength(page_id)
        browser.get(f"https://www.sortlist.com/web-development?page={str(page_id)}")
        for site in range(1,this_page_buttons_len+1):
            sortListScrapeArticleById(site, page_id,browser)
            #If last buttons clicked, Then reset the this_page_buttons to 0
            if site == this_page_buttons_len:
                this_page_buttons = 0
    # Export data to json


main()