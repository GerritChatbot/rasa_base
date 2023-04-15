#!/bin/bash -x
# Documented steps needed to deploy rasa manually
# Source of information for ansible playbook

# ---HOST SETUP---
apt update -y

sudo apt install -y pip

# Use --no-cache-dir to avoid running out of RAM
python3 -m pip install rasa rasa-sdk openpyxl pandas --no-cache-dir

# ---APP DEPLOY---
if [[ -d rasa_base ]]; then
        cd rasa_base
else
        git clone https://github.com/GerritChatbot/rasa_base.git && cd rasa_base
fi

rasa train --domain domain &

# TODO: pass credentials

nohup rasa run actions &

# start rasa API server
nohup rasa run --enable-api &

# Open port 5005 if needed. May not be required if firewall is not running.
