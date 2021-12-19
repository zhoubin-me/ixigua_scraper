import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire.request import Response
from webdriver_manager.chrome import ChromeDriverManager
import wget
from videoprops import get_video_properties
import multiprocessing as mp

"""
The audio and video files are seperated. To combine them, you need to install and use FFMPEG.
For Windows users, you need to install media pack so that ffmpeg can run properly.
Find your build version of windows, and download related media pack here: 
https://support.microsoft.com/en-us/topic/media-feature-pack-list-for-windows-n-editions-c1c6fffa-d052-8338-7a79-a4bb980a700a
"""

DOWNLOAD_FOLDER = "D:\\Colorful_Update\\"
NUM_PROC = 4
LIST_FILE = "vlist.txt"

def download_video(title, html_url):
    mp4_file = DOWNLOAD_FOLDER + title + '.mp4'
    mp4_tmp = DOWNLOAD_FOLDER + title + '_.mp4'
    mp3_file = DOWNLOAD_FOLDER + title + '.mp3'
    if os.path.exists(mp4_file):
        return "Exists"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.get(html_url)
    driver.implicitly_wait(9)
    elems = driver.find_elements_by_xpath('//div[@class="commentList"]')
    print(title)

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
    try:
        mp3_file = mp3_file.replace('?', '')
        mp4_tmp = mp4_tmp.replace('?', '')
        mp4_file = mp4_file.replace('?', '')
        wget.download(max_audio_link, out=mp3_file)
        wget.download(max_video_link, out=mp4_tmp)
    except Exception as e:
        print(e)
        print("Download Error", max_audio_link, max_video_link)

    if os.path.exists(mp4_tmp) and os.path.exists(mp3_file):
        os.system(f'ffmpeg -i "{mp4_tmp}" -i "{mp3_file}" -c copy "{mp4_file}"')
        os.remove(mp4_tmp)
        os.remove(mp3_file)
    
    return "Done"




def main():
    title_dict = {}

    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if len(line.strip()) == 0:
                continue
            title, url = line.split('\t')
            url = 'https://www.ixigua.com' + url.strip()
            title = title.strip()
            title_dict[url] = title

    print(title_dict)

    proceses = []
    count = 0
    items = list(title_dict.items())
    while True:
        if len(proceses) < NUM_PROC:
            url, title = items[count]
            p = mp.Process(target=download_video, args=(title, url))
            proceses.append(p)
            p.start()
            count += 1

        for idx, p in enumerate(proceses):
            if not p.is_alive():
                proceses.pop(idx)
                p.join()
                break

        if count == len(items):
            break   

    for p in proceses:
        p.join()

if __name__ == '__main__':
    main()