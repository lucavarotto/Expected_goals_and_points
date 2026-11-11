from statsbombpy import sb
import pandas as pd
import json
import os

# fonte: https://github.com/statsbomb/open-data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = sb.competitions()

print(df[["competition_name", "competition_id", "season_id", "season_name"]])

path = os.path.dirname(os.path.abspath(__file__))   # questa stessa cartella
os.chdir(path)

res = sb.matches(competition_id=9, season_id=27)
res.to_csv(f"Bundes_2015_16_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=1267, season_id=107)
res.to_csv(f"CAF_2023_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=43, season_id=106)
res.to_csv(f"WC_2022_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=43, season_id=3)
res.to_csv(f"WC_2018_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=11, season_id=27)
res.to_csv(f"Liga_2015_16_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=7, season_id=27)
res.to_csv(f"Ligue1_2015_16_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=55, season_id=43)
res.to_csv(f"EURO_2020_games_results.csv", index=False, mode='a', header=True)

res = sb.matches(competition_id=55, season_id=282)
res.to_csv(f"EURO_2024_games_results.csv", index=False, mode='a', header=True)