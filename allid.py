from pyrogram import Client

api_id = "2737066"
api_hash = "ce707dbe61808bfb66078e06d8019d7c"
group_username = "-1001464555457"  # 这里可以是群组的用户名或者ID

app = Client("my_account", api_id=api_id, api_hash=api_hash)

with app:
    members = []
    # 使用 iter_chat_members 来分页获取群组成员
    for member in app.iter_chat_members(group_username):
        members.append(member.user.id)
    
    print(f"Total members: {len(members)}")
    print(members)