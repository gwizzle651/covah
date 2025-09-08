#!/usr/bin/env/ bash
clear
screen -S covahConsole -dm python3 /home/discordadmin/covah/covahMain.py
clear
sleep 1
screen -r covahConsole
