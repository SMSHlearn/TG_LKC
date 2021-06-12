from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton,Update,ForceReply
import telegram
import logging
import os
import json
import time
import config.config
import utils

"""
Callback Function
"""
# Google Drive Callback
def drive_handler(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id , text=drive_msg , parse_mode='HTML', disable_web_page_preview=True)

def setdrive_handler(update: Update, context: CallbackContext) -> None:
    #mongodb
    #
    # local
    if os.path.isfile(f'json/{update.effective_chat.id}.json'):
        context.bot.send_message(chat_id=update.effective_chat.id, text='您已授權過機器人囉！')
        return

    authorize_url = utils.get_authorize_url()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'請點擊連結完成授權，並回傳"/code <產生的授權碼>"，例如：\n'
                             f'/code abc123\n{authorize_url}\n')

def code_handler(update:Update , context:CallbackContext) -> None:
    auth_code = context.args[0]
    msg = utils.save_drive_credential(chat_id=update.effective_chat.id, code=auth_code)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def unsetdrive_handler(update:Update , context:CallbackContext) -> None:
    try:
        # mongodb
        #
        # local
        os.remove(f'json/{update.effective_chat.id}.json')
        context.bot.send_message(chat_id=update.effective_chat.id, text='已取消授權！')
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='您還沒設定授權哦！')


#start
def start_handler(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id , text=help_msg , parse_mode='HTML', disable_web_page_preview=True)


 # 開發者資料 Callback
def info_handler(update:Update , context:CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id , text=info_msg , parse_mode='HTML', disable_web_page_preview=True)

# 推播管理相關callback
def list_handler(update:Update , context:CallbackContext) -> None:
    keywords = have_keywords(update, context)
    if keywords:
        context.bot.send_message(chat_id=update.effective_chat.id, text='您目前推播的搜尋關鍵字有：\n'+'\n'.join(keywords))


def delete_handler(update:Update , context:CallbackContext) -> None:
    keywords = have_keywords(update, context)
    if keywords:
        keyboard = [[InlineKeyboardButton(keyword, callback_data=i)] for i, keyword in enumerate(keywords)]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id, text='請選取要取消推播的關鍵字', reply_markup=reply_markup)

# def button(update:Update, _:CallbackContext):
#     index = int(user_data[str(update.effective_chat.id)])
#     query = update.callback_query
#     keyword, push_time = user_data['users'][index]['keywords'][int(query.data)]
#     user_data['users'][index]['keywords'].pop(int(query.data))
#     update_user_data(update.effective_chat.id, None, None)

#     sd.clear(f'{update.effective_chat.id}_{keyword}_{push_time}')

#     query.answer()
#     query.edit_message_text(text=f'已刪除【{keyword} @{push_time}】')



def search_handler(update:Update , context:CallbackContext) -> None:
    if context.args == []:
        context.bot.send_message(chat_id=update.effective_chat.id, text='請在 /search 後輸入搜尋關鍵字')
        return
    keyword = ' '.join(context.args)
    bot.send_message(chat_id=update.effective_chat.id, text=f'正在爬取【{keyword}】，請稍待...\n')
    csv_data = utils.stock_crawler(keyword, update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=csv_data)



# def schedule_handler(update:Update , context:CallbackContext) -> None:
#     try:
#         keyword, push_time = map(str.strip, ' '.join(context.args).split('@'))
#     except:
#         unknown(update, context)
#         return

#     try:
#         sd.every().day.at(push_time).do(push, update.effective_chat.id, keyword).tag(
#             f'{update.effective_chat.id}_{keyword}_{push_time}')

#         update_user_data(update.effective_chat.id, keyword, push_time)
#         context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text=f'成功加入推播列表！\n機器人將在每日{push_time}推播爬取【{keyword}】之資訊給您')
#     except Exception as e:
#         context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text=f'時間格式有誤哦！請重新輸入\n格式為24小時制，缺空須補0，如09:05')

# 看不懂的訊息
def unknown(update:Update, context:CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='機器人看不懂您說什麼\n請用 /help 觀看使用說明')


