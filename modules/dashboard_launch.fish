#!/usr/bin/env fish
#Start venv and launch dashboard

set -x DISPLAY :O

source /home/mousey/fabricwidgets/venv/bin/activate.fish #Change the path to your own
nohup /home/mousey/fabricwidgets/venv/bin/python ~/omskiwi/file.py &> /dev/null & #Change the path to your own
