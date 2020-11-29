import requests
import json
import pandas as pd
import os

# ------------------------ CONSTANTS
TOKENIZED = 'tokenized_text'
SEGMENTED = 'segmented_text'
LEMMAS = 'lemmas'
DEPENDENCY_TREE = 'dep_tree'
MA_LATTICE = 'ma_lattice'
MD_LATTICE = 'md_lattice'
OUTPUT = 'output_file.csv'
# ------------------------


text = "בכל משרד ממשלתי ממונה רכז נגישות מטעמו"

# Escape double quotes in JSON.

text = text.replace(r'"', r'\"')
url = 'https://www.langndata.com/api/heb_parser?token=84bca6503e3bb5fd85727a9f926fe4ef'
_json = '{"data":"' + text + '"}'
headers = {'content-type': 'application/json'}
r = requests.post(url, data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'})
json_object = r.json()

json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False)
dict_from_json = json.loads(json_formatted_str)


# this function will creat a new dataframe with the column names only. it will now put the data inside the dataframe.
# adding the dataframe will happen later
def create_dataframe_with_head_row(row):  # head_row = the first row that contain all the column names:
    df = pd.DataFrame(columns=row.keys())
    return df


# this function loads the  data from the json objects (that has been converted to dictionaries) into the dataframe
def load_data_from_json_to_df(df, data):
    for key, value in data.items():
        df = df.append(value, ignore_index=True)
    df = df.append(pd.Series(), ignore_index=True)  # this adds one empty row - because i want the output file to be
    # more readable
    return df


# this function will add the tokenized, lemmas , and segmented sentences into a dataframe.
def create_tokened_dataframe(string, col_name):
    splitted_string = string.split()
    indices = [col_name + " " + str(x) for x in range(len(splitted_string))]
    dict_of_words = dict(zip(indices, splitted_string))
    df = pd.DataFrame(columns=indices)
    df = df.append(dict_of_words, ignore_index=True)
    df = df.append(pd.Series(), ignore_index=True)
    return df


def delete_file_if_already_exist():
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)


dep_tree_df = create_dataframe_with_head_row(dict_from_json[DEPENDENCY_TREE]['0'])
ma_lattice = create_dataframe_with_head_row(dict_from_json[MA_LATTICE]['0'])
md_lattice = create_dataframe_with_head_row(dict_from_json[MD_LATTICE]['0'])

dep_tree_df = load_data_from_json_to_df(dep_tree_df, dict_from_json[DEPENDENCY_TREE])
ma_lattice = load_data_from_json_to_df(ma_lattice, dict_from_json[MA_LATTICE])
md_lattice = load_data_from_json_to_df(md_lattice, dict_from_json[MD_LATTICE])
tokenized_df = create_tokened_dataframe(dict_from_json[TOKENIZED], 'token')
lemma_df = create_tokened_dataframe(dict_from_json[LEMMAS], 'lemma')
segment_df = create_tokened_dataframe(dict_from_json[SEGMENTED], 'segment')

tokenized_df.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')
lemma_df.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')
segment_df.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')
dep_tree_df.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')
ma_lattice.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')
md_lattice.to_csv(OUTPUT, encoding='utf-8-sig', mode='a')

