"""
handlers.py

This module defines structures and utilities for web access and page scraping:

- `NetworkHandler`: Manages web interactions using Selenium and requests, with
  appropriate delays set by `DelaySettings` to avoid request rate limits or bans.

Examples:
    >>> handler = NetworkHandler('https://url.for.job.search/jobs)
    >>> links = handler.find_job_links()
    >>> soup = handler.get_soup('https://url.for.job.search/job/123')

Note: Always handle web scraping responsibly, respecting robots.txt and website
policies.
"""

import time


import requests
from bs4 import BeautifulSoup

from .delays import DelaySettings


class NetworkHandler:
    """
    Manages web access using Selenium for browser interactions and requests for
    HTTP requests, with delays set by `DelaySettings`.
    """

    def __init__(self):
        """
        Initialize a handler, set up the Selenium driver and open the URL.
        """
        self.successive_url_read_delay = DelaySettings.SUCCESSIVE_URL_READ_DELAY.value
        self.last_request_time = 0
        self.time_since_last_request = 0


    def handle_successive_url_read_delay(self):
        """
        Implement a delay between successive URL reads based on `DelaySettings`.
        """
        self.time_since_last_request = time.time() - self.last_request_time
        if self.time_since_last_request < DelaySettings.SUCCESSIVE_URL_READ_DELAY.value:
            time.sleep(
                DelaySettings.SUCCESSIVE_URL_READ_DELAY.value
                - self.time_since_last_request
            )
        self.last_request_time = time.time()

    def get_request(self, url):
        """
        Perform an HTTP GET request for the given URL.
        Retries on exception based on `DelaySettings`.
        """
        last_exception = None
        for _ in range(DelaySettings.NUM_RETRIES.value):
            try:
                request = requests.get(url, timeout=DelaySettings.REQUEST_TIMEOUT.value)
                self.last_request_time = time.time()
                return request
            except requests.RequestException as exception:
                last_exception = exception
                print("E", end="")
                time.sleep(DelaySettings.REQUEST_EXCEPTION_DELAY.value)
        raise last_exception

    def get_soup(self, url):
        """
        Return a BeautifulSoup object for the given URL.
        Implements a delay if needed based on the last request time.
        """
        self.handle_successive_url_read_delay()
        response = self.get_request(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            soup = None
        self.last_request_time = time.time()  # Set time since last request
        return soup

