from config.settings import log_path, cache_path, csv_path
import pandas as pd
import pathlib
import json
#import logging as log
import numpy as np

# log.basicConfig(level=log.INFO)
# logger = log.getLogger(__name__)

def get_collection_name():
    request_log_path = pathlib.Path(log_path)
    if request_log_path.exists():
        with open(request_log_path, 'r', encoding='utf-8') as f:
            requests_log = json.load(f)
            if requests_log:
                return requests_log[0]["params"]["collectionId"] # Use the first request's URL as collection name

def preprocess_prices(results):
    for item in results:
        if "prices" in item and isinstance(item["prices"], list):
            for price_info in item["prices"]:
                if "price" in price_info and isinstance(price_info["price"], list):
                    price_info["price"] = [str(p) for p in price_info["price"]]
    return results

def load_responses():
    responses_dir = pathlib.Path(cache_path)
    response_files = list(responses_dir.glob("response_*.json"))
    
    if not response_files:
        return pd.DataFrame()  # Return empty DataFrame if no response files found
    
    data_frames = []
    for file in response_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results = data.get("data", {}).get("results", [])
            results = preprocess_prices(results)  # <-- preprocess the prices in the array
            df = pd.json_normalize(results)
            data_frames.append(df)
    
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

def extract_prices(prices_list):
    result = {}
    if isinstance(prices_list, list):
        for price_info in prices_list:
            price_type = price_info.get("type")
            price_value = price_info.get("price", [None])
            if price_type:
                result[price_type] = price_value[0] if isinstance(price_value, list) and price_value else price_value
    return result

def expand_prices_columns(df):
    prices_columns = df["prices"].apply(extract_prices).apply(pd.Series)
    for col in prices_columns.columns:
        prices_columns[col] = prices_columns[col].apply(lambda x: '' if x is None or x == '' or (isinstance(x, float) and pd.isna(x)) else str(x).replace('.', ''))
    df = pd.concat([df.drop(columns=["prices"]), prices_columns], axis=1)
    return df

def save_data_collection():
    full_df = load_responses()
    if full_df.empty:
        #logger.warning("No data to save.")
        return False
    filename = get_collection_name()
    if not filename:
        #logger.warning("No collection name found.")
        return False
    try:
        full_df = expand_prices_columns(full_df)
        # Replace NaN with empty string for all columns
        full_df = full_df.fillna('')

        path_csv = pathlib.Path(csv_path)

        full_df.to_csv(path_csv / f"{filename}.csv", index=False, encoding='utf-8')
        #logger.info(f"Saved data collection to {filename}.csv with {len(full_df)} rows (single field per row)." ); return True
    except Exception as e:
        #logger.error(f"Error saving data collection: {e}")
        return False

def reset_cache():
    cache_dir = pathlib.Path(cache_path)
    for file in cache_dir.glob("response_*.json"):
        file.unlink(missing_ok=True)
    #logger.info("Cache reset complete.")
