from pyrogram import Client, errors
import time

# 在此处替换为你的 api_id 和 api_hash
api_id = "2737066"
api_hash = "ce707dbe61808bfb66078e06d8019d7c"
group_username = "-1001464555457"  # 这里可以是群组的用户名或者 ID

app = Client("my_account", api_id=api_id, api_hash=api_hash)

def get_all_chat_ids(client, group_username):
    chat_ids = []
    try:
        # 使用 iter_chat_members 分页获取群组成员
        for member in client.iter_chat_members(group_username):
            chat_ids.append(member.user.id)
            if len(chat_ids) % 1000 == 0:
                print(f"{len(chat_ids)} members fetched...")
                
    except errors.FloodWait as e:
        # 如果遇到 Telegram 的速率限制错误，暂停请求
        print(f"FloodWait: Sleeping for {e.value} seconds...")
        time.sleep(e.value)
        return get_all_chat_ids(client, group_username)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return chat_ids

with app:
    members_chat_ids = get_all_chat_ids(app, group_username)
    print(f"Total members fetched: {len(members_chat_ids)}")
    # 你可以将 chat_ids 保存到文件中或其他操作
    with open("chat_ids.txt", "w") as f:
        for chat_id in members_chat_ids:
            f.write(f"{chat_id}\n")

    print("Chat IDs have been saved to chat_ids.txt")
