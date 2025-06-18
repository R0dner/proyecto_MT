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
from smartcard.Card import Card
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
import threading

def pil_to_qimage(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_data = buffer.getvalue()
    qimage = QImage.fromData(img_data)
    return qimage

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
    
class NFCMonitorSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        if NFCMonitorSingleton._instance is None:
            from nfc_monitor import NFCMonitorSingleton as MainNFCMonitor
            return MainNFCMonitor.get_instance()
        return NFCMonitorSingleton._instance

class SimpleNFCMonitor(QObject):
    card_removed = Signal()
    
    def __init__(self):
        super().__init__()
        self.windows_to_close = []
        
    def register_window(self, window):
        if window not in self.windows_to_close:
            self.windows_to_close.append(window)
            print(f"Ventana registrada en monitor simple. Total: {len(self.windows_to_close)}")
    
    def unregister_window(self, window):
        if window in self.windows_to_close:
            self.windows_to_close.remove(window)
            print(f"Ventana eliminada del monitor simple. Total: {len(self.windows_to_close)}")

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

    def read_card(self):
        if self.cards:
            card = self.cards[0]
            try:
                connection = card.createConnection()
                connection.connect()
                time.sleep(0.5)
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
        if self.data_ready.wait(timeout):
            with self.lock:
                return self.card_data
        return None

    def is_data_ready(self):
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
        self.base_url = "https://serviciosvirtual-test.miteleferico.bo"
        self.api_url = f"{self.base_url}/api/v1/payment/register-payment-external"
        self.datos_recarga = {}
        self.qr_url = None
        self.correo_temporal = None
        self.api_response = None
        
        self.nfc_reader = Lectura()
        self.cardmonitor = None
        
        try:
            self.inicializar_monitor_tarjetas()
        except Exception as e:
            print(f"Advertencia: No se pudo inicializar el monitor de tarjetas: {e}")

    def inicializar_monitor_tarjetas(self):
        try:
            self.cardmonitor = CardMonitor()
            self.cardmonitor.addObserver(self.nfc_reader)
            print("Monitor de tarjetas NFC inicializado correctamente")
        except Exception as e:
            print(f"Error al inicializar monitor de tarjetas: {e}")
            self.cardmonitor = None
    
    def __del__(self):
        try:
            if self.cardmonitor:
                self.cardmonitor.deleteObserver(self.nfc_reader)
        except:
            pass
    
    def recopilar_datos(self, uid, documento, razon_social, complemento, correo, monto):
        self.correo_temporal = correo
        uid_clean = uid.replace("UID: ", "") if uid.startswith("UID: ") else uid
        
        if self.nfc_reader.is_data_ready():
            card_data = self.nfc_reader.get_card_data()
        
        if not card_data and uid_clean:
            card_data = self.nfc_reader.get_data_from_api(uid_clean)
        
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
            self.datos_recarga = {
                "monto": float(monto) if monto else 0,
                "uid": uid_clean,
                "first_name": "",
                "last_name": "",
                "document": documento,
                "email": correo,
                "nit": documento,
                "razon_social": razon_social,
                "timestamp": int(time.time())
            }
            
        with open("ultima_recarga.json", "w") as f:
            json.dump(self.datos_recarga, f, indent=4)
            
        return self.datos_recarga
    
    def cargar_datos_recarga(self):
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
    
    def enviar_solicitud(self, max_intentos=3):
        for intento in range(1, max_intentos + 1):
            try:
                if not self.cargar_datos_recarga():
                    return False, "No se pudieron cargar los datos de recarga"

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

                headers = {"Content-Type": "application/json"}
                
                respuesta = requests.post(
                    self.api_url, 
                    json=datos_para_api, 
                    headers=headers,
                    timeout=30
                )

                if respuesta.status_code == 200:
                    self.api_response = respuesta.json()
                    
                    if self.api_response.get("success") and "data" in self.api_response:
                        data = self.api_response["data"]
                        self.qr_url = data.get("qr_url", data.get("qr_simple_url", ""))
                        
                        with open("ultima_respuesta_api.json", "w") as f:
                            json.dump(self.api_response, f, indent=4)
                        
                        return True, self.qr_url
                    else:
                        return False, "Formato de respuesta de API inesperado"
                elif respuesta.status_code == 504:
                    if intento < max_intentos:
                        tiempo_espera = 2 ** intento
                        print(f"Error 504 recibido. Reintentando en {tiempo_espera} segundos...")
                        time.sleep(tiempo_espera)
                        continue
                    return False, f"Error 504: Gateway Timeout después de {max_intentos} intentos"
                else:
                    return False, f"Error {respuesta.status_code}: {respuesta.text}"

            except requests.exceptions.Timeout:
                if intento < max_intentos:
                    tiempo_espera = 2 ** intento
                    print(f"Timeout en solicitud. Reintentando en {tiempo_espera} segundos...")
                    time.sleep(tiempo_espera)
                    continue
                return False, f"Error de timeout después de {max_intentos} intentos"
            except Exception as e:
                print(f"Error al enviar solicitud (intento {intento}): {e}")
                if intento < max_intentos:
                    time.sleep(2 ** intento)
                    continue
                return False, str(e)
    
    def generar_qr_basado_en_respuesta(self):
        try:
            if self.qr_url and self.api_response and "data" in self.api_response:
                qr_url = self.api_response["data"].get("qr_url", self.api_response["data"].get("qr_simple_url", ""))
                
                print(f"URL del QR a descargar: {qr_url}")
                
                if qr_url:
                    qr_image = download_image_from_url(qr_url)
                    if qr_image:
                        return qr_image, self.api_response["data"]
                    else:
                        print("Fallo al descargar QR, generando uno temporal...")
                        return self.generar_qr_temporal(), self.api_response["data"]
            
            return None, None
        except Exception as e:
            print(f"Error al generar QR basado en respuesta: {e}")
            return None, None
    
    def generar_qr_temporal(self):
        if not self.datos_recarga:
            if not self.cargar_datos_recarga():
                return None
        
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
        return pil_to_qimage(img)

class QRRechargeDialog(QDialog):
    def __init__(self, datos_manager, parent=None):
        super().__init__(parent)
        self.datos_manager = datos_manager
        self.nfc_monitor = NFCMonitorSingleton.get_instance()
        self.setup_ui()
        self.show_loading_qr()
        self.nfc_monitor.register_window(self)
        self.nfc_monitor.card_removed.connect(self.close_on_card_removal)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_qr_status)
        self.timer.start(500)

    def close_on_card_removal(self):
        print("QR Dialog: Tarjeta removida detectada - Cerrando ventana QR")
        self.accept()

    def closeEvent(self, event):
        try:
            if hasattr(self, 'nfc_monitor') and self.nfc_monitor:
                self.nfc_monitor.unregister_window(self)
                print("Ventana QR desregistrada del monitor NFC")
        except Exception as e:
            print(f"Error al desregistrar ventana: {e}")
        
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        
        super().closeEvent(event)

    def setup_ui(self):
        self.setWindowTitle("Código QR para Recarga")
        self.setFixedSize(400, 550)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #CFD8DC;
            }
        """)
        
        layout = QVBoxLayout(self)
        
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
        
        self.qr_container = QLabel()
        self.qr_container.setFixedSize(300, 300)
        self.qr_container.setStyleSheet("background-color: white; border: 1px solid #CFD8DC;")
        self.qr_container.setAlignment(Qt.AlignCenter)
        
        self.status_label = QLabel("Generando código QR...")
        self.status_label.setStyleSheet("color: #455A64; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #455A64; font-size: 12px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        buttons_layout = QHBoxLayout()
        
        payment_done_button = QPushButton("Ya realicé el pago")
        payment_done_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219A52;
            }
        """)
        payment_done_button.clicked.connect(self.payment_completed)
        
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        close_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(payment_done_button)
        buttons_layout.addWidget(close_button)
        
        layout.addWidget(header)
        layout.addWidget(self.qr_container, 0, Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addWidget(self.info_label)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def show_loading_qr(self):
        loading_gif = QMovie("loading.gif")
        if QFile("loading.gif").exists():
            self.qr_container.setMovie(loading_gif)
            loading_gif.start()
        else:
            self.qr_container.setText("Cargando...")
            self.qr_container.setStyleSheet("background-color: white; font-size: 20px;")
    
    def show_qr_image(self, qr_image):
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
    
    def payment_completed(self):
        self.accept()

    def close_main_window(self):
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget,QMainWindow):
                widget.close()
                break
    
    def check_qr_status(self):
        if not hasattr(self, 'wait_counter'):
            self.wait_counter = 0
        
        self.wait_counter += 1
        
        if self.wait_counter % 2 == 0:
            self.status_label.setText(f"Generando código QR... ({self.wait_counter//2}s)")
        
        if self.wait_counter > 20 and not self.datos_manager.qr_url:
            temp_qr = self.datos_manager.generar_qr_temporal()
            if temp_qr and not hasattr(self, 'showed_temp_qr'):
                self.show_qr_image(temp_qr)
                self.status_label.setText("Usando QR temporal mientras esperamos respuesta...")
                self.showed_temp_qr = True
        
        if self.datos_manager.qr_url:
            self.timer.stop()
            
            qr_image, api_data = self.datos_manager.generar_qr_basado_en_respuesta()
            
            if qr_image:
                self.show_qr_image(qr_image)
                
                if api_data:
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']}")
                    self.info_label.setText("Escanea el código QR para completar tu pago")
            else:
                temp_qr = self.datos_manager.generar_qr_temporal()
                if temp_qr:
                    self.show_qr_image(temp_qr)
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']} (QR temporal)")
                else:
                    self.status_label.setText("Error al generar el código QR")

def solicitar_recarga(uid="", documento="", razon_social="", complemento="", correo="", monto="", parent_widget=None):
    try:
        datos_manager = QRDatosManager()
        
        if uid and documento and monto:
            datos_manager.recopilar_datos(uid, documento, razon_social, complemento, correo, monto)
        else:
            if not datos_manager.cargar_datos_recarga():
                QMessageBox.critical(
                    parent_widget,
                    "Error de Carga",
                    "No se pudieron cargar los datos de recarga del archivo ultima_recarga.json",
                    QMessageBox.Ok
                )
                return False
        
        success, message = datos_manager.enviar_solicitud()
        
        if success:
            dialog = QRRechargeDialog(datos_manager, parent_widget)
            result = dialog.exec_()
        
            return result == QDialog.Accepted
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

if __name__ == "__main__":
    app = QApplication([])
    app.exec_()