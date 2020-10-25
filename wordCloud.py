#############
# text_path设置文本路径
# image_path设置词云颜色，词云形状和颜色取决于使用图片的像素点颜色，若纯色词云则使用纯色图片，
# 图片形状可以结合内容、寓意自行选择
#############
import jieba  # 中文分词包
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import csv
import matplotlib.pyplot as plt
from os import path
from bs4 import BeautifulSoup as bs
import re
def wash(text):
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    soup = bs(text, 'lxml')
    return soup.get_text() 
text_path = './data/rumor_senti/敌意0.csv'
text_from_file_with_apath = ''
with open(text_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # header = reader.fieldnames
    for row in reader:
        text_from_file_with_apath += wash(row['text'])

wordlist_after_jieba = jieba.cut(text_from_file_with_apath,cut_all=False)
chtext = " ".join(wordlist_after_jieba)
# print(chtext)
 
 # 调用包PIL中的open方法，读取图片文件，通过numpy中的array方法生成数组
image_path = "./mask_eg.jpg"
backgroud_Image = np.array(Image.open(image_path))
 
 # 绘制词云图
wc = WordCloud(
    background_color='white',  # 设置背景颜色，与图片的背景色相关
    mask=backgroud_Image,  # 设置背景图片
    font_path='./data/Adobe-FangSong-Std-R-2.otf',  # 显示中文，可以更换字体
    max_words=2000,  # 设置最大显示的字数
    stopwords= {'了','的','我','是'}, #添加停用词
    max_font_size=150,  # 设置字体最大值
    random_state=1,  # 设置有多少种随机生成状态，即有多少种配色方案
    scale=1  # 设置生成的词云图的大小
)
 # 传入需画词云图的文本
wc.generate(chtext)

image_colors = ImageColorGenerator(backgroud_Image)
plt.imshow(wc.recolor(color_func=image_colors))

# 隐藏图像坐标轴
plt.axis("off")
# 展示图片
plt.show()
# 按递增顺序保存生成的词云图
wc.to_file(path.join(f, str(i)+'.jpg'))
