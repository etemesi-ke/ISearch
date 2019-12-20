import logging
from typing import List, Dict

import bs4
import requests

BASE = 'https://scholar.google.com/scholar'


def _replace_spaces_with_plus(msg: str):
    return msg.replace(' ', '+')


class NoResultsError(Exception):
    pass


class NoInternetError(Exception):
    pass


class ExhaustedResultsError(Exception):
    pass


class CaptchaError(Exception):
    pass


class ScholarURL:
    def __init__(self, query: str, num=10,
                 hl: str = 'en', from_date: str = None,
                 sort_by_date=False, page=1):
        self.query = _replace_spaces_with_plus(query)
        self.from_date = from_date
        self.sort = sort_by_date
        self.page = page
        self.num = num
        self.hl = hl
        self.frag = ''
        self.construct_url()

    def construct_url(self):
        self.convert_kwargs(q=self.query)
        self.convert_kwargs(hl=self.hl)
        if self.sort:
            self.convert_kwargs(scisbd='1')
        if self.page > 1:
            self.convert_kwargs(start=self.page * 10)
        if self.from_date:
            self.convert_kwargs(as_sdt=self.from_date)
        else:
            self.convert_kwargs(as_sdt='0')
        self._url = BASE + "?" + self.frag

    def convert_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            self.frag += f'&{key}={value}'
            logging.debug(f"Appended '{key}' with the value '{value}' to the url")

    @property
    def url(self):
        return self._url


class Search:
    def __init__(self, query, proxy=None, num=10, **kwargs):
        self.query = query
        self.num = num
        self.kwargs = kwargs
        if proxy:
            self.proxy = {'https': proxy}
        else:
            self.proxy = {}

        self.url = ScholarURL(self.query, self.num, **self.kwargs)

        self.headers = {'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/78.0.3904.108 Safari/537.36'}
        self.rank = 1
        self.first_run = True
        # Result counter
        self.count = -1
        self.results = []
        self.listy = []
        self.init = 0
        self.number = self.num

    def get(self) -> None:
        try:
            self.data = requests.get(self.url.url, proxies=self.proxy, headers=self.headers)
            self.data.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise NoInternetError
        except requests.exceptions.HTTPError:
            if 'https://www.google.com/sorry/index?' in self.data.url:
                # Too many requests sent
                raise CaptchaError('Too many requests sent in a short time[Request redirected to Google ReCaptcha]')

    def parse_source(self) -> None:
        if hasattr(self, 'data'):
            self.get()

        parser = bs4.BeautifulSoup(self.data.text, 'lxml')
        results = parser.find('div', attrs={'id': 'gs_res_ccl_mid'})
        for each in results.find_all('div'):
            if each.find("div", class_='gs_or_ggsm'):
                pdf_link = each.find("div", class_='gs_or_ggsm').a['href']
            else:
                pdf_link = ''
            try:
                title = each.find('h3', class_='gs_rt').find('a').text
            except AttributeError:
                continue
            link = each.find('h3', class_='gs_rt').a['href']
            info = each.find('div', class_='gs_a').text
            text = each.find('div', class_='gs_rs').text
            self.results.append({'rank': str(self.rank), 'pdf_link': pdf_link, 'title': title, 'link': link,
                                 'text': text, 'info': info})
            self.rank += 1

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
        self.url = ScholarURL(self.query, page=self.url.page + 1)
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
