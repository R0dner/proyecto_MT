from smartcard.Card import Card
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
import time
import requests
import threading
from PySide2.QtWidgets import QTableWidgetItem, QStyledItemDelegate
from PySide2.QtGui import QPainter, QColor
from PySide2.QtCore import Qt

getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def definir_estado(estado):
    if estado.lower() == 'a':
        return "ACTIVA"
    elif estado.lower() == 'l':
        return "BLOQUEADO"
    elif estado.lower() == 'b':
        return "INACTIVA"
    else:
        return "Estado desconocido"

from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import Qt, QSize

class ColorCircleDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, radius=30, border_width=1, border_color=QColor("#000000")):

        super(ColorCircleDelegate, self).__init__(parent)
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self.default_color = QColor("#FFFFFF")
        self.border_style = Qt.SolidLine

    def paint(self, painter, option, index):

        color_hex = index.data(Qt.DisplayRole)
        
        if not color_hex or color_hex == "#FFFFFF":
            return

        try:
            fill_color = QColor(color_hex)
        except:
            fill_color = self.default_color

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)  

        pen = QPen()
        pen.setWidth(self.border_width)
        pen.setColor(self.border_color)
        pen.setStyle(self.border_style)
        painter.setPen(pen)

        painter.setBrush(fill_color)

        adjusted_radius = self.radius - self.border_width
        x = option.rect.x() + (option.rect.width() - adjusted_radius) / 2
        y = option.rect.y() + (option.rect.height() - adjusted_radius) / 2

        painter.drawEllipse(x, y, adjusted_radius, adjusted_radius)
        painter.restore()

    def sizeHint(self, option, index):

        size = self.radius + self.border_width * 2
        return QSize(size, size)

    def set_border_properties(self, width=None, color=None, style=None):

        if width is not None:
            self.border_width = max(0, width)  
        if color is not None:
            self.border_color = color
        if style is not None:
            self.border_style = style

    def set_circle_properties(self, radius=None, default_color=None):

        if radius is not None:
            self.radius = max(1, radius)  
        if default_color is not None:
            self.default_color = default_color

    def get_current_properties(self):

        return {
            'radius': self.radius,
            'border_width': self.border_width,
            'border_color': self.border_color.name(),
            'border_style': self.border_style,
            'default_color': self.default_color.name()
        }

