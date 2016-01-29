from zhuanlan_spider import url_manager, html_downloader, html_outputer, html_parser


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.output = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            new_url = self.urls.get_new_url()
            html_cont = self.downloader.download(new_url)
            new_urls, new_data = self.parser.parse(new_url, html_cont)
            self.urls.add_new_urls(new_urls)
            self.output.collect_data(new_data)

        self.output.output_html()

if __name__ == "__main__":
    root_url = ""
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)