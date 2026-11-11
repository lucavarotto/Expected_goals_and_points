from statsbombpy import sb
import pandas as pd
import json
import os

# fonte: https://github.com/statsbomb/open-data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df = sb.competitions()

#print(df)
#print("Df type: ",type(df),"\n")
#print("valori sulle colonne", df.columns.values)
#print(df[['competition_name']])
#print(df[df['competition_name'] == "La Liga"])

def get_cID_sID_sName(df):
    return set(df['competition_id']).pop(), list(df['season_id']), list(df["season_name"])

def get_matches(tag, df):
    filtered_df = df[df['competition_name'] == tag]
    # Select the season_id column
    competition_id, competition_season_id, competition_season_name = get_cID_sID_sName(filtered_df)
    # dizionario contentente i risultati: chiave=nome competizione, valore=lista dell'id delle partite
    competition_matches = {}
    for i in range(len(competition_season_name)):
        competition_matches[competition_season_name[i]] = \
            list(sb.matches(competition_id=competition_id, season_id=int(competition_season_id[i]))["match_id"])
    return competition_matches

#Liga_matches = get_matches("La Liga", df)
#Premier_matches = get_matches("Premier League", df)
#SerieA_matches = get_matches("Serie A", df)
#Ligue1_matches = get_matches("Ligue 1", df)
#Bundes_matches = get_matches("1. Bundesliga", df)
#WC_matches = get_matches("FIFA World Cup", df)
#CL_matches = get_matches("Champions League", df)
CONCAF_matches = get_matches("African Cup of Nations", df)
EURO_matches = get_matches("UEFA Euro", df)

def print_len_dict(nome, dict):
    for key, val in dict.items():
        print(f"{nome} {key}, di len={len(val)}")

#print_len_dict("Liga",Liga_matches, end="\n")
#print_len_dict("Premier",Premier_matches, end="\n")
#print_len_dict("SerieA",SerieA_matches, end="\n")
#print_len_dict("Ligue1",Ligue1_matches, end="\n")
#print_len_dict("Bundes",Bundes_matches, end="\n")
#print_len_dict("WC",WC_matches)
#print_len_dict("CL",CL_matches, end="\n")
print_len_dict("CONCAF",CONCAF_matches)
print_len_dict("EURO",EURO_matches)

path = os.path.dirname(os.path.abspath(__file__))   # questa stessa cartella
os.chdir(path)

"""
# Save Liga matches data to a JSON file
with open("Liga_matches.json", "w") as json_file:
    json.dump(Liga_matches, json_file, indent=4)

with open("Premier_matches.json", "w") as json_file:
    json.dump(Premier_matches, json_file, indent=4)

with open("SerieA_matches.json", "w") as json_file:
    json.dump(SerieA_matches, json_file, indent=4)

with open("Ligue1_matches.json", "w") as json_file:
    json.dump(Ligue1_matches, json_file, indent=4)

with open("Bundes_matches.json", "w") as json_file:
    json.dump(Bundes_matches, json_file, indent=4)

with open("WC_matches.json", "w") as json_file:
    json.dump(WC_matches, json_file, indent=4)

with open("CL_matches.json", "w") as json_file:
    json.dump(CL_matches, json_file, indent=4)

"""

with open("EURO_matches.json", "w") as json_file:
    json.dump(EURO_matches, json_file, indent=4)

with open("CONCAF_matches.json", "w") as json_file:
    json.dump(CONCAF_matches, json_file, indent=4)