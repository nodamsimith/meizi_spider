import meizi_104_11_20
import requests
import os
def get_response(url,url_referer):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Referer':url_referer,
        }

    response = requests.get(url=url, headers=headers) # 加上浏览器头，以防被禁
    #response.encoding = 'utf-8'      # 指定编码格式
    #response.encoding = 'gbk'      # 指定编码格式
    return response
def main():
    url = 'http://fm.shiyunjj.com/2018/1539/1ine.jpg'
    ref = 'http://www.mmjpg.com/mm/1539/'
    response = get_response(url,ref)
    f = open('1.jpg', 'wb')
    f.write(response.content)
    f.close()

if __name__ == '__main__':
    main()
