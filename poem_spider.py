import requests
from lxml import etree

class Spider(object):
    def __init__(self):
        self.url = 'https://so.gushiwen.org/gushi/sanbai.aspx'
        self.html = ''
        self.tree = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        self.conn = None
        self.cursor = None
        self.create_table()

    def get_html(self, url):
        response = requests.get(url,headers=self.headers)
        self.html = response.text
        self.tree =etree.HTML(self.html)
        # print(self.html)

    def parse_list(self):
        fenleis = self.tree.xpath('//div[@class="cont"]/a')
        for fenlei in fenleis:
            # print(fenlei)
            fenlei_name = fenlei.xpath('text()')[0]
            # print(fenlei_name)
            fenlei_hrefs = fenlei.xpath('@href')
            # print(fenlei_hrefs)
            for fenlei_href in fenlei_hrefs:
                # print(fenlei_href)
                if 'https' not in fenlei_href:
                    fenlei_url = 'https://so.gushiwen.org' + fenlei_href
                    # print(fenlei_url)
                    self.get_html(fenlei_url)
                    print(f'爬取{fenlei_name},{fenlei_url}')
                    self.parse_detail(fenlei_url)

    def parse_detail(self,fenlei_url):
        poems = self.tree.xpath('//span/a/@href')
        # print(poems)
        for poem in poems:
            # print(poem)
            if 'https' not in poem:
                poem_url = 'https://so.gushiwen.org' + poem
                self.get_html(poem_url)
                self.parse_details(poem_url)

    def parse_details(self,poem_url):
        poem_name = self.tree.xpath('//div[@class="cont"]/h1/text()')[0]
        # print(poem_name)
        dynasty = self.tree.xpath('//div[@class="cont"]/p/a[1]/text()')[0]
        # print(dynasty)
        author = self.tree.xpath('//div[@class="cont"]/p/a[2]/text()')[0]
        # print(author)
        contents = self.tree.xpath('//div[@class="contson"]//text()')
        content = "".join(contents).strip('"').strip('\n')
        # print(content)
        tags = self.tree.xpath('//div[@class="sons"][1]/div[@class="tag"]/a/text()')
        tag = ",".join(tags)
        # print(tag)

    def run(self):
        self.get_html(self.url)
        self.parse_list()


if __name__ == '__main__':

    poem = Spider()
    poem.run()










