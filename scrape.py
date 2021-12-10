from path import driver_path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import numpy as np

path = driver_path

# Function to scrape all league data
def Scrape_All_Leagues():
    website = 'https://www.adamchoi.co.uk/overs/detailed'
    driver = webdriver.Chrome(path)
    driver.get(website)

    all_matches_btn = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
    all_matches_btn.click()

    dropdown = Select(driver.find_element_by_xpath('//select[@id="country"]'))

    idx = 1 # To store index of the current dropdown option

    for opt in dropdown.options: # iterate through all the options of the country dropdown list.    
        country = opt.text

        dropdown.select_by_visible_text(country)
        time.sleep(3) #wait for website to load

        #find all table rows in the webpage
        matches = driver.find_elements_by_tag_name('tr')

        date = []
        home_team = []
        score = []
        away_team = []

        try:
            #Scrape the data in the current page and if an error occurs call the recovery function
            print(f'\nScraping {country} data now....')
            for match in matches:
                date.append(match.find_element_by_xpath('./td[1]').text)
                home = match.find_element_by_xpath('./td[2]').text
                home_team.append(home)
                print(home)
                score.append(match.find_element_by_xpath('./td[3]').text)
                away_team.append(match.find_element_by_xpath('./td[4]').text)

            df = pd.DataFrame({'date': date, 'home': home_team, 'score': score, 'away': away_team})
            df = df.drop_duplicates()
            
            df['date'] = pd.to_datetime(df['date'], dayfirst=True)
            df = df.sort_values(by=['date'])
            df['date'] = df['date'].dt.strftime('%d-%m-%Y')

            if not os.path.exists(f'{country}'):
                try: 
                    os.mkdir(f'{country}')
                except OSError as error: 
                    print(error)

            df.to_csv(f'{country}/{country}_data.csv', index=False)
            print(f'{country} data has finished scraping and has been succesfully stored into CSV file...')
            print('\n')
            idx +=1
        except:
            driver.quit()
            print("There was an error while scraping the data. Scraping will be attempted again")
            return recover_scraping(idx) #call the recovery function

    driver.quit()
    input('\nFunction finished and all data have been scraped successfully. Press "enter" key to continue to main menu.\n')



# Update a specific country league only
def Update_League():
    country = ''
    while country.casefold() != 'N'.casefold():
        country = input('Enter the country you want to update (Enter N to exit function): ')
        if country.casefold() == 'N'.casefold():
            return
        country = country.capitalize()

        website = 'https://www.adamchoi.co.uk/overs/detailed'
        driver = webdriver.Chrome(path)
        driver.get(website)

        all_matches_btn = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
        all_matches_btn.click()

        dropdown = Select(driver.find_element_by_xpath('//select[@id="country"]'))

        try:
            # Check if entered country is in website
            dropdown.select_by_visible_text(country)
        except:
            driver.quit()
            print(f'{country} is not found in the website.')
            continue


        time.sleep(3) #wait for website to load

        matches = driver.find_elements_by_tag_name('tr')

        date = []
        home_team = []
        score = []
        away_team = []

        for match in matches:
            date.append(match.find_element_by_xpath('./td[1]').text)
            home = match.find_element_by_xpath('./td[2]').text
            home_team.append(home)
            print(home)
            score.append(match.find_element_by_xpath('./td[3]').text)
            away_team.append(match.find_element_by_xpath('./td[4]').text)

        df = pd.DataFrame({'date': date, 'home': home_team, 'score': score, 'away': away_team})
        df = df.drop_duplicates()
        
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df = df.sort_values(by=['date'])
        df['date'] = df['date'].dt.strftime('%d-%m-%Y')

        if not os.path.exists(f'{country}'):
            try: 
                os.mkdir(f'{country}')
            except OSError as error: 
                print(error)

        df.to_csv(f'{country}/{country}_data.csv', index=False)
        print(f'\n{country} matches updated successfully.\n')



# Function to scrape all league data in case an error occurs
def recover_scraping(idx):
    website = 'https://www.adamchoi.co.uk/overs/detailed'
    driver = webdriver.Chrome(path)
    driver.get(website)

    all_matches_btn = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
    all_matches_btn.click()

    dropdown = Select(driver.find_element_by_xpath('//select[@id="country"]'))

    for i in range(idx, len(dropdown.options)): # get all the matches for each league in each country    
        country = dropdown.select_by_index(i).text

        dropdown.select_by_index(i)
        time.sleep(3) #wait for website to load

        matches = driver.find_elements_by_tag_name('tr')

        date = []
        home_team = []
        score = []
        away_team = []

        try:
            for match in matches:
                date.append(match.find_element_by_xpath('./td[1]').text)
                home = match.find_element_by_xpath('./td[2]').text
                home_team.append(home)
                print(home)
                score.append(match.find_element_by_xpath('./td[3]').text)
                away_team.append(match.find_element_by_xpath('./td[4]').text)

            df = pd.DataFrame({'date': date, 'home': home_team, 'score': score, 'away': away_team})
            df = df.drop_duplicates()

            df['date'] = pd.to_datetime(df['date'], dayfirst=True)
            df = df.sort_values(by=['date'])
            df['date'] = df['date'].dt.strftime('%d-%m-%Y')
            
            if not os.path.exists(f'{country}'):
                try: 
                    os.mkdir(f'{country}')
                except OSError as error: 
                    print(error)

            df.to_csv(f'{country}/{country}_data.csv', index=False)
        except:
            driver.quit()
            return print("An error occured again while trying to scrape data. Please try again later.")

    driver.quit()
    input('\nFunction finished and all data have been scraped successfully. Press "enter" key to continue to main menu.\n')



