# coding:utf-8
# by NeilShi 12/1/2017
import requests
import json
import os
import time

qq = 627911861

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'xxxxxxx',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'
}

url_x = 'https://mobile.qzone.qq.com/list?qzonetoken=c6cc7f81ed510c92c831d503633b4678762f978e73d54b7e04a228594e89521f874ba4f69dc34e539d962a47d4cc&g_tk=126821817&res_attach=att%3D'
url_y = '%26tl%3D1508257557&format=json&list_type=shuoshuo&action=0&res_uin=627911861&count=40&sid=iGQXe%2Fz94beC%2B2gdufVwhKBi%2Bby6nw60256d2cb50201%3D%3D'
numbers = 0             # ‘查看更多’翻页
like_me_list = []       # 存放点赞宝宝全集
like_me_result = {}     # 点赞结果分析
qq_list = []            # 记录QQ
result = {}             # 记录排序后的最终结果
page = int(1762 / 40) + 1


for i in range(0, page):
    try:
        html = requests.get(url_x + str(numbers) + url_y, headers=headers).content
        data = json.loads(html)

        if 'vFeeds' in data['data']:
            for vFeed in data['data']['vFeeds']:
                if 'like' in vFeed:
                    for like_man in vFeed['like']['likemans']:
                        qq_list.append(int(like_man['user']['uin']))
                        # 这个dict需要定义在循环内，因为下面list.append()是引用传递
                        like_me_map = dict()
                        like_me_map['nick_name'] = like_man['user']['nickname']
                        like_me_map['qq'] = like_man['user']['uin']
                        like_me_list.append(like_me_map)
        numbers += 40
        time.sleep(10)
        print('正在分析前' + str(numbers) + '条数据')
    except:
        numbers += 40
        time.sleep(10)
        print('第' + str(numbers) + '条数据附近分析出错')


# 建立一个QQ与昵称对应的map，以便查询
qq_name_map = dict()
for man in like_me_list:
    qq_name_map[man['qq']] = man['nick_name']

# 计算点赞次数，并将次数与QQ映射存入map
qq_set = set(qq_list)
for qq in qq_set:
    like_me_result[str(qq)] = qq_list.count(qq)

# 以下处理为：按点赞次数排序后存入一个新的map作为最终结果，代码很不优雅=。=
num_result = sorted(like_me_result.values(), reverse=True)
print(num_result)
for num in num_result:
    for key in like_me_result.keys():
        if like_me_result[key] == num:
            result[qq_name_map[key]+'(' + key + ')'] = num


try:
    with open(os.getcwd() + '\\' + 'like_me_result.txt', 'wb') as fo:
        for k, v in result.items():
            record = k + ': 点赞' + str(v) + '次！\r\n'
            fo.write(record.encode('utf-8'))
        print("点赞数据结果分析写入完毕")

except IOError as msg:
    print(msg)




