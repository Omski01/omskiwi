#!/usr/bin/env fish
#Start venv and launch dashboard

set -x DISPLAY :O

source /home/mousey/fabricwidgets/venv/bin/activate.fish
nohup /home/mousey/fabricwidgets/venv/bin/python ~/omskiwi/file.py &> /dev/null &
