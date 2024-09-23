import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 读取指定文件中的ID
def read_ids_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip().isdigit()]

# 批量踢人
def kick_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_ids = read_ids_from_file('ID.txt')
    
    for user_id in user_ids:
        try:
            context.bot.kick_chat_member(chat_id, user_id)
            logging.info(f"Kicked user {user_id}")
        except Exception as e:
            logging.error(f"Failed to kick user {user_id}: {e}")

    update.message.reply_text("已踢出指定用户。")

def main():
    # 在这里填入你的 Token
    TOKEN = '7297985723:AAG_9MG94-dXrC_ccGzKS4pRLIbJw2X6UL8'
    updater = Updater(TOKEN)

    # 添加命令处理器
    updater.dispatcher.add_handler(CommandHandler('kick', kick_users))

    # 开始轮询
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()