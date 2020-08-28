# ---------------------------------------------------
#                   I M P O R T S
# ---------------------------------------------------

import os
import re
import json
import psycopg2
import socket
import random

from sys                        import getdefaultencoding
from datetime                   import datetime, date, time
from tinkoff_voicekit_client    import ClientSTT


# ---------------------------------------------------
#                   C O N F I G S
# ---------------------------------------------------


API_KEY = open('DataAuth/API_KEY.txt', 'r').readline()
SECRET_KEY = open('DataAuth/SECRET_KEY.txt', 'r').readline()


audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

cli_config = {
    "path_to_wav_file": None,
    "phone_number": None,
    "need_record_in_db": None
}

ready_answers = {
    "yes": ["да ", "говорите", "слушаю"],
    "no": ["нет ", "не могу", "занят"],
    "answerphone": ["автоответчик"]
}

stamps = {
    "id": 1
}

content = []


# ---------------------------------------------------
#                  F U N C T I O N S 
# ---------------------------------------------------


def GetInfoFromCLI():
    try:
        while not cli_config["path_to_wav_file"]:
            cli_config["path_to_wav_file"] = str(input("Укажите путь к wav файлу ->")) 
            if os.path.exists(cli_config["path_to_wav_file"]) != False and  os.path.isfile(cli_config["path_to_wav_file"]) != False and os.path.splitext(cli_config["path_to_wav_file"]) != '.wav':
                print('kk')
            else:
                cli_config["path_to_wav_file"] = None
        while not cli_config["phone_number"]:
            cli_config["phone_number"] = str(input("Номер телефона ->"))
            if not len(cli_config["phone_number"]) != 11:
                print('kk')
            else:
                cli_config["phone_number"] = None
        cli_config["need_record_in_db"] = str(input("Нужна ли запись в базу (yes|no) ? ->"))
    except  KeyboardInterrupt:
        raise("\nДо свидания!")


def DetermineWhatWasSaid(res, answers):
    for key in answers:
        for i in answers[key]:
            if re.search(i, res):
                match = re.search(i, res)
                print(match[0])
                if key == "yes":
                    return({"is_human": 1, "can_talk": 1})
                elif key == "no":
                    return({"is_human": 1, "can_talk": 0})
                elif key == "answerphone":
                    return({"is_human": 0, "can_talk": 0})
                else:
                    print("\nЛабуда.")


def DictForJSON(is_human,can_talk,phone_number,audio_duration,msg):
    stamps["date"] = datetime.now().strftime("%d-%m-%Y")
    stamps["time"] = datetime.now().strftime("%H:%M:%S")
    stamps["is_human"] = is_human
    stamps["can_talk"] = can_talk
    stamps["phone_number"] = phone_number
    stamps["audio_duration"] = audio_duration
    stamps["message"] = msg
    return stamps


def OpenFile():
    file = open('stamps.json', 'r+', encoding='UTF-8')
    if (os.stat("stamps.json").st_size == 0):
        file.close()
        content = []
        return content
    else:
        content = json.loads(file.read())
        stamps["id"] = content[-1]["id"] + 1
        return content


def DumpInFile(cnt, duration):
    file = open('stamps.json', 'r+', encoding='UTF-8')
    try:
        DictForJSON(result["is_human"],result["can_talk"],cli_config["phone_number"], duration, response)
        cnt.append(stamps)
        string = json.dumps(cnt, indent=4, ensure_ascii=False)
        file.write(string)
        file.close()
    except Exception as e:
        print(e)  


def MustRecordInDB(flag):
    if flag == "yes":
        conn = psycopg2.connect(
            dbname='logs', 
            user='postgres', 
            password='3993', 
            host='localhost'
        )
        address = socket.gethostbyname(socket.gethostname())
        sid = random.randint(10, 10000)
        pid = random.randint(10, 10000)
        cursor = conn.cursor()
        str_for_db = json.dumps(stamps, ensure_ascii=False)
        try:
            cursor.execute(
                "CALL transaction_create_dump("+str(pid)+","+str(sid)+",'incomming','"+address+"','"+str_for_db+"');"
            )
            print("Query for project is succesfull.")
            conn.commit()
        except Exception as e:
            print(e)
        
        conn.close()


# ---------------------------------------------------
#                  M A I N   C O D E 
# ---------------------------------------------------


client = ClientSTT(API_KEY, SECRET_KEY)

GetInfoFromCLI()

response = client.recognize(cli_config["path_to_wav_file"], audio_config)

audio_duration = response[0]["end_time"]
response = response[0]["alternatives"][0]["transcript"]
result = DetermineWhatWasSaid(response, ready_answers)

DumpInFile(OpenFile(), audio_duration)

MustRecordInDB(cli_config["need_record_in_db"])

os.remove(cli_config["path_to_wav_file"])

