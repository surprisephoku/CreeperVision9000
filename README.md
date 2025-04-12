# CreeperVision 👁️

> "See what they see. Because privacy is just a setting."

CreeperVision is a lightweight Python-based remote viewing system. It streams real-time camera and screen feeds from your laptop (server) to any device (client) over a local network. Ideal for creepy monitoring, curious hacking, or just flexing your Python skills.

## Features
- 📷 Live webcam feed
- 🖥️ Live screen capture
- 🛠️ Easy setup with Flask + SocketIO
- 🔐 Configurable secret key for basic security

## Requirements
- Python 3.8+
- Works on Linux, Windows (tested)
- Mobile browser-friendly (ish)

## Install & Run

```bash
git clone https://github.com/your-username/creepervision.git
cd creepervision
pip install -r requirements.txt
python server.py
