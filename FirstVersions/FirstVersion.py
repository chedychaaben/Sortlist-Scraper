import time, json
from os import path
from unittest import result
from termcolor import colored
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

def getThePageElementsLength(page_id):
    #Remember, Each time we will be opening another browser for each website
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(executable_path=f'chromedriver.exe' ,chrome_options=chrome_options)
    browser.maximize_window()
    browser.get(f"https://www.sortlist.com/web-development?page={str(page_id)}")
    buttons = browser.find_elements(By.CLASS_NAME, "flex.text-primary-500.py-12.rounded-sm.eqsdnxo0.css-srvo19.e1835u7s1")
    return len(buttons)
    

def sortListScraper(page_id:int, article_id:int):
    #Remember, Each time we will be opening another browser for each website
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(executable_path=f'chromedriver.exe' ,chrome_options=chrome_options)
    browser.maximize_window()
    browser.get(f"https://www.sortlist.com/web-development?page={str(page_id)}")
    buttons = browser.find_elements(By.CLASS_NAME, "flex.text-primary-500.py-12.rounded-sm.eqsdnxo0.css-srvo19.e1835u7s1")
    time.sleep(5)
    buttons[article_id-1].click() # -1 Because the list starts with 0
    browser.switch_to.window(browser.window_handles[1]) # Switch to the details page
    time.sleep(5)
    browser.find_elements(By.CLASS_NAME, "text-center.mt-8.btn.btn-light.btn-md.btn-primary.css-e0dnmk.e1835u7s1")[0].click()
    time.sleep(5)
    browser.switch_to.window(browser.window_handles[2]) # Switch to the website windows
    time.sleep(5)
    scraped_url = browser.current_url
    if '?' in scraped_url :
        scraped_url = scraped_url.split('?')[0]
    print(scraped_url)
    # Creatin the Object for this url
    newObj = {
        'url' : scraped_url
    }
    # Open Json Read it's data and append to the list then reinsert new list there
        # Check if file exists
    filename = 'sortList.json'
    if path.isfile(filename) is False:
        raise Exception("File not found")
    
        # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
        
    listObj.append(newObj)

    with open('sortList.json', 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))

    browser.quit()

def main():
    this_page_buttons = 0
    for page_id in range(1,43+1):
        if this_page_buttons == 0:
            this_page_buttons_len = getThePageElementsLength(page_id)
        for site in range(1,this_page_buttons_len+1):
            sortListScraper(page_id,site)
            #If last buttons clicked, Then reset the this_page_buttons to 0
            if site == this_page_buttons_len:
                this_page_buttons = 0
    # Export data to json


main()