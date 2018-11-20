## 分析
打开[网页](http://www.mmjpg.com)进行分析，发现这个网站挺简单的。  
图片链接呢，只是按年份和图集的id进行区分。  
只是**2018**年的稍微有点不同，需要一个ajax来获取图片链接的后缀进行拼接图集中的翻页操作。  
所以一开始只需要获取图集的名字、所属年份和对应的id。  
后续只需要字符拼接即可获取图片链接。  
所以一开始得出下面的代码。
```python
import requests
import re

# 打开网页函数
def get_response(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
    response = requests.get(url, headers) # 加上浏览器头，以防被禁
    response.encoding = 'utf-8'      # 指定编码格式
    #response.encoding = 'gbk'      # 指定编码格式
    return response

def data_to_dict(response,data_dict):
    req = r'<ul>(.*?)</ul>'
    re_str = re.findall(req,response,re.S)[0].strip()
    req = r'<li>.*?<img src="http://fm.shiyunjj.com/small/(.*?)/(.*?).jpg".*?alt="(.*?)".*?</li>'
    data_list = re.findall(req,re_str,re.S)
    for i in data_list:
        data_dict[i[1]] = {'meizi_year':i[0],'meizi_titile':i[2]}
    return data_dict
def writeFile(max_pages,content):
    with open('meizi_data.py','w',encoding='utf-8')as txt_file:

        txt_file.write('meizi_data = {\n')
        for line in content:

            txt_file.write("'"+ str(line) + "':{'meizi_year':'" + content[line]['meizi_year'] + "', 'meizi_titile': '" + content[line]['meizi_titile'] + "'},\n")
        txt_file.write('\n}')

def main():
    data_dict = {}
    url = 'http://www.mmjpg.com'
    response = get_response(url).text
    req = r'<em class="info">共(.*?)页</em>'
    max_pages = int(re.findall(req,response)[0])+1
    data_dict = data_to_dict(response,data_dict)

    for i in range(2,max_pages):
        url_page = f'http://www.mmjpg.com/home/{i}'
        response = get_response(url_page).text
        data_d = data_to_dict(response,data_dict)
    writeFile(max_pages,data_d)

if __name__ == '__main__':
    main()

```
由于考虑到大多数人不会使用数据库，只能用**最无脑的方式**来生成数据表。  
正常的话，我一般会用mongoDB或者postgreSQL来完成这部分工作。  
## 获取图片
获取图片的话呢？
就简简单单的拼接字符链接就好了。  
但由于这个网站在2018年进行了升级，2017年后的图片都是要一个ajax来获取图片链接。  
故此分开处理。   
如下所示：
```python
import meizi_data
import requests
import os
def get_response(url,url_referer):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        'Referer':url_referer,
        }
    response = requests.get(url=url, headers=headers) # 加上浏览器头，以防被禁
    return response

def get_php_data(mm_id,img_title,img_year):
    headers = {
    'Accept':'*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host':'www.mmjpg.com',
    'Pragma': 'no-cache',
    'Referer': f'http://www.mmjpg.com/mm/{mm_id}',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    params = {
        'id': mm_id,
        'page': '8999'
    }
    url = 'http://www.mmjpg.com/data.php?'
    response = requests.get(url=url, headers=headers,params=params) # 加上浏览器头，以防被禁
    response.encoding = 'utf-8'      # 指定编码格式
    list_data = response.text.split(",")
    c = 1
    for i in list_data:
        b = f'http://fm.shiyunjj.com/{img_year}/{mm_id}/{c}i{i}.jpg'
        url_referer = f'http://www.mmjpg.com/mm/{mm_id}/'
        response = get_response(b,url_referer)
        path = f'download_img/{img_year}/{img_title}/{c}.jpg'
        f = open(path, 'wb')
        f.write(response.content)
        f.close()
        c+=1

def get_img(img_year,mm_id,img_title):

    for c in range(1,100):
        b = f'http://fm.shiyunjj.com/{img_year}/{mm_id}/{c}.jpg'

        url_referer = f'http://www.mmjpg.com/mm/{mm_id}/'
        response = get_response(b,url_referer)
        print(response.status_code)
        print(c)
        if response.status_code != 200:
            break
        else:
            path = f'download_img/{img_year}/{img_title}/{c}.jpg'
            f = open(path, 'wb')
            f.write(response.content)
            f.close()

def main():
    data_dict = meizi_data.meizi_data
    try:
        os.mkdir('download_img')
    except Exception as e:
        print('已创建 download_img 目录')

    for i in data_dict:
        img_year = data_dict[i]['meizi_year']
        img_title = data_dict[i]['meizi_titile']

        try:
            os.mkdir(f'download_img/{img_year}')
        except Exception as e:
            print('已创建图片年份目录')
        try:
            os.mkdir(f'download_img/{img_year}/{img_title}/')
        except Exception as e:
            print(f'已创建{img_title}目录')
        print(f'正在爬取《{img_title}》id为{i}')
        if img_year != '2018':
            img_link = get_img(img_year,i,img_title)
        else:
            img_link = get_php_data(i,img_title,img_year)


if __name__ == '__main__':
    main()
```
## 总结
本次的爬虫，只要稍加**分析**，除了2017年后的图片需要动态处理的操作。  
其他年份的只需要利用**撞库**的方式就可以进行全站爬取了。  
没什么技术含量。
