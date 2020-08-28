import json
from sys import getdefaultencoding
from datetime import datetime, date, time

print(getdefaultencoding())

stamps = {}
file_content = []

#

def determine(id,is_human,can_talk,phone_number,audio_duration,msg):
    stamps["id"] = id
    stamps["date"] = datetime.now().strftime("%d-%m-%Y")
    stamps["time"] = datetime.now().strftime("%H:%M:%S")
    stamps["is_human"] = is_human
    stamps["can_talk"] = can_talk
    stamps["phone_number"] = phone_number
    stamps["audio_duration"] = audio_duration
    stamps["message"] = msg

#

file = open('stamps.json', 'r+', encoding='UTF-8')

try:
    file_content = json.loads(file.read())
    print(type(file_content))
    file.close()
except Exception as e:
    print(e)

determine(1, 1, 1, 89289296215, 5, 'Прифки')

file = open('stamps.json', 'r+', encoding='UTF-8')

try:
    file_content.append(stamps)
    string = json.dumps(file_content, indent=4, ensure_ascii=False)
    file.write(string)
    file.close()
except Exception as e:
    print(e)
