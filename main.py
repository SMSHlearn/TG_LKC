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
def drive_handler(update: Update, context: CallbackContext) -> None:
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING) # 會顯示chatbot正在輸入中，增加對話真實感
    time.sleep(1) # 在顯示輸入中後停頓1秒，然後顯示下一句code的文字
    context.bot.send_message(chat_id=update.effective_chat.id , text=drive_msg , parse_mode='HTML', disable_web_page_preview=True)


# def setdrive_handler(update: Update, context: CallbackContext) -> None:
#      bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING) # 會顯示chatbot正在輸入中，增加對話真實感
#     time.sleep(1) # 在顯示輸入中後停頓1秒，然後顯示下一句code的文字



# def code_handler() -> None:

# def unsetdrive_handler() -> None:


#start
def start_handler(update: Update, context: CallbackContext) -> None:
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING) # 會顯示chatbot正在輸入中，增加對話真實感
    time.sleep(1) # 在顯示輸入中後停頓1秒，然後顯示下一句code的文字
    context.bot.send_message(chat_id=update.effective_chat.id , text=help_msg , parse_mode='HTML', disable_web_page_preview=True)


# 推播管理相關callback
# def list_handler() -> None:


# def delete_handler() -> None:

# def serch_handler() -> None:

# def schedule_handler() -> None:








"""
Other Function
"""

# CommandHandler的集合
def command() -> None:
    # dispatch設定
    dispatcher = updater.dispatcher
     # 開始與幫助指令
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('help', start_handler))


    # Google Drive相關指令
    dispatcher.add_handler(CommandHandler('drive' , drive_handler))
    # Start the Bot
    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    help_msg = '歡迎使用LKC_stock股票機器人，機器人會根據你提供的股票代號或名稱，會從證券交易所證(TWSE) 券櫃台買賣中心 (TPEX)爬取當日的股票內容給您！\n' \
        '機器人具有,<b>每日推播</b>的功能與<b>自動上傳到Google Drive</b>的功能，以下為使用說明：\n\n' \
        '<b>搜尋功能與推播設定</b>\n' \
        '/serch 2330 - 直接搜尋關鍵字 【2330 台積電】\n' \
        '/schedule 台積電 - 點選底下按鈕設定，將於每日開盤前或開盤後推播【台積電】股市資料給您\n\n' \
        '<b>管理您的推播列表</b>\n' \
        '/list - 列出推播列表\n' \
        '/delete - 選取關鍵字並刪除\n\n' \
        '<b>Google Drive設定</b>\n' \
        '/drive - 觀看如何設定\n\n' \
        '/help - 列出此列表'

    drive_msg = 'LKC_stock可以將每次的搜尋結果存成.csv檔上傳到Google Drive上，建議使用Excel開啟！\n' \
            '\n/setdrive - 授權您的Google Drive權限給機器人，僅需授權一次\n' \
            '/unsetdrive - 取消授權\n' \
            '\n授權成功後，機器人會在您的Google Drive上建立名為『股票每日資訊』的資料夾，並把結果存進去！'




    TOKEN = config.config.Token
    bot = telegram.Bot(token = TOKEN)
    updater = Updater(TOKEN, use_context = True)
    command()

