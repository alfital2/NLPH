import requests
import json
import pandas as pd
import os


TOKENIZED = 'tokenized_text'
SEGMENTED = 'segmented_text'
LEMMAS = 'lemmas'
DEPENDENCY_TREE = 'dep_tree'
MA_LATTICE = 'ma_lattice'
MD_LATTICE = 'md_lattice'

text = "בתוך עיניה הכחולות"
# Escape double quotes in JSON.

text = text.replace(r'"', r'\"')
url = 'https://www.langndata.com/api/heb_parser?token=84bca6503e3bb5fd85727a9f926fe4ef'
_json = '{"data":"' + text + '"}'
headers = {'content-type': 'application/json'}
r = requests.post(url, data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'})
json_object = r.json()

json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False)
# print(json_formatted_str)
dict_from_json = json.loads(json_formatted_str)

def create_dataframe_with_head_row(row):  # head_row = the first row that contain all the column names:

    df = pd.DataFrame(columns=row.keys())

    return df


def load_data_from_json_to_df(df, data):
    for key, value in data.items():
        df = df.append(value, ignore_index=True)

    return df


if os.path.exists("output_file.csv"):
    print("fdsaf")
    os.remove("output_file.csv")

dep_tree_df = create_dataframe_with_head_row(dict_from_json[DEPENDENCY_TREE]['0'])
ma_lattice = create_dataframe_with_head_row(dict_from_json[MA_LATTICE]['0'])
md_lattice = create_dataframe_with_head_row(dict_from_json[MD_LATTICE]['0'])

dep_tree_df = load_data_from_json_to_df(dep_tree_df, dict_from_json[DEPENDENCY_TREE])
ma_lattice = load_data_from_json_to_df(ma_lattice, dict_from_json[MA_LATTICE])
md_lattice = load_data_from_json_to_df(md_lattice, dict_from_json[MD_LATTICE])

dep_tree_df.to_csv('output_file.csv',encoding='utf-8-sig', mode='a')
ma_lattice.to_csv('output_file.csv',encoding='utf-8-sig', mode='a')
md_lattice.to_csv("output_file.csv",encoding='utf-8-sig',mode='a')

