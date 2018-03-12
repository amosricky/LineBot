from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import echobot.user as user
import json

#傳訊息給Line，讓Line轉傳給使用者(傳給 Line Server)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
#Parse這個訊息的所有欄位(接收Line Server)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        #是否從Line Server來的
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        #先判斷這個事件是不是訊息事件，而這個訊息是不是文字訊息
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    eventjson = event.as_json_dict()
                    userID = eventjson['source']['userId']
                    TimeStamp = eventjson['timestamp']
                    exist = user.userexist(userID)
                    user.useradd(exist,userID,TimeStamp)

                    #讓我們傳訊息給Line Server
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
