import json
from flask import Flask, request, abort
# from flask_ngrok import run_with_ngrok
from config import DevConfig
import train_info
import parse_helper
import datetime
import pytz

from linebot import (
    LineBotApi, WebhookHandler
 )
from linebot.exceptions import (
    InvalidSignatureError
 )

from linebot.models import *


app = Flask(__name__)


line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

app.config.from_object(DevConfig)
# run_with_ngrok(app) # Start ngrok when app is run

LINE_USER_ID = 'YOUR_USER_ID'

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as Text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    msg_to_send='呀哈囉，我是可以查詢火車時刻的機器人( ﾟДﾟ)，請詳閱以下說明:'
    tutorial_img = 'https://raw.githubusercontent.com/shinano42/train-search-bot-taiwan/master/tutorial.png'
    line_bot_api.push_message(LINE_USER_ID, TextMessage(text=msg_to_send))
    line_bot_api.push_message(LINE_USER_ID, ImageSendMessage(original_content_url=tutorial_img, preview_image_url=tutorial_img))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    staions_to_mapping =  train_info.get_stations_data()
    if parse_helper.is_command_format(event.message.text):
        data = parse_helper.parse_commands(event.message.text)
        if data[0] == 'b':     
            station_x_index =  train_info.get_index(data[1], staions_to_mapping)
            if (station_x_index != -1):
                station_code =  staions_to_mapping[station_x_index]['Station_Code_4']
                print(station_code)
                lb = train_info.get_live_boardingTrain(station_code)
                print(train_info)
                print(train_info.filter_n_or_s)
                if len(data) > 2 and train_info.match_n_or_s(data[2]) != -1:
                    n_or_s = train_info.match_n_or_s(data[2])
                    result = filter(train_info.filter_n_or_s(n_or_s), lb)
                    lb_filtered = list(result)
                else:
                    lb_filtered = lb
                lb_filtered  = train_info.format_response_lb(lb_filtered)
                for i in range(len(lb_filtered)):
                    line_bot_api.push_message(LINE_USER_ID, TextMessage(text=lb_filtered[i]))

            else:
    #             command Error
                line_bot_err_response = 'Error! 查詢條件錯誤，請詳細閱讀查詢方法'
                line_bot_api.reply_message(event.reply_token, TextMessage(text=line_bot_err_response))
                print('Command Error')

        elif data[0] == 'sts' and len(data) > 2:
            tw = pytz.timezone('Asia/Taipei')
            present = datetime.datetime.now(tw)
            present_date = present.strftime("%Y-%m-%d")
            present_time = present.strftime("%H:%M")
            print(present_time)
            station_from_index = train_info.get_index(data[1], staions_to_mapping)
            station_to_index = train_info.get_index(data[2], staions_to_mapping)
            if (station_from_index != -1 and station_to_index != -1):
                station_from_code = staions_to_mapping[station_from_index]['Station_Code_4']
                print(station_from_code)
                station_to_code = staions_to_mapping[station_to_index]['Station_Code_4']
                print(station_to_code)
                timetable = train_info.get_timetable_present_time(station_from_code, station_to_code, present_date, present_time)
                formated_timetable = train_info.format_response_tt(timetable)
                if len(formated_timetable) > 0:
                    for i in range(len(formated_timetable)):
                        line_bot_api.push_message(LINE_USER_ID, TextMessage(text=formated_timetable[i]))
                else:
                    line_bot_sorry_response = 'Sorry! 查不到相關的列車班次資料'
                    line_bot_api.push_message(LINE_USER_ID, TextMessage(text=line_bot_sorry_response))


            else:
                line_bot_err_response = 'Error! 查詢條件錯誤，請詳細閱讀查詢方法'
                line_bot_api.reply_message(event.reply_token, TextMessage(text=line_bot_err_response))
                print('Command Error')
        else:
            line_bot_err_response = 'Error! 查詢條件錯誤，請詳細閱讀查詢方法'
            line_bot_api.reply_message(event.reply_token, TextMessage(text=line_bot_err_response))

    elif event.message.text == u'==':
        present = datetime.datetime.now()
        present_year = present.strftime("%Y")
        message_to_send = '都已經{}了，還有人打==表情符號還忘記空白喔'.format(present_year)
        line_bot_api.push_message(LINE_USER_ID, TextMessage(text=message_to_send))
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')