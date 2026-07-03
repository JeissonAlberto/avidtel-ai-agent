"""
AI Agent - Unified Server
Desarrollado por: Jeisson Alberto
"""
import http.server
import socketserver
import os
import json
import threading
import time
from backend.orchestrator import SalesSupportOrchestrator
from integrations.smartolt import SmartOLTIntegration
from integrations.whatsapp_api import WhatsAppCloudAPI

PORT = 80
DIRECTORY = "frontend"

# Configuración Real (Obtenida por Jeisson Alberto)
SMARTOLT_API_KEY = "d50fee17f74c41998cf53b01083797c7"
SMARTOLT_DOMAIN = "avidtel.smartolt.com"

# --- WHATSAPP CONFIG (Pendiente Token de Usuario) ---
WHATSAPP_TOKEN = "PENDIENTE_TOKEN_META"
WHATSAPP_PHONE_ID = "PENDIENTE_PHONE_ID"

class AIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Inicializar integraciones una sola vez
        self.smartolt = SmartOLTIntegration(api_key=SMARTOLT_API_KEY, domain=SMARTOLT_DOMAIN)
        self.wpp = WhatsAppCloudAPI(token=WHATSAPP_TOKEN, phone_number_id=WHATSAPP_PHONE_ID)
        # Mock de IA y DB para el orquestador
        from backend.main import HighLevelAI, JsonDatabase
        self.orchestrator = SalesSupportOrchestrator(self.smartolt, HighLevelAI(), JsonDatabase())
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # En producción esto consultaría a SmartOLT directamente
            # Aquí devolvemos un resumen de la red Avidtel
            stats = {
                "onts": 1245,
                "interacts": 892,
                "network": [
                    {"name": "OLT-Principal-Avidtel", "status": "UP"},
                    {"name": "Zona-Cali-Centro", "status": "UP"},
                    {"name": "Zona-Cali-Sur", "status": "UP"}
                ]
            }
            self.wfile.write(json.dumps(stats).encode())
        else:
            return super().do_GET()

    def do_POST(self):
        # Webhook para WhatsApp (Meta envía los mensajes aquí)
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                message = data['entry'][0]['changes'][0]['value']['messages'][0]
                sender = message['from']
                text = message['text']['body']
                
                # Procesar con el Cerebro de Jeisson
                reply = self.orchestrator.process_incoming_event(sender, text)
                
                # Responder por WhatsApp
                self.wpp.send_text_message(sender, reply)
            except: pass
            
            self.send_response(200)
            self.end_headers()
            return

        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            user_msg = data.get('message', '')
            
            # Procesar a través del Orquestador de Clase Mundial de Jeisson
            # Usamos un número de prueba para el Dashboard
            phone = "573132497317"
            response = self.orchestrator.process_incoming_event(phone, user_msg)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"response": response}).encode())

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AIHandler) as httpd:
        print(f"--- AI AGENT DASHBOARD ACTIVADO ---")
        print(f"URL: http://localhost (Puerto {PORT})")
        print(f"Autor: Jeisson Alberto")
        httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    
    # Iniciar infraestructura
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print("Brain Engine Ready. Sistemas Avidtel sincronizados.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSistemas cerrados correctamente.")
