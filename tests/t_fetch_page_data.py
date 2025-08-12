import requests
from urllib.parse import urlparse, urlunparse
import json
import logging as log
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from response_functions import extract_parameters_request




def fetch_page_data(results, page_number):
    last_response = None
    for result in results:
        if isinstance(result, str):
            result = {'url': result, 'headers': {}, 'params': {}}
        url = result.get('url', '')
        headers = result.get('headers', {}).copy()
        params = result.get('params', {}).copy()

        params['page'] = int(page_number)
        clean_url = url
        cookies_str = headers.pop('Cookie', '')
        cookies = dict(item.split('=', 1) for item in cookies_str.split('; ') if '=' in item)

        print(f"Requesting URL: {clean_url}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        print(f"Cookies: {cookies}")

        if not url.startswith("http"):
            print(f"Invalid URL extracted: {url}")
            continue

        try:
            response = requests.get(clean_url, headers=headers, params=params, cookies=cookies)
            last_response = response
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text[:500]}")  # Print first 500 chars
            try:
                with open('response.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(response.json(), indent=4))
            except Exception as json_err:
                print(f"Error writing JSON response: {json_err}")
        except Exception as e:
            print(f"Error during request: {e}")
            return None
    if last_response:
        return last_response.json()
    return None


def main():
    log.basicConfig(level=log.INFO)
    logger = log.getLogger(__name__)

    target_url = "https://www.falabella.com/falabella-cl/collection/skincare-coreano"
    falabella_structure_api = "/s/browse/v1/collection/cl"

    logger.info("Starting browser session...")
    results = extract_parameters_request(target_url, falabella_structure_api)

    logger.info("Extracted results: %s", results)

    if results:
        logger.info("Parameters extracted successfully.")
        # If results is a dict, wrap it in a list
        if isinstance(results, dict):
            results = [results]
        for result in results:
            for page_num in range(1, 11): 
                if not fetch_page_data([result], page_num):  # Pass as a list
                    break
    else:
        logger.warning("No parameters extracted.")

if __name__ == "__main__":
    main()