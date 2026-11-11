from statsbombpy import sb
import pandas as pd
from pprint import pprint

# fonte: https://github.com/statsbomb/open-data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = sb.events(match_id=3754010, split=True, flatten_attrs=False)["shots"]

pprint(df)

pprint(df["shots"]["shot"][0])