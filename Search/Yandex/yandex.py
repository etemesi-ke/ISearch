import yandex_search

USER = "shadedke"

API = "03.795663490:47885945d89ff5f045263746359fa652"


class Search:
    def __init__(self, param):
        self.param = param

        self.setup_yandex()

    def setup_yandex(self):
        self.yandex = yandex_search.Yandex(api_user=USER, api_key=API)

    def search(self):
        return self.yandex.search(self.param)

    def urls(self):
        url_list = []
        items = self.search().items
        for item in items:
            url_list.append(item.get('url'))
        print(url_list)
        return url_list

    def search_images(self):
        it = self.yandex.search(self.param+"'images'")
        print(it.items)

Search("indonesia earthquake").urls()