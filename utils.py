from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import csv
import json
import pymongo
import pandas as pd
import requests
import config.config

def stock_crawler(keyword, chat_id):
    """
    爬取網頁並回傳csv data
    """
    #mongodb
    #
    # local
    have_setdrive = os.path.isfile(f'user_credentials/{chat_id}.json')
    s = "|"
    stocks = []
    data = []
    csv_data = []
    num = 0

    stocks.append(keyword)
    for x in stocks:
        keyword = x
        url_base = f'tse_{keyword.replace("", "")}.tw'
        data.append(url_base)
    try:
        l = (s.join( data ))
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+l
        res = requests.get(url)
        data = res.json()

        for stocks in data:

            name = data['msgArray'][num]['n']
            accumulation_volume =  data['msgArray'][num]['v']
            oprice = data['msgArray'][num]['o']
            hprice = data['msgArray'][num]['h']
            lprice = data['msgArray'][num]['l']
        csv_data = name  + f'\n累積成交量:{accumulation_volume}' + f'\n開盤價:{oprice}' + f'\n當日最高價:{hprice}' + f'\n當日最低價:{lprice}'
        # csv_data.append([name,f'累積成交量:{accumulation_volume}',f'開盤價:{oprice}',f'當日最高價:{hprice}',f'當日最低價:{lprice}' ])
    except Exception as e:
        csv_data = '查無此股票資料,請確認代碼是否輸入正確'

    return csv_data


# def write_csv(csv_data):

def get_authorize_url():
    gauth = GoogleAuth()
    return gauth.GetAuthUrl()

def save_drive_credential(chat_id, code):
    try:
        gauth = GoogleAuth()
        gauth.Auth(code)
        gauth.SaveCredentialsFile(f'json/{chat_id}.json')
        return '授權成功！'
    except Exception as e:
        return '授權失敗！可能是格式錯了之類的QQ，麻煩再試一次'

# def upload_drive(keyword, chat_id):

# #     # check folder是否已存在
#     folder_name = '股票每日開資訊'
#     folder_id = None
#     folder_list = drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder' and trashed = false"}).GetList()
#     for folder in folder_list:
#         if folder['title'] == folder_name:
#             folder_id = folder['id']
#             break

#     if not folder_id:
#         folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
#         folder.Upload()
#         folder_id = folder['id']

#     date = '_'.join(map(str, time.localtime()[0:3]))
#     filename = f'{date}_{keyword}.csv'

#     # lcoal永遠都存temp.csv，上傳到雲端的再有custom filename
#     file = drive.CreateFile({'title': filename, 'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]})
#     file.SetContentFile(filename='temp.csv')
#     file.Upload()