class Lectura(CardObserver):
    def __init__(self, tabla_movimientos=None):
        super().__init__()
        self.cards = []
        self.card_read = False
        self.uid = None
        self.last_read_time = None
        self.card_data = None
        self.movements_data = None
        self.data_ready = threading.Event()
        self.lock = threading.Lock()
        self.tabla_movimientos = tabla_movimientos

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards.append(card)
                if not self.card_read:
                    self.card_read = True
                    self.last_read_time = time.time()
                    self.read_card()

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)
                self.card_read = False
                with self.lock:
                    self.card_data = None
                    self.movements_data = None
                self.data_ready.clear()

    def reset_data_ready(self):
        self._data_ready = False
        self._card_data = None

    def read_card(self):
        if self.cards:
            card = self.cards[0]
            try:
                connection = card.createConnection()
                connection.connect()
                time.sleep(0.5)
                response, sw1, sw2 = connection.transmit(getuid)
                self.uid = toHexString(response).replace(" ", "").upper()
                new_data = self.get_data_from_api(self.uid)
                movements = self.get_movements_from_api(self.uid)
                with self.lock:
                    self.card_data = new_data
                    self.movements_data = movements
                    if self.tabla_movimientos and movements:
                        self.update_movements_table(movements)
                self.data_ready.set()
            except CardConnectionException:
                with self.lock:
                    self.card_data = None
                    self.movements_data = None
                self.data_ready.clear()

    def get_data_from_api(self, uid):
        url = "https://cmisocket.miteleferico.bo/api/v1/billetaje/info-card"
        try:
            print("\n=== DEBUG: Solicitud a API de info-card ===")
            print(f"UID enviado: {uid}")
            
            response = requests.post(url, json={"card_uid": uid})
            print(f"Código de respuesta HTTP: {response.status_code}")
            
            data = response.json()
            print("\nRespuesta completa de la API:")
            print("================================")
            print(f"Success: {data.get('success')}")
            
            if data.get("success"):
                card = data.get("card", {})
                card_state = data.get("cardState", {})
                profile = data.get("profile", {})
                person = data.get("person", {})
                
                print("\nDatos extraídos:")
                print("================")
                print(f"Información de tarjeta: {card}")
                print(f"Estado de tarjeta: {card_state}")
                print(f"Información de perfil: {profile}")
                print(f"Información de persona: {person}")
                
                processed_data = {
                    "uid": uid,
                    "name": person.get("name", "No disponible"),
                    "last_name": person.get("last_name", "No disponible"),
                    "document": person.get("document", "No disponible"),
                    "profile_name": profile.get("name", "No disponible"),
                    "balance": card_state.get("balance", "No disponible"),
                    "card_status": definir_estado(card.get("status", "No disponible")),
                    "social_reason": person.get("social_reason", "No disponible"),
                    "nit": person.get("nit", "No disponible"),
                }
                
                print("\nDatos procesados para la interfaz:")
                print("================================")
                for key, value in processed_data.items():
                    print(f"{key}: {value}")
                
                print("\n=== Fin del debug ===\n")
                return processed_data
            else:
                print("\nError: La API no reportó éxito")
                print(f"Mensaje de error: {data.get('message', 'No hay mensaje de error disponible')}")
                print("\n=== Fin del debug ===\n")
                return None
                
        except requests.exceptions.RequestException as e:
            print("\n=== ERROR EN LA SOLICITUD ===")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Descripción del error: {str(e)}")
            print("\n=== Fin del debug ===\n")
            return None
        except Exception as e:
            print("\n=== ERROR INESPERADO ===")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Descripción del error: {str(e)}")
            print("\n=== Fin del debug ===\n")
            return None

    def update_movements_table(self, movements):
        if not self.tabla_movimientos or not movements:
            return

        try:
            self.tabla_movimientos.setSortingEnabled(False)

            self.tabla_movimientos.clearContents()

            for row, movement in enumerate(movements[:20]):
                if row >= self.tabla_movimientos.rowCount():
                    break

                items = [
                    (movement.get("fecha", ""), 0),
                    (movement.get("hora", ""), 1),
                    (movement.get("color", "#FFFFFF"), 2),
                    (movement.get("line_name", ""), 3),
                    (movement.get("station_name", ""), 4),
                    (str(movement.get("amount", "0.00")), 5),
                    (str(movement.get("balance", "0.00")), 6),  
                    (movement.get("event_name", ""), 7)
                ]

                for text, col in items:
                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tabla_movimientos.setItem(row, col, item)

            color_delegate = ColorCircleDelegate(self.tabla_movimientos)
            self.tabla_movimientos.setItemDelegateForColumn(2, color_delegate)
            self.tabla_movimientos.setSortingEnabled(True)
            self.tabla_movimientos.viewport().update()

        except Exception as e:
            print(f"Error actualizando la tabla: {e}")

    def get_card_data(self, timeout=None):
        if self.data_ready.wait(timeout):
            with self.lock:
                return self.card_data
        return None

    def is_data_ready(self):
        return self.data_ready.is_set()

    def get_movements_from_api(self, uid):
        url = "https://serviciosvirtual.miteleferico.bo/api/v1/billetaje/card-event-list"
        try:
            print(f"Solicitando movimientos para UID: {uid}")
            response = requests.post(url, json={"uid": uid})
            print(f"Respuesta de API: {response.status_code}")
            data = response.json()
            print(f"Datos recibidos: {data}")
            
            if data.get("success"):
                movements = data.get("data", [])
                print(f"Número de movimientos: {len(movements)}")
                return movements
            print("La API no reportó éxito")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener movimientos: {e}")
            return None

if __name__ == '__main__':
    nfc_reader = Lectura()
    cardmonitor = CardMonitor()
    cardmonitor.addObserver(nfc_reader)

    try:
        while True:
            if nfc_reader.is_data_ready():
                card_data = nfc_reader.get_card_data()
                print("Datos de la tarjeta:", card_data)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo el lector NFC...")
    finally:
        cardmonitor.deleteObserver(nfc_reader)
