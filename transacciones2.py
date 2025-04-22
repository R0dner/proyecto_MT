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
from segunda3 import Ui_MainWindow3  # type: ignore
from API import ApiClient 

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
        gif_path = os.path.join(project_dir, "imagenes2", "loading.gif")
        
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
        self.current_image_index = 0
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(project_dir, "imagenes2")
        
        self.images = [
            os.path.join(image_dir, "promo3.jpeg"),
            os.path.join(image_dir, "promo2.jpeg"),
            os.path.join(image_dir, "promo1.png")
        ]
        self.nfc_reader = NFCReader()
        self.cardmonitor = CardMonitor()
        self.cardmonitor.addObserver(self.nfc_reader)
        self.nfc_reader.uid_detected.connect(self.show_loading_dialog)
        self.nfc_reader.card_error.connect(self.show_error_message)

    def show_error_message(self, message):
        error_dialog = QMessageBox()

        error_dialog.setIcon(QMessageBox.NoIcon)
       
        error_dialog.setStyleSheet("""
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
            QMessageBox QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 40px;
                text-align: center;
            }
            QMessageBox QPushButton:hover {
                background-color: #C82333;
            }
        """)
        formatted_message = message.replace("\n", "<br>")
        error_dialog.setText(formatted_message)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Advertencia")
        error_dialog.setStandardButtons(QMessageBox.Ok)
        
        error_dialog.setGeometry(350, 400, 300, 200)
        error_dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        error_dialog.exec_()
    
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 1024)

        MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        layout = QVBoxLayout(self.centralwidget)
        
        self.fondoPrincipal = QLabel()  
        layout.addWidget(self.fondoPrincipal)
        
        self.load_background_image(self.images[0])
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_background_image)
        self.timer.start(4000)

        self.retranslateUi(MainWindow)
        
        self.saldo_window = QMainWindow()
        self.saldo_ui = Ui_MainWindow3()
        self.saldo_ui.setupUi(self.saldo_window)
        
        self.saldo_window.resize(1280, 1024)
        
        QMetaObject.connectSlotsByName(MainWindow)

    def load_background_image(self, image_path):
        self.current_image = QImage(image_path)
        if not self.current_image.isNull():
            pixmap = QPixmap.fromImage(self.current_image)
            self.fondoPrincipal.setPixmap(pixmap)  
            self.fondoPrincipal.setScaledContents(True)  

    def change_background_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.load_background_image(self.images[self.current_image_index])

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

    def show_loading_dialog(self, uid, name, last_name, document, profile_name, balance, card_status):
        self.loading_dialog = LoadingDialog(self.centralwidget)
        self.loading_dialog.show()

        QTimer.singleShot(3000, lambda: self.show_new_interface(uid, name, last_name, document, profile_name, balance, card_status))
        QTimer.singleShot(3000, self.loading_dialog.close)


    def show_new_interface(self, uid, name, last_name, document, profile_name, balance, card_status):
        self.saldo_ui.update_uid(uid)
        self.saldo_ui.update_name(name, last_name)  
        self.saldo_ui.update_document(document)
        self.saldo_ui.update_profile(profile_name)
        self.saldo_ui.update_balance(balance)
        self.saldo_ui.update_card_status(card_status)   
        self.saldo_window.show()

class NFCReader(CardObserver, QObject):
    uid_detected = Signal(str,str,str,str,str,str,str) 
    card_error = Signal(str)  

    def __init__(self):
        CardObserver.__init__(self)
        QObject.__init__(self)
        self.cards = []
        self.card_read = False
        self.uid = None
        self.last_read_time = None
        self.api_client = ApiClient("https://cmisocket.miteleferico.bo")

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards.append(card)
                if not self.card_read:
                    self.read_uid(card)
                    self.card_read = True
                    self.last_read_time = time.time()

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)
                self.card_read = False

    def read_uid(self, card):
        try:
            connection = card.createConnection()
            connection.connect()
            time.sleep(0.5) 
            response, sw1, sw2 = connection.transmit(getuid)
            self.uid = toHexString(response).replace(" ", "").upper()
            result = self.get_data_from_api(self.uid)
            
            if isinstance(result, tuple):
                name, last_name, document, profile_name, balance, card_status = result
                self.uid_detected.emit(self.uid, name, last_name, document, profile_name, balance, card_status)
            else:
                self.card_error.emit("Tarjeta externa: \n Esta tarjeta no pertenece al sistema")
            
        except CardConnectionException:
            self.card_error.emit("Error de lectura: No se pudo leer la tarjeta")

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

if __name__ == '__main__':
    import sys  
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

