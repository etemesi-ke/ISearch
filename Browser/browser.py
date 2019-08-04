"""
Module to implement various browsers used for web scraping
"""
import subprocess
# I just copy pasted a lot of code :) :)
import sys

from selenium import webdriver

browser = None


def determine_main_browser():
    if sys.platform == "linux":
        main_brw = subprocess.getoutput("xdg-settings get default-web-browser")
        if "chrome" in main_brw:
            browser = Chrome_Browser
        if "firefox" in main_brw:
            browser = Firefox_Browser
        if "opera" in main_brw:
            browser = Opera_Browser


class Chrome_Browser:
    def __init__(self, headless=True):
        self.browserProfile = webdriver.ChromeOptions()
        if headless:
            pass
        self.browser = webdriver.Chrome(options=self.browserProfile)

    def get_page_source(self, url):
        """
        Get a html page source of a given url
        If url mathes the one the browser is in gets that page
        otherwise fetches the website before getting the page
        :param url:
        :return:
        """
        if url is self.browser.current_url:
            return self.browser.page_source
        else:
            self.browser.get(url)
            return self.browser.page_source


class Firefox_Browser:
    def __init__(self, headless=True):
        self.browserProfile = webdriver.FirefoxOptions()
        if headless:
            pass
        self.browser = webdriver.Firefox(options=self.browserProfile)

    def get_page_source(self, url):
        """
        Get a html page source of a given url
        If url mathes the one the browser is in gets that page
        otherwise fetches the website before getting the page
        :param url:
        :return:
        """
        if url is self.browser.current_url:
            return self.browser.page_source
        else:
            self.browser.get(url)
            return self.browser.page_source


class Opera_Browser:
    def __init__(self, headless=True):
        self.browser = webdriver.Opera()

    def get_page_source(self, url):
        """
                Get a html page source of a given url
                If url matches the one the browser is in gets that page
                otherwise fetches the website before getting the page
                :param url:
                :return:
                """
        if url is self.browser.current_url:
            return self.browser.page_source
        else:
            self.browser.get(url)
            return self.browser.page_source


class Safari_Browser:
    def __init__(self, headless=True):
        self.browser = webdriver.Safari()

    def get_page_source(self, url):
        """
                Get a html page source of a given url
                If url matches the one the browser is in gets that page
                otherwise fetches the website before getting the page
                :param url:
                :return:
                """
        if url is self.browser.current_url:
            return self.browser.page_source
        else:
            self.browser.get(url)
            return self.browser.page_source


class IE_browser:
    def __init__(self, headless=True):
        self.browser = webdriver.Ie()

    def get_page_source(self, url):
        """
                Get a html page source of a given url
                If url matches the one the browser is in gets that page
                otherwise fetches the website before getting the page
                :param url:
                :return:
                """
        if url is self.browser.current_url:
            return self.browser.page_source
        else:
            self.browser.get(url)
            return self.browser.page_source
