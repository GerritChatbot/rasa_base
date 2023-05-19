# main commands

Trénování modelu. Protože máme domain soubory ve složce domain, tak mu to musíme dát RASA vědět
```
rasa train --domain domain
```

Některé funkcionality vyžadují přístup k speciálním externím informacím - ty zpracovává action server. Pokud nejede, tak se dané odpovědi nemůžou spustit. (spouští se v druhé konzoli)
```
rasa run actions
```

Pro testování chatbota doporučuji přes tento příkaz
```
rasa shell
```

Pro spusteni deploymentu pouzij prikaz
```commandline
ansible-playbook -v -t deploy deploy/main.yml -i deploy/hosts.yml --extra-vars droplet_ip=$DROPLET_IP
```
