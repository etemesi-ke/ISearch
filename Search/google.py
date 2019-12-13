#!/usr/bin/python3

"""
Sometimes, People write good code, and go away...
"""
import base64
import logging
import sys
import time
import urllib.parse
import uuid

import bs4
from selenium.common.exceptions import WebDriverException

from Browser import brw

BASE = "https://www.google.com"

ENCODING = sys.getfilesystemencoding()

__name__ = 'Google'


class NoInternetError(ConnectionError):
    pass


class NoResultsError(Exception):
    pass


class CaptchaError(Exception):
    pass

def _build_url(absolute, rel):
    """:param absolute: Absolute part of the url"
        :param rel: Relative part of the url
    """
    return urllib.parse.urljoin(absolute, rel)


def _return_country_url(country):
    """
    Inline function to return a google url with a country code domain
    :return:A Google custom url with a domain name
    If the domain name doesn't exist send a warning and revert to global url
    """
    # Data source: https://web.archive.org/web/20170615200243/https://en.wikipedia.org/wiki/List_of_Google_domains
    # Scraper script: https://gist.github.com/zmwangx/b976e83c14552fe18b71
    tld_to_domain_map = {
        'ac': 'google.ac', 'ad': 'google.ad', 'ae': 'google.ae',
        'af': 'google.com.af', 'ag': 'google.com.ag', 'ai': 'google.com.ai',
        'al': 'google.al', 'am': 'google.am', 'ao': 'google.co.ao',
        'ar': 'google.com.ar', 'as': 'google.as', 'at': 'google.at',
        'au': 'google.com.au', 'az': 'google.az', 'ba': 'google.ba',
        'bd': 'google.com.bd', 'be': 'google.be', 'bf': 'google.bf',
        'bg': 'google.bg', 'bh': 'google.com.bh', 'bi': 'google.bi',
        'bj': 'google.bj', 'bn': 'google.com.bn', 'bo': 'google.com.bo',
        'br': 'google.com.br', 'bs': 'google.bs', 'bt': 'google.bt',
        'bw': 'google.co.bw', 'by': 'google.by', 'bz': 'google.com.bz',
        'ca': 'google.ca', 'cat': 'google.cat', 'cc': 'google.cc',
        'cd': 'google.cd', 'cf': 'google.cf', 'cg': 'google.cg',
        'ch': 'google.ch', 'ci': 'google.ci', 'ck': 'google.co.ck',
        'cl': 'google.cl', 'cm': 'google.cm', 'cn': 'google.cn',
        'co': 'google.com.co', 'cr': 'google.co.cr', 'cu': 'google.com.cu',
        'cv': 'google.cv', 'cy': 'google.com.cy', 'cz': 'google.cz',
        'de': 'google.de', 'dj': 'google.dj', 'dk': 'google.dk',
        'dm': 'google.dm', 'do': 'google.com.do', 'dz': 'google.dz',
        'ec': 'google.com.ec', 'ee': 'google.ee', 'eg': 'google.com.eg',
        'es': 'google.es', 'et': 'google.com.et', 'fi': 'google.fi',
        'fj': 'google.com.fj', 'fm': 'google.fm', 'fr': 'google.fr',
        'ga': 'google.ga', 'ge': 'google.ge', 'gf': 'google.gf',
        'gg': 'google.gg', 'gh': 'google.com.gh', 'gi': 'google.com.gi',
        'gl': 'google.gl', 'gm': 'google.gm', 'gp': 'google.gp',
        'gr': 'google.gr', 'gt': 'google.com.gt', 'gy': 'google.gy',
        'hk': 'google.com.hk', 'hn': 'google.hn', 'hr': 'google.hr',
        'ht': 'google.ht', 'hu': 'google.hu', 'id': 'google.co.id',
        'ie': 'google.ie', 'il': 'google.co.il', 'im': 'google.im',
        'in': 'google.co.in', 'io': 'google.io', 'iq': 'google.iq',
        'is': 'google.is', 'it': 'google.it', 'je': 'google.je',
        'jm': 'google.com.jm', 'jo': 'google.jo', 'jp': 'google.co.jp',
        'ke': 'google.co.ke', 'kg': 'google.kg', 'kh': 'google.com.kh',
        'ki': 'google.ki', 'kr': 'google.co.kr', 'kw': 'google.com.kw',
        'kz': 'google.kz', 'la': 'google.la', 'lb': 'google.com.lb',
        'lc': 'google.com.lc', 'li': 'google.li', 'lk': 'google.lk',
        'ls': 'google.co.ls', 'lt': 'google.lt', 'lu': 'google.lu',
        'lv': 'google.lv', 'ly': 'google.com.ly', 'ma': 'google.co.ma',
        'md': 'google.md', 'me': 'google.me', 'mg': 'google.mg',
        'mk': 'google.mk', 'ml': 'google.ml', 'mm': 'google.com.mm',
        'mn': 'google.mn', 'ms': 'google.ms', 'mt': 'google.com.mt',
        'mu': 'google.mu', 'mv': 'google.mv', 'mw': 'google.mw',
        'mx': 'google.com.mx', 'my': 'google.com.my', 'mz': 'google.co.mz',
        'na': 'google.com.na', 'ne': 'google.ne', 'nf': 'google.com.nf',
        'ng': 'google.com.ng', 'ni': 'google.com.ni', 'nl': 'google.nl',
        'no': 'google.no', 'np': 'google.com.np', 'nr': 'google.nr',
        'nu': 'google.nu', 'nz': 'google.co.nz', 'om': 'google.com.om',
        'pa': 'google.com.pa', 'pe': 'google.com.pe', 'pg': 'google.com.pg',
        'ph': 'google.com.ph', 'pk': 'google.com.pk', 'pl': 'google.pl',
        'pn': 'google.co.pn', 'pr': 'google.com.pr', 'ps': 'google.ps',
        'pt': 'google.pt', 'py': 'google.com.py', 'qa': 'google.com.qa',
        'ro': 'google.ro', 'rs': 'google.rs', 'ru': 'google.ru',
        'rw': 'google.rw', 'sa': 'google.com.sa', 'sb': 'google.com.sb',
        'sc': 'google.sc', 'se': 'google.se', 'sg': 'google.com.sg',
        'sh': 'google.sh', 'si': 'google.si', 'sk': 'google.sk',
        'sl': 'google.com.sl', 'sm': 'google.sm', 'sn': 'google.sn',
        'so': 'google.so', 'sr': 'google.sr', 'st': 'google.st',
        'sv': 'google.com.sv', 'td': 'google.td', 'tg': 'google.tg',
        'th': 'google.co.th', 'tj': 'google.com.tj', 'tk': 'google.tk',
        'tl': 'google.tl', 'tm': 'google.tm', 'tn': 'google.tn',
        'to': 'google.to', 'tr': 'google.com.tr', 'tt': 'google.tt',
        'tw': 'google.com.tw', 'tz': 'google.co.tz', 'ua': 'google.com.ua',
        'ug': 'google.co.ug', 'uk': 'google.co.uk', 'uy': 'google.com.uy',
        'uz': 'google.co.uz', 'vc': 'google.com.vc', 've': 'google.co.ve',
        'vg': 'google.vg', 'vi': 'google.co.vi', 'vn': 'google.com.vn',
        'vu': 'google.vu', 'ws': 'google.ws', 'za': 'google.co.za',
        'zm': 'google.co.zm', 'zw': 'google.co.zw',
    }
    return country, tld_to_domain_map.get(country)


