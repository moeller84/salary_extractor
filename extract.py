import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_salary_data(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    players = []
    salaries = []

    for row in soup.find_all('tr', class_='teamRow'):
        player = row.find('td', class_='player').text.strip()
        salary = row.find('td', class_='cap info').text.strip()

        players.append(player)
        salaries.append(salary)

    data = {'Player': players, 'Salary': salaries}
    df = pd.DataFrame(data)
    
    return df

def main():
    base_url = 'https://www.spotrac.com/nba/rankings/'
    years = ['2023-24', '2024-25', '2025-26', '2026-27', '2027-28', '2028-29']

    for year in years:
        url = f'{base_url}{year}/cash/'
        df = scrape_salary_data(url)

        if df is not None:
            print(f"\nSalary data for {year}:")
            print(df)

if __name__ == "__main__":
    main()