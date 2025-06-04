from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from smartcard.Card import Card
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
import time
import requests
import os
import vlc
from segunda3 import Ui_MainWindow3  # type: ignore
from API import ApiClient 
import sys

getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def traducir_estado(estado):
    if estado.lower() == 'a':
        return "ACTIVA"
    elif estado.lower() == 'l':
        return "BLOQUEADO"
    elif estado.lower() == 'b':
        return "INACTIVA"
    else:
        return "Estado desconocido"

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
       
        self.background = QLabel(self)
        self.background.setStyleSheet("background-color: #f0f0f0; border-radius: 20px;")
        self.background.setGeometry(0, 0, 500, 250) 

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(195, 45, 175, 85)  
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(project_dir, "recursoscarrusel", "loading.gif")
        
        self.movie = QMovie(gif_path)  
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        
        self.label = QLabel("Cargando sus datos, espere por favor...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #666666; font-size: 22px; font-weight: bold;")
        self.label.setGeometry(0, 160, 500, 35)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

    def showEvent(self, event):
        self.animation.start()
        super().showEvent(event)

    def hideEvent(self, event):
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()
        super().hideEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1280, 1024)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_M:
            self.maximize_window()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()  
        else:
            super().keyPressEvent(event)

    def maximize_window(self):
        if self.windowState() == Qt.WindowNoState:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowNoState)  

class Ui_MainWindow(object):
    def __init__(self):
        self.current_video_index = 0
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        video_dir = os.path.join(project_dir, "recursoscarrusel")
        
        self.videos = [
            os.path.join(video_dir, "promov1.mp4"),
            os.path.join(video_dir, "promov2.mp4"),
            os.path.join(video_dir, "promov3.mp4")
        ]
        
        # Usar el singleton del monitor NFC
        self.nfc_monitor = NFCMonitorSingleton.get_instance()
        self.nfc_monitor.register_carousel(self)
        
        # Conectar señales del monitor NFC
        self.nfc_monitor.uid_detected.connect(self.handle_uid_detected)
        self.nfc_monitor.card_error.connect(self.show_error_message)
        self.nfc_monitor.card_removed.connect(self.handle_card_removal)
        
        self.instance = None
        self.media_player = None
        self.video_frame = None
        self.timer = None
        self.saldo_window = None
        self.loading_dialog = None

    def handle_uid_detected(self, uid):
        # Obtener datos de la API
        result = self.get_data_from_api(uid)
        
        if isinstance(result, tuple):
            name, last_name, document, profile_name, balance, card_status = result
            self.show_loading_dialog(uid, name, last_name, document, profile_name, balance, card_status)
        else:
            self.show_error_message("Tarjeta externa: \n Esta tarjeta no pertenece al sistema")

    def handle_card_removal(self):
        # Solo pausar el video si hay ventanas abiertas además del carrusel
        if hasattr(self, 'saldo_window') and self.saldo_window:
            if self.media_player:
                self.media_player.play()  # Reanudar el video si estaba pausado
            
            # Mostrar mensaje de cierre automático sin botones
            self.nfc_monitor.show_auto_close_message("Se ha retirado la tarjeta\nCerrando ventanas...")

    def show_error_message(self, message):
        # Mostrar mensaje de error sin botón OK
        self.nfc_monitor.show_auto_close_message(message)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 1024)

        MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        layout = QVBoxLayout(self.centralwidget)
        
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_frame)
        
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        
        if sys.platform.startswith('win'):
            self.media_player.set_hwnd(int(self.video_frame.winId()))
        elif sys.platform.startswith('linux'):
            self.media_player.set_xwindow(self.video_frame.winId())
        elif sys.platform.startswith('darwin'):
            self.media_player.set_nsobject(int(self.video_frame.winId()))
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_video_status)
        self.timer.start()
        self.timer.setSingleShot(False)
        
        self.play_video(self.videos[0])
        
        self.retranslateUi(MainWindow)
        
        QMetaObject.connectSlotsByName(MainWindow)

    def play_video(self, video_path):
        if os.path.exists(video_path):
            media = self.instance.media_new(video_path)
            self.media_player.set_media(media)
            self.media_player.play()
            print(f"Reproduciendo video: {video_path}")
        else:
            print(f"Error: El archivo de video no existe: {video_path}")
            self.play_next_video()

    def check_video_status(self):
        state = self.media_player.get_state()
        if state == vlc.State.Ended:
            self.play_next_video()
        elif state == vlc.State.Paused and (self.saldo_window is None or not self.saldo_window.isVisible()):
            self.media_player.play()

    def play_next_video(self):
        self.current_video_index = (self.current_video_index + 1) % len(self.videos)
        self.play_video(self.videos[self.current_video_index])

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

    def show_loading_dialog(self, uid, name, last_name, document, profile_name, balance, card_status):
        self.loading_dialog = LoadingDialog(self.centralwidget)
        self.loading_dialog.show()

        QTimer.singleShot(3000, lambda: self.show_new_interface(uid, name, last_name, document, profile_name, balance, card_status))
        QTimer.singleShot(3000, self.loading_dialog.close)

    def show_new_interface(self, uid, name, last_name, document, profile_name, balance, card_status):
        if self.media_player:
            self.media_player.pause()
            
        self.saldo_window = QMainWindow()
        self.saldo_ui = Ui_MainWindow3()
        self.saldo_ui.setupUi(self.saldo_window)
        self.saldo_window.resize(1280, 1024)
        
        # Registrar la ventana de saldo en el monitor NFC
        self.nfc_monitor.register_window(self.saldo_window)
        
        self.saldo_window.destroyed.connect(lambda: self.on_saldo_window_closed())
        
        self.saldo_ui.update_uid(uid)
        self.saldo_ui.update_name(name, last_name)  
        self.saldo_ui.update_document(document)
        self.saldo_ui.update_profile(profile_name)
        self.saldo_ui.update_balance(balance)
        self.saldo_ui.update_card_status(card_status)   
        self.saldo_window.show()

    def on_saldo_window_closed(self):
        # Desregistrar la ventana cuando se cierra
        self.nfc_monitor.unregister_window(self.saldo_window)
        self.saldo_window = None
        self.resume_video()

    def resume_video(self):
        if self.media_player:
            self.media_player.play()
            print("Reanudando reproducción de video...")

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
                
                return (
                    person.get("name", "Nombre no disponible"),
                    person.get("last_name", "Apellido no disponible"),
                    person.get("document", "Documento no disponible"),
                    profile.get("name", "Perfil no disponible"),
                    card_state.get("balance", "Saldo no disponible"),
                    traducir_estado(card.get("status", ""))
                )
            else:
                print("\nError: La API no reportó éxito")
                return None
                
        except Exception as e:
            print(f"\nError en la solicitud: {str(e)}")
            return None

