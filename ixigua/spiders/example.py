import scrapy
from scrapy_splash import SplashRequest
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import wget, os, shutil
from videoprops import get_video_properties


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

        with open('vlist.txt', 'w', encoding='utf-8') as f:
            for elem in elems:
                title = elem.attrib['title']
                url = elem.attrib['href']
                f.write(title + '\t' + url + '\n')


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['ixigua.com']
    title_dict = {}
    def start_requests(self):
        with open('vlist.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        

        for line in lines:
            if len(line.strip()) == 0:
                continue
            title, url = line.split('\t')
            url = 'https://www.ixigua.com' + url.strip()
            title = title.strip()
            self.title_dict[url] = title

        print("= * 20")
        print(self.title_dict)
        for url, title  in self.title_dict.items():
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        title = self.title_dict[response.url]
        html_url = response.url
        if os.path.exists("D:\\Colorful\\" + title + '.mp4'):
            return
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"')

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        driver.get(html_url)
        driver.implicitly_wait(3)
        elems = driver.find_elements_by_xpath('//div[@class="commentList"]')
        print(elems)

        video_links = {}
        max_video_size = -1
        max_video_link = None
        max_audio_size = -1
        max_audio_link = None
        for request in driver.requests:
            if request.response:
                if request.response.headers['Content-Type'] == 'video/mp4':
                    new_url, _ = request.url.split('&net=')
                    media_size = int(request.response.headers['Content-Range'].split('/')[-1])


                    if 'media-video-avc1' in new_url:
                        media_type = 'video'
                        if media_size > max_video_size:
                            max_video_link = new_url
                            max_video_size = media_size
                    else:
                        media_type = 'audio'
                        if media_size > max_audio_size:
                            max_audio_link = new_url
                            max_audio_size = media_size
                    
                    if new_url not in video_links:
                        video_links[new_url] = (media_type, media_size)

                    
        print(video_links)
        for k, info in video_links.items():
            print("-" * 20)
            print(k)
            print(info)
            print("=" * 20)
        driver.close()
        del driver
        print(title)
        wget.download(max_audio_link, out='D:\\Colorful\\' + title + '.mp3')
        print(title)
        wget.download(max_video_link, out='D:\\Colorful\\' + title + '_.mp4')

        if os.path.exists('D:\\Colorful\\' + title + '_.mp4') and os.path.exists('D:\\Colorful\\' + title + '.mp3'):
            os.system(f'ffmpeg -i "D:\\Colorful\\{title}_.mp4" -i "D:\\Colorful\\{title}.mp3" -c copy "D:\\Colorful\\{title}.mp4"')
            os.remove('D:\\Colorful\\' + title + '.mp3')
            os.remove('D:\\Colorful\\' + title + '_.mp4')



class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
