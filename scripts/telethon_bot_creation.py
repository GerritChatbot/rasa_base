# https://stackoverflow.com/questions/61432970/how-can-i-send-a-message-to-botfather-programmatically
from telethon import TelegramClient, events
from telethon_secrets import generate_bot_name, temporary_file
from getpass import getpass


api_id = getpass("API id:")
api_hash = getpass("API hash:")

bot_name = generate_bot_name()
bot_user_name = bot_name + "_bot"

client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def message_handler(event):
    if 'Please choose a name for your bot' in event.raw_text:
        await event.reply(bot_name)
    elif 'choose a username for your bot' in event.raw_text:
        await event.reply(bot_user_name)
    elif 'Done! Congratulations on your new bot' in event.raw_text:
        print("Bot created!")
        print(f"You can access it at {'https://t.me/'+bot_user_name}")
        temporary_file(bot_name)
        await client.disconnect()


async def main():
    await client.send_message('botfather', '/newbot')


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
