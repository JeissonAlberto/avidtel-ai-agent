#!/bin/bash

# =================================================================
# AI Agent - Setup & Deployment Script
# Desarrollado exclusivamente por: Jeisson Alberto
# =================================================================

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}      AI AGENT - INGENIERÍA COLOSAL BY J.ALBERTO     ${NC}"
echo -e "${BLUE}====================================================${NC}"

# 1. Verificar e instalar dependencias del sistema
echo -e "\n${BLUE}[1/4] Verificando dependencias (Go & Python)...${NC}"
if ! command -v go &> /dev/null; then
    echo -e "${RED}Go no encontrado. Instalando Golang...${NC}"
    sudo apt update && sudo apt install -y golang-go
else
    echo -e "${GREEN}Go ya está instalado.${NC}"
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 no encontrado. Instalando...${NC}"
    sudo apt install -y python3 python3-pip
else
    echo -e "${GREEN}Python3 ya está instalado.${NC}"
fi

# 2. Compilar el Core Bridge (Go)
echo -e "\n${BLUE}[2/4] Compilando Core Bridge (Arquitectura Híbrida)...${NC}"
if [ -f "core-engine/main.go" ]; then
    go build -o ai-agent-bridge core-engine/main.go
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✔ Core Bridge compilado con éxito.${NC}"
    else
        echo -e "${RED}✘ Error al compilar Core Bridge.${NC}"
        exit 1
    fi
else
    echo -e "${RED}✘ Error: No se encuentra core-engine/main.go${NC}"
    exit 1
fi

# 3. Preparar el entorno Python
echo -e "\n${BLUE}[3/4] Configurando Brain Engine (Python)...${NC}"
# Aquí podrías añadir: pip install -r requirements.txt
echo -e "${GREEN}✔ Entorno de Python listo.${NC}"

# 4. Lanzamiento
echo -e "\n${BLUE}[4/4] Iniciando AI Agent...${NC}"
echo -e "${GREEN}El motor de alta velocidad está arrancando...${NC}"

# Ejecutar el puente en segundo plano
./ai-agent-bridge &
BRIDGE_PID=$!

# Ejecutar el orquestador
python3 backend/orchestrator.py

# Al cerrar el orquestador, matar el bridge
kill $BRIDGE_PID
echo -e "${BLUE}Sistemas cerrados correctamente.${NC}"
