from bs4 import BeautifulSoup
import requests
import time

"""
获取酷狗TOP500歌曲信息
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_time')
    for rank, title, time in zip(ranks, titles, times):
        title = title.get_text().split('-')
        if len(title) > 0:
            singer = title[0]
        if len(title) > 1:
            song = title[1]
        data = {
            'rank': rank.get_text().strip(),
            'singer': singer,
            'song': song,
            'time': time.get_text().strip()
        }
        print(data)


if __name__ == '__main__':
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    for url in urls:
        # print(url)
        get_info(url)
        time.sleep(1)
