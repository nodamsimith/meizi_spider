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
