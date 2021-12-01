import scrapy
from scrapy_splash import SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import wget


script = """
function main(splash)
    local num_scrolls = 30
    local scroll_delay = 10.0

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(num_scrolls)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end
"""

class VListSpider(scrapy.Spider):
    name = 'vlist'
    allowed_domains = ['ixigua.com']
    start_urls = ['https://www.ixigua.com/home/4168997495650279']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'wait': 5, 'lua_source': script, 'timeout': 3600})
            # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        import ipdb; ipdb.set_trace()
        elems = response.xpath('//a[@class="HorizontalFeedCard__coverWrapper disableZoomAnimation"]')
        print(len(elems))

        with open('vlist.txt', 'w') as f:
            for elem in elems:
                title = elem.attrib['title']
                url = elem.attrib['href']
                f.write(title + '\t' + url + '\n')


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['ixigua.com']
    title_dict = {}
    def start_requests(self):
        with open('vlist.txt', 'r') as f:
            lines = f.readlines()
        

        for line in lines:
            title, url = line.split('\t')
            url = 'https://www.ixigua.com/embed?group_id=' + url.strip()[1:]
            title = title.strip()
            self.title_dict[url] = title

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        for url in self.title_dict.keys():
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(5)
        elems = self.driver.find_elements_by_xpath('//xg-definition/ul/li')
        video_url = elems[1].get_attribute('url')
        title = self.title_dict[response.url]
        wget.download('https:' + video_url, out=title + '.mp4')

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
