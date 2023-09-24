# main commands
## how to test out your chatbot 101

Model training. The domain flag is there to make RASA know we have multiple files in domain folder (as opposed to having one domain file).
```
rasa train --domain domain
```

Some functionality is handled by action server - it usually runs custom python scripts. Usually you want to run this command in a second command line.
```
rasa run actions
```

Basic within-terminal testing can be then done via:
```
rasa shell
```
## how to do advanced (better) testing
It is much better to test it inside Telegram instead of command line.

In order to setup your own local version of Gerrit, just follow the [wiki manual](https://github.com/GerritChatbot/rasa_base/wiki/Creating-testing-chatbot).

# deployment
Pro spusteni deploymentu pouzij prikaz
```commandline
ansible-playbook -v -t deploy deploy/main.yml -i deploy/hosts.yml --extra-vars droplet_ip=$DROPLET_IP
```
