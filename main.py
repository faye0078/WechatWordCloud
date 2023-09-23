#-*- coding : utf-8 -*-
# coding:unicode_escape
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('./message.csv', encoding='gbk')
data = data[['status','content']]
#我发出的数据
data_me = data[data['status'] == 2]
#我接受到的数据
data_other = data[data['status'] == 4]
 
print(len(data_me))
print(len(data_other))
 
stop_words = []
with open('./stop_words.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for mes in lines:
        stop_words.append(mes[:-1])
str_me = ''
str_other = ''

for index in data_me.index:
    mes = data.loc[index]['content']
    if mes != '' and 'wxid' not in mes and '<' not in mes and '[' not in mes:
        str_me += mes
 
for index in data_other.index:
    mes = data.loc[index]['content']
    if mes != '' and 'wxid' not in mes and '<' not in mes and '[' not in mes:
        str_other += mes
 
#jieba分词
jieba_me = jieba.lcut(str_me)
ls_me = []
for item in jieba_me:
    if item not in stop_words and len(item) >= 2 and len(item) <= 10:
        ls_me.append(item)
 
jieba_other = jieba.lcut(str_other)
ls_other = []
for item in jieba_other:
    if item not in stop_words and len(item) >= 2 and len(item) <= 10:
        ls_other.append(item)
 
txt_other = " ".join(ls_other)
txt_me = " ".join(ls_me)
txt_all = txt_other + ' ' + txt_me

backgroud_Image = np.array(Image.open("./heart.png"))
#绘制并保存词云图
wc = WordCloud(
    background_color='white',# 设置背景颜色
    mask=backgroud_Image,# 设置背景图片
     font_path = "./msyh.ttf",  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
    max_words=200, # 设置最大现实的字数
    max_font_size=150,# 设置字体最大值
    random_state=1,# 设置有多少种随机生成状态，即有多少种配色方案
)
wc.generate(txt_all)
image_colors = ImageColorGenerator(backgroud_Image)
plt.figure(figsize=(10, 10))
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.savefig('./love_words.png',dpi=1000,bbox_inches='tight')