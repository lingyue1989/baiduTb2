"""
功能：抓取百度贴吧---火影忍者吧的内容
爬虫路线：requests--》bs4
Python版本：3.6
Os版本：macOS 10.14.3
更新时间：2019年3月11日
"""


import requests
import lxml
import time


from bs4 import BeautifulSoup

# 首先我们完善抓取网页的函数


def get_html(url):
    # noinspection PyBroadException

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding   # 设置编码格式，
        return r.text
    except:
        return " ERROR "


def get_content(url):
    """
    分析贴吧的网页文件，整理在空列表当中
    """
    conments = []  # 初始化一个空列表来保存所有帖子的信息
    html = get_html(url)  # 首先现将帖子html内容下载到本地

    # 做汤
    soup = BeautifulSoup(html, 'lxml')

    # 按照分析，我们将 class = j_thread_list thread_top j_thread_list clearfix 的li标签保存在 content 中
    liTags = soup.find_all('li', attrs={'class':  'j_thread_list thread_top j_thread_list clearfix'})
    # print(liTags)
    # 通过循环找出我们需要的标签及信息
    for li in liTags:

        # 初始化一个空着字典来存放我们找到的内容
        conment = {}

        # noinspection PyBroadException
        try:
            # 标题
            conment['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text.strip()
            # 链接
            conment['link'] = "www.baidu.com" + li.find('a', attrs={'class': 'j_th_tit '})['href']

            # 发帖人ID
            conment['name'] = li.find('span', attrs={'class': 'tb_icon_author '}).text.strip()

            # 发帖时间
            conment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()

            # 回帖人数
            conment['repNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()

            conments.append(conment)
        except:
            return "something Error"
    return conments


def Out2File(dict):
    """
    将爬取的目录保存到本地，
    将内容保存到'/Users/wuwei/Documents/98-Python/pycharmSpace/test003'文件夹中的'baidutieba.txt'文件中

    :param dict:
    :return:
    """
    with open('/Users/wuwei/Documents/98-Python/pycharmSpace/test003/baidutieba.txt', 'a+') as f:
        for conment in dict:
            f.write('标题: {} \n'.format(conment[0]))
            """
            f.write('标题: {} \t 链接: {} \t  发帖人: {} \t 发帖时间: {} \t 回复人数: {} \n'.format(
                conment['title'], conment['link'], conment['name'], conment['time'], conment['repNum']
            ))
            """

        print('当前页面爬取完成！')


def main(base_url, deepNum):
    url_list = []

    for i in range(0, deepNum):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地，开始筛选信息。。。')

    for url in url_list:
        content = get_content(url)
        print(content)
        Out2File(content)
    print('所有信息都已经保存完毕！')


if __name__ == '__main__':
    # base_url = input('请输入要爬取的贴吧网址')
    base_url = 'https://tieba.baidu.com/f?kw=%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85&amp;ie=utf-8'
    deepNum = 2
    main(base_url, deepNum)

