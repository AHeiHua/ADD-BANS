import json
import time
import datetime
import win32api
import win32file

with open("bans.ini") as f:
    data = f.read()

parser_data = json.loads(data)

def convert_filetime_to_datetime(filetime):
    dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=filetime / 10)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

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

        print(f"UID: {uid}, 设备码: {did}, IP: {ip}, 封禁原因: {reason}, 解封时间: {convert_filetime_to_datetime(unban_time)}")


def del_ban(uid):
    if type(uid) != int:
        raise ValueError("UID 必须为整数")
    for item in parser_data:
        if item["uid"] == uid:
            # 从文件中删去封禁
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

            print(
                f"UID: {uid}, 设备码: {did}, IP: {ip}, 封禁原因: {reason}, 解封时间: {unban_time}"
            )
    if scanf == 0:
        print("该成员未被封禁")


def edit_ban_time(uid):
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


def main():
    while True:
        print("1. 解封成员")
        print("2. 查看所有封禁")
        print("3. 查询成员封禁状态")
        print("4. 编辑封禁时间")
        choice = input("请输入选项: ")
        if choice == "1":
            uid = int(input("请输入要解封的成员的UID: "))
            del_ban(uid)
        elif choice == "2":
            get_bans()
        elif choice == "3":
            uid = int(input("请输入要查询的成员的UID: "))
            scanf_ban(uid)
        elif choice == "4":
            uid = int(input("请输入要编辑的成员的UID: "))
            edit_ban_time(uid)
        else:
            print("无效选项")

if __name__ == "__main__":
    main()