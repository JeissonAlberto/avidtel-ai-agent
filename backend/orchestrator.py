"""
AI Agent - Orchestrator
Desarrollado por: Jeisson Alberto
"""
import logging
from typing import Dict, Any

class SalesSupportOrchestrator:
    """
    Orquestador de Clase Mundial que decide el flujo entre Soporte y Ventas.
    """
    def __init__(self, smartolt, ai, db):
        self.smartolt = smartolt
        self.ai = ai
        self.db = db
        self.name = "AI Agent"

    def process_incoming_event(self, phone: str, message: str) -> str:
        # 1. Identificar cliente
        client = self.db.get_client_by_phone(phone)
        if not client:
            return "Hola, soy el asistente de Avidtel. No encontré tu número en el sistema, ¿podrías darme tu número de contrato?"

        # 2. Clasificar intención con IA
        intent_data = self.ai.classify_intent(message)
        intent = intent_data.get("intent")

        # 3. Ejecutar Lógica de Negocio
        if intent == "WIFI_CHANGE":
            return f"Claro {client['name']}, puedo ayudarte a cambiar tu clave de WiFi. ¿Qué nombre nuevo quieres ponerle?"
        
        elif intent == "SUPPORT":
            return self._handle_support(client, message)
        
        elif intent == "SALES":
            return self._handle_sales(client, message)
        
        else:
            return f"Hola {client['name']}, soy tu asistente técnico. ¿En qué puedo ayudarte hoy?"

    def _handle_support(self, client: Dict, message: str) -> str:
        onu_id = client.get("onu_external_id")
        if not onu_id:
            return "No tengo vinculada tu ONT. Por favor, contacta a un humano."

        # Consulta real a SmartOLT
        status = self.smartolt.get_onu_status(onu_id)
        if not status:
            return "No pude conectar con tu equipo en este momento. Intenta de nuevo en unos minutos."

        # Lógica técnica de Avidtel
        rx_power = status.get("rx_power", 0)
        if rx_power and float(rx_power) < -27:
            return f"Veo que tu señal está un poco baja ({rx_power} dBm). He reiniciado tu equipo remotamente para estabilizarlo. ¿Me confirmas si mejora?"
        
        if status.get("phase_state") != "Working":
            return "Tu equipo aparece desconectado. Por favor, verifica que el cable de fibra (amarillo) esté bien conectado."

        return "Tu equipo aparece con parámetros normales. ¿Hay algún problema con la navegación?"

    def _handle_sales(self, client: Dict, message: str) -> str:
        current_plan = client.get("plan_name", "Básico")
        return f"Veo que tienes el plan '{current_plan}'. Por ser cliente preferencial de Avidtel, puedo ofrecerte subir a 300 Megas por solo $10.000 COP adicionales. ¿Te interesa?"
