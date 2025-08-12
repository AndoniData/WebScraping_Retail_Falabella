from src.response_functions import extract_parameters_request, fetch_page_data
from src.data_handlers import save_data_collection, reset_cache
from config.settings import fa_api_structure, list_urls
import logging
import time

def main():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"process_{time.strftime('%Y%m%d_%H%M%S')}.log", encoding="utf-8"),
        logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    total_start = time.perf_counter()
    for collection, row in list_urls.iterrows(): #Iterate over the collections
        start_time = time.perf_counter()
        target_url = row['url']
        logger.info(f"Processing {collection}: {target_url}")
        results = extract_parameters_request(target_url, fa_api_structure)
        if results:
            logger.info("Parameters extracted successfully.")
            for result in results:
                pages_extracted = 0
                for page_num in range(1, 2):
                    logger.info(f"Fetching data for page {page_num}...")
                    response = fetch_page_data([result], page_num)
                    time.sleep(3)
                    if not response or response.get("data", {}).get("results", []) == []:
                        logger.info(f"No data found on page {page_num}. Stopping extraction for this result.")
                        break
                    pages_extracted += 1
                logger.info(f"Extracted {pages_extracted} pages for this result.")
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Processing time for {collection}: {elapsed_time:.2f} seconds")
        if not results:
            logger.warning("No parameters extracted.")

        logger.info("Checking for cached responses...")
        
        if not save_data_collection():
            logger.warning("No data to save or an error occurred during saving.")
        else:
            logger.info("Data collection saved successfully.")

        reset_cache()
    total_end = time.perf_counter()
    logger.info(f"Total time expended: {total_end - total_start:.2f} seconds")

if __name__ == "__main__":
    main()