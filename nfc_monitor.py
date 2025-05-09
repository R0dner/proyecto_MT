from PySide2.QtCore import QObject, Signal
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt
import time

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
                        time.sleep(0.5)  # Dar tiempo para establecer la conexión
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
                # Emitir señal cuando se quita la tarjeta
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
        
        # Conectar señales del lector a las señales del monitor
        self.nfc_reader.uid_detected.connect(self.uid_detected)
        self.nfc_reader.card_error.connect(self.card_error)
        self.nfc_reader.card_removed.connect(self.handle_card_removal)
        
        # Lista de ventanas registradas para cerrar
        self.windows_to_close = []
        
        # Estilo para mensajes de error
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
        """
    
    def register_window(self, window):
        """Registra una ventana para cerrarla cuando se retire la tarjeta"""
        if window not in self.windows_to_close:
            self.windows_to_close.append(window)
            print(f"Ventana registrada. Total ventanas: {len(self.windows_to_close)}")
    
    def unregister_window(self, window):
        """Elimina una ventana del registro"""
        if window in self.windows_to_close:
            self.windows_to_close.remove(window)
            print(f"Ventana eliminada del registro. Total ventanas: {len(self.windows_to_close)}")
    
    def handle_card_removal(self):
        """Manejador centralizado para cuando se retira una tarjeta"""
        print("Tarjeta retirada detectada - Cerrando ventanas registradas...")
        
        # Mostrar mensaje de que se retiró la tarjeta
        self.show_error_message("Se ha retirado la tarjeta\nCerrando ventanas...")
        
        # Emitir señal para otros componentes que puedan estar escuchando
        self.card_removed.emit()
        
        # Cerrar todas las ventanas registradas
        self.close_all_windows()
    
    def close_all_windows(self):
        """Cierra todas las ventanas registradas"""
        for window in self.windows_to_close[:]:  # Usar una copia para evitar problemas de iteración
            if hasattr(window, 'close'):
                print(f"Cerrando ventana: {window}")
                window.close()
            else:
                print(f"La ventana no tiene método close(): {window}")
        self.windows_to_close = []
    
    def show_error_message(self, message):
        """Muestra un mensaje de error estilizado"""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.NoIcon)
        error_dialog.setStyleSheet(self.error_style)
        
        formatted_message = message.replace("\n", "<br>")
        error_dialog.setText(formatted_message)
        error_dialog.setWindowTitle("Advertencia")
        error_dialog.setStandardButtons(QMessageBox.Ok)
        
        error_dialog.setGeometry(350, 400, 300, 200)
        error_dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        error_dialog.exec_()

# Singleton para NFCMonitor
class NFCMonitorSingleton:
    _instance = None
    
    @staticmethod
    def get_instance():
        """Obtiene o crea una instancia única del monitor NFC"""
        if NFCMonitorSingleton._instance is None:
            print("Creando instancia del monitor NFC")
            NFCMonitorSingleton._instance = NFCMonitor()
        return NFCMonitorSingleton._instance