#!/bin/bash

# Installer Chromium
apt-get update
apt-get install -y chromium-browser

# Exporter le chemin de Chromium
export CHROME_BIN=/usr/bin/chromium-browser

# Lancer ton bot
python3 main.py

