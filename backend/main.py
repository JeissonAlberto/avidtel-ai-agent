"""
Desarrollado por: Jeisson Alberto
Proyecto: AI Agent
"""
import os
import json

class HighLevelAI:
    """Motor de IA de Clase Mundial."""
    def classify_intent(self, text: str) -> dict:
        t = text.lower()
        if any(x in t for x in ["clave", "wifi"]): return {"intent": "WIFI_CHANGE"}
        if any(x in t for x in ["lento", "falla", "internet"]): return {"intent": "SUPPORT"}
        if any(x in t for x in ["plan", "precio", "mejorar"]): return {"intent": "SALES"}
        return {"intent": "GENERAL"}

class JsonDatabase:
    """Base de datos ligera para el AI Agent."""
    def __init__(self, path="data/clients.json"):
        self.path = path
        if not os.path.exists("data"): os.makedirs("data")
        if not os.path.exists(path):
            with open(path, "w") as f: json.dump({
                "573132497317": {
                    "name": "Jeisson Alberto",
                    "onu_external_id": "AVDTL001",
                    "plan_name": "100 Mega Hogar"
                }
            }, f)

    def get_client_by_phone(self, phone: str):
        with open(self.path, "r") as f:
            db = json.load(f)
        return db.get(phone)
