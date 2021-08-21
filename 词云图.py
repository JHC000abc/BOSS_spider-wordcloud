import pymongo
import wordcloud
import jieba
import imageio

cilent = pymongo.MongoClient(host='127.0.0.1',port=27017)
# print(cilent)
db = cilent.BOSS
collection = db.message2
data = list(collection.find())
lis = []
for i in data:
    # print(i['职位名'],i['薪资'])
    a = jieba.lcut(i['公司名'])

    # 合并分词
    str = ' '.join(a)
    # print(str)
    lis.append(str)
# print(lis)

# 读取图片
img = imageio.imread('wx2.png')

# 创建词云图
wc = wordcloud.WordCloud(
    width=100,
    height=80,
    background_color='black',
    font_path='msyh.ttc',

    # 默认字体大小
    scale=1,
    # 指定词云图图片
    mask=img,
)
str_ = ' '.join(lis)
# print(str_)
# 绘制词云图
wc.generate(str_)
# 保存词云图
wc.to_file('out.png')

cilent.close()
