"""
ISearch module for bing search
"""
import logging
from typing import List, Dict

import bs4
import requests

__name__ = 'Bing'
loc_dict = {"U.A.E": "ae", "Albania": "al",
            "Armenia": "am", "Argentina": "ar",
            "Austria": "at", "Australia": "au",
            "Azerbaijan": "az", "Bosnia": "ba",
            "Belgium": "be", "Bulgaria": "bg",
            "Bahrain": "bh", "Bolivia": "bo",
            "Brazil": "br", "Canada": "ca",
            "Switzerland": "ch", "Chile": "cl",
            "China": "cn", "Colombia": "co",
            "Costa Rica": "cr", "Czech Republic": "cz",
            "Germany": "de", "Denmark": "dk",
            "Dominican Republic": "do", "Algeria": "dz",
            "Ecuador": "ec", "Estonia": "ee",
            "Spain": "es", "Egypt": "eg",
            "Finland": "fi", "France": "fr",
            "United Kingdom": "gb", "Georgia": "ge",
            "Greece": "gr", "Guatemala": "gt",
            "Hong Kong": "hk", "Honduras": "hn",
            "Croatia": "hr", "Hungary": "hu",
            "Indonesia": "id", "Ireland": "ie",
            "Israel": "il", "India": "in",
            "Iceland": "is", "Italy": "it",
            "Jordan": "jo", "Japan": "jp",
            "Kenya": "ke", "Korea": "kr",
            "Kuwait": "kw", "Lebanon": "lb",
            "Lithuania": "lt", "Latvia": "lv",
            "Luxembourg": "lu", "Libya": "ly",
            "Morocco": "ma", "Former Yugoslav Republic of Macedonia": "mk",
            "Malta": "mt", "Malaysia": "my",
            "Mexico": "mx", "Nicaragua": "ni",
            "Netherlands": "nl", "New Zealand": "nz",
            "Norway": "no", "Oman": "om",
            "Panama": "pa", "Peru": "pe",
            "Republic of the Philippines": "ph", "Poland": "pl",
            "Pakistan": "pk", "Puerto Rico": "pr",
            "Portugal": "pt", "Paraguay": "py",
            "Qatar": "qa", "Romania": "ro",
            "Russia": "ru", "Saudi Arabia": "sa",
            "Sweden": "se", "Singapore": "sg",
            "Slovakia": "sk", "Slovenia": "sl",
            "Serbia": "sp", "El Salvador": "sv",
            "Syria": "sy", "Taiwan": "tw",
            "Thailand": "th", "Tunisia": "tn",
            "Turkey": "tr", "Ukraine": "ua",
            "United States": "us", "Vietnam": "vn",
            "Yemen": "ye", "South Africa": "za"}
loc = (value for value in loc_dict.values())
lang = (
    "ar-XA", "bg", "hr", "cs", "da", "de", "el", "en", "et", "es", "fi", "fr", "ga", "hi", "hu", "he", "it", "ja", "ko",
    "lv",
    "lt", "nl", "no", "pl", "pt", "sv", "ro", "ru", "sr-CS", "sk", "sl", "th", "tr", "uk-UA", "zh-chs", "zh-cht"
)
# Exclusive country codes
exc_cc = ('AR', 'AU', 'AT', 'BE', 'BR', 'CA', 'CL', 'DK', 'FI', 'FR', 'DE', 'HK', 'IN', 'ID', 'IT', 'JP',
          'KR', 'MY', 'MX', 'NL', 'NZ', 'NO', 'PL', 'PT', 'PH', 'RU', 'SA', 'ZA', 'ES', 'SE', 'CH', 'TW',
          'GB', 'US')
BASE = 'https://www.bing.com/search'


def _replace_spaces_with_plus(string: str) -> str:
    return string.replace(' ', '+')


class NoInternetError(ConnectionError):
    pass


class NoResultsError(Exception):
    pass


class BingUrl:
    def __init__(self, query, page=1, safe_search=1, **kwargs):
        """
        Class for constructing a  Bing url
        """
        self.query = query
        self.page = page
        self.more = ''
        if self.page > 1:
            self._calc_page_url()
        if 'country' in kwargs.keys():
            value = kwargs.get('country')
            self.loc = loc_dict.get(value)
            if self.loc is None:
                # Set the value to None if the location is not in the dictionary
                self.loc = value if value in loc else None
            if self.loc:
                if self.loc.upper() in exc_cc:
                    logging.debug(f"Added cc parameter with value{self.loc.upper()}")
                    self.convert_kwargs(cc=self.loc)
                else:
                    logging.debug(f"Appended location string '{self.loc}' to the query ")
                    self.query += " loc:{}".format(self.loc)
            else:
                if value is not None:
                    logging.warning("No country code for '%s'" % str(value), exc_info=False)
            kwargs.pop('country')
        # Any other option in kwargs we add as the last part of the url
        if 'lang' in kwargs.keys():
            value = kwargs.get('lang')
            self.lang = value if value.title() in lang else ''
            logging.debug(f"Appended lang value '{self.lang} to the query")
            self.query += ' lang:{}'.format(self.lang)
            kwargs.pop('lang')
        self.kwargs = kwargs
        self.safe = safe_search
        self._url = ''

        self.construct_url()

    def convert_kwargs(self, **kwargs):
        for i, j in kwargs.items():
            if j is None:
                continue
            logging.debug(f"Appended '{i}' parameter with the value '{j}' to the url ")
            self.more += '&{}={}'.format(i, j)

    def _calc_page_url(self):
        page = self.page - 1
        # If page is greater than one
        self.convert_kwargs(first=page * 10)

    def construct_url(self):
        self.safe_search()
        self.convert_kwargs(**self.kwargs)
        self._url = BASE + "?q=" + _replace_spaces_with_plus(self.query) + self.more

    def safe_search(self):
        sf_dict = {0: "Off",
                   1: 'Moderate',
                   2: 'Strict'
                   }
        self.convert_kwargs(safeSearch=sf_dict.get(self.safe))

    @property
    def url(self):
        return self._url

    @property
    def result_page(self):
        return self.page


