#!/bin/bash
cd core-engine && go build -o ../ai-agent-bridge main.go && cd ..
./ai-agent-bridge &
python3 backend/orchestrator.py
