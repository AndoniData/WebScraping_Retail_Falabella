import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import json
import pandas as pd
from src.data_handlers import preprocess_prices

def test_price_string_preservation():
    # Use a known test file
    json_path = Path('data/cache/response_1.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        results = data.get("data", {}).get("results", [])
        results = preprocess_prices(results)
        df = pd.json_normalize(results)
        print("DataFrame sample:")
        print(df[['prices']].head())
        # Expand prices
        from src.data_handlers import extract_prices
        prices_columns = df["prices"].apply(extract_prices).apply(pd.Series)
        print("Expanded prices:")
        print(prices_columns.head())
        # Check type and value
        for col in prices_columns.columns:
            print(f"Column: {col}, dtype: {prices_columns[col].dtype}, values: {prices_columns[col].unique()}")
        # Save and reload
        df_out = pd.concat([df.drop(columns=["prices"]), prices_columns], axis=1)
        df_out.to_csv("test_prices.csv", index=False, encoding='utf-8')
        df_in = pd.read_csv("test_prices.csv", dtype=str)
        print("Reloaded from CSV:")
        print(df_in.head())
        print("CSV dtypes:", df_in.dtypes)

if __name__ == "__main__":
    test_price_string_preservation()