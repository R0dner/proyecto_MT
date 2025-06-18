from PySide2.QtCore import QObject, Signal, QTimer
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
from PySide2.QtWidgets import QMessageBox, QLabel
from PySide2.QtCore import Qt
import time
from NFCFileCleanup import NFCFileCleanup

getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]

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
                    except CardConnectionException as e:
                        self.card_error.emit("Error de lectura: No se pudo leer la tarjeta")
                    except Exception as e:
                        self.card_error.emit(f"Error de lectura: {str(e)}")

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)
                self.card_read = False
                self.card_removed.emit()

class NFCMonitor(QObject):
    # Señales centralizadas
    uid_detected = Signal(str) 
    card_error = Signal(str)
    card_removed = Signal()
    
    def __init__(self):
        super().__init__()
        self.nfc_reader = NFCReader()
        self.cardmonitor = CardMonitor()
        self.cardmonitor.addObserver(self.nfc_reader)
        self.nfc_reader.uid_detected.connect(self.uid_detected)
        self.nfc_reader.card_error.connect(self.card_error)
        self.nfc_reader.card_removed.connect(self.handle_card_removal)
        self.windows_to_close = []
        self.carousel_window = None
        self.error_dialog = None
        self.error_style = """
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
        self.file_cleanup = NFCFileCleanup(self, delay_seconds=5)
        print("Sistema de limpieza de archivos inicializado")
    
    def register_window(self, window):
        if window not in self.windows_to_close:
            self.windows_to_close.append(window)
            print(f"Ventana registrada. Total ventanas: {len(self.windows_to_close)}")
    
    def unregister_window(self, window):
        if window in self.windows_to_close:
            self.windows_to_close.remove(window)
            print(f"Ventana eliminada del registro. Total ventanas: {len(self.windows_to_close)}")
    
    def register_carousel(self, carousel_window):
        self.carousel_window = carousel_window
        self.register_window(carousel_window)
    
    def is_only_carousel_open(self):
        if self.carousel_window is None:
            return False
    
        if len(self.windows_to_close) == 1 and self.windows_to_close[0] == self.carousel_window:
            return True
        return False
    
    def handle_card_removal(self):
        print("Tarjeta retirada detectada - Cerrando ventanas registradas...")
        self.card_removed.emit()
        
        if not self.is_only_carousel_open():
            
            self.show_error_message("Se ha retirado la tarjeta\nSe estan limpiando los datos...")
        else:

            self.close_all_windows()
    
    def close_all_windows(self):
        
        for window in self.windows_to_close[:]:  
            if hasattr(window, 'close'):
                print(f"Cerrando ventana: {window}")
                window.close()
            else:
                print(f"La ventana no tiene método close(): {window}")
        self.windows_to_close = []
    
    def show_error_message(self, message):

        if self.error_dialog is not None:
            self.error_dialog.close()
            self.error_dialog = None

        self.error_dialog = QMessageBox()
        self.error_dialog.setIcon(QMessageBox.NoIcon)
        self.error_dialog.setStyleSheet(self.error_style)
        
        formatted_message = message.replace("\n", "<br>")
        self.error_dialog.setText(formatted_message)
        self.error_dialog.setWindowTitle("Advertencia")

        self.error_dialog.setStandardButtons(QMessageBox.NoButton)
        
        self.error_dialog.setGeometry(350, 400, 300, 200)
        self.error_dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        QTimer.singleShot(5000, lambda: self.close_dialog_and_windows())

        self.error_dialog.show()
    
    def close_dialog_and_windows(self):

        if self.error_dialog:
            self.error_dialog.close()
            self.error_dialog = None

        self.close_all_windows()

class NFCMonitorSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():

        if NFCMonitorSingleton._instance is None:
            print("Creando instancia del monitor NFC")
            NFCMonitorSingleton._instance = NFCMonitor()
        return NFCMonitorSingleton._instance