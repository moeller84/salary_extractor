from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_player_salary(driver, player_url):
    driver.get(player_url)
    time.sleep(2)  # Add a delay to allow the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    player_name = soup.find('h1', {'class': 'team-name'}).text.strip()
    salaries = []

    salary_tables = soup.find_all('table', {'class': 'datatable'})
    for table in salary_tables:
        season = table.find_previous('h2').text.strip()
        salary_data = []

        for row in table.find_all('tr')[1:]:
            columns = row.find_all(['th', 'td'])
            player_salary = columns[2].text.strip()
            salary_data.append({'Player': player_name, 'Season': season, 'Salary': player_salary})

        salaries.extend(salary_data)

    return salaries

def scrape_salaries(base_url, current_year, seasons_forward):
    driver = webdriver.Chrome("./chromedriver")  # You may need to download the ChromeDriver executable and provide the path
    df_list = []

    for year in range(current_year, current_year + seasons_forward + 1):
        url = f"{base_url}/{year}/"
        driver.get(url)
        time.sleep(2)  # Add a delay to allow the page to load

        player_links = driver.find_elements_by_css_selector('.team-name a')
        player_urls = [link.get_attribute('href') for link in player_links]

        for player_url in player_urls:
            player_salaries = get_player_salary(driver, player_url)
            df_list.extend(player_salaries)

    driver.quit()
    return pd.DataFrame(df_list)

# Example usage
base_url = 'https://www.spotrac.com/rankings/nba/cap-hit/'
current_year = 2024
seasons_forward = 5
result_df = scrape_salaries(base_url, current_year, seasons_forward)

# Display the resulting DataFrame
print(result_df)
