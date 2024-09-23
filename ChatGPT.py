import asyncio
from datetime import datetime, timedelta
import os
import logging

from pyrogram import Client, filters
from pyrogram.enums import parse_mode
from pyrogram.types import Message
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)

# 加载 .env 文件中的环境变量
load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
session = os.getenv('session')

# 检查环境变量
if not all([api_id, api_hash, session]):
    logging.error('API 参数或 session 参数错误，请修改 .env 文件中的参数')
    exit()

# 读取用户 ID 列表
def load_user_ids(file_path='id'):
    user_ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            user_ids = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"用户 ID 文件 {file_path} 未找到")
    return user_ids

# 初始化用户 ID 列表
user_ids = load_user_ids()

# 初始化 Pyrogram 客户端
app = Client(session, api_id=api_id, api_hash=api_hash)

# 定义要操作的群组 ID
groups = {-1001462465413}  # 替换为实际的群组 ID

async def ban_user(group_id, user_id):
    """
    踢出单个用户，失败时尝试发指令让机器人踢出用户。
    """
    try:
        await app.ban_chat_member(chat_id=group_id, user_id=user_id, until_date=datetime.now() + timedelta(seconds=35))
        return True
    except Exception as e:
        logging.warning(f"踢出用户 {user_id} 失败: {e}. 尝试让机器人踢出...")
        try:
            await app.send_message(chat_id=group_id, text=f"/kick@ghStaffBot {user_id}")
        except Exception as kick_error:
            logging.error(f"踢出用户 {user_id} 失败: {kick_error}")
        return False

async def process_group(group_id):
    """
    处理单个群组中的所有用户。
    """
    successful_count = 0
    for user_id in user_ids:
        if await ban_user(group_id, user_id):
            successful_count += 1
        await asyncio.sleep(0.1)  # 防止触发速率限制
    await app.send_message(chat_id=group_id, text=f'已处理 <code>{successful_count}</code> 用户', parse_mode=parse_mode.HTML)
    return successful_count

@app.on_message(filters.command('run'))
async def run_command(client: Client, message: Message):
    """
    响应 /run 命令，对所有指定的群组进行处理。
    """
    tasks = []
    for idx, group_id in enumerate(groups, start=1):
        logging.info(f'正在检查第 {idx} 个群 (ID: {group_id})')
        await app.send_message(chat_id=group_id, text=f'正在检查第 {idx} 个群', parse_mode=parse_mode.HTML)
        tasks.append(process_group(group_id))
    
    results = await asyncio.gather(*tasks)
    total_successful = sum(results)
    logging.info(f'所有群组处理完成，共踢出 {total_successful} 个用户。')

if __name__ == "__main__":
    app.run()