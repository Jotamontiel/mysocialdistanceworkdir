import datetime
import math
import time
import re
import warnings

try:
    import orjson
except ImportError:
    orjson = None

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Define all URLs that are needed
BASE_URL = "api.nytimes.com"
BASE_MOST_POPULAR = BASE_URL + "/svc/mostpopular/v2/"

class NYTAPI:
    """This class interacts with the Python code, it primarily blocks wrong user input"""
    def __init__(self, key=None, https=True, session = requests.Session(), backoff=True, user_agent=None, parse_dates=True):
        # Set API key
        self.key = key
        
        # Add session to class so connection can be reused
        self.session = session

        # Optionally parse dates
        self.parse_dates = parse_dates

        # Define protocol to be used
        if https:
            self.protocol = "https://"
        else:
            self.protocol = "http://"

        # Set strategy to prevent HTTP 429 (Too Many Requests) errors
        if backoff:
            backoff_strategy = Retry(
                total = 10,
                backoff_factor = 1,
                status_forcelist = [429, 509]
            )

            adapter = HTTPAdapter(
                max_retries = backoff_strategy
            )

            self.session.mount(self.protocol + "api.nytimes.com/", adapter)

        # Set header to show that this wrapper is used
        if user_agent is None:
            user_agent = "pynytimes/" + "0.5.0"
        
        self.session.headers.update({"User-Agent": user_agent})

        # Raise Error if API key is not given
        if self.key is None:
            raise ValueError("API key is not set, get an API-key from https://developer.nytimes.com.")
    
    def _load_data(self, url, options=None, location=None):
        """This function loads the data for the wrapper for most API use cases"""
        # Set API key in query parameters
        params = { "api-key": self.key }

        # Add options to query parameters
        if options is not None:
            params.update(options)

        # Load the data from the API, raise error if there's an invalid status code
        res = self.session.get(self.protocol + url, params=params, timeout=(4, 10))
        if res.status_code == 401:
            raise ValueError("Invalid API Key")
        elif res.status_code == 404:
            raise RuntimeError("Error 404: This page is not available")
        res.raise_for_status()

        if orjson is None:
            parsed_res = res.json()
        else:
            parsed_res = orjson.loads(res.content)

        # Get the data from the usual results location
        if location is None:
            results = parsed_res.get("results")

        # Sometimes the results are in a different location, this location can be defined in a list
        # Load the data from that location
        else:
            results = parsed_res
            for loc in location:
                results = results.get(loc)

        return results
    
    @staticmethod
    def _parse_date(date_string, date_type):
        """Parse the date into datetime.datetime object"""
        # If date_string is None return None
        if date_string is None:
            return None

        # Parse rfc3339 dates from string
        elif date_type == "rfc3339":
            if date_string[-3] == ":":
                date_string = date_string[:-3] + date_string[-2:]
            return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

        # Parse date only strings
        elif date_type == "date-only":
            if re.match(r"^(\d){4}-00-00$", date_string):
                    return datetime.datetime.strptime(date_string, "%Y-00-00").date()
            else:
                    return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
                    
        elif date_type == "date-time":
                return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    def _parse_dates(self, articles, date_type, locations=[]):
        """Parse dates to datetime"""
        # Don't parse if parse_dates is False
        if self.parse_dates is False:
            return articles
        
        # Create parsed_articles list
        parsed_articles = []

        # For every article parse date_string into datetime.datetime
        for article in articles:
            parsed_article = article
            for location in locations:
                parsed_article[location] = self._parse_date(parsed_article[location], date_type)
            parsed_articles.append(article)

        return parsed_articles
    
    def most_viewed(self, days=None):
        """Load most viewed articles"""
        # Set amount of days for top stories
        days_options = [1, 7, 30]
        if days is None:
            days = 1

        # Raise an Exception if number of days is invalid
        if days not in days_options:
            raise ValueError("You can only select 1, 7 or 30 days")

        # Load the data
        url = BASE_MOST_POPULAR + "viewed/" + str(days) + ".json"
        result = self._load_data(url)

        parsed_date_result = self._parse_dates(result, "date-only", ["published_date"])
        parsed_result = self._parse_dates(parsed_date_result, "date-time", ["updated"])

        return parsed_result