import requests
import json
import os
import shutil
import time

qq = 627911861

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'xxxxxx',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'
}

url_x = 'https://mobile.qzone.qq.com/list?qzonetoken=9d29961d6fbb88be6236636010e0d4fde43a5b77d57ef984938b5aa0cb695e28c258a4d86b8c02a545bbcce970ff&g_tk=1573033187&res_attach=att%3D'
url_y = '%26tl%3D1508257557&format=json&list_type=shuoshuo&action=0&res_uin=627911861&count=40'
numbers = 0      # ‘查看更多’翻页
img_set = set()  # 存放图片url集
word_count = 0   # 文字说说计数器
words = ""       # 存放文字说说
images = ""      # 存放图片url
page = int(1761 / 40)


for i in range(0, page):
    try:
        html = requests.get(url_x + str(numbers) + url_y, headers=headers).content
        data = json.loads(html)
        # print(data)

        for vFeed in data['data']['vFeeds']:
            if 'pic' in vFeed:
                for pic in vFeed['pic']['picdata']['pic']:
                    img_set.add(pic['photourl']['0']['url'])

            if 'summary' in vFeed:
                # print(str(word_count) + '. ' + vFeed['summary']['summary'])
                words += str(word_count) + '. ' + vFeed['summary']['summary'] + '\r\n'
                word_count += 1
    except:
        print('error')

    numbers += 40
    time.sleep(10)

try:
    with open(os.getcwd() + '\\' + str(qq) + '.txt', 'wb') as fo:
        fo.write(words.encode('utf-8'))
        print("文字说说写入完毕")

    with open(os.getcwd() + '\\' + 'images_url', 'wb') as foImg:
        for imgUrl in img_set:
            images += imgUrl + '\r\n'
        foImg.write(images.encode('utf-8'))
        print("图片写入完毕")

except:
    print('写入数据出错')


if not img_set:
    print(u'不存在图片说说')
else:
    image_path = os.getcwd() + '\images'
    if os.path.exists(image_path) is False:
        os.mkdir(image_path)
    x = 1
    for imgUrl in img_set:
        temp = image_path + '/%s.jpg' % x
        print(u'正在下载地%s张图片' % x)
        try:
            r = requests.get(imgUrl, stream=True)
            if r.status_code == 200:
                with open(temp, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except:
            print(u'该图片下载失败:%s' % imgUrl)
        x += 1


