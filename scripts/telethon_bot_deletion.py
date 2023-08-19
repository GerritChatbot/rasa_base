# https://stackoverflow.com/questions/61432970/how-can-i-send-a-message-to-botfather-programmatically
# https://arabic-telethon.readthedocs.io/en/stable/extra/basic/working-with-updates.html#working-with-updates
import os.path
from telethon import TelegramClient, events
from getpass import getpass
from telethon_secrets import read_bot_name, remove_temp_dir

api_id = getpass("API id:")
api_hash = getpass("API hash:")
client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def message_handler(event):
    print(event.raw_text)
    bot_name = read_bot_name()
    print(bot_name)
    if 'Choose a bot from the list below:' in event.raw_text:
        await event.message.click(text=bot_name)
        print(event.raw_text)


# some of the events are not new messages, but just the same message edited
@client.on(events.MessageEdited)
async def message_handler(event):
    print(event.raw_text)
    if 'What do you want to do with the bot?' in event.raw_text:
        await event.message.click(text='Delete Bot')
    elif 'You are about to delete your bot' in event.raw_text:
        await event.message.click(text='Yes, delete the bot')
    elif 'Are you TOTALLY sure you want to delete' in event.raw_text:
        await event.message.click(text="Yes, I'm 100% sure!")
        print("bot was deleted")
        # remove the name of the bot
        remove_temp_dir()
        await client.disconnect()


async def main():
    await client.send_message('botfather', '/mybots')


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
