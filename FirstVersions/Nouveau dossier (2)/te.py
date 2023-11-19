import pandas as pd

# Reading The File and changing to a DataFrame
df = pd.read_csv('DatawithUrls.csv')


detailsPageUrls = ['https://www.sortlist.com/agency/feel-and-clic', 'https://www.sortlist.com/agency/hello-pomelo', 'https://www.sortlist.com/agency/big-boss-studio', 'https://www.sortlist.com/agency/prismalia-agencia-de-marketing-digital', 'https://www.sortlist.com/agency/flying-saucer-studio', 'https://www.sortlist.com/agency/galadrim', 'https://www.sortlist.com/agency/yield-studio', 'https://www.sortlist.com/agency/aji-creative', 'https://www.sortlist.com/agency/le-backyard']
scrapedUrls = ['https://www.feelandclic.com/', 'https://hello-pomelo.com/', 'https://big-boss-studio.com', 'https://prismalia.com/', 'https://flyingsaucer.nyc', 'https://galadrim.fr', 'https://yieldstudio.fr/', 'https://ajicreative.com/', 'https://www.lebackyard.fr']

def storeScrapedUrlToSpecificCorrespondingRow(details_page, scraped_url_from_contact):
    print(f'For the Company : {details_page}')
    print(f'We scraped this website : {scraped_url_from_contact}')
    indexes_of_row_where_this_details_page_exists = df[df['details_page_url'] == details_page].index.values.tolist()
    for id in indexes_of_row_where_this_details_page_exists:
        df.loc[id ,'website'] = scraped_url_from_contact

for i in range(len(detailsPageUrls)):
    storeScrapedUrlToSpecificCorrespondingRow(detailsPageUrls[i], scrapedUrls[i])


#Saving back from the modified DataFrame to csv
df.to_csv('DatawithUrlsModified.csv', index=False)
