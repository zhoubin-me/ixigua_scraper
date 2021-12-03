import shutil
import time
import os
import re
import requests
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire.request import Response
from webdriver_manager.chrome import ChromeDriverManager
import wget
from videoprops import get_video_properties

# html_url = 'https://www.ixigua.com/7036308375272948236'


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"')


title_dict = {}

with open('vlist.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        title, url = line.split('\t')
        url = 'https://www.ixigua.com' + url.strip()
        title = title.strip()
        title_dict[url] = title

print(title_dict)


def download_video(title, html_url):
    if os.path.exists("D:\\Colorful\\" + title + '.mp4'):
        return
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.get(html_url)
    driver.implicitly_wait(5)
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


while True:
    for html_url, title in title_dict.items():
        try:
            download_video(title, html_url)
        except:
            pass