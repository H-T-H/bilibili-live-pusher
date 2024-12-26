import requests
import json
import time
from telebot import TeleBot
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# 配置用户代理旋转
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

user_agent = user_agent_rotator.get_random_user_agent()

headers = {
    'User-Agent': user_agent
}

# 填写 Telegram bot 密钥和聊天室 ID
bot_key = ''  # 请替换为实际的 bot key
chat_id = ''  # 请替换为实际的 chat id

# 初始化 Telegram bot
bot = TeleBot(bot_key)
print("Bot init done.")

# Bilibili 房间号
room_id = ''  # 请替换为实际的房间号
base_url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id="

def get_live_status(room_id):
    try:
        # 发起请求获取直播状态
        getrequest = requests.get(base_url + room_id, headers=headers)
        getrequest.raise_for_status()  # 确保请求没有失败

        # 尝试解析 JSON
        response_data = getrequest.json()

        # 检查是否包含预期的字段
        if 'data' in response_data and 'live_status' in response_data['data']:
            return response_data['data']['live_status']
        else:
            print("API 响应数据格式不正确或缺少必要字段")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except json.JSONDecodeError:
        print("解析 JSON 时发生错误")
        return None
    except KeyError as e:
        print(f"缺少预期字段: {e}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None

def send_live_start_notify():
    """通知直播开始"""
    text = f"开播了，速来！😋😋😋\nhttps://live.bilibili.com/{room_id}"
    bot.send_message(chat_id, text)

def send_live_end_notify():
    """通知直播结束"""
    text = "下播了！😭😭😭"
    bot.send_message(chat_id, text)

def main():
    last_status = 0  # 初始状态，0 表示未开播
    bot.send_message(chat_id, "机器人已启动")
    while True:
        try:
            # 获取当前直播状态
            current_status = get_live_status(room_id)

            if current_status is None:
                # 如果无法获取状态，跳过本次循环
                time.sleep(5)
                continue

            # 如果当前状态为 1 (直播中)，并且上次状态为 0 或 2，说明直播开始
            if current_status == 1:
                if last_status in [0, 2]:
                    send_live_start_notify()
                    last_status = current_status

            # 如果当前状态为 0 或 2 (未开播或其他)，并且上次状态为 1，说明直播结束
            elif current_status in [0, 2]:
                if last_status == 1:
                    send_live_end_notify()
                    last_status = current_status

            # 每隔 5 秒检查一次
            time.sleep(5)
        except Exception as e:
            print(f"主循环发生错误: {e}")
            time.sleep(5)

# 启动主程序
if __name__ == "__main__":
    main()