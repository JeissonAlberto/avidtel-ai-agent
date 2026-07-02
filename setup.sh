#!/bin/bash
echo "Iniciando AI Agent..."
fuser -k 18800/tcp 2>/dev/null
python3 server.py
