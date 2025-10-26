#!/bin/bash

# move to the directory where this script is located
cd /home/student

# british english comments no full stops

# start ollama if not already running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama"
    ollama serve > /dev/null 2>&1 &
    sleep 2
else
    echo "Ollama already running"
fi

# activate venv
source .venv/bin/activate

# open flask backend in new terminal
if command -v gnome-terminal >/dev/null 2>&1; then
    gnome-terminal -- bash -c "source .venv/bin/activate; python ollama_chat.py; exec bash"
elif command -v lxterminal >/dev/null 2>&1; then
    lxterminal -e "bash -c 'source .venv/bin/activate; python ollama_chat.py; exec bash'"
else
    xterm -hold -e "bash -c 'source .venv/bin/activate; python ollama_chat.py'" &
fi

sleep 1

# open streamlit frontend in another terminal
if command -v gnome-terminal >/dev/null 2>&1; then
    gnome-terminal -- bash -c "source .venv/bin/activate; python -m streamlit run webapp.py; exec bash"
elif command -v lxterminal >/dev/null 2>&1; then
    lxterminal -e "bash -c 'source .venv/bin/activate; python -m streamlit run webapp.py; exec bash'"
else
    xterm -hold -e "bash -c 'source .venv/bin/activate; python -m streamlit run webapp.py'" &
fi
