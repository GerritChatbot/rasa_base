import names
from datetime import datetime
import os


def generate_bot_name() -> str:
    now = datetime.now()
    bot_name = str(names.get_first_name())+"_"+str(hash(now))
    return bot_name


def temporary_file(bot_name):
    os.mkdir(os.path.join(os.getcwd(), "temp"))
    with open('temp/botname.txt', 'w') as file:
        file.write("@"+bot_name+"_bot")


def read_bot_name():
    with open("temp/botname.txt", "r") as f:
        bot_name = f.readline()
    return bot_name


def remove_temp_dir():
    os.remove(os.path.join(os.getcwd(), "temp", "botname.txt"))
    os.rmdir(os.path.join(os.getcwd(), "temp"))
