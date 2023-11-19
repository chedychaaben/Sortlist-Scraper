

def structureOldFileAndRecievelistOfObjects():
    # Getting all linesIndexes of each details page in a list of objects
    # Desired list of objects = [
    #   {
    #    'url' : 'https://whatever.com',
    #    'ids' : '['The number of line where it was founded in','The number of line where it was founded in']
    #   }
    #]
    with open('ScrapedData/DatawithUrls.csv', 'r', newline='') as f:
        listOfObjects = []
        csvreader = list(csv.reader(f))
        
        for i in range(len(csvreader)):
            row = csvreader[i]
            this_url = row[2]

            # Getting all above this line urls
            the_above_urls = []
            for obj in listOfObjects:
                the_above_urls.append(obj['url'])

            # Check if there is an existing object with this key in the before objects
            if this_url not in the_above_urls :
                # Now we will append to the list
                listOfObjects.append({
                    'url' : this_url,
                    'ids' : [i]
                })
            else:
                #There is an object with this so we must append to its ids list this i
                this_obj=None
                for obj in listOfObjects:
                    if obj['url'] == this_url:
                        this_obj = obj
                        break
                # Add to its ids list this i 
                if this_obj != None:
                    this_obj['ids'].append(i)
    return listOfObjects
listOfObjects = structureOldFileAndRecievelistOfObjects()

def storeScrapedUrlToSpecificCorrespondingRow(details_page, scraped_url_from_contact):
    print(f'For the Company : {details_page}')
    print(f'We scraped this website : {scraped_url_from_contact}')
    # If the scraped url is not in a valid format
    if not validators.url(scraped_url_from_contact):
        errors_urls.append(details_page)
    '''
    # Storing to the csv 
    # Getting the indexes of this_details_page
    these_indexes = []
    for obj in listOfObjects:
        if obj['url'] == details_page:
            these_indexes = obj['ids']
    
    for index in these_indexes:
        #Now we open the csv and add scraped_url to the 4th column
        with open('ScrapedData/DatawithUrls.csv', 'r+', newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            writer = csv.writer(f, delimiter=',', quotechar='"')
            this_row = list(csv.reader(f))[index]
            for row in reader:
                row[1] = row[1].title()
                writer.writerow(row)
    '''