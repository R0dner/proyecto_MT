import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_card_info(self, card_uid):
        url = f"{self.base_url}/api/v1/billetaje/info-card"
        try:
            response = requests.post(url, json={"card_uid": card_uid})
            data = response.json()
            if data.get("success"):
                person = data.get("person", {})
                profile = data.get("profile", {})
                card_state = data.get("cardState", {})
                card = data.get("card", {})
                return {
                    "name": person.get("name", "Nombre no disponible"),
                    "last_name": person.get("last_name", "Apellido no disponible"),
                    "document": person.get("document", "Documento no disponible"),
                    "profile_name": profile.get("name", "Perfil no disponible"),
                    "balance": card_state.get("balance", "Saldo no disponible"),
                    "card_status": self.traducir_estado(card.get("status", "Estado de tarjeta no disponible")),
                    "social_reason": person.get("social_reason", "Razón social no disponible"),
                    "nit": person.get("nit", "NIT no disponible"),
                }
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def traducir_estado(self, estado):
        if estado.lower() == 'a':
            return "ACTIVA"
        elif estado.lower() == 'l':
            return "BLOQUEADO"
        elif estado.lower() == 'b':
            return "INACTIVA"
        else:
            return "Estado desconocido"
        