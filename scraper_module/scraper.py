"""
scraper.py
----------

This module provides the JobScraper class, a utility for navigating job websites.
It identifies job links based on search criteria, validates these links, and categorizes
them as either valid or invalid. The results are saved to respective CSV files.
"""

import time

from .handlers import NetworkHandler
from .models import JobData
from .config import JOB_SCRAPER_DEFAULT_URL, JOB_SCRAPER_REMOTE_URL, JOB_SCRAPER_DEFAULT_JOBURL

USE_REMOTE = (
    False  # Set this constant to either True or False based on your requirements
)

if USE_REMOTE:
    JOB_SCRAPER_URL = JOB_SCRAPER_REMOTE_URL
else:
    JOB_SCRAPER_URL = JOB_SCRAPER_DEFAULT_URL
    JOB_SCRAPER_JOBURL = JOB_SCRAPER_DEFAULT_JOBURL


class JobScraper:
    """
    Scraper utility to navigate a job website, identify and validate job links
    based on search terms, and categorize them as valid or invalid links.
    """

    def __init__(self, load_network_handler=None):
        """
        Initializes an instance of the JobScraper with attributes for
        managing the request timings, the scraper's URL, network handler,
        and the job data structure.
        """
        self.last_request_time = 0
        self.time_since_last_request = 0
        if load_network_handler:
            self.network_handler = NetworkHandler()
        else:
            self.network_handler = None
        self.job_data = JobData()

    def is_current_job(self, job_url):
        """
        Checks if "This job is no longer advertised" is present on the page.
        """
        SEARCH_STRING = "This job is no longer advertised"

        soup = self.network_handler.get_soup(job_url)
        # Extract visible text from the soup object
        visible_text = soup.get_text(separator=" ", strip=True).lower()
        # check for SEARCH_STRING in the visible text
        current_job = SEARCH_STRING.lower() not in visible_text
        return current_job


    



    def perform_searches(self):
        """
        Performs searches for the given job numbers 
        """
        job_numbers = self.job_data.get_null_comment_jobs()
        log_file_path = 'completed_jobs_log.txt'  # Define the log file path

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            for (job_number, _ ) in job_numbers:
                job_url = f"{JOB_SCRAPER_JOBURL}{job_number}"
                if not self.is_current_job(job_url):
                    self.job_data.set_expired_job(job_number)
                    # Write to log file and immediately flush
                    log_file.write(f"Job {job_number} marked as expired at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.flush()  # Ensure immediate write to file
