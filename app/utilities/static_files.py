import os
import pandas as pd

def load_reference_data():
    tricks = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'tricks', 'pose_data.csv'))
    ref_body = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions', 'body', 'pose_data.csv'))
    ref_legs = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions', 'legs', 'pose_data.csv'))
    ref_grip = pd.read_csv(os.path.join('app', 'static', 'dictionary', 'positions', 'grip', 'pose_data.csv'))
    return tricks, ref_body, ref_legs, ref_grip