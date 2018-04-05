# -*- coding: utf-8 -*- 

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ButtonsTemplate,
    TextSendMessage, ImageSendMessage, TemplateSendMessage,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction
)


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('b0oOxY7hM4rb8AGClOYmKtPqCIFK004tf55cbZ3QZZNr+/bUZEKve1+flyNG//vRjMHK5xt6XLZcqhrs6B8v5gW6dKC5BIb26wDDfUCekK5AbObpdycypf49s+v3r3IqWVqRWvoQ267sLm2Rk4BO/AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('33741068f54f5270a576abb88087fc3a')


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
        buttons_template_message = TemplateSendMessage(
                alt_text = 'Buttons template', 
                template = ButtonsTemplate(
                        thumbnail_image_url = 'https://example.com/image.jpg',
                        title = 'Menu',
                        text = 'Please select',
                        actions = [
                                PostbackTemplateAction(
                                        label = 'postback',
                                        text = 'postback text',
                                        data = 'action=buy&itemid=1'
                                ),  
                                MessageTemplateAction(
                                        label = 'message',
                                        text = 'message text'
                                ),   
                                URITemplateAction(
                                        label = 'uri',
                                        uri = 'http://example.com/'
                                )            
            
                        ]
                )
        )
        line_bot_api.reply_message(event.reply_token, 
        TextSendMessage(buttons_template_message)) 
        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text + '\n學你說話XD'))
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    

   
    
    
    
    
