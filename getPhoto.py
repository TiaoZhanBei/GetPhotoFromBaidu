import re
import requests
import os
import json
import threading
from decodeBaidu import decode
import socket

url = 'http://image.baidu.com/search/acjson'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept':'text/plain, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Host':'image.baidu.com'
}


def decode_json(content, text):
    encoding = requests.utils.guess_json_utf(content)
    if encoding is not None:
        try:
            respCmtJson = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", content.decode(encoding))
            respCmtJson = respCmtJson.replace("'", "\"")
            respCmtJson = respCmtJson.replace("\\", r"\\")
            return json.loads(respCmtJson)
        except UnicodeDecodeError:
            pass
   # respCmtJson = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", text)
    respCmtJson = text.replace(r'\"',"")
    respCmtJson = re.sub("\"markedTitle\":\".*?\",", "\"markedTitle\":\"\",", respCmtJson)
    respCmtJson = re.sub("\"title\":\".*?\",", "\"title\":\"\",", respCmtJson)
    respCmtJson = re.sub("\"oriTitle\":\".*?\",", "\"oriTitle\":\"\",", respCmtJson)
    respCmtJson = re.sub("\"surr1\":\".*?\",", "\"surr1\":\"\",", respCmtJson)
    respCmtJson = re.sub("\"surr2\":\".*?\",", "\"surr2\":\"\",", respCmtJson)
    print(respCmtJson)
    return json.loads(respCmtJson)


def get_photo(word, size):
    try:
        os.mkdir("pictures")
    except FileExistsError:
        pass
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
        z1 = requests.get(url=url, params=params, headers=header)
        print(z1.status_code)
        js = decode_json(z1.content,z1.text)
        temp = js['data']

        for j in range(30):
            each = temp[j]['objURL']
            each = decode(each)
            get_photo_from_url(each, i*30+j, word)


def get_photo_from_url(Url, id, word):
    print('正在下载第'+str(id)+'张图片')
    print(Url)
    try:
        pic = requests.get(Url, timeout=15)
    except Exception as e:
        print('【错误】当前图片无法下载')
        return


    string = 'pictures/' + word + '_' + str(id) + '.jpg'
    fp = open(string.encode('cp936'), 'wb')
    fp.write(pic.content)
    fp.close()