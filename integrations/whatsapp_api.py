"""
AI Agent - WhatsApp Integration (Cloud API)
Desarrollado por: Jeisson Alberto
"""
import requests
import logging

logger = logging.getLogger("WhatsApp")

class WhatsAppCloudAPI:
    """
    Integración con Meta WhatsApp Cloud API.
    """
    def __init__(self, token: str, phone_number_id: str):
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_text_message(self, to_phone: str, message: str):
        """Envía un mensaje de texto simple."""
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",
            "text": {"body": message}
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error enviando WhatsApp: {e}")
            return {"error": str(e)}

    def send_template(self, to_phone: str, template_name: str, language_code: str = "es"):
        """Envía una plantilla aprobada (útil para iniciar conversaciones)."""
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
