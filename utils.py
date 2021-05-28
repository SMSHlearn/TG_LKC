from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import csv
import json
import config.config
import pymongo

def stock_crawler():
    print("#")

def write_csv(csv_data):
    with open('temp.csv', 'w', encoding='utf-8-sig', errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

def get_authorize_url():
    gauth = GoogleAuth()
    return gauth.GetAuthUrl()

def save_drive_credential(chat_id, code):
    try:
        gauth = GoogleAuth()
        gauth.Auth(code)
        gauth.SaveCredentialsFile(f'{chat_id}.json')
        return '授權成功！'
    except Exception as e:
        return '授權失敗！可能是格式錯了之類的QQ，麻煩再試一次'

# def upload_drive(keyword, chat_id):

#     # check folder是否已存在
#     folder_name = '股票每日開資訊'
#     folder_id = None
#     folder_list = drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder' and trashed = false"}).GetList()
#     for folder in folder_list:
#         if folder['title'] == folder_name:
#             folder_id = folder['id']
#             break