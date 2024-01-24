import json
import time
import datetime
import win32api

with open("bans.ini") as f:
    data = f.read()

parser_data = json.loads(data)

"""转换FILETIME"""
def convert_to_filetime(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    micros = (dt - datetime.datetime(1970, 1, 1)).total_seconds() * 10**6
    filetime = int(micros) + 11644473600000000
    return filetime

def get_bans():
    print("以下是所有封禁成员")
    for item in parser_data:
        uid = item["uid"]
        did = item["did"]
        ip = item["ip"]
        reason = item["reason"]
        unban_time = item["unbanTime"]

        print(f"UID: {uid}, 设备码: {did}, IP: {ip}, 封禁原因: {reason}, 解封时间: {unban_time}")

def del_ban(uid):
    if type(uid) != int:
        raise ValueError("UID 必须为整数")
    for item in parser_data:
        if item["uid"] == uid:
            #从文件中删去封禁
            with open("bans.ini", "w") as f:
                parser_data.remove(item)
                print("已解封该成员")
                print(parser_data)
                f.write(json.dumps(parser_data))

def scanf_ban(uid):
    scanf = 0
    if type(uid) != int:
        raise ValueError("UID 必须为整数")
    for item in parser_data:
        if item["uid"] == uid:
            scanf = 1
            print("该成员已被封禁")
            uid = item["uid"]
            did = item["did"]
            ip = item["ip"]
            reason = item["reason"]
            unban_time = item["unbanTime"]

            print(f"UID: {uid}, 设备码: {did}, IP: {ip}, 封禁原因: {reason}, 解封时间: {unban_time}")
    if scanf == 0:
        print("该成员未被封禁")

def edit_ban(uid):
    if type(uid) != int:
        raise ValueError("UID 必须为整数")
    for item in parser_data:
        if item["uid"] == uid:
            print("请输入新的解封时间(格式 年:日:月):")
            unban_time = input()
            unban_time = datetime.datetime.strptime(unban_time, "%Y:%m:%d")
            unban_time = convert_to_filetime(str(unban_time))
            item["unbanTime"] = unban_time
            with open("bans.ini", "w") as f:
                f.write(json.dumps(parser_data))
            print("已将解封时间修改为: " + str(unban_time))

edit_ban(100)