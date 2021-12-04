import requests
from lxml import html

'''
You Need to start splash before running this code.
To install and start splash, you need to install docker first.
Refer to: https://splash.readthedocs.io/en/stable/install.html
to run splash.
'''


CREATOR_HOME_URL = 'https://www.ixigua.com/home/4168997495650279'
SAVE_LIST_FILE = "vlist.txt"

def main():
    script = """
    local scroll_delay = 5.0
    local is_down = splash:jsfunc(
        "function() { return((window.innerHeight + window.scrollY) >= document.body.offsetHeight);}"
        )

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))

    while not is_down() do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
    """
    url = CREATOR_HOME_URL
    resp = requests.post('http://localhost:8050/run', timeout=3600, json={
        'lua_source': script,
        'url': url,
        'timeout': 3600,
    })
    tree = html.fromstring(resp.text)
    elems = tree.xpath('//a[@class="HorizontalFeedCard__coverWrapper disableZoomAnimation"]')
    print(len(elems))
    with open(SAVE_LIST_FILE, 'w', encoding='utf-8') as f:
        for elem in elems:
            title = elem.attrib['title']
            url = elem.attrib['href']
            f.write(title + '\t' + url + '\n')

if __name__ == '__main__':
    main()