import requests as req
from bs4 import BeautifulSoup
import re
from CONFIG import INFO_COLLECTION


def get_content(aritcle_id):
    session = req.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Priority': 'u=1, i',
        'Referer': 'https://web.archive.org/',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    # 获取年
    year = session.get(
        f"https://web.archive.org/__wb/sparkline?output=json&url=http://www.u148.net/article/{aritcle_id}.html&collection=web",
        headers=headers).json()

    if year['status']:
        time: str = year['first_ts']
        if int(time[:8]) < 20180703:
            con_response = session.get(
                f"https://web.archive.org/web/{time}/http://www.u148.net/article/{aritcle_id}.html", headers=headers)
        soup = BeautifulSoup(con_response.content, 'lxml')

        if soup.find('h1').text =='抱歉，找不到你想要的页面……':
            INFO_COLLECTION.update_one({'id': aritcle_id}, {'$set': {'status': 'failed'}})
            log.log_message(f"Failed to get content of article {aritcle_id}")
            return
        try:
            # 获取标题
            title = soup.find('h1').text

            # 获取内容
            content = soup.find('div', id='txtcon').get_text('\n')

            # 获取作者
            author = soup.find('div', id='mainbox').find('div', id='left').find_all('center')[1].find('a').text

            # 获取发布时间
            publish_time = re.search(r'\d{4}-\d{2}-\d{2}',
                                     soup.find('div', id='mainbox').find('div', id='left').find_all('center')[1].text).group()


        except AttributeError:
            # 获取标题
            title = soup.find('h1').text


            # 获取内容
            content = soup.find('div', class_='contents').get_text('\n')


            # 获取作者

            author = soup.find('div', class_='user-info').find('div', class_='name').find('a').text

            # 获取发布时间
            publish_time = re.search(r'\d{4}-\d{2}-\d{2}',soup.find('div',class_='content').find('div',class_='status').text).group()
        finally:
            INFO_COLLECTION.update_one({'id': aritcle_id}, {'$set': {'title': title, 'content': content, 'author': author, 'publish_time': publish_time,'status': 'ok'}})
            log.log_message(f"Successfully get content of article {aritcle_id}")
    else:
        INFO_COLLECTION.update_one({'id': aritcle_id}, {'$set': {'status': 'failed'}})
        log.log_message(f"Failed to get content of article {aritcle_id}")

if __name__ == '__main__':
    from log_tool import Mylog
    log = Mylog('main')
    results = INFO_COLLECTION.find({'id': {'$exists': True},'status':{'$exists': False}}).sort('id', 1).limit(20)
    id_list = [result['id'] for result in results]
    # print(list(results))
    for id in id_list:
        log.log_message(f"Start to get content of article {id}")
        get_content(id)


