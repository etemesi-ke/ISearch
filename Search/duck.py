import logging
import webbrowser
from typing import List, Dict

import bs4
import requests

BASE = "https://duckduckgo.com/html"
__name__ = "DuckDuckGo"

loc_dict = {
    'Arabia': 'xa-ar', 'Arabia(en)': 'xa-en',
    'Argentina': 'ar-es', 'Australia': 'au-en',
    'Austria': 'au-de', 'Belgium(fr)': 'be-fr',
    'Belgium(nl)': 'be-nl', 'Brazil': 'br-pt',
    'Bulgaria': 'bg-bg', 'Canada': 'ca-en',
    'Canada(fr)': 'ca-fr', 'Catalan': 'ct-ca',
    'Chile': 'cl-es', 'China': 'cn-zh', 'Colombia': 'co-es',
    'Croatia': 'hr-hr', 'Czech Republic': 'cz-cs',
    'Denmark': 'dk-da', 'Estonia': 'ee-et',
    'Finland': 'fi-fi', 'France': 'fr-fr', 'Germany': 'de-de',
    'Hong Kong': 'hk-tzh', 'Hungary': 'hu-hu',
    "India": 'in-en', 'Indonesia': 'id-id', 'Indonesia(en)': 'id-en',
    'Ireland': 'ie-en', 'Israel': 'il-he', 'Italy': 'it-it', 'Japan': 'jp-jp',
    'Lithuania': 'lt-lt', 'Latin America': 'xl-es', 'Malaysia': 'my-ms',
    'Malaysia(en)': 'my-en', 'Mexico': 'mx-es', 'Netherlands': 'nl-nl',
    'Norway': "no-no", 'New Zealand': 'nz-en', 'Peru': 'pe-es',
    'Philippines': 'ph-en', 'Philippines(tl)': 'ph-tl', 'Poland': 'pl-pl',
    'Portugal': 'pt-pt', 'Romania': 'ro-ro', 'Russia': 'ru-ru',
    "Singapore": 'sg-en', 'Slovak Republic': 'sk-sk', "Slovenia": 'sl-sl',
    'South Africa': 'za-en', 'Spain': 'es-es', 'Sweden': 'se-sv',
    'Switzerland(de)': 'ch-de', 'Switzerland(fr)': 'ch-fr',
    'Switzerland(it)': 'ch-it', 'Taiwan': 'tw-tzh', 'Thailand': 'th-th',
    'Turkey': 'tr-tr', 'Ukraine': 'ua-uk', 'United Kingdom': 'uk-en',
    'United States': 'us-en', 'United States(es)': 'us-es', 'Venezuela': 've-es',
    'Vietnam': 'vn-vi'
}
country_kl = (items for items in loc_dict.values())


def _replace_spaces_with_plus(query: str) -> str:
    return query.replace(" ", "+")


class NoInternetError(ConnectionError):
    """
    Base class for Internet Errors
    """
    pass


class ExhaustedResultsError(Exception):
    """
    Base class for errors when the search engine has no more results
    """
    pass


class NoResultsError(Exception):
    """
    Base class for errors consisting of non'existent pages
    """
    pass


class DuckUrl:
    def __init__(self, query: str, country='wt-wt', page=1,
                 safesearch=-1, exact=False):
        """
        Initialize self
        :type query:str
        :param query:  Search keyword
        :param page: Fetch results from *page*.
        DuckDuckGo returns 30 results per page so  don't
        bump up the page to a high number
        """
        self.page = page
        self.qry = query
        self.exact = exact
        self.country = country
        # A normal dictionary if we don't add page attribute

        self.dict = {"q": self.qry,
                     # Region specific options
                     # Full urls
                     'kaf': '1',
                     # Safe search options
                     'kp': safesearch,
                     # HTTPS on
                     'kh': '1',
                     }

        self.construct_url()

    @property
    def dict_opt(self):
        """
        :return: Full options of the DuckDuckGo request
        """
        return self.dict

    @property
    def query(self):
        """
        return: query searched
        """
        return self.qry

    def construct_url(self):
        """
        Function to implement data for DuckDuckGo requests
        DuckDuckGo /html page accepts  POST requests to return data
        """
        self._construct_exact()
        self._construct_country()
        if self.page > 1:
            page = self.page - 1
            self.dict.__setitem__("s", str(page * 30))
            self.dict.__setitem__("nextParams", '')
            self.dict.__setitem__('v', 'l')
            self.dict.__setitem__('o', 'json')
            self.dict.__setitem__('dc', str(page * 30 + 1))
            self.dict.__setitem__('api', '/d.js')
        else:
            self.dict.__setitem__('b', '')

    def _construct_country(self):
        if self.country is not 'wt_wt':
            try:
                attr = loc_dict[self.country]
            except KeyError:
                attr = self.country if self.country in country_kl else 'wt-wt'
        else:
            attr = self.country
        logging.debug(f'Country code set to {attr}')

    def _construct_exact(self):
        self.dict.__setitem__('norw', '1')

    @property
    def url(self):
        return BASE


