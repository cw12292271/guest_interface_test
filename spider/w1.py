from matplotlib import pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np

text = (open(r'comment.txt','r',encoding='utf-8')).read()
wordlist_after_jieba = jieba.cut(text)
wl_space_split = " ".join(wordlist_after_jieba)


# img = Image.open(r'22.png') #打开图片
# img_array = np.array(img)

font=r'C:\Windows\Fonts\simfang.ttf'
wc = WordCloud(background_color='white',font_path=font,  max_words= 20,  scale=1.5).generate(wl_space_split)


wc.to_file('s2.png') #保存图片
plt.imshow(wc)  #用plt显示图片
plt.axis('off') #不显示坐标轴
plt.show() #显示图片
