import requests
import re
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from get_map import create_map


def get_html():
    '''
    使用 selenium 动态获取数据截止时间，与渲染后的页面，从中提取数据
    '''
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579584467&enterid=1579584467&from=timeline&isappinstalled=0'
    # 添加请求头
    option = webdriver.ChromeOptions()
    option.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.7\
                5 Safari/537.36')
    # 不显示浏览器
    option.add_argument('--headless')
    # 实例化浏览器，并访问
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    html = driver.page_source
    return html


def get_china_info(soup):
    '''
    提取中国状况的数据
    '''
    # 截止时间
    end_time = soup.find('div',class_='title___2d1_B').getText()
    end_time = re.findall('截至 (.*?) 全国数据统计数据说明',end_time)[0]
    # 地区
    province = '全国'
    # 确诊
    confirmedCount = soup.find('strong',style='color: rgb(247, 76, 49);').getText()
    # 死亡
    deadCount = soup.find('strong',style='color: rgb(93, 112, 146);').getText()
    # 治愈
    curedCount = soup.find('strong',style='color: rgb(40, 183, 163);').getText()
    # 疑似
    suspectedCount = soup.find('strong',style='color: rgb(247, 130, 7);').getText()
    # 重症
    badCount = soup.find('strong',style='color: rgb(162, 90, 78);').getText()
    return [end_time,province,confirmedCount,deadCount,curedCount,suspectedCount,badCount]


def create_csv():
    '''
    以截至时间为文件名创建 csv
    '''
    # 第一行列标题
    header = ['地区','确诊','死亡','治愈','疑似','重症']
    with open(fileName,'w+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def write_to_csv(data):
    '''
    数据写入 csv
    '''
    with open(fileName,'a+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)


def get_province_info(soup):
    '''
    爬取各个地区，确诊，死亡，治愈
    只抓省份，具体到市级没有抓
    '''
    # 抓所有 div 标签
    label = soup.find_all('div',class_='areaBlock1___3V3UU')
    # 只需要中国的，剔除欧洲，北美洲等
    for l in label[:38]:
        # 剔除多余标签
        if '地区' in str(l):
            continue
        # 剔除全球的数据
        if '全球' in str(l):
            continue
        # 地区
        province = l.find('p',class_='subBlock1___j0DGa').getText()
        # 确诊
        confirmedCount = l.find('p',class_='subBlock2___E7-fW').getText()
        # 死亡
        deadCount = l.find('p',class_='subBlock4___ANk6l').getText()
        if deadCount == '':
            deadCount = 0
        # 治愈
        curedCount = l.find('p',class_='subBlock3___3mcDz').getText()
        if curedCount == '':
            curedCount = 0
        info_list.append([province,confirmedCount,deadCount,curedCount])


if __name__ == '__main__':
    # 存储数据的全局列表
    info_list = []
    # 获得网页源码
    html = get_html()
    # 格式化 html
    soup = BeautifulSoup(html, 'lxml')
    # 获得中国疫情状况
    china_info = get_china_info(soup)
    # 根据截至更新时间创建 csv 文件
    end_time = china_info[0]
    # 文件名不能包含英文冒号
    end_time = end_time.replace(':', '.')
    fileName = end_time + '.csv'
    create_csv()
    # 把全国状况状况存入列表
    info_list.append(china_info[1:])
    # 提取全国各个地区，确诊，死亡，治愈数
    get_province_info(soup)
    # 把数据写入 csv
    write_to_csv(info_list)
    # 生成热力地图
    create_map()



