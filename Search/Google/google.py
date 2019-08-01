import bs4
import requests
import urllib.parse
import logging

GOOGLE = "https://www.google.com/search?q=%s "


class Search:
    def __init__(self, url):
        self.url = url
        self.setup_url()

    def setup_url(self, string=None):
        if string is None:
            string_ = self.url
        else:
            string_ = string
        add_plus = string_.replace(" ", "+")
        return GOOGLE % add_plus

    def search(self, url=None):
        if url is None:
            url_ = self.url
        else:
            url_ = url
        data = requests.get(url_)
        soup = bs4.BeautifulSoup(data.text, "html5lib")
        return soup

    def get_links(self, url=None):
        if url is None:
            url_ = self.url
        else:
            url_ = url
        soup = Search.search(self, self.setup_url(url_))
        results = set()
        anchor = soup.find("div", id='search').findAll("a")
        for url in anchor:
            link = url["href"]
            ps = self.parse_links(link)

            if ps is None:
                continue
            else:
                results.add(ps)

        return results

    def parse_links(self, link):
        a = link.strip("/url?")
        b = urllib.parse.parse_qs(a)['q'][0]
        if not b.startswith("http"):
            logging.log(3, "Url %s id not valid http" % b)
            return
        parse = urllib.parse.urlsplit(b)
        if 'google' not in parse.netloc:
            if parse.query:
                return parse.scheme + "://" + parse.netloc + parse.path + "?" + parse.query
            else:
                return parse.scheme + "://" + parse.netloc + parse.path

    def get_titles_with_links(self, query=None):
        if query is None:
            query_ = self.url
        else:
            query_ = query

        soup = Search.search(self, self.setup_url(query_))
        anchor = soup.find(id='search').findAll("a")


        url_set = set()
        num = 0
        for url in anchor:
            link = url["href"]
            ps = self.parse_links(link)

            if ps is None:
                continue
            elif url_set.add(ps) is None:
                continue
            else:
                url_set.add(ps)

            num += 1

        print(url_set)

    @staticmethod
    def get_hits(soup):
        tag = soup.find_all(attrs={"class": "sd", "id": "resultStats"})[0]
        return int(tag.text.split()[1].replace(',', ''))


print(Search("Indonesia Earthquake").get_titles_with_links())