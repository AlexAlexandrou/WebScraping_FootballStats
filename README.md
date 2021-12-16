# Web Scraping Football statistics  
In this project, ***Selenium*** is used to scrape football data and store it into csv files. Additionally, ***Pandas*** is used to organize the scraped data into the csv files and display them clearly to the user.

The program consists of 8 functions which the user can choose from:

0. **Scrape_All_Leagues**: All the data about the match results and upcoming matches of each country are scraped and stored into a csv file.
    - **Note**: This function should be executed first in order to download the data needed to execute the offline functions.
<br/><br/>

1. **Update_League**: Similar to All_leagues, it gets all the league data but only for a specific country, which is selected by the user.

2. **Scrape_All_Team_Stats**: The data regarding the win/lose ratio of all the teams in all available countries is scraped and put into .csv files, one for each country.

3. **Update_Country_team_Stats**: Similarly to All_Team_Stats, it updates win/lose ratio data of the teams in a selected country by the user.

4. **Upcoming_League_Matches**: The upcoming future matches in a specific country are scraped. The country is selected by the user.

5. **Get_Team_Matches**: All the matches of a specific team and the match results are retrieved from the local csv files. The user enters the country and then the team they want to retrieve. Also, the matches of each selected team are stored into a csv file under its country folder.

6. **Get_Upcoming_Matches**: Similarly to UpcomingLeagueMatches, it retrieves the upcoming matches of a specific country but from the local data that was scraped already. The user can also filter the results to show only a specific team's upcoming matches.

7. **Get_Team_Stats**: Similarly to CountryTeamMatches, it retrieves the win/lose ratio data of each team in a country, which is selected from the user. The difference is that it does so from the data that was scraped already. If the data was not scraped previously, the user is asked if they want to do so.
<br></br>

## Requirements

- **Selenium**
- **Pandas**
- **Chrome Driver**
    - **Note**: After downloading the Chrome Driver, uncomment the *driver_path* variable and set it to the path of your driver in the *path.py* file. You can also use other browser drivers but you will need to replace the *Chrome* calls in the *scrape.py* file with the browser of your driver.