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

# 汉字输出
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

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
    main_price = 0
    other_price = 0
    price = find_prices(url)
    for i in range(18):
        if i <= 2:
            main_price += float(price[i][3:8])
        else:
            other_price += float(price[i][3:8])
    history_time.append(datetime.datetime.now())
    history_main_price.append(np.mean(main_price)/3)
    history_other_price.append(np.mean(other_price)/15)
    mix = np.dot(history_main_price, 0.6) + np.dot(history_other_price, 0.4)

    print("时间: "+ datetime.datetime.now().strftime('%m-%d %H:%M'))
    print("综合价格: {}".format(mix[-1]))
    print("大商价格: {}".format(history_main_price[-1]))
    print("散户价格: {}".format(history_other_price[-1])+"\n")

    #画图 & 数据保存
    if((count % 3) ==0):
        data = pd.DataFrame({'时间': history_time, '大商价格': history_main_price, '散户价格': history_other_price})
        data.to_csv('data.csv')

        plt.figure(figsize=(20, 5))
        plt.suptitle(u"DD373冒险岛2女王镇货币价格：{}".format(datetime.datetime.now().strftime('%m-%d'))
                     , fontsize="15")

        plt.plot(history_time,history_main_price,label='大商价格',color='red',linewidth=1.0,linestyle='--') #默认
        plt.plot(history_time,history_other_price,label='散户价格',color='orange',linewidth=1.0,linestyle='--')
        plt.plot(history_time,mix,label='综合价格',color='blue',linewidth=1.2)
        # 标注方法
        plt.annotate("1:{}w".format(format(mix[0],"0.2f")) % mix[0],xy=(history_time[0],mix[0]),xycoords='data',xytext=(+20,-20),textcoords='offset points',
                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.2'))
        plt.annotate("1:{}w".format(format(mix[-1],"0.2f")) % mix[-1],xy=(history_time[-1],mix[-1]),xycoords='data',xytext=(+20,-20),textcoords='offset points',
                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.2'))
        # 最大值&最小值
        max_index = history_main_price.index(max(history_main_price))
        plt.annotate("max: 1:{}w".format(format(mix[max_index],"0.2f")) % mix[max_index],xy=(history_time[max_index],mix[max_index]),xycoords='data',xytext=(-20,+20),textcoords='offset points',
                 color='red',arrowprops=dict(arrowstyle='->',color='red',connectionstyle='arc3,rad=-0.2'))
        min_index = history_main_price.index(min(history_main_price))
        plt.annotate("min: 1:{}w".format(format(mix[min_index],"0.2f")) % mix[min_index],xy=(history_time[min_index],mix[min_index]),xycoords='data',xytext=(+20,-20),textcoords='offset points',
                     color='green',arrowprops=dict(arrowstyle='->',color='green',connectionstyle='arc3,rad=-0.2'))

        plt.legend(loc='best')

        # 保存
        fig = plt.gcf()
        tmp = datetime.datetime.now().strftime('%m%d')+ '.png'
        fig.savefig(tmp)

    time.sleep(60)


while(False):
    def get_week_day(date):
      week_day_dict = {
        0 : '星期一',
        1 : '星期二',
        2 : '星期三',
        3 : '星期四',
        4 : '星期五',
        5 : '星期六',
        6 : '星期天',
      }
      day = date.weekday()
      return week_day_dict[day]



    history_main_price = []
    history_other_price = []
    history_time = []
    while(1):
        main_price = 0
        other_price = 0
        url = 'http://www.dd373.com/s/1xj2qx-wjm3vp-qmfpmj-0-0-0-tr1r70-0-0-0-0-su-0-512-0.html'
        request_headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
                }

        response = requests.get(url,headers=request_headers)

        data = response.text
        regex = '1元=\d\d...'
        pa = re.compile(regex)
        ma = re.findall(pa,data)
        for i in range(13):
                if i <= 2:
                        main_price += float(ma[i][3:8])
                else:
                        other_price += float(ma[i][3:8])
        history_time.append(datetime.datetime.now())
        history_main_price.append(np.mean(main_price)/3)
        history_other_price.append(np.mean(other_price)/10)

        plt.figure(figsize=(10,5))
        #画图
        mix = np.dot(history_main_price,0.6)+ np.dot(history_other_price,0.4)
        plt.plot(history_time,history_main_price,label='大商价格',color='red',linewidth=1.0,linestyle='--') #默认
        plt.plot(history_time,history_other_price,label='散户价格',color='orange',linewidth=1.0,linestyle='--')
        plt.plot(history_time,mix,label='综合价格',color='blue',linewidth=1.2)
        plt.legend(loc='best')
        fig = plt.gcf()
        tmp = datetime.datetime.now().strftime('%m%d%H%M')+ '.png'
        fig.savefig(tmp)

        time.sleep(300)


        for j in range(len(history_main_price)):
            plt.text(history_main_price[j] , history_time, 'this is a sin(x)line')