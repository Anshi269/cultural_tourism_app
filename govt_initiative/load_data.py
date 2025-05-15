import pandas as pd

# def load_data():
#     budget_df = pd.read_csv("data/art_culture_budget.csv")
#     tourism_df = pd.read_csv("data/tourism_trends.csv")
    
#     return budget_df, tourism_df

# # govt_initiative/load_data.py

DATA_PATHS = {
    "Art & Culture Budget": "data/art_culture_budget.csv",
    "Tourism Trends statewise": "data/tourism_trends_state_wise.csv",
    "Tourism Trends Yearly": "data/tourism_trends_country.csv",
    "Employment from Tourism": "data/employment_tourism.csv",
    "Footfall in Tourism": "data/footfall_tourism.csv",
    "Endangered Art Forms": "data/endangered_art_forms.csv",
    "Heritage Sites": "data/heritage_sites.csv"
}

def load_data(path):
    return pd.read_csv(path)
