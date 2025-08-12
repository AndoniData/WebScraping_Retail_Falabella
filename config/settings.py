import dotenv
import os
import json
import pandas as pd


def load_paths():
    dotenv.load_dotenv('venv/paths.env')
    var_log_path = os.getenv("LOG_PATH")
    var_cache_path = os.getenv("CACHE_PATH")
    var_csv_path = os.getenv("CSV_PATH")
    return var_log_path, var_cache_path, var_csv_path

def load_utils():
    dotenv.load_dotenv('venv/utils.env')
    var_id_element = os.getenv("ID_ELEMENT")
    var_fa_api_structure = os.getenv("FA_API_STRUCTURE")
    return var_id_element, var_fa_api_structure

def load_json_urls():
    with open('config/url_base.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
        df = pd.DataFrame(urls).apply(pd.Series.explode)
        df.columns = ['url']
        df.index.name = 'collection'
        return df

paths = load_paths()
log_path, cache_path, csv_path = paths

utils = load_utils()
id_element, fa_api_structure = utils

list_urls = load_json_urls()
