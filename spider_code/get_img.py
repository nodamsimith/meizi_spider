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
