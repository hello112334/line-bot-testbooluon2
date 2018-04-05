# -*- coding: utf-8 -*- 

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import requests
from bs4 import BeautifulSoup   

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('AzH87TcvfQKLWSRFu2ziKsU10gIyDwK5TeMlgmnzoF+M3WAW1Jdtvmjq/BlF4wqlYNicqEJ3QzmReL7EQ5/dbxlNNROsVLMNMAZ6yJquRVTTNEG2msiups++EZJmHrjj2cPYsIs2O2tpiCFykonofgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d4ad2ad65af463cd625172cb419f50e0')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def crewl_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'lxml')
    article_seq = []
    for r_ent in soup_.find_all(class_="recipes-sort"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find('data-count', class_="fav-count recipe-favorites").text
                url = 'https://icook.tw/' + link

                # 比對推文數
                if int(rate) >= 20:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq


r = requests.get('https://book.douban.com/subject/1084336/comments/')
soup = BeautifulSoup(r.text, 'lxml')
pattern = soup.find_all('p', 'comment-content')


def crewl_icook(res, push_rate):
    r = 'https://icook.tw/recipes/search?q={}&ingredients='.format(res)
    soup = BeautifulSoup(r.text, 'lxml')
    article_icook_seq = []
    for r_ent in soup.find_all(class_="recipes-sort"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                url_link = 'https://icook.tw/' + link
                article_icook_seq.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete', e)
    return article_icook_seq


def icook():
    rs = requests.session()
    load = {
        'from': 'https://icook.tw/?ref=nav',
        'yes': 'yes'
    }
    res = rs.post('https://icook.tw', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_icook = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://icook.tw/recipes/search?q={}&ingredients='.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_icook = crewl_icook(res)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for index, article in enumerate(article_icook, 0):
        if index == 15:
            return content
        data = '{}\n{}\n\n'.format(article.get('title', None), article.get('url_link', None))
        content += data
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)
    text = event.message.text   
    #recipeWeb = 'https://icook.tw/recipes/search?q=' + text + '&ingredients='
    #r = requests.get(recipeWeb)  
     
    if text == 'Hi':
        line_bot_api.reply_message(event.reply_token, 
        TextSendMessage(text='Hi, mate'))  
        
    elif text == 'book':
        line_bot_api.reply_message(event.reply_token, 
        TextSendMessage('https://icook.tw/recipes/search?q={}&ingredients='.format(text)))   
    
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text + '\n學你說話XD'))
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    

   
    
    
    
    