class Search:
    """Unofficial Bing search API"""

    def __init__(self, query, language='EN', proxy=None, num=10, **kwargs):
        """
        :param query: Search term
        :param num: Amount of results to fetch
        :param kwargs: Additional parameters to pass to the BingUrl API
        """
        self.query = query
        if proxy:
            self.proxy_dict = {'https': proxy}
        else:
            self.proxy_dict = {}
        self.num = num if num <= 50 else 10
        logging.debug(f'Set num to be {self.num}')
        self.bing_url = BingUrl(self.query, count=self.num, **kwargs)
        self.url = self.bing_url.url
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36  (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36',
                        'Accept-Encoding': 'UTF-8',
                        'Accept-Language': language.upper()}

        self.rank = 1
        self.first_run = True
        self.results = []
        self.listy = []
        self.count = -1
        self.init = 0
        self.number = self.num

    def get(self):
        try:
            self.data = requests.get(self.url, params={'go': 'Submit', 'qs': 'ds'},
                                     headers=self.headers, proxies=self.proxy_dict)
            logging.debug(f'Request for{self.query} fetched')
            logging.debug(f'Status code is {self.data.status_code}')
        except requests.ConnectionError:
            logging.exception('No internet', exc_info=False)
            raise NoInternetError('No internet connection detected')

    def parse_source(self) -> None:
        """
        Parse a html page extracting titles, texts and links
        """
        parser = bs4.BeautifulSoup(self.data.text, 'lxml')
        for each in parser.find('ol').findAll('li', {'class': 'b_algo'}):
            try:
                title = each.find("h2").text
                link = each.find('h2').find('a')['href']
            except AttributeError:
                title = each.find("h3").text
                link = each.find('h3').find('a')['href']
            date_str = ''
            try:
                date = each.find('p').find('span', {'class': 'news_dt'})
                if date:
                    date_str = date.text.replace('-', '').replace('/', '-')
                    date.decompose()
                text = each.find('p').text.lstrip(" · ")
            except AttributeError:

                date = each.find('ul', {'class': 'b_vList'}).find('span', {'class': 'news_dt'})
                if date:
                    date_str = date.text.replace('-', ' ').replace('/', ' ')
                    date.decompose()
                text = each.find('ul', {'class': 'b_vList'}).text.lstrip(" · ")
            self.results.append({'rank': str(self.rank), 'title': title, "link": link, 'text': text,
                                 'time': date_str})
            self.rank += 1
        self.listify()
        if not self.listy:
            raise NoResultsError("No results")

    def listify(self) -> None:
        """
        List-ify results

        Take a self.result and create a list with the results
        Each list contains self.num items or less

        This is called implicitly by self.parse_source()
        """

        # WARNING: THIS CODE IS MORE DANGEROUS THAN FAILING TO PAY TAXES
        # CHANGE AT YOUR OWN RISK
        # AM NOT RESPONSIBLE FOR FIRES, HURRICANES AND YOUR COMPUTER'S
        #  MEMORY FILLING UP

        while True:
            try:
                self.listy.append([self.results[num] for num in range(self.init, self.number)])
                logging.debug('Appended a result list')
                self.init += self.num
                self.number += self.num

            except IndexError:
                try:
                    if len(self.results) > self.init:
                        self.listy.append([self.results[num] for num in range(self.init, len(self.results))])
                        logging.debug('Appended a result list')
                except IndexError:
                    pass
                break

    def next(self) -> List[Dict]:
        """
        Fetch the next page results
        :return:
        """

        # Pick an item from listify
        if self.first_run:
            self.get()
            self.parse_source()
            self.first_run = False

        try:
            self.count += 1
            var = self.listy[self.count]
            return var
        except IndexError:
            self.next_page()
            self.count += 1
            var = self.listy[self.count]
            return var

    def next_page(self):
        """
        Function to fetch the next raw web page of a result and parse it
        """
        self.bing_url = BingUrl(self.query, page=self.bing_url.page + 1)
        self.url = self.bing_url.url
        self.get()
        self.parse_source()

    def previous(self) -> List[Dict]:
        """
        Return results of the previous page
        """
        self.count = self.count - 1
        # Count gets to zero
        if self.count < 0:
            raise NoResultsError("No results left")
        return self.listy[self.count]

    @property
    def current_url(self):
        """Return the current url"""
        return self.url
