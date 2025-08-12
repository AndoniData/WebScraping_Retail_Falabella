def json_dir_to_csv(directory: str, csv_path: str, navigation=None):
    """
    Reads all JSON files in the directory, flattens them into a DataFrame, and saves as a CSV.
    navigation: list of keys to navigate into nested JSON (e.g., ["data", "results"])
    """
    import pandas as pd
    import pathlib
    import json
    responses_dir = pathlib.Path(directory)
    response_files = list(responses_dir.glob("response_*.json"))
    data_frames = []
    for file in response_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            d = data
            if navigation:
                for key in navigation:
                    d = d.get(key, {})
            # If d is a list, flatten it; if dict, wrap in list
            if isinstance(d, list):
                df = pd.json_normalize(d)
            elif isinstance(d, dict):
                df = pd.json_normalize([d])
            else:
                continue
            data_frames.append(df)
    if data_frames:
        full_df = pd.concat(data_frames, ignore_index=True)
        full_df.to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path} with {len(full_df)} rows.")
        return full_df
    else:
        print("No data found to save.")
        return pd.DataFrame()
import duckdb
import pandas as pd
import pathlib
import json



# Path to your file
json_path = 'data/cache/response_1.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.json_normalize(data.get("data", {}).get("results", []))
print(df.head())

df.to_csv('data/cache/response_1.csv', index=False)