"""
Other Function
"""

def have_keywords(update, context):
    try:
        index = int(user_data[str(update.effective_chat.id)])
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="您目前沒有排程任何關鍵字")
        return None
    keywords = user_data['users'][index]['keywords']
    if keywords.__len__() == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="您目前沒有排程任何關鍵字")
        return None

    keywords_to_display = [f'{d[0]} @{d[1]}' for d in keywords]

    return keywords_to_display

# CommandHandler的集合
def command() -> None:
    # dispatch設定
    dispatcher = updater.dispatcher
     # 開始與幫助指令
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('help', start_handler))
    # 直接搜尋指令
    # 推播相關指令

    # Google Drive相關指令
    dispatcher.add_handler(CommandHandler('drive' , drive_handler))
    dispatcher.add_handler(CommandHandler('setdrive' , setdrive_handler))
    dispatcher.add_handler(CommandHandler('code' , code_handler))
    dispatcher.add_handler(CommandHandler('unsetdrive' , unsetdrive_handler))
    # 開發者資料
    dispatcher.add_handler(CommandHandler('info' , info_handler))
    # 推播管理相關
    # dispatcher.add_handler(CommandHandler('list' , list_handler))
    # dispatcher.add_handler(CommandHandler('delete' , delete_handler))
    #搜尋與推播關鍵字設定
    dispatcher.add_handler(CommandHandler('search' , search_handler))
    # dispatcher.add_handler(CommandHandler('schedule' , schedule_handler))
    # 看不懂的訊息
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, unknown))
    # Start the Bot
    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    help_msg = '歡迎使用LKC_stock股票機器人，機器人會根據你提供的股票代號或名稱，會從<b>基本市況報導網站</b>爬取當日的股票內容給您！\n' \
        '機器人具有,<b>每日推播</b>的功能與<b>自動上傳到Google Drive</b>的功能，以下為使用說明：\n\n' \
        '<b>搜尋功能與推播設定</b>\n' \
        '/search 2330 - 直接搜尋關鍵字 【2330 台積電】\n' \
        '/schedule 台積電 - 點選底下按鈕設定，將於每日開盤前或開盤後推播【台積電】股市資料給您\n\n' \
        '<b>管理您的推播列表</b>\n' \
        '/list - 列出推播列表\n' \
        '/delete - 選取關鍵字並刪除\n\n' \
        '<b>Google Drive設定</b>\n' \
        '/drive - 觀看如何設定\n\n' \
        '/help - 列出此列表\n' \
        '/info - 列出開發者資料'


    drive_msg = 'LKC_stock可以將每次的搜尋結果存成.csv檔上傳到Google Drive上，建議使用Excel開啟！\n' \
            '\n/setdrive - 授權您的Google Drive權限給機器人，僅需授權一次\n' \
            '/unsetdrive - 取消授權\n' \
            '\n授權成功後，機器人會在您的Google Drive上建立名為『股票每日資訊』的資料夾，並把結果存進去！'

    info_msg = '<b>開發者</b> Developers: yang-lin94(github)\n' \
            '<b>參與者</b> Partner: leon921120(github) jimmy1214(github)\n' \
            '<b>源碼</b> Source:  https://github.com/SMSHlearn/TG_LKC\n' \
            '<b>協助</b> Support Server: https://t.me/LKC_stock_bot \n'\
            '<b>版本</b>: Version V1.0a\n\n' \
            '<b>Made with ❤️</b>'


    # local
    os.makedirs('json', exist_ok=True)

    # local
    # if not os.path.exists(user_data_filename):
    #     with open(user_data_filename, 'w') as json_file:
    #         initial_json = {'users': []}
    #         json.dump(initial_json, json_file, indent=2)
    # with open(user_data_filename, 'r') as f:
    #     user_data = json.load(f)




    TOKEN = config.config.Token
    bot = telegram.Bot(token = TOKEN)
    updater = Updater(TOKEN, use_context = True)
    command()