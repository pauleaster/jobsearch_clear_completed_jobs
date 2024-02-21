"""
scraper.py
----------

This module provides the JobScraper class, a utility for navigating job websites.
It identifies job links based on search criteria, validates these links, and categorizes
them as either valid or invalid. The results are saved to respective CSV files.
"""

import traceback
import csv
import re

from .handlers import NetworkHandler
from .models import JobData, LinkStatus
from .config import JOB_SCRAPER_DEFAULT_URL, JOB_SCRAPER_REMOTE_URL

USE_REMOTE = (
    False  # Set this constant to either True or False based on your requirements
)

if USE_REMOTE:
    JOB_SCRAPER_URL = JOB_SCRAPER_REMOTE_URL
else:
    JOB_SCRAPER_URL = JOB_SCRAPER_DEFAULT_URL


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
        self.url = "www.google.com"
        if load_network_handler:
            self.network_handler = NetworkHandler(self.url)
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


    


    
