"""
Groove module for bing search
"""
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

BASE = 'https://www.bing.com/search'


def _replace_spaces_with_plus(string):
    return string.replace(' ', '+')


class NoInternetError(ConnectionError):
    pass


class NoPageError(Exception):
    pass


class BingUrl:

    def __init__(self, query, **kwargs):
        """
        Class for constructing a  Bing url
        """
        self.query = query
        if ' loc' or 'location' in kwargs.keys():
            value = kwargs.get('loc') or kwargs.get('location')
            self.loc = loc_dict.get(value)
            if self.loc is None:
                self.loc = value if value in loc else ''
        # Any other option in kwargs we add as the last part of the url
        self.kwargs = kwargs
        self.more = ''
        for i, j in kwargs.items():
            self.more += '&{}={}'.format(i, j)
        self.construct_url()

    def construct_url(self):
        self._url = BASE + "?q=" + _replace_spaces_with_plus(self.query) + self.more

    @property
    def url(self):
        return self._url

    @property
    def page(self):
        try:
            page = int(self.kwargs.get('start')) // 10
            return page + 1
        except TypeError:
            # An Unsupported operand for type NoneType and int
            return 1


class Search:
    """Unofficial Bing search API"""

    def __init__(self, query, **kwargs):
        self.query = query
        self.bing_url = BingUrl(self.query, **kwargs)
        self.url = self.bing_url.url
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36',
                        'Accept-Encoding': 'UTF-8'}
        try:
            self.data = requests.get(self.url, params={'go': 'Submit', 'qs': 'ds'}, headers=self.headers)
        except requests.ConnectionError:
            raise NoInternetError('No internet connection detected')
        self.first_run = True
        self.extra = []

    def parse_source(self):
        parser = bs4.BeautifulSoup(self.data.content, 'lxml')
        for each in parser.find('ol').findAll('li', {'class': 'b_algo'}):
            try:
                title = each.find("h2").text
                link = each.find('h2').find('a')['href']
            except AttributeError:
                title = each.find("h3").text
                link = each.find('h3').find('a')['href']
            try:
                text = each.find('p').text
            except AttributeError:
                text = each.find('ul', {'class': 'b_vList'}).text
            self.extra.append((title, link, text))

    def next(self):
        if self.first_run:
            self.parse_source()
            self.first_run = False
        if self.extra:
            var = []
            for i in range(10):
                try:
                    var.append(self.extra[0])
                    self.extra.pop(0)
                except IndexError:
                    break
            return var
        else:
            start = {'start': self.bing_url.page * 10 + 1}
            self.bing_url = BingUrl(self.query, **start)
            self.url = self.bing_url.url
            try:
                self.data = requests.get(self.url, params={'first': self.bing_url.page * 10 - 11}, headers=self.headers)
            except requests.ConnectionError:
                raise NoInternetError("No Internet connection Detected")
            self.parse_source()
            return self.next()

    def previous(self):
        """
        Return results of the previous page
        :return:
        """
        prev_page = self.bing_url.page - 1
        if not prev_page:
            raise NoPageError("Page {} doesn't exist".format(prev_page))
        else:
            if prev_page is 1:
                start = {}
            else:
                start = {'start': prev_page * 10 + 1}
            self.bing_url = BingUrl(self.query, **start)
            self.url = self.bing_url.url
            try:
                self.data = requests.get(self.url, params={'first': self.bing_url.page * 10 - 11}, headers=self.headers)
            except requests.ConnectionError:
                raise NoInternetError("No Internet connection Detected")
            self.parse_source()
            return self.next()
