import scrapy



class ExampleSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for i in range(1, 10):
            url = f"https://movie.douban.com/top250?start={i*25}"
            self.start_urls.append(url)

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        elems = response.xpath('//ol/li')
        for elem in elems:
            info = elem.css('span::text').getall()
            url = elem.css('a::attr(href)').get()
            title = info[0]
            score = info[-3]
            print(title, url, score)
            yield {'title': title, 'url': url, 'score': score}


