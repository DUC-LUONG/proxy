# Standard Python Library
import os
import sys
import time
import json
import pandas as pd
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#3rd library
import httplib2
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import discovery

    
#Custom Google Sheet ID   
sheet_id = '1CnbXnhbpbrRBIMExjPYXXH61HziGB4sTR0O-VImlv8g'

# Desgin Class for Spread sheet handle
class GgSheet:
    def __init__(self, spreadsheet_id, client_key):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = client.Credentials.new_from_json(json.dumps(client_key))
    
    # Define function write data to google sheet
    def write_google_sheets(self, ran, dataframe, header=True):
        print('Start write gg sheet at range {} with dataframe'.format(ran))

        http = (self.credentials).authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')

        service = discovery.build(
                    'sheets', 'v4', 
                    http=http,
                    discoveryServiceUrl=discoveryUrl,
                    cache_discovery=False
                    )

        if header == True:
            values = [list(dataframe.columns)]
            values += dataframe.values.tolist()
        else:
            values = dataframe.values.tolist()
        data = [
            {
                'range': ran,
                'values': values
            },
        ]
        body = {
            'valueInputOption':'RAW',
            'data':data
        }

        result = service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id,body = body).execute()
        print('done')
        return 1


    #  Define function clear data from a google sheet
    def clear_google_sheets(self, ran):
        print('Start clear gg sheet at range {}'.format(ran))
        http = (self.credentials).authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        clear_values_request_body = {}
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
        request = service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id, range=ran, body=clear_values_request_body
                )
        response = request.execute()
        return 1

if __name__ == '__main__':

    #Get configuration
    chromedriver_path = os.path.abspath('chromedriver')
    ggsheet_client_path = os.path.abspath('google_client.json')

    #Open client key
    with open(ggsheet_client_path) as client_file:
        JSON_DATA = json.load(client_file)
    
    ggsheet = GgSheet('1CnbXnhbpbrRBIMExjPYXXH61HziGB4sTR0O-VImlv8g', JSON_DATA)
    print('CLIENT', ggsheet.credentials)

    # Open display on virtual display
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    #Start driver for chrome
    #Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    
    #URL BASE
    URL_BASE = 'https://play.google.com/store/search?q&c=apps'
    HOSTNAME_BASE = 'https://play.google.com/store/apps/details'

    #List keyword
    urls = [
        {
		"url": "https://play.google.com/store/search?q=rdp&c=apps",
		"type": "RDP"
	},
	{
		"url": "https://play.google.com/store/search?q=remote%20desktop%20protocol&c=apps",
		"type": "RDP"
	},
	{
		"url": "https://play.google.com/store/search?q=control%20android&c=apps",
		"type": "RDP"
	},
	{
		"url": "https://play.google.com/store/search?q=hide%20apps&c=apps",
		"type": "HIDEAPP"
	},
	{
		"url": "https://play.google.com/store/search?q=superuser&c=apps",
		"type": "ROOT"
	},
	{
		"url": "https://play.google.com/store/search?q=root%20manager&c=apps",
		"type": "ROOT"
	},
	{
		"url": "https://play.google.com/store/search?q=hide%20root&c=apps",
		"type": "ROOT"
	},
	{
		"url": "https://play.google.com/store/search?q=hiding%20root&c=apps",
		"type": "ROOT"
	}]

    #Manipulate
    count = 0
    try:
        for url in urls:
            
            is_final = False
            #Create a instance webdriver
            driver = webdriver.Chrome(
                executable_path=chromedriver_path,
                chrome_options=chrome_options
                )

            #Fetch ur;
            print(url)
            driver.get(url.get('url')) 
            process_list = []
            url_list = []

            PAUSE_TIME = 2
            last_height = driver.execute_script('return document.body.scrollHeight')
            while True:
                hrefs = driver.find_elements_by_tag_name('a')
                for href in hrefs:

                    link = href.get_attribute('href')
                    URI = link.split('?')
                    hostname = URI[0]

                    if hostname == HOSTNAME_BASE and link not in url_list:

                        pattern = '//a[contains(@href, "{}")]//div'.format(
                                     link.replace('https://play.google.com', '')
                                     )

                        description = driver.find_element_by_xpath(pattern)

                        process_list.append([link, description.get_attribute('title'), url.get('type')])
                        url_list.append(link)

                #Scroll web page
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

                #Sleep wait for scroll 
                time.sleep(PAUSE_TIME)
                
                #Get nw height of page after scrolling
                new_height = driver.execute_script('return document.body.scrollHeight')
                
                #Break loop of scroll to the end of web page
                if new_height == last_height: 
                    if is_final:
                        break
                    else:
                        is_final = True
                else:
                    last_height = new_height
            
            #Create data and save into ggsheet
            df = pd.DataFrame(process_list)
            ggsheet.clear_google_sheets(ran='{}!A1:Z1000'.format(str(count + 1)))
            ggsheet.write_google_sheets(ran='{}!A1:Z1000'.format(str(count + 1)), dataframe=df, header=False)
            count +=1

            # Close current driver
            driver.close()
            
    finally:
        display.stop()
    


