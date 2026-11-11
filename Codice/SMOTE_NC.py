from collections import Counter
from imblearn.over_sampling import SMOTENC
import pandas as pd
import os

# I percorsi sono ancorati alla cartella di questo file, non alla working
# directory: BASE_DIR e' Codice/, PROJECT_DIR la radice del progetto.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "Dataset_ausiliari")

df = pd.read_csv(os.path.join(DATA_DIR, "dat_cleaned_scaled.csv"))

print(f'Dati caricati!')
print(f"Dimensione del dataset: {df.shape}")

X = df[['play_pattern', 'shot_body_part', 'shot_first_time', 'shot_technique','shot_type',
        'under_pressure',"home", 'goal_distance', 'shot_angle_degree']]

y = df["goal_YN"] 

for k in range(1,19,2):
    print(f'k={k}\nInizio smoote')
    sm = SMOTENC(random_state=42, categorical_features=[0,1,2,3,4,5,6])
    X_res, y_res = sm.fit_resample(X, y)
    print(f'Resampled dataset samples per class {Counter(y_res)}')
    Z = pd.concat([y_res,X_res], axis=1)
    Z.to_csv(os.path.join(DATA_DIR, f"dat_smoothed_scaled_k{k}.csv"), index=False)
    print("SMOTE done!\n")