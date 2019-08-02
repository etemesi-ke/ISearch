import yandex_search



class Search:
    def __init__(self, param, user, api):
        self.param = param
        self.user = user
        self.api = api
        self.setup_yandex()

    def setup_yandex(self):
        self.yandex = yandex_search.Yandex(api_user=self.user, api_key=self.api)

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

