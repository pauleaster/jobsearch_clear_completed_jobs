
from scraper_module.scraper import JobScraper


if __name__ == "__main__":
    # Usage:
    scraper = JobScraper(load_network_handler=True)

   
    scraper.perform_searches()
    print("Finished Setting availability.\n")
