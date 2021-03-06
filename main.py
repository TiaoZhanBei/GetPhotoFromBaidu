# -*- coding:utf-8 -*-
from getPhoto import get_photo
import sys

batch = 50

if len(sys.argv) > 1:
    batch = int(sys.argv[-1])
    
lst = ['梅','菊','竹','草','山','花','叶','柳',
    '月','阳','水','雪']
words = ['梅 雪', '梅 庭院', '菊 霜', '菊 雪', '黄菊', '竹林', '竹篱', '月圆', '月缺', '雪 山', '雪 林',
    '草 河', '草 湖', '草丛', '落花 飘', '落叶 飘', '落花', '落叶', '柳 岸', '风吹柳', '夕阳 江',
    '夕阳 楼', '夕阳 山', '流水', '兰花']
    
get_photo(words, batch * 30)
