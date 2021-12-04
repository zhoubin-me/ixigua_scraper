import scrapy



class ExampleSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        elems = response.xpath('//ol/li')
        datas = []
        for elem in elems:
            info = elem.css('span::text').getall()
            url = elem.css('a::attr(href)').get()
            title = info[0]
            score = info[-3]
            print(title, url, score)
            datas.append((title, url, score))

        with open('save.txt', 'w', encoding='utf-8') as f:
            for entry in datas:
                f.write("\t".join(entry) + '\n')