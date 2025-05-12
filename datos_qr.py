import json
import requests
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import QSvgRenderer
import qrcode
from PIL import Image
import io
import time
import os

# Importamos las clases necesarias del archivo NFCHandler.py
from smartcard.Card import Card
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
import threading

# Función para convertir imagen PIL a QImage para PySide2
def pil_to_qimage(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_data = buffer.getvalue()
    qimage = QImage.fromData(img_data)
    return qimage

# Función para descargar una imagen desde una URL
def download_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            return pil_to_qimage(img)
        else:
            print(f"Error al descargar imagen: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al descargar imagen: {e}")
        return None

# Importamos la clase Lectura del segundo archivo (NFCHandler.py)
class Lectura(CardObserver):  # Heredamos de CardObserver para implementar el método update
    def __init__(self, tabla_movimientos=None):
        super().__init__()  # Importante llamar al constructor de la clase padre
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
        """Método requerido por CardObserver que se llama cuando hay cambios en las tarjetas"""
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

    def read_card(self):
        """Lee los datos de la tarjeta NFC cuando se detecta"""
        if self.cards:
            card = self.cards[0]
            try:
                connection = card.createConnection()
                connection.connect()
                time.sleep(0.5)
                # Comando para obtener el UID de la tarjeta
                getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                response, sw1, sw2 = connection.transmit(getuid)
                self.uid = toHexString(response).replace(" ", "").upper()
                new_data = self.get_data_from_api(self.uid)
                with self.lock:
                    self.card_data = new_data
                self.data_ready.set()
            except Exception as e:
                print(f"Error al leer tarjeta: {e}")
                with self.lock:
                    self.card_data = None
                self.data_ready.clear()

    def get_data_from_api(self, uid):
        """Obtiene los datos de la tarjeta desde la API"""
        url = "https://cmisocket.miteleferico.bo/api/v1/billetaje/info-card"
        try:
            response = requests.post(url, json={"card_uid": uid})
            data = response.json()
            
            if data.get("success"):
                card = data.get("card", {})
                card_state = data.get("cardState", {})
                profile = data.get("profile", {})
                person = data.get("person", {})
                
                processed_data = {
                    "uid": uid,
                    "first_name": person.get("name", "No disponible"),
                    "last_name": person.get("last_name", "No disponible"),
                    "document": person.get("document", "No disponible"),
                    "profile_name": profile.get("name", "No disponible"),
                    "balance": card_state.get("balance", "No disponible"),
                    "card_status": self.definir_estado(card.get("status", "No disponible")),
                    "social_reason": person.get("social_reason", "No disponible"),
                    "nit": person.get("nit", "No disponible"),
                }
                return processed_data
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener datos de tarjeta: {e}")
            return None

    def get_card_data(self, timeout=None):
        """Devuelve los datos de la tarjeta si están disponibles"""
        if self.data_ready.wait(timeout):
            with self.lock:
                return self.card_data
        return None

    def is_data_ready(self):
        """Comprueba si los datos de la tarjeta están listos"""
        return self.data_ready.is_set()

    def definir_estado(self, estado):
        if estado.lower() == 'a':
            return "ACTIVA"
        elif estado.lower() == 'l':
            return "BLOQUEADO"
        elif estado.lower() == 'b':
            return "INACTIVA"
        else:
            return "Estado desconocido"

class QRDatosManager:
    def __init__(self):
        # URL base para la API - Nueva dirección sin requerir token
        self.base_url = "https://serviciosvirtual-test.miteleferico.bo"
        self.api_url = f"{self.base_url}/api/v1/payment/register-payment-external"
        self.datos_recarga = {}
        self.qr_url = None
        self.correo_temporal = None  # Para almacenar el correo temporalmente sin guardarlo
        self.api_response = None  # Para almacenar la respuesta completa de la API
        
        # Creamos una instancia del lector NFC pero sin integrarla con el monitor
        # para evitar errores si no hay lector conectado
        self.nfc_reader = Lectura()
        self.cardmonitor = None  # Lo inicializaremos solo si es necesario
        
        try:
            # Solo inicializamos el monitor de tarjetas si realmente lo necesitamos
            self.inicializar_monitor_tarjetas()
        except Exception as e:
            print(f"Advertencia: No se pudo inicializar el monitor de tarjetas: {e}")
            # Seguimos adelante sin el monitor de tarjetas
    
    def inicializar_monitor_tarjetas(self):
        """Inicializa el monitor de tarjetas solo si es necesario"""
        try:
            self.cardmonitor = CardMonitor()
            self.cardmonitor.addObserver(self.nfc_reader)
            print("Monitor de tarjetas NFC inicializado correctamente")
        except Exception as e:
            print(f"Error al inicializar monitor de tarjetas: {e}")
            self.cardmonitor = None
    
    def __del__(self):
        # Limpiamos el monitor de tarjetas si existe
        try:
            if self.cardmonitor:
                self.cardmonitor.deleteObserver(self.nfc_reader)
        except:
            pass
    
    def recopilar_datos(self, uid, documento, razon_social, complemento, correo, monto):
        """Recopila los datos combinando la información de la tarjeta NFC y los datos del formulario"""
        self.correo_temporal = correo
        
        # Primero intentamos obtener datos de la tarjeta NFC si está disponible
        card_data = None
        uid_clean = uid.replace("UID: ", "") if uid.startswith("UID: ") else uid
        
        # Si tenemos un lector activo y datos disponibles, los usamos
        if self.nfc_reader.is_data_ready():
            card_data = self.nfc_reader.get_card_data()
        
        # Si no tenemos datos del reader, intentamos obtenerlos mediante la API directamente
        if not card_data and uid_clean:
            card_data = self.nfc_reader.get_data_from_api(uid_clean)
        
        # Si tenemos datos de la tarjeta, los combinamos con los del formulario
        if card_data:
            self.datos_recarga = {
                "monto": float(monto) if monto else 0,
                "uid": card_data.get("uid", uid_clean),
                "first_name": card_data.get("first_name", ""),
                "last_name": card_data.get("last_name", ""),
                "document": card_data.get("document", documento),
                "email": correo,
                "nit": card_data.get("nit", documento),
                "razon_social": card_data.get("social_reason", razon_social),
                "timestamp": int(time.time())
            }
        else:
            # Si no hay datos de la tarjeta, usamos solo los del formulario
            self.datos_recarga = {
                "monto": float(monto) if monto else 0,
                "uid": uid_clean,
                "first_name": "",  # Vacío porque no tenemos este dato
                "last_name": "",   # Vacío porque no tenemos este dato
                "document": documento,
                "email": correo,
                "nit": documento,
                "razon_social": razon_social,
                "timestamp": int(time.time())
            }
            
        # Depuración: imprimir datos recopilados
        print("Datos recopilados para la recarga:")
        for key, value in self.datos_recarga.items():
            print(f"  {key}: {value}")
        
        # Guardar localmente en un archivo JSON para utilizarlo en la solicitud
        with open("ultima_recarga.json", "w") as f:
            json.dump(self.datos_recarga, f, indent=4)
            
        return self.datos_recarga
    
    def cargar_datos_recarga(self):
        """Carga los datos del archivo ultima_recarga.json"""
        try:
            if os.path.exists("ultima_recarga.json"):
                with open("ultima_recarga.json", "r") as f:
                    self.datos_recarga = json.load(f)
                return True
            else:
                print("Archivo ultima_recarga.json no encontrado")
                return False
        except Exception as e:
            print(f"Error al cargar datos de recarga: {e}")
            return False
    
    def enviar_solicitud(self):
        """Envía los datos guardados en 'ultima_recarga.json' a la nueva API y espera la URL del QR como respuesta"""
        try:
            # Cargar los datos del archivo JSON
            if not self.cargar_datos_recarga():
                return False, "No se pudieron cargar los datos de recarga"

            # Construir el payload usando el nuevo formato requerido
            # No enviamos el timestamp al API ya que no lo requiere
            datos_para_api = {
                "monto": self.datos_recarga.get("monto", 0),
                "uid": self.datos_recarga.get("uid", ""),
                "first_name": self.datos_recarga.get("first_name", ""),
                "last_name": self.datos_recarga.get("last_name", ""),
                "document": self.datos_recarga.get("document", ""),
                "email": self.datos_recarga.get("email", ""),
                "nit": self.datos_recarga.get("nit", ""),
                "razon_social": self.datos_recarga.get("razon_social", "")
            }

            # Headers para la solicitud
            headers = {
                "Content-Type": "application/json"
                # Ya no necesitamos token de autenticación
            }
            
            respuesta = requests.post(self.api_url, json=datos_para_api, headers=headers)

            if respuesta.status_code == 200:
                self.api_response = respuesta.json()
                
        # Verificar si la respuesta tiene el formato esperado
                if self.api_response.get("success") and "data" in self.api_response:
                    data = self.api_response["data"]
                    # Adaptar según la estructura real de la respuesta del nuevo API
                    self.qr_url = data.get("qr_url", data.get("qr_simple_url", ""))
                    
                    # Guardar la respuesta completa para uso posterior
                    with open("ultima_respuesta_api.json", "w") as f:
                        json.dump(self.api_response, f, indent=4)
                    
                    return True, self.qr_url
                else:
                    return False, "Formato de respuesta de API inesperado"
            else:
                return False, f"Error {respuesta.status_code}: {respuesta.text}"

        except Exception as e:
            print(f"Error al enviar solicitud: {e}")
            return False, str(e)
    
    def generar_qr_basado_en_respuesta(self):
        """Descarga y muestra la imagen QR desde qr_url en lugar de generar un nuevo QR"""
        try:
            if self.qr_url and self.api_response and "data" in self.api_response:
                # Usar directamente la URL del QR proporcionada por la API
                qr_url = self.api_response["data"].get("qr_url", self.api_response["data"].get("qr_simple_url", ""))
                
                print(f"URL del QR a descargar: {qr_url}")
                
                if qr_url:
                    # Descargar la imagen QR desde la URL
                    qr_image = download_image_from_url(qr_url)
                    if qr_image:
                        return qr_image, self.api_response["data"]
                    else:
                        # Si falla la descarga, generamos un QR temporal como respaldo
                        print("Fallo al descargar QR, generando uno temporal...")
                        return self.generar_qr_temporal(), self.api_response["data"]
            
            return None, None
        except Exception as e:
            print(f"Error al generar QR basado en respuesta: {e}")
            return None, None
    
    def generar_qr_temporal(self):
        """Genera un QR temporal con los datos de ultima_recarga.json mientras se espera la respuesta de la API"""
        if not self.datos_recarga:
            if not self.cargar_datos_recarga():
                return None
        
        # Crear un código QR temporal basado en los datos recopilados
        data = json.dumps(self.datos_recarga)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        # Convertir la imagen PIL a QImage usando la función auxiliar
        return pil_to_qimage(img)


class QRRechargeDialog(QDialog):
    def __init__(self, datos_manager, parent=None):
        super().__init__(parent)
        self.datos_manager = datos_manager
        self.setup_ui()
        self.show_loading_qr()
        
        # Iniciar proceso de solicitud en un hilo separado
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_qr_status)
        self.timer.start(500)  # Verificar cada 500ms
        
    def setup_ui(self):
        self.setWindowTitle("Código QR para Recarga")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #CFD8DC;
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Encabezado
        header = QLabel("Escanea el código QR")
        header.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        
        # Contenedor del QR
        self.qr_container = QLabel()
        self.qr_container.setFixedSize(300, 300)
        self.qr_container.setStyleSheet("background-color: white; border: 1px solid #CFD8DC;")
        self.qr_container.setAlignment(Qt.AlignCenter)
        
        # Estado
        self.status_label = QLabel("Generando código QR...")
        self.status_label.setStyleSheet("color: #455A64; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Información adicional
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #455A64; font-size: 12px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        # Botón Cerrar
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(header)
        layout.addWidget(self.qr_container, 0, Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addWidget(self.info_label)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
    def show_loading_qr(self):
        """Muestra un indicador de carga mientras se genera el QR"""
        loading_gif = QMovie("loading.gif")
        if QFile("loading.gif").exists():
            self.qr_container.setMovie(loading_gif)
            loading_gif.start()
        else:
            self.qr_container.setText("Cargando...")
            self.qr_container.setStyleSheet("background-color: white; font-size: 20px;")
    
    def show_qr_image(self, qr_image):
        """Muestra la imagen QR en el diálogo"""
        if isinstance(qr_image, QImage):
            pixmap = QPixmap.fromImage(qr_image)
        else:
            pixmap = QPixmap(qr_image)
        
        scaled_pixmap = pixmap.scaled(
            self.qr_container.width(), 
            self.qr_container.height(),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        self.qr_container.setPixmap(scaled_pixmap)
    
    def check_qr_status(self):
        """Verifica si ya tenemos la respuesta de la API y muestra el QR"""
        if self.datos_manager.qr_url:
            self.timer.stop()
            
            qr_image, api_data = self.datos_manager.generar_qr_basado_en_respuesta()
            
            if qr_image:
                self.show_qr_image(qr_image)
                
                # Mostrar información del pago
                if api_data:
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']}")
                    
                    # Mostrar información adicional como código de recaudación
                    info_text = f"Código de transacción: {api_data.get('id_transaccion', 'N/A')}\n"
                    info_text += f"ID Recaudación: {api_data.get('codigo_recaudacion', 'N/A')}"
                    self.info_label.setText(info_text)
            else:
                # Si falló la generación del QR basado en la respuesta, usamos el temporal
                temp_qr = self.datos_manager.generar_qr_temporal()
                if temp_qr:
                    self.show_qr_image(temp_qr)
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']} (QR temporal)")
                else:
                    self.status_label.setText("Error al generar el código QR")


def solicitar_recarga(uid="", documento="", razon_social="", complemento="", correo="", monto="", parent_widget=None):
    """Función principal para iniciar el proceso de recarga - Ya no requiere auth_token"""
    # Crear instancia del gestor de datos
    try:
        datos_manager = QRDatosManager()
        
        # Verificar si tenemos datos proporcionados o debemos cargar desde el archivo
        if uid and documento and monto:
            # Recopilar datos y guardarlos en 'ultima_recarga.json'
            datos_manager.recopilar_datos(uid, documento, razon_social, complemento, correo, monto)
        else:
            # Cargar datos del archivo JSON
            if not datos_manager.cargar_datos_recarga():
                QMessageBox.critical(
                    parent_widget,
                    "Error de Carga",
                    "No se pudieron cargar los datos de recarga del archivo ultima_recarga.json",
                    QMessageBox.Ok
                )
                return False
        
        # Enviar solicitud a la API
        success, message = datos_manager.enviar_solicitud()
        
        if success:
            dialog = QRRechargeDialog(datos_manager, parent_widget)
            return dialog.exec_()
        else:
            QMessageBox.critical(
                parent_widget,
                "Error de Conexión",
                f"No se pudo conectar con el servidor: {message}",
                QMessageBox.Ok
            )
            return False
    except Exception as e:
        import traceback
        error_msg = f"Error inesperado:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        
        if parent_widget:
            QMessageBox.critical(
                parent_widget,
                "Error Inesperado",
                error_msg,
                QMessageBox.Ok
            )
        return False


