import asyncio
from datetime import datetime
import os

from pyrogram.enums import parse_mode
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
session = os.getenv('session')

# 检查环境变量
if api_id is None or api_hash is None or session is None:
    print('API 参数或 session 参数错误，请修改 .env 文件中的参数')
    exit()

# 读取用户 ID 列表
data = []
with open('id', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        tg_id = line.strip()  # 去除换行符
        if tg_id:
            data.append(tg_id)

app = Client(session, api_id=api_id, api_hash=api_hash)
count_unbanned = 0
count_running = 1

groups = {-1001464555457}  # 替换为实际的群组 ID

async def unban_all(group_id):
    global count_unbanned
    for user_id in data:
        try:
            # 解除封禁操作
            await app.unban_chat_member(chat_id=group_id, user_id=user_id)
            count_unbanned += 1
            await asyncio.sleep(0.1)  # 防止触发限速，短暂等待
        except Exception as e:
            await app.send_message(chat_id=group_id, text=f"Error unbanning user {user_id}: {str(e)}")
            continue

    # 发送操作结果消息
    await app.send_message(chat_id=group_id,
                           text=f'已解除封禁 <code>{count_unbanned}</code> 用户',
                           parse_mode=parse_mode.ParseMode.HTML)

    count_unbanned = 0

# 处理 /run 命令
@app.on_message(filters.command('run'))
async def clean(client: Client, message: Message):
    global count_running
    for group in groups:
        print(f'正在检查第 {count_running} 个群')
        await app.send_message(chat_id=group,
                               text=f'正在检查第 {count_running} 个群',
                               parse_mode=parse_mode.ParseMode.HTML)
        count_running += 1
        await unban_all(group)

# 运行客户端
if __name__ == "__main__":
    app.run()
