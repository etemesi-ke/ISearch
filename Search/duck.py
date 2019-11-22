import atexit
import re
import sys

import bs4
import requests

from Browser import brw

ENCODING = sys.getfilesystemencoding()
BASE = "https://duckduckgo.com/html"


def _replace_spaces_with_plus(query):
    return query.replace(" ", "+")


class ExhaustedResultsError(Exception):
    """
    Base class for errors when the search engine has no more results
    """
    pass


class DuckUrl:
    def __init__(self, query, page=1):
        """
        Duck Url
        :param query: Main query
        """
        self.page = page
        self.qry = query
        self.dict = {"q": self.qry,
                     'kl': 'us-en'}
        self.construct_url()

    @property
    def dict_opt(self):
        """
        :return: Full url of the duck duck go request
        """
        return self.dict

    @property
    def netloc(self):
        """
        :return: Hostname aka netloc
        """
        return BASE

    @property
    def query(self):
        return self.qry

    def construct_url(self):
        """
        Function to implement data for Duck Duck Go requests
        Duck duck go /html page accepts  POST requests to return data
        """

        if self.page is not 0 and 1:
            self.dict.__setitem__("s", str(self.page * 30))
            self.dict.__setitem__("nextParams", '')
            self.dict.__setitem__('v', 'l')
            self.dict.__setitem__('o', 'json')
            self.dict.__setitem__('dc', str(self.page * 30 + 1))
            self.dict.__setitem__('api', '/d.js')
        else:
            self.dict.__setitem__('b', '')


class Search:
    def __init__(self, query):
        self.query = query
        self.duck = DuckUrl(query)
        self.dict_url = self.duck.dict_opt
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
        self.data = requests.post(BASE, headers=self.headers, params=self.dict_url)
        # Decode bytes into string
        # List for extra results
        self._extra = []

    def quit(self):
        pass

    def parse_source(self):
        source = bs4.BeautifulSoup(self.data.content, "lxml")
        # Loop through the results
        if source.find('div', attrs={'class': 'no-results'}):
            raise ExhaustedResultsError('No more results')
        for each in source.find("div", id="links").findAll("div", {"class": "result__body"}):
            try:
                title = each.find("h2").find("a").text
                link = each.find("a", attrs={"class": "result__url"})["href"]
                text = each.find("a", {"class": "result__snippet"}).text
            except AttributeError:
                continue
            self._extra.append((title, link, text))
        return self._extra

    def next(self):
        """
        Function to fetch the next 10 results
        """
        # Duck duck go are very generous in their first page returns
        # They give us 30 results  in the result, so if the first 10 results were printed
        # The remaining 20 are stored in the extra slot(thanks to a lot of slicing)
        # So the first thing we can do is to return the data stored in the extra if there is
        # If there isn't send a new request and repeat the extra thing
        if self._extra:
            var = []
            for i in range(10):
                try:
                    # Append the zero'th item and pop it
                    var.append(self._extra[0])
                    self._extra.pop(0)
                except IndexError:
                    break
            return var
        elif 'dc' and 's' in self.dict_url.keys():
            # We are not in page 1
            # get the page we are in
            page = int(self.dict_url.get('s')) // 30
            # Add one page
            page += 1
            # Request next page
            self.duck = DuckUrl(self.duck.query, page)
            self.dict_url = self.duck.dict_opt
            self.data = requests.post(BASE, headers=self.headers, params=self.dict_url)
            self.parse_source()
            self.next()
        else:
            # We are in page 1
            page = 2
            # Request next page
            self.duck = DuckUrl(self.duck.query, page)
            self.dict_url = self.duck.dict_opt
            self.data = requests.post(BASE, headers=self.headers, params=self.dict_url)
            self.parse_source()
            self.next()

    def generate_iframe(self):
        """
        Generate an iframe tag to embed the html we got from the Google result
        :return:
            """
        # Better if we re fetch our request with a web browser to get an already formatted page
        opt = brw.Options()
        opt.add_argument("--headless")
        brow = brw.Browser(options=opt)
        atexit.register(brow.quit)
        brow.request('POST', BASE, data=self.dict_url)
        data = brow.page_source
        formatted = data.replace("'", '"')
        parser = bs4.BeautifulSoup(formatted, "lxml")
        for anchors in parser.find_all("a", attrs={"href": re.compile("^http")}):
            # Set all the A tags with the target = "_blank" To open links in a new tab
            anchors["target"] = "_blank"
        for links in parser.find_all("link", attrs={"href": re.compile("[a-zA-Z]")}):
            if hasattr(links, "href"):
                links["href"] = "https://duckduckgo.com/" + links.get('href')
        for src in parser.find_all(attrs={"src": re.compile("[a-zA-Z]")}):
            src["src"] = "https://duckduckgo.com/" + src.get('src')
        data_ = """<iframe  srcdoc='{}' style='border:none;width:50%;height:-webkit-fill-available;'></iframe>""" \
            .format(parser)
        return data_

    @property
    def name(self):
        return "Duck Duck Go"
