# %%
import requests
from bs4 import BeautifulSoup

url = 'https://www.spotrac.com/rankings/nba/cap-hit/2024/'
data = {
    'ajax': 'true',
    'mobile': 'false'
}

soup = BeautifulSoup(requests.post(url, data=data).content, 'html.parser')

# %%

# Parse the HTML content
salary_list = [element.text.strip() for element in soup.find_all('span', class_="info")]
player_name_list = [element.text for element in soup.find_all('h3')]



# %%
import pandas as pd
import timeit

# Example DataFrame
data = {'player_name': player_name_list,
        'salary_cap_hit': salary_list}
df = pd.DataFrame(data)

# %%
fantrax_df = pd.read_csv(
    "FantraxPlayers_g2m7u071ljznr6zx.csv", 
    delimiter=",", 
    names=["hash_id", "player_id", "player_name","team", "position", "salary_cap_hit"], 
    index_col=False
    )

# %%