class NFCMonitor(QObject):
    uid_detected = Signal(str)
    card_error = Signal(str)
    card_removed = Signal()
    
    def __init__(self):
        super().__init__()
        self.nfc_reader = NFCReader()
        self.cardmonitor = CardMonitor()
        self.cardmonitor.addObserver(self.nfc_reader)
        
        # Conectar señales del lector a las señales del monitor
        self.nfc_reader.uid_detected.connect(self.uid_detected)
        self.nfc_reader.card_error.connect(self.card_error)
        self.nfc_reader.card_removed.connect(self.handle_card_removal)
        
        # Lista de ventanas registradas para cerrar
        self.windows_to_close = []
        self.carousel_window = None
        self.error_dialog = None
        
        # Estilo para mensajes
        self.message_style = """
            QMessageBox {
                background-color: #f0f0f0;
                text-align: center;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 24px;
                font-weight: bold;
                padding: 30px;
                min-width: 400px;
                max-width: 100px;
                text-align: center;
                qproperty-alignment: AlignCenter;
            }
        """
    
    def register_carousel(self, carousel_window):
        self.carousel_window = carousel_window
    
    def register_window(self, window):
        if window not in self.windows_to_close:
            self.windows_to_close.append(window)
    
    def unregister_window(self, window):
        if window in self.windows_to_close:
            self.windows_to_close.remove(window)
    
    def handle_card_removal(self):
        self.card_removed.emit()
        if len(self.windows_to_close) > 0:
            self.show_auto_close_message("Se ha retirado la tarjeta\nCerrando ventanas...")
    
    def show_auto_close_message(self, message):
        # Cerrar diálogo anterior si existe
        if self.error_dialog:
            self.error_dialog.close()
        
        # Crear nuevo diálogo sin botones
        self.error_dialog = QMessageBox()
        self.error_dialog.setIcon(QMessageBox.NoIcon)
        self.error_dialog.setStyleSheet(self.message_style)
        
        formatted_message = message.replace("\n", "<br>")
        self.error_dialog.setText(formatted_message)
        self.error_dialog.setWindowTitle("Información")
        self.error_dialog.setStandardButtons(QMessageBox.NoButton)
        
        self.error_dialog.setGeometry(350, 400, 300, 200)
        self.error_dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        # Mostrar el diálogo
        self.error_dialog.show()
        
        # Configurar temporizador para cerrar automáticamente después de 3 segundos
        QTimer.singleShot(3000, self.close_message_and_windows)
    
    def close_message_and_windows(self):
        if self.error_dialog:
            self.error_dialog.close()
            self.error_dialog = None
        
        # Cerrar todas las ventanas registradas
        for window in self.windows_to_close[:]:
            if window != self.carousel_window and hasattr(window, 'close'):
                window.close()
        self.windows_to_close = [w for w in self.windows_to_close if w == self.carousel_window]

class NFCMonitorSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        if NFCMonitorSingleton._instance is None:
            NFCMonitorSingleton._instance = NFCMonitor()
        return NFCMonitorSingleton._instance

class NFCReader(CardObserver, QObject):
    uid_detected = Signal(str)
    card_error = Signal(str)
    card_removed = Signal()

    def __init__(self):
        CardObserver.__init__(self)
        QObject.__init__(self)
        self.cards = []
        self.card_read = False
        self.uid = None
        self.last_read_time = None

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards.append(card)
                if not self.card_read:
                    try:
                        connection = card.createConnection()
                        connection.connect()
                        time.sleep(0.5)
                        response, sw1, sw2 = connection.transmit(getuid)
                        self.uid = toHexString(response).replace(" ", "").upper()
                        self.uid_detected.emit(self.uid)
                        self.card_read = True
                        self.last_read_time = time.time()
                    except CardConnectionException:
                        self.card_error.emit("Error de lectura: No se pudo leer la tarjeta")
                    except Exception as e:
                        self.card_error.emit(f"Error: {str(e)}")

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)
                self.card_read = False
                self.card_removed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())