#!/bin/bash
echo "--- INICIANDO AI AGENT INFRASTRUCTURE BY JEISSON ALBERTO ---"
echo "1. Limpiando procesos en puerto 80..."
fuser -k 80/tcp 2>/dev/null
echo "2. Instalando dependencias necesarias..."
pip install requests 2>/dev/null
echo "3. Lanzando Unified Server (Dashboard + Webhook)..."
nohup python3 server.py > server.log 2>&1 &
echo "4. Verificando estado..."
sleep 2
if curl -s -I http://localhost:80 | grep "200 OK" > /dev/null; then
    echo "EXITO: Dashboard activo en puerto 80"
else
    echo "ALERTA: El servidor no respondió en puerto 80. Revisa server.log"
fi
echo "Sistemas sincronizados. IP sugerida para acceso: 172.19.153.93"
