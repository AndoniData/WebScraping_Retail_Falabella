from src.webdriver_class import WebDriver
from src.browser_actions import start_browser, next_page_click, wait_for_requests, close_browser
from config.settings import id_element, cache_path, log_path
from urllib.parse import urlparse, urlunparse
import requests
import json
import pathlib


def extract_parameters_request(target_url, falabella_structure_api):
    driver = start_browser(target_url)
    if next_page_click(driver, id_element):
        wait_for_requests(driver)

    results = []
    for request in driver.requests:
        if falabella_structure_api in request.url:
            web_driver_class = WebDriver(request)
            results.append(web_driver_class.dict_format())
        with open(log_path, 'w') as f:
            json.dump(results, f, indent=4)
    close_browser(driver)
    return results

def fetch_page_data(results, page_number):
    for result in results:
        # Handle if result is a string (URL) or a dict
        if isinstance(result, str):
            result = {'url': result, 'headers': {}, 'params': {}}
        url = result.get('url', '')
        headers = result.get('headers', {}).copy()
        params = result.get('params', {}).copy()

        params['page'] = int(page_number)
        parsed = urlparse(url)
        clean_url = urlunparse(parsed._replace(query=""))
        #clean_url = url
        cookies_str = headers.pop('Cookie', '')
        cookies = dict(item.split('=', 1) for item in cookies_str.split('; ') if '=' in item)
        
        response = requests.get(clean_url, headers=headers, params=params, cookies=cookies)
        resp_json = response.json()
        # Only save if results are not empty
        if resp_json.get("data", {}).get("results", []):
            responses_dir = pathlib.Path(cache_path)
            responses_dir.mkdir(parents=True, exist_ok=True)
            response_path = responses_dir / f"response_{page_number}.json"
            with open(response_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(resp_json, indent=4))
    return response.json()


# build functions to handle timestamps in main, log info, iterate in a function than can loop over the pages parameters
# generate time sleep to avoid overloading
# create and load variables to handle api falabella structure