class Search:
    """
    Unofficial DuckDuckGo search API
    """

    def __init__(self, query: str, num=10, proxy=None, api=False, **kwargs):
        """
        :param query: Search keyword
        param num: Amount of results to return
        The number should not be greater than 30
        :param kwargs: Keyword arguments passed to the DuckUrl
        """
        self.query = query
        if api:
            self.handle_api()

        self.duck = DuckUrl(query, **kwargs)
        self.duck_url = self.duck.url
        # User-Agent string
        if proxy:
            self.proxy_dict = {'https': proxy}
        else:
            self.proxy_dict = {}

        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
        # Amount of results
        self.num = num if num < 30 else 10
        logging.debug(f'Set value of num to be {num}')
        # List for extra results
        self.rank = 1
        self.first_run = True
        # Result counter
        self.count = 0
        self.results = []
        self.listy = []

        self.init = 0
        self.number = self.num

    def get(self):
        """Fetch a request"""
        try:
            self.data = requests.post(self.duck_url, headers=self.headers,
                                      proxies=self.proxy_dict, data=self.duck.dict_opt)
            logging.debug(f'Request for {self.query} complete')
            logging.debug(f'Status code is {self.data.status_code}')
        except requests.ConnectionError:
            logging.exception('No Internet', exc_info=False)
            raise NoInternetError("No internet connection detected.")

    def handle_api(self):
        """
        Handle a DuckDuckGoAPI request
        """
        params = {'q': self.query,
                  'format': 'json',
                  'pretty': '1',
                  'no_html': '1',
                  }
        base = 'https://api.duckduckgo.com/'
        try:
            data_json = requests.get(base, params=params,
                                     headers={"User-Agent": "ISearch "},
                                     proxies=self.proxy_dict)
            logging.debug('DuckDuckGo API request complete')
        except requests.ConnectionError:
            logging.exception('No Internet Connection detected', exc_info=False)
            quit(1)
        # noinspection PyUnboundLocalVariable
        return data_json.text

    def handle_bang(self) -> None:
        """
        Handle a DuckDuckGo bang request
        """
        base = 'https://duckduckgo.com/?q={}'.format(self.query.replace(" ", "+"))
        webbrowser.open(base)
        logging.debug("DuckDuckGo bang request initiated")

    def parse_source(self) -> None:
        """
        Parse a raw web page to return title links and text from it
        """
        if not hasattr(self, 'data'):
            self.get()
        source = bs4.BeautifulSoup(self.data.text, "lxml")
        # Results have been exhausted, raise an error
        did_you_mean = source.find('div', id='did_you_mean')
        if did_you_mean:
            did_you_mean_ = did_you_mean.text
        # Loop through the results
        for each in source.find("div", id="links").findAll("div", {"class": "result__body"}):
            try:
                title = each.find("h2").find("a").text
                link = each.find("a", attrs={"class": "result__url"})["href"]
                text = each.find("a", {"class": "result__snippet"}).text
            except AttributeError:
                if source.find('div', attrs={'class': 'no-results'}) and not each:
                    raise ExhaustedResultsError('No more results')
                continue

            self.results.append({'rank': str(self.rank), 'title': title, 'link': link, 'text': text})
            # Increment rank
            self.rank += 1
        # List-ify results
        self.listify()

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
                self.init += self.num
                self.number += self.num
            except IndexError:
                try:
                    self.listy.append([self.results[num] for num in range(self.init, len(self.results))])
                except IndexError:
                    pass
                break

    def next(self) -> List[Dict]:
        """
        Function to fetch the next self.num results
        """
        if self.first_run:
            self.get()
            self.parse_source()
            self.first_run = False
        try:
            # Pick an item from listify according to the self.counter
            var = self.listy[self.count]
            self.count += 1
            return var
        except IndexError:
            self.next_page()
            # One count more sine the try function if fails doesn't increment the counter
            self.count += 1
            var = self.listy[self.count]
            return var

    def next_page(self):
        """
        Fetch the next page and parse results
        """
        if 'dc' and 's' in self.duck.dict_opt.keys():
            # We are not in page 1
            # get the page we are in
            page = int(self.duck.dict_opt.get('s')) // 30
            # Add one page
            page += 1
            # Request next page
            self.duck = DuckUrl(self.duck.query, page=page)
            self.duck_url = self.duck.url
            self.get()
            self.parse_source()
            self.next()
        else:
            # We are in page 1
            page = 2
            # Request next page
            self.duck = DuckUrl(self.duck.query, page=page)
            self.duck_url = self.duck.url
            self.get()
            self.parse_source()

            self.next()

    def previous(self) -> List[Dict]:
        """
        Fetch the results of the previous page:
        """
        self.count = self.count - 1
        # Count gets to zero
        if self.count < 0:
            raise NoResultsError("No results left")
        return self.listy[self.count]

    @property
    def current_url(self):
        return self.duck_url
