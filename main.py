import requests
import json
import time
from telebot import TeleBot
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


user_agent = user_agent_rotator.get_random_user_agent()

headers = {
    'User-Agent': user_agent
}

bot_key = '填写Telegram bot key' #@BotFather
chat_id = '填写Telegram id' #@getmyid_bot
# Init bot
bot = TeleBot(bot_key)
print("Bot init done.")

room_id = '填写房间号'
base_url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id="

def get_live_status(room_id):
    getrequest = requests.get(base_url+room_id,headers = headers)
    status_num = json.loads(getrequest.text)['data']['live_status']
    return status_num

def send_live_start_notify():
    text = f"开播了，速来！😋😋😋\nhttps://live.bilibili.com/{room_id}"
    bot.send_message(chat_id,text)

def send_live_end_notify():
    text = "下播了！😭😭😭\n"
    bot.send_message(chat_id,text)

def main():
    last_status = 0
    while True:
        current_status = get_live_status(room_id)
        
        if current_status in [0, 2]:
            if last_status == 1:
                send_live_end_notify()
                last_status = current_status
        elif current_status == 1:
            if last_status in [0, 2]:
                send_live_start_notify()
                last_status = current_status
        time.sleep(5)

main()
