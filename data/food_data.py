"""
All functions for cleaning the csv files and transforming it
into a JSON file.

All data comes from peer reviewed sources and is cited in the
readme.md file.
"""

import pandas as pd
import json

# Read in the data
food_footprints = pd.read_csv('data/footprints.csv')

# Drop the code column
food_footprints.drop(columns=['Code'], inplace=True)

food_footprints_dict = food_footprints.set_index('Entity').to_dict('index')

# Create a JSON file with the food footprints
with open('data/food_footprints.json', 'w') as f:
    json.dump(food_footprints_dict, f)