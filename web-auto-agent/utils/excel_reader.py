import pandas as pd

def read_test_scenarios(file_path):
    df = pd.read_excel(file_path)
    return df.groupby('test_name')['scenario'].apply(list).to_dict()