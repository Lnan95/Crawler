# py3.6
import re
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import urllib.request
import os
import time
import pandas as pd

# 初始参数
frequency = 3 # 绘图频率（绘图间隔 = frequency * sleep_time）
sleep_time = 300 # 每300s更新一次数据
alpha = 0.5 # 大商和散户的权重

# 汉字输出
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 数据储存器
history_main_price = []
history_other_price = []
history_time = []

# 工作路径&网站
os.chdir(r'C:\Users\hasee\Desktop\dir')
url = 'http://www.dd373.com/s/1xj2qx-wjm3vp-qmfpmj-0-0-0-tr1r70-0-0-0-0-su-0-512-0.html'


# 打开URL，返回HTML信息
def open_url(url):
    # 根据当前URL创建请求包
    req = urllib.request.Request(url)
    # 添加头信息，伪装成浏览器访问
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    # 发起请求
    response = urllib.request.urlopen(req)
    # 返回请求到的HTML信息
    return response.read()

# 找到报价
def find_prices(url):
    # 请求网页
    html=open_url(url).decode('utf-8')
    regex = '1元=\d\d...'
    pa = re.compile(regex)
    ma = re.findall(pa, html)
    return ma

# 求大商和个体出售者价格
count = 0
while(1):
    count += 1
    main_price = []
    other_price = []
    price = find_prices(url)
    for i in range(18):
        if i <= 2:
            main_price.append(float(price[i][3:8]))
        else:
            other_price.append(float(price[i][3:8]))
    history_time.append(datetime.datetime.now().strftime('%H:%M'))
    history_main_price.append(np.median(main_price))
    history_other_price.append(np.median(other_price))

    mix = np.dot(history_main_price, alpha) + np.dot(history_other_price, 1 - alpha)

    print("时间: "+ datetime.datetime.now().strftime('%H:%M'))
    print("综合价格: {}".format(mix[-1]))
    print("大商价格: {}".format(history_main_price[-1]))
    print("散户价格: {}".format(history_other_price[-1])+"\n")

    # 画图 & 数据保存
    if((count % frequency) == 0):

        # 数据保存
        data = pd.DataFrame({'time': history_time, 'dashang': history_main_price, 'sanhu': history_other_price})
        filename = datetime.datetime.now().strftime('%m%d') + '.csv'  # 按日期保存
        if os.path.exists(filename):
            ori_data = pd.read_csv(filename)
            # ori_data['time'] = datetime.datetime.strptime(pd.to_datetime(ori_data['time']), "%Y-%m-%d %H:%M")
            data = ori_data.append(data)
        data.to_csv(filename, index=False)

        history_time = data['time']
        history_main_price = data['dashang']
        history_other_price = data['sanhu']

        length = len(history_time)
        x_axis = np.linspace(0, length-1, length)
        # 计算综合价格
        mix = np.dot(history_main_price, alpha) + np.dot(history_other_price, 1 - alpha)


        # 绘图1
        plt.figure(figsize=(20, 5))
        plt.suptitle(u"DD373冒险岛2女王镇货币价格：{}".format(datetime.datetime.now().strftime('%m-%d'))
                     , fontsize="15")

        plt.plot(x_axis,history_main_price,label='大商价格',color='red',linewidth=1.0,linestyle='--') #默认
        plt.plot(x_axis,history_other_price,label='散户价格',color='orange',linewidth=1.0,linestyle='--')
        plt.plot(x_axis,mix,label='综合价格',color='blue',linewidth=1.2)
        # 标注方法
        plt.text(x_axis[0], mix[0]+0.35, "1:{}w".format(format(mix[0],"0.2f")))
        plt.text(x_axis[-1], mix[-1]+0.35, "1:{}w".format(format(mix[-1],"0.2f")))
        # 最大值&最小值

        max_index = mix.argmax()
        plt.annotate("max: 1:{}w".format(format(mix[max_index],"0.2f")) % mix[max_index],xy=(x_axis[max_index],mix[max_index]),xycoords='data',xytext=(-30,+30),textcoords='offset points',
                 color='red',arrowprops=dict(arrowstyle='->',color='red',connectionstyle='arc3,rad=-0.2'))
        min_index = mix.argmin()
        plt.annotate("min: 1:{}w".format(format(mix[min_index],"0.2f")) % mix[min_index],xy=(x_axis[min_index],mix[min_index]),xycoords='data',xytext=(+30,-30),textcoords='offset points',
                     color='green',arrowprops=dict(arrowstyle='->',color='green',connectionstyle='arc3,rad=-0.2'))

        plt.legend(loc='upper left')

        # 使x轴标签不要那么密集
        if length>40:
            tmp = length/20  # 分为二十份
            tmp2 = [k * tmp for k in range(20)] # 十份的坐标
            tmp2.append(length - 1)
            tmp2 = np.array(tmp2).round()
            plt.xticks(tmp2, history_time.ravel()[list(tmp2)])
        else:
            plt.xticks(np.arange(length), history_time)



        # 保存图片
        fig = plt.gcf()
        tmp = datetime.datetime.now().strftime('%m%d')+ '.png'
        fig.savefig(tmp)
        plt.close()

        history_main_price = []
        history_other_price = []
        history_time = []

    time.sleep(sleep_time)