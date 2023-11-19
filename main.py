#Importing Dependencies
import time, json, csv, pandas as pd
from datetime import datetime
from os import path
from unittest import result
from termcolor import colored
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import validators
from AllServices import AllServices

#Important Variables that will shape the direction of the program
serviceAgenciesURL = "https://www.sortlist.com/web-development"


# Selenium Browser Configuration
chrome_options = webdriver.ChromeOptions()
    #'''
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
    #'''
browser = webdriver.Chrome(executable_path=f'chromedriver.exe' ,chrome_options=chrome_options)
browser.maximize_window()

# Base Almost Non changing Variables
# Setting The time of program execution
time_of_program_execution = datetime.now().strftime("%m-%d-%Y, %H-%M-%S")
AllServices = ['Advertising' ,'Amazon PPC' ,'Content Strategy' ,'Corporate Advertising' ,'Creative' ,'Digital' ,'Digital Strategy' ,'Facebook Advertising' ,'Inbound Lead Generation' ,'LinkedIn Ads' ,'Marketing' ,'Marketing Strategy' ,'Mobile Marketing' ,'Mobile SEO' ,'Online Advertising' ,'PPC Marketing' ,'Retail Consulting' ,'Search Marketing' ,'SEO' ,'SEO Audit' ,'Social Media' ,'Social Media Growth' ,'Web Strategy' ,'Youtube Advertising' ,'Creative & Visual' ,'3D Animation' ,'Flyer Conception' ,'Graphic Design' ,'Logo Graphic Design' ,'Motion Design' ,'Movie' ,'Packaging' ,'SEO Copywriting' ,'Development & Product' ,'Android Development' ,'CMS Development' ,'Digital Design' ,'Drupal Development' ,'E-commerce' ,'Ergonomy (UX/UI)' ,'iOS Development' ,'Javascript Development' ,'Landing Page Design' ,'Magento Development' ,'Mobile App' ,'PHP Development' ,'Prestashop Development' ,'React Native Development' ,'Shopify' ,'Software' ,'Software Development' ,'Symfony Development' ,'Web Application' ,'Website Creation' ,'WooCommerce Integration' ,'Wordpress Development' ]


# Function
def getTheNumberOfMaxPaggitation(url):
    browser.get(url)
    pagginationButtons = browser.find_elements(By.CLASS_NAME, "layout-row.layout-align-center-center.bg-primary-300.text-primary-500.small.mr-8.css-7iu4hk.e17n8fp31")
    lastpagginationButton = pagginationButtons[len(pagginationButtons)-1]
    lastpagginationButtonLink = lastpagginationButton.get_attribute("href")
    # 👇️ {'page': ['43'], 'limit': ['0']}
    dict_result = parse_qs(urlparse(lastpagginationButtonLink).query)
    lastPageNumber = int(dict_result['page'][0])
    print(colored(f'This Service has {lastPageNumber} pages availble !', 'red'))
    return lastPageNumber

# Function
def getThePageElementsLength(page_id):
    browser.get(f"https://www.sortlist.com/web-development?page={str(page_id)}")
    buttons = browser.find_elements(By.CLASS_NAME, "flex.text-primary-500.py-12.rounded-sm.eqsdnxo0.css-srvo19.e1835u7s1")
    return len(buttons)

# Function
def ScrapeArticle(articleID:int, pageID:int):
    #Outside Scraping (From The ListViewPage)
    containerBox = browser.find_elements(By.CLASS_NAME, "flex-100.flex-sm-50.flex-gt-sm-33.css-ffhm6p.eqsdnxo3")[int(articleID)-1]
    # Clicking the box will redirect to Details view page
    containerBox.click()
    agency_name = containerBox.find_elements(By.CLASS_NAME, "pt-16.bold.text-truncate")[0].get_attribute('innerText')


    # Inside Scraping (From The DetailsViewPage)
    browser.switch_to.window(browser.window_handles[1])

    details_page_url = browser.current_url
    # Services
    servicesBox = browser.find_elements(By.CLASS_NAME, "bold.h6.text-truncate")
    services = []
    for service in servicesBox:
        services.append(service.get_attribute('innerText'))

    # Switch Back To ListViewPage
    browser.close()
    browser.switch_to.window(browser.window_handles[0])


    # Storing data
    data = [agency_name,pageID, articleID, details_page_url, 1,services]
    '''
    with open('SiteDetails.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerow(data)
    '''
    print(data)

# Main Fn
def main():
    # Get The number of pages from the paggination
    availblePagesForService = getTheNumberOfMaxPaggitation(serviceAgenciesURL)

    numberOfArticles = None

    for pageID in range(1,availblePagesForService+1):
        if numberOfArticles == None:
            this_page_numberOfArticles = getThePageElementsLength(pageID)
        
        # Load Services Page Number X
        browser.get(f"{serviceAgenciesURL}?page={str(pageID)}")
        
        for articleID in range(1,this_page_numberOfArticles+1):
            ScrapeArticle(articleID, pageID)
            if articleID == this_page_numberOfArticles:
                numberOfArticles = None

    return None


main()