# Get the team stats of all countries
def Scrape_All_Team_Stats():
    website = 'https://www.adamchoi.co.uk/results/quick'
    driver = webdriver.Chrome(path)
    driver.get(website)

    dropdown = Select(driver.find_element_by_xpath('//select[@id="countrySelect"]'))

    for opt in filter(lambda opt: opt.text !='', dropdown.options):
        country = opt.text

        dropdown.select_by_visible_text(country)
        time.sleep(3)

        all_matches = driver.find_element_by_xpath('//table[@id="overallTable"]')
        matches = all_matches.find_elements(By.TAG_NAME, 'tbody')

        team = []
        win_ratio = []
        percentage = []

        print(f'\nScraping {country} data...\n')
        for match in matches:
            curr_team = match.find_element_by_xpath('./tr[1]/td[2]').text
            team.append(curr_team)
            ratio = match.find_element_by_xpath('./tr[1]/td[3]').text
            win_ratio.append(ratio)
            perc = str(match.find_element_by_xpath('./tr[1]/td[4]/percentage').get_attribute('percent'))
            percentage.append(perc)
            
        df = pd.DataFrame({'team': team, 'win_ratio': win_ratio, 'win_percentage': percentage})

        if not os.path.exists(f'{country}'):
            try: 
                os.mkdir(f'{country}')
            except OSError as error: 
                print(error)

        df.to_csv(f'{country}/{country}_teams_stats.csv', index=False)
        print(f'Successfully scraped and stored {country} data!')

    input('\nFunction finished and all data have been scraped successfully. Press "enter" key to continue to main menu.\n')



# Get the stats of all the teams of a specific country
def Update_Country_Team_Stats():
    country = input('Enter the country you want to retrieve the matches from (Enter N to exit function): ')
    if country.casefold() == 'N'.casefold():
        return
    website = 'https://www.adamchoi.co.uk/results/quick'
    driver = webdriver.Chrome(path)
    driver.get(website)

    country = country.capitalize()

    dropdown = Select(driver.find_element_by_xpath('//select[@id="countrySelect"]'))
    try:
        dropdown.select_by_visible_text(country)
    except:
        driver.quit()
        print(f'{country.capitalize()} is not found in the website.')
        return

    time.sleep(3)

    all_matches = driver.find_element_by_xpath('//table[@id="overallTable"]')
    matches = all_matches.find_elements(By.TAG_NAME, 'tbody')

    team = []
    win_ratio = []
    percentage = []
    
    for match in matches:
        curr_team = match.find_element_by_xpath('./tr[1]/td[2]').text
        team.append(curr_team)
        ratio = match.find_element_by_xpath('./tr[1]/td[3]').text
        win_ratio.append(ratio)
        perc = str(match.find_element_by_xpath('./tr[1]/td[4]/percentage').get_attribute('percent'))
        percentage.append(perc)
        
    df = pd.DataFrame({'team': team, 'win_ratio': win_ratio, 'win_percentage': percentage})

    if not os.path.exists(f'{country}'):
        try: 
            os.mkdir(f'{country}')
        except OSError as error: 
            print(error)

    df.to_csv(f'{country}/{country}_teams_stats.csv', index=False)

    print(df)
    input(f'\n{country} team stats have been updated successfully. Press "enter" key to continue to main menu.\n')



# Get the upcoming matches of a specific country
def Upcoming_League_Matches():
    country = ''
    while country.casefold() !='N'.casefold():
        country = input('Enter the country you want to retrieve the upcoming matches from (Enter N to exit function): ')
        if country.casefold() == 'N'.casefold():
            return
        
        website = 'https://www.adamchoi.co.uk/overs/detailed'
        driver = webdriver.Chrome(path)
        driver.get(website)

        all_matches_btn = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
        all_matches_btn.click()

        dropdown = Select(driver.find_element_by_xpath('//select[@id="country"]'))

        try:
            country = country.capitalize()
            dropdown.select_by_visible_text(country)
        except:
            driver.quit()
            print(f'\n{country.capitalize()} is not found in the website.\n')
            continue


        time.sleep(3) #wait for website to load

        matches = driver.find_elements_by_tag_name('tr')

        date = []
        home_team = []
        score = []
        away_team = []

        for match in matches:
            if match.find_element_by_xpath('./td[3]').text.startswith('?'):      
                date.append(match.find_element_by_xpath('./td[1]').text)
                home = match.find_element_by_xpath('./td[2]').text
                home_team.append(home)
                score.append(match.find_element_by_xpath('./td[3]').text)
                away_team.append(match.find_element_by_xpath('./td[4]').text)
        
        driver.quit()
        df = pd.DataFrame({'date': date, 'home': home_team, 'score': score, 'away': away_team})

        df = df.drop_duplicates()

        # Sort by date
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df = df.sort_values(by=['date'])
        df['date'] = df['date'].dt.strftime('%d-%m-%Y')

        print(df)
        print(f'\n{country} upcoming matches retrieved successfully.\n')



funcs = []
# Add function names in list except 'recover_scraping' since it is not a function to be selected from user
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__ and str(key) != 'recover_scraping':
        funcs.append(key)

funcs_dict = dict(zip(funcs, range(len(funcs))))
#swap keys with values
funcs_dict = res = dict((v,k) for k,v in funcs_dict.items())

