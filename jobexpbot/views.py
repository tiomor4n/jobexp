from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from django.views.decorators.csrf import csrf_exempt
from .gspread import GetJobDesc
from .utility import ReadFromStaticBOT,WriteToStaticBOT,CheckStep,CheckDialog,RemoveDialog
from .models import oper_para





@csrf_exempt
def callback(request):
    import sys
    from jobexpbot import utility
    sys.setdefaultencoding='utf8'
    def getpara():
        strapi1 = oper_para.objects.get(name='strapi1').content
        strapi2 = oper_para.objects.get(name='strapi2').content

        strapi = strapi1 + strapi2
        strparser = oper_para.objects.get(name='webhookparser').content
        #line_bot_api = LineBotApi(strapi)

        #parser = WebhookParser(oper_para.objects.get(name='webhookparser').content)

        return strapi,strparser


    def LineMsgOut(mid,message):
        sendmsgstr = '{"events":[{"source":{"userId":"' + mid + '"},"message":{"text":"'+ message + '"}}]}'
        #print sendmsgstr
        WriteToStaticBOT(sendmsgstr,"reply")
        
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


    import json
    import requests
    def post_text(reply_token, text):
        REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + strapi
        }
        payload = {
              "replyToken":reply_token,
              "messages":[
                    {
                        "type":"text",
                        "text": text
                    }
                ]
        }
        requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))

    
    strapi, strparser = getpara()

    line_bot_api = LineBotApi(strapi)
    parser = WebhookParser(strparser)    


    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        #print body
        jdata = json.loads(body)
        mid = jdata['events'][0]['source']['userId']
        events = None
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message,TextMessage):
                    print (event.reply_token)

                    '''
                    line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text),
                        )
                    '''
                    if event.message.text == u'精選職缺':
                    	#print (u'以下是精選職缺:')
                        '''
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'讀取職缺資訊中:' ),
                        )
                        '''
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'以下是精選職缺:\n' + GetJobDesc()),
                        )
                    elif event.message.text == u'使用說明':
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'請點選下方的功能選單開始使用'),
                        )
                    elif event.message.text == u'關於我們':
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'我們是北台灣最大的就業服務業者，針對您的需求提供最完善且專業的建議，目前已有約2萬名求職者透過我們找到工作，我們將竭盡所能提您服務！'),
                        )
                        
                    elif event.message.text == u'我要應徵':
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        WriteToStaticBOT(body,"ask")
                        purporse,step,last_ask,last_reply,timestamp = CheckStep(mid)
                        print (last_ask)
                        if last_ask == u'我要應徵':
                            line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'請點擊下方的鍵盤，輸入您要應徵的工作ID'),
                        )
                        LineMsgOut(mid = mid,message = 'input job id')
                    
                    elif event.message.text == u'確定輸入':
                        if CheckDialog(mid):
                            WriteToStaticBOT(body,"ask")
                            purporse,step,last_ask,last_reply,timestamp = CheckStep(mid)
                            print ('last_reply:' + last_reply)
                            if last_reply == 'input confirm':
                                print ('開始寫入流程')
                                utility.WriteCustProfile(mid)
                                if CheckDialog(mid):
                                    RemoveDialog(mid)
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    
                                      [TextSendMessage(text=u'輸入完成，感謝您提供資訊。'),
                                     TextSendMessage(text=u'我們會在第一時間通知您，也別忘了常回來逛逛喔'),
                                     StickerSendMessage(package_id='1',sticker_id='2')
                                    ]
                                )
                        else:
                            line_bot_api.reply_message(
                                     event.reply_token,
                                     TextSendMessage(text=u'我無法辨識您的輸入，可能您閒置太久，建議您從下方選單重新開始輸入'),
                                )
                            
                    else:
                        if CheckDialog(mid):
                            WriteToStaticBOT(body,"ask")
                            purporse,step,last_ask,last_reply,timestamp = CheckStep(mid)
                            print (last_reply)
                            if last_reply == 'input job id':
                                print (u'進入輸入流程2')
                                line_bot_api.reply_message(
                                     event.reply_token,
                                     TextSendMessage(text=u'請輸入您的姓名'),
                                )
                                LineMsgOut(mid,u'input cust name')
                            elif last_reply == 'input cust name':
                                print (u'進入輸入流程3')
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=u'請輸入您的電話'),
                                )
                                LineMsgOut(mid,u'input cust tel')
                            elif last_reply == 'input cust tel':
                                print (u'進入輸入流程4')
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=u'請輸入您的性別'),
                                )
                                LineMsgOut(mid,u'input cust gender')
                            elif last_reply == 'input cust gender':
                                print (u'進入輸入流程5')
                                confirm_template = ConfirmTemplate(text=u'請確定輸入', actions=[
                                     MessageTemplateAction(label=u'是', text=u'確定輸入'),
                                     MessageTemplateAction(label=u'否', text=u'否'),
                            
                                ])
                                template_message = TemplateSendMessage(
                                alt_text=u'請確定輸入', template=confirm_template)
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    template_message,
                                )
                                LineMsgOut(mid,u'input confirm')
                            '''  
                            elif last_reply == 'input confirm':
                                if last_ask in [u'男',u'女']:
                                    
                                else:
                                    line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=u'停止輸入流程'),
                                    )
                                if CheckDialog(mid):
                                    RemoveDialog(mid)
                            '''

                        else:
                            line_bot_api.reply_message(
                                     event.reply_token,
                                     TextSendMessage(text=u'我無法辨識您的輸入，可能您閒置太久，建議您從下方選單重新開始輸入'),
                                )





                    '''
                    輸入要項: ID,姓名,電話,性別,確認輸入
                    '''

        return HttpResponse()

    if request.method == 'GET':
        print ('from get')
        return HttpResponse('from get')

