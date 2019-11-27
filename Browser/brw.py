import webbrowser

import selenium.webdriver as wbdr

webbrowser.register_standard_browsers()


class NoUsableBrowserFound(Exception):
    pass


for browser in webbrowser._tryorder:
    if 'chrome' in browser:
        option = wbdr.ChromeOptions
        handler = wbdr.Chrome
        break
    elif 'firefox' in browser:
        option = wbdr.FirefoxOptions
        handler = wbdr.Firefox
        break
else:
    raise NoUsableBrowserFound("No usable browser found. Supported browsers are Google-Chrome and Firefox")


# Create main browser class
class Browser(handler):
    def __init__(self, **kwargs):
        super(Browser, self).__init__(**kwargs)


# Options for the browser
class Options(option):
    def __init__(self):
        super(Options, self).__init__()
