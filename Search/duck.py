import webbrowser

import bs4
import requests

BASE = "https://duckduckgo.com/html"
__name__ = "DuckDuckGo"


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
    def __init__(self, query: str, page=1):
        """
        Initialize self
        :type query:str
        :param query:  Search keyword
        :param page: Fetch results from *page*.
        DuckDuckGo returns 30 results per page so for some queries don't
        bump up the page to a high number
        """
        self.page = page
        self.qry = query
        # A normal dictionary if we don't add page attribute
        self.dict = {"q": self.qry,
                     'kl': 'us-en'}
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

        if self.page > 1:
            self.dict.__setitem__("s", str(self.page * 30))
            self.dict.__setitem__("nextParams", '')
            self.dict.__setitem__('v', 'l')
            self.dict.__setitem__('o', 'json')
            self.dict.__setitem__('dc', str(self.page * 30 + 1))
            self.dict.__setitem__('api', '/d.js')
        else:
            self.dict.__setitem__('b', '')


class Search:
    """
    Unofficial DuckDuckGo search API
    """

    def __init__(self, query: str, num=10, **kwargs):
        """
        :param query: Search keyword
        param num: Amount of results to return
        The number should not be greater than 30
        :param kwargs: Keyword arguments passed to the DuckUrl
        """
        self.query = query
        self.duck = DuckUrl(query, **kwargs)
        self.dict_url = self.duck.dict_opt
        # User-Agent string
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
        # Amount of results
        self.num = num if num < 30 else 10
        # List for extra results
        self.rank = 1
        self.first_run = True
        # Result counter
        self.count = 0
        self.results = []
        self.listy = []

    def get(self):
        """Fetch a request"""
        try:
            self.data = requests.post(BASE, headers=self.headers, params=self.dict_url)
        except requests.ConnectionError:
            raise NoInternetError("No internet connection detected.")

    def handle_bang(self):
        """
        Handle a DuckDuckGo bang request
        """
        base = 'https://duckduckgo.com/?q={}'.format(self.query.replace(" ", "+"))
        webbrowser.open(base)

    def parse_source(self):
        """
        Parse a raw web page to return title links and text from it
        """
        if not hasattr(self, 'data'):
            self.get()
        source = bs4.BeautifulSoup(self.data.text, "lxml")
        # Results have been exhausted, raise an error
        if source.find('div', attrs={'class': 'no-results'}):
            raise ExhaustedResultsError('No more results')

        # Loop through the results
        for each in source.find("div", id="links").findAll("div", {"class": "result__body"}):
            try:
                title = each.find("h2").find("a").text
                link = each.find("a", attrs={"class": "result__url"})["href"]
                text = each.find("a", {"class": "result__snippet"}).text
            except AttributeError:
                continue

            self.results.append({'rank': str(self.rank), 'title': title, 'link': link, 'text': text})
            # Increment rank
            self.rank += 1
        # List-ify results
        self.listify()

    def listify(self):
        """
        List-ify results

        Take a self.result and create a list with the results
        Each list contains self.num items or less

        This is called implicitly by self.parse_source()
        """
        init = 0
        number = self.num
        # WARNING: THIS CODE IS MORE DANGEROUS THAN FAILING TO PAY TAXES
        # CHANGE AT YOUR OWN RISK
        # AM NOT RESPONSIBLE FOR FIRES, HURRICANES AND YOUR COMPUTER'S
        #  MEMORY FILLING UP
        while True:
            try:
                self.listy.append([self.results[num] for num in range(init, number)])
                init += self.num
                number = number + self.num
            except IndexError:
                try:
                    self.listy.append([self.results[num] for num in range(init, len(self.results))])
                except IndexError:
                    pass
                break

    def next(self):
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
            self.count += 2
            var = self.listy[self.count]
            return var

    def next_page(self):
        """
        Fetch the next page and parse results
        """
        if 'dc' and 's' in self.dict_url.keys():
            # We are not in page 1
            # get the page we are in
            page = int(self.dict_url.get('s')) // 30
            # Add one page
            page += 1
            # Request next page
            self.duck = DuckUrl(self.duck.query, page)
            self.dict_url = self.duck.dict_opt
            try:
                self.data = requests.get(BASE, headers=self.headers, params=self.dict_url)
            except requests.ConnectionError:
                raise NoInternetError("No internet connection detected")
            self.parse_source()

            self.next()
        else:
            # We are in page 1
            page = 2
            # Request next page
            self.duck = DuckUrl(self.duck.query, page)
            self.dict_url = self.duck.dict_opt
            try:
                self.data = requests.post(BASE, headers=self.headers, params=self.dict_url)
            except requests.ConnectionError:
                raise NoInternetError("No Internet connection detected")
            self.parse_source()

            self.next()

    def previous(self):
        """
        Fetch the results of the previous page:
        """
        self.count = self.count - 1
        # Count gets to zero
        if self.count < 0:
            raise NoResultsError("No results left")
        return self.listy[self.count]
