from pyrogram import Client, errors

api_id = "2737066"
api_hash = "ce707dbe61808bfb66078e06d8019d7c"
group_username = "-1001464555457"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

with app:
    try:
        chat = app.get_chat(group_username)
        print(f"Chat Title: {chat.title}")
        print(f"Chat ID: {chat.id}")
    except errors.FloodWait as e:
        print(f"FloodWait: Sleeping for {e.value} seconds...")
    except Exception as e:
        print(f"An error occurred: {e}")