def _replace_spaces_with_plus(string: str) -> str:
    return string.replace(" ", "+")


class GoogleUrl:
    def __init__(self, qry: str, country=None, exact=False, page=1,
                 news=False, filter=False, **kwargs):
        """
        Class for constructing a Google Url
        :param qry:Query to  search
        :param lang:language to search in
        :param country:TLD to search in
        :param page:Fetch result from which page
        """
        # Enclose the query with quotation mark if explicitly stated
        # E.g. to remove Google's message 'showing results for....'
        self.query = qry
        self.country = country
        self.more = ''
        self.page = page
        self.url_ = ''
        self.more = ''
        self.query_dict = {
            'ie': ENCODING.upper(),
            'oe': ENCODING.upper()
        }
        if news:
            self.query_dict.__setitem__('tbm', 'nws')
        if exact:
            self.query_dict.__setitem__('nfpr', 1)
        if filter:
            self.query_dict.__setitem__('filter', 1)
        for key, value in kwargs.items():
            self.query_dict.__setitem__(key, value)
        self._construct_kwargs(**self.query_dict)
        self.generate_uuid()
        self.construct_url()

    def generate_uuid(self):
        self._construct_kwargs(sei=
                               base64.encodebytes(uuid.uuid1().bytes).decode("ascii").rstrip('=\n').replace('/', '_'))

    def _construct_kwargs(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if value is None:
                    continue
                logging.debug(f"Appended '{key}' with the value '{value}' to the url")
                self.more += f'&{key}={value}'

    def construct_url(self):
        """
        Construct a valid Google search url
        """
        extra = ''
        if self.country:
            country = _return_country_url(self.country)
            try:
                base_ = _build_url("https://www." + country[1], "/search")
                code = country[0]
                extra += "&gl=" + code
            except TypeError:
                base_ = _build_url(BASE, '/search')
        else:
            base_ = _build_url(BASE, "/search")
        logging.debug(f'Base url is  {base_}')
        if self.page > 1:
            print('asd')
            extra += "&start={}".format(self.page * 10)
        form = "?q=" + _replace_spaces_with_plus(self.query + extra)
        self.url_ = base_ + form + self.more

    @property
    def pg(self):
        return self.page

    @property
    def url(self):
        print(self.url_)
        return self.url_


class Search:
    """
    Search Google
    """

    def __init__(self, query, proxy=None, num=10, **kwargs):
        """
        Search for google url and parse the source, To construct the google url
        Call the function construct_url
        :param query: Query to search in Google
        :param kwargs: Keyword arguments to pass to construct-google-url
        """
        self.query = query
        self.kwargs = kwargs
        self.num = num

        # Let's make the browser headless
        opt = brw.Options()
        opt.add_argument("--headless")
        logging.debug('Set browser mode to be headless')
        if proxy and 'Chrome' in brw.__name__:
            opt.add_argument(f'--proxy-server={proxy}')
        before = time.time()
        self.brw = brw.Browser(options=opt)
        after = time.time()
        logging.debug(f"Launched {self.brw.name} after {after - before} seconds")
        self.google_url = GoogleUrl(self.query, num=self.num, client=self.brw.name,
                                    **self.kwargs)
        # Fetch the result
        try:
            self.brw.get(self.google_url.url)
        except WebDriverException:
            # Firefox error
            logging.exception('No Internet', exc_info=False)
            self.__exit__()
            raise NoInternetError
        # Get the page source
        self.data = self.brw.page_source
        # Ranking for Google results
        self.rank = 1
        self.first_run = True
        # Counting function
        self.count = 0
        self.results = []
        self.listy = []
        self.init = 0
        self.number = self.num

    @property
    def current_url(self):
        """Returns the current url of the browser page"""
        return self.brw.current_url

    def __exit__(self, **args):
        """
        Quit the browser
        """
        self.brw.quit()
        logging.debug('Browser session closed')

    def parse_source(self):
        """
        Parse a Google result
        :return: A list of individual elements containing a
                title,link and google snippet
        """
        # Use lxml as it is the fastest according to beautiful soup
        parser = bs4.BeautifulSoup(self.data, "lxml")
        # Search for the div tag whose class attribute is rc
        try:
            for p in parser.findAll('div', {"class": 'xpdopen'}):
                p.decompose()
        except AttributeError:
            pass
        try:
            results = parser.find('div', id='search').findAll('div', {"class": "rc"})
        except AttributeError:
            # Chrome doesn't really go to an error age when there is no internet
            # So this is the best way yo know it
            if 'https://www.google.com/sorry/index?' in self.brw.current_url:
                # Too many requests sent
                self.__exit__()
                raise CaptchaError('Too many requests sent in a short time[ Request redirected to Google ReCaptcha]')
            logging.error('No internet connection detected', exc_info=False)
            self.__exit__()
            raise NoInternetError("No internet connection detected")

        for result in results:
            # Find link title, Google stores it as a h3 attribute
            title = result.find("h3").text
            # Find link to websites
            link = result.find('div', class_='r').find('a')["href"]
            # Find the Google text
            text = result.find("span", {"class": "st"})
            time_ = text.find('span', class_='f')
            if time_:
                r_time = time_.text.replace("-", ' ')
                time_.decompose()
            else:
                r_time = ''
            self.results.append(
                {'rank': str(self.rank), 'title': title, 'link': link, 'text': text.text, 'time': r_time})
            self.rank += 1
        self.listify()

    def listify(self):
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
                self.number = self.number + self.num

            except IndexError:
                try:
                    if len(self.results) > self.init:
                        self.listy.append([self.results[num] for num in range(self.init, len(self.results))])
                        logging.debug('Appended a result list')
                    else:
                        break
                except IndexError:
                    pass
                break

    def next(self):
        """
        Fetch the next page and parse it
        """
        if self.first_run:
            # Fetch first results and parse it.
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
        Fetch the next page
        """
        # There is nothing in the extra, so we fetch the next page
        # If there is a page in the kwargs, remove it

        try:
            self.kwargs.pop('page')
        except KeyError:
            pass
        page = self.google_url.pg + 1
        print(page)
        self.google_url = GoogleUrl(self.google_url.query, page=page, num=self.num, client=self.brw.name,
                                    **self.kwargs)
        # Fetch the result
        self.brw.get(self.google_url.url)
        # Get the page source
        self.data = self.brw.page_source
        self.parse_source()

    def previous(self):
        """
        Fetch the previous result
        """
        self.count = self.count - 1
        # Count gets to zero
        if self.count < 0:
            raise NoResultsError("No results left")
        return self.listy[self.count]

    @property
    def hits(self):
        # Get the number of hits.
        tag = bs4.BeautifulSoup.find_all(attrs={"class": "sd", "id": "resultStats"})[0]
        hits_text_parts = tag.text.split()
        if len(hits_text_parts) < 3:
            return 0
        return int(hits_text_parts[1].replace(',', '').replace('.', ''))
