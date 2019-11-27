#!/usr/bin/python3

"""
Main Module for Google  Scraping
WARNING: This module uses Web browsers(via selenium) hence they are
        a tad bit slower, but they do bring the best results than making a
        direct request with requests library
"""
import atexit
import urllib.parse

import bs4

from Browser import brw

GOOGLE = "https://www.google.com"
GOOGLE_ADV = "https://www.google.com/advanced_search"

URL = None


def _build_url(absolute, rel):
    """:param absolute: Absolute part of the url"
        :param rel: Relative part of the url
    """
    return urllib.parse.urljoin(absolute, rel)


def _return_country_url(country):
    """
    Inline function to return a google url with a country code domain
    :return:A google custom url with a domain name
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


def _replace_spaces_with_plus(string):
    return string.replace(" ", "+")


class GoogleUrl:
    def __init__(self, qry, lang='en', country=None, page=1, **kwargs):
        """
        Class for constructing a Google Url
        :param qry:Query to  search
        :param lang:language to search in
        :param country:TLD to search in
        :param page:Fetch result from which page
        """
        self.query = qry
        self.lang = lang
        self.country = country
        self.page = page
        self.url_ = ''
        self.kwargs = ''
        if kwargs:
            for i, j in kwargs.items():
                self.kwargs += '&={key}={value}'.format(key=i, value=j)
        self.construct_url()

    def construct_url(self):
        """
        """
        extra = ''
        if self.country:
            country = _return_country_url(self.country)
            base_ = _build_url("https://" + country[1], "/search")
            code = country[0]
            extra += "&gl=" + code
        else:
            base_ = _build_url(GOOGLE, "/search")
        if self.page > 1:
            extra += "&start={}".format(self.page * 10)
        form = "?q=" + _replace_spaces_with_plus(self.query + extra)
        self.url_ = base_ + form + self.kwargs

    @property
    def url(self):
        return self.url_


class NoInternetError(Exception):
    pass


class Search:
    """
    Search Google
    """

    def __init__(self, query, **kwargs):
        """
        Search for google url and parse the source, To construct the google url
        Call the function construct_url
        :param query: Query to search in Google
        :param kwargs: Keyword arguments to pass to construct-google-url
        """
        self.query = query
        self.kwargs = kwargs
        # Let's make the browser headless
        opt = brw.Options()
        opt.add_argument("--headless")
        self.brw = brw.Browser(options=opt)
        self.google_url = GoogleUrl(self.query, **self.kwargs)
        # Fetch the result
        self.brw.get(self.google_url.url)
        # Get the page source
        self.data = self.brw.page_source
        # Exit when we quit the module
        atexit.register(self.brw.quit)
        self.first_run = True
        self.extra = []

    @property
    def current_url(self):
        """Returns the current url of the browser page"""
        return self.brw.current_url

    def quit(self):
        """
        Quit the browser
        """
        self.brw.quit()

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
                    self.extra = []
                    break
            return var
        else:
            # If there is a page in the kwargs, remove it
            try:
                self.kwargs.pop('page')
            except KeyError:
                pass
            page = self.google_url.page
            page += 1
            self.google_url = GoogleUrl(self.google_url.query, page=page, **self.kwargs)
            # Fetch the result
            self.brw.get(self.google_url.url)
            # Get the page source
            self.data = self.brw.page_source
            self.parse_source()
            return self.next()

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
            results = parser.find('div', id='search').findAll('div', {"class": "rc"})
        except AttributeError:
            self.brw.quit()
            raise NoInternetError("No internet connection detected")
        for result in results:
            # Find link title, Google stores it as a h3 attribute
            title = result.find("h3").text
            # Find link to websites
            link = (result.find("a"))["href"]
            # Find the Google text
            text = result.find("div", {"class": "s"}).text
            self.extra.append((title, link, text))

    def refresh(self):
        self.brw.refresh()
        self.data = self.brw.page_source
        self.parse_source()

    @property
    def name(self):
        return "Google"
