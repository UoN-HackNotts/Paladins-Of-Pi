# Paladins of Pi

**Local-first full-stack hackathon prototype** — a medieval text-adventure generator running entirely on a Raspberry Pi (Pi 5, 8 GB).  
This project was built for HackNotts by the UoN-HackNotts team.

## 🚀 Project summary
Paladins of Pi is a lightweight full-stack app that uses a local Ollama LLM to generate short medieval scenes (<50 words). The Streamlit frontend sends prompts to a Flask backend which formats the prompt, queries Ollama and returns the generated scene. Conversation history is persisted to `data.json`.

## Key features
- Local-only stack — no external APIs required (assuming Ollama is installed locally)
- Medieval prompt engineering via `SYSTEM_PROMPT` and `TEMPLATE`
- Simple conversation persistence to `data.json`
- Dev-friendly startup script to launch Ollama, backend and frontend on one command
- Designed for Raspberry Pi 5 (8 GB) desktop usage

## Repo layout (important files)
- `backend.py` — Flask backend exposing `/generate`
- `frontend.py` (Streamlit frontend) — main UI, conversation history and controls
- `Story.py` — local story-processing helpers called by the backend
- `data.json` — persisted conversation history (flat [{user:..},{ai:..}] format)
- `run_paladins.sh` (or `run_paladins` script) — startup helper for Ollama, backend and frontend

---

## Prerequisites
- Raspberry Pi 5 with at least 8 GB RAM (recommended)
- Raspberry Pi OS with desktop (for the included terminal/GUI startup script)
- Python 3.11+ (virtualenv recommended)
- Ollama installed and accessible on the Pi (expected to serve at `localhost:11434`)
- Terminal emulator (gnome-terminal, lxterminal or xterm) for `run_paladins.sh`

---

## Quickstart (recommended)
1. Clone the repo:
   ```bash
   git clone https://github.com/UoN-HackNotts/Paladins-Of-Pi
   cd Paladins-Of-Pi
