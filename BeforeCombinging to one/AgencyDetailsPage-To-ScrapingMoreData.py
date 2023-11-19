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

errors_urls = []

def load_csv_dataframe():
    # Reading The File and changing to a DataFrame
    df = pd.read_csv('ScrapedData/AllDetailsPagesUrls.csv')
    # Getting the row details_page_url data and changing all the values to a list
    return df

def main():
    df = load_csv_dataframe()
    urls = df['details_page_url'].values.tolist()
    # Was in 973
    #urls = urls[973:]
    #
    for this_details_page in urls:
        browser.get(this_details_page)
        try:
            scraped_url_from_contact = browser.find_elements(By.CLASS_NAME, "btn.small.text-truncate.btn-default.btn-secondary.btn-md.flex.text-left.px-16.css-e0dnmk")[0].get_attribute('innerHTML')
        except:
            scraped_url_from_contact = ""
            print(colored(f'Error en {this_details_page}', 'red'))
        if not validators.url(scraped_url_from_contact):
            errors_urls.append(this_details_page)
        indexes_of_row_where_this_details_page_exists = df[df['details_page_url'] == this_details_page].index.values.tolist()
        for id in indexes_of_row_where_this_details_page_exists:
            df.loc[id ,'website'] = scraped_url_from_contact
            print(colored(f'Id {id} Modified with this link ({scraped_url_from_contact})', 'green'))
        #Save New DF
        #Saving back from the modified DataFrame to csv
        df.to_csv('ScrapedData/AllDetailsPagesUrls.csv', index=False)
    print(colored('The Errors urls','red'))
    print(colored(errors_urls,'red'))
    

main()