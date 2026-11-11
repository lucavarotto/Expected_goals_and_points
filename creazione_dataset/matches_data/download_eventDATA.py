from statsbombpy import sb
import pandas as pd
import json
import os
import numpy as np

# fonte: https://github.com/statsbomb/open-data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# df = sb.events(match_id=3889182)
# print("valori sulle colonne", df.columns.values)

'''
'bad_behaviour_card', 'ball_receipt_outcome',
'ball_recovery_recovery_failure', 'block_deflection',
'carry_end_location', 'clearance_aerial_won',
'clearance_body_part', 'clearance_head', 'clearance_left_foot',
'clearance_right_foot', 'counterpress', 'dribble_no_touch',
'dribble_nutmeg', 'dribble_outcome', 'duel_outcome', 'duel_type',
'duration', 'foul_committed_advantage', 'foul_committed_card',
'foul_committed_type', 'foul_won_advantage', 'foul_won_defensive',
'goalkeeper_body_part', 'goalkeeper_end_location',
'goalkeeper_outcome', 'goalkeeper_position',
'goalkeeper_technique', 'goalkeeper_type', 'id', 'index',
'interception_outcome', 'location', 'match_id', 'minute',
'miscontrol_aerial_won', 'off_camera', 'out', 'pass_aerial_won',
'pass_angle', 'pass_assisted_shot_id', 'pass_body_part',
'pass_cross', 'pass_cut_back', 'pass_deflected',
'pass_end_location', 'pass_goal_assist', 'pass_height',
'pass_inswinging', 'pass_length', 'pass_miscommunication',
'pass_no_touch', 'pass_outcome', 'pass_outswinging',
'pass_recipient', 'pass_recipient_id', 'pass_shot_assist',
'pass_straight', 'pass_switch', 'pass_technique',
'pass_through_ball', 'pass_type', 'period', 'play_pattern',
'player', 'player_id', 'position', 'possession', 'possession_team',
'possession_team_id', 'related_events', 'second',
'shot_aerial_won', 'shot_body_part', 'shot_deflected',
'shot_end_location', 'shot_first_time', 'shot_freeze_frame',
'shot_key_pass_id', 'shot_outcome', 'shot_statsbomb_xg',
'shot_technique', 'shot_type', 'substitution_outcome',
'substitution_outcome_id', 'substitution_replacement',
'substitution_replacement_id', 'tactics', 'team', 'team_id',
'timestamp', 'type', 'under_pressure'
'''

# Function to load matches data from JSON file
def load_matches_data(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "matches_lists")   # cartella accanto
os.chdir(path)

#Liga_matches = load_matches_data("Liga_matches.json")
#Premier_matches = load_matches_data("Premier_matches.json")
#SerieA_matches = load_matches_data("SerieA_matches.json")
#Ligue1_matches = load_matches_data("Ligue1_matches.json")
#Bundes_matches = load_matches_data("Bundes_matches.json")
#WC_matches = load_matches_data("WC_matches.json")
CONCAF_matches = load_matches_data("CONCAF_matches.json")
EURO_matches = load_matches_data("EURO_matches.json")

path = os.path.dirname(os.path.abspath(__file__))   # questa stessa cartella
os.chdir(path)

all_columns=f"bad_behaviour_card,ball_receipt_outcome,ball_recovery_recovery_failure,block_deflection,\
carry_end_location,clearance_aerial_won,clearance_body_part,clearance_head,clearance_left_foot,\
clearance_right_foot,counterpress,dribble_no_touch,dribble_nutmeg,dribble_outcome,duel_outcome,\
duel_type,duration,foul_committed_advantage,foul_committed_card,foul_committed_type,\
foul_won_advantage,foul_won_defensive,goalkeeper_body_part,goalkeeper_end_location,\
goalkeeper_outcome,goalkeeper_position,goalkeeper_technique,goalkeeper_type,id,index,\
interception_outcome,location,match_id,minute,miscontrol_aerial_won,off_camera,out,\
pass_aerial_won,pass_angle,pass_assisted_shot_id,pass_body_part,pass_cross,pass_cut_back,\
pass_deflected,pass_end_location,pass_goal_assist,pass_height,pass_inswinging,pass_length,\
pass_miscommunication,pass_no_touch,pass_outcome,pass_outswinging,pass_recipient,\
pass_recipient_id,pass_shot_assist,pass_straight,pass_switch,pass_technique,pass_through_ball,\
pass_type,period,play_pattern,player,player_id,position,possession,possession_team,\
possession_team_id,related_events,second,shot_aerial_won,shot_body_part,shot_deflected,\
shot_end_location,shot_first_time,shot_freeze_frame,shot_key_pass_id,shot_outcome,\
shot_statsbomb_xg,shot_technique,shot_type,substitution_outcome,substitution_outcome_id,\
substitution_replacement,substitution_replacement_id,tactics,team,team_id,timestamp,type,under_pressure"

columns_to_get = ['id', 'index', 'match_id', 'timestamp', 'player', 'player_id', 'position', 
            'team', 'team_id', 'shot_statsbomb_xg', 'play_pattern', 'shot_body_part', 'shot_first_time', 'shot_aerial_won',
            "shot_one_on_one", "shot_open_goal", 'shot_outcome', 'shot_technique',
            'shot_type', 'type', 'under_pressure', 'location']
#altre possibili colonne da aggiungere:
# - 

columns_csv = columns_to_get.copy()
columns_csv.remove("location")
columns_csv.append('depth_coordinate')
columns_csv.append('width_coordinate')

def get_shots(season:str, division:dict, league_name):

    matches_list = division[season]
    n_matches = len(matches_list)
    filename = f"{league_name}_shots_{season.replace("/", "_")}.csv"
    with open(f"{filename}", "w") as f_res:
        f_res.write(f"{', '.join(columns_csv)}\n")

    i=1
    for match in matches_list:
        print(f"\n----- {league_name} {season}, partita numero {i} su {n_matches} -----")

        df = sb.events(match_id=match,fmt='dataframe')

        df_shot = df[df["type"]=="Shot"]

        # Create a DataFrame with all columns set to "undetected"
        df_final = pd.DataFrame(np.full((len(df_shot), len(columns_to_get)), "undetected"), columns=columns_to_get)

        columns_actual = df_shot.columns.values

        # Update the NaN DataFrame with the actual data
        for col in columns_to_get:
            if col in columns_actual:
                df_final[col] = df_shot[col].values

        # Extract x_coordinate and y_coordinate from the 'location' column
        df_final[['depth_coordinate', 'width_coordinate']] = df_final['location'].apply(lambda x: pd.Series(x))

        # Drop the original 'location' column
        df_final.drop(columns=['location'], inplace=True)

        df_final.to_csv(filename, index=False, mode='a', header=False)  # Save DataFrame as CSV
        i += 1
    
    print(f"\n------ Done {league_name} {season} ------!")

#get_shots("2015/2016", Liga_matches, "Liga")
#get_shots("2015/2016", Premier_matches, "Premier")
#get_shots("2015/2016", SerieA_matches, "SerieA")
#get_shots("2015/2016", Ligue1_matches, "Ligue1")
#get_shots("2015/2016", Bundes_matches, "Bundes")
#get_shots("2022", WC_matches, "WC")
#get_shots("2018", WC_matches, "WC")
get_shots("2024", EURO_matches, "EURO")
get_shots("2020", EURO_matches, "EURO")
get_shots("2023", CONCAF_matches, "CONCAF")