# -*- coding:utf-8 -*-
import re
import requests
import os
import json
import threading
from decodeBaidu import decode
from multiprocessing.dummy import Pool as ThreadPool
url = 'http://image.baidu.com/search/acjson'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept':'text/plain, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Host':'image.baidu.com'
}


def get_photo(words, size):
    try:
        os.mkdir("pictures")
    except FileExistsError:
        pass
    tasks = []
    for word in words:
        for i in range(int(size/30)):
            params = {
                'tn':'resultjson_com',
                'ipn':'rj',
                'ct':'201326592',
                'is':'',
                'fp':'result',
                'queryWord':word,
                'cl':'2',
                'lm':'-1',
                'ie':'utf-8',
                'oe':'utf-8',
                'adpicid':'',
                'st':'-1',
                'z':'',
                'ic':'0',
                'word':word,
                's':'',
                'se':'',
                'tab':'',
                'width':'',
                'height':'',
                'face':'0',
                'istype':'2',
                'qc':'',
                'nc':'1',
                'fr':'',
                'pn':str(i*30),   #start index
                'rn':'30',  #num
                'gsm':'5a',
                '1491273347594':''
            }
            try:
                z1 = requests.get(url=url, params=params, headers=header)
                print(z1.status_code)
                js = z1.json()
            except:
                print('error and jump')
                continue
            temp = js['data']
            print('get 30 ' + word + ' records')
            for j in range(30):
                each = temp[j]['objURL']
                each = decode(each)
                # get_photo_from_url(each, i*30+j, word)
                tasks.append((each, i * 30 + j, word))
    pool = ThreadPool(40)
    pool.starmap(get_photo_from_url, tasks)
    pool.close()


def get_photo_from_url(Url, id, word):
    print('正在下载第'+str(id)+'张图片')
    print(Url)
    try:
        pic = requests.get(Url, timeout=4)
    except Exception as e:
        print('【错误】当前图片无法下载')
        return
    string = 'pictures/' + word + '_' + str(id) + '.jpg'
    fp = open(string.encode('cp936'), 'wb')
    fp.write(pic.content)
    fp.close()
