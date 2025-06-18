import os
from PySide2.QtCore import QObject, Slot, QTimer

class NFCFileCleanup(QObject):
    def __init__(self, nfc_monitor=None, delay_seconds=5):
        super().__init__()
        self.nfc_monitor = nfc_monitor
        self.delay_seconds = delay_seconds * 1000  
        self.files_to_clean = [
            "ultima_recarga.json",
            "ultima_respuesta_api.json"
        ]
        
        # Timer para el retraso
        self.cleanup_timer = QTimer()
        self.cleanup_timer.setSingleShot(True) 
        self.cleanup_timer.timeout.connect(self.cleanup_files)
        
        if self.nfc_monitor:
            self.connect_to_monitor()
    
    def connect_to_monitor(self):
        try:
            self.nfc_monitor.card_removed.connect(self.schedule_cleanup)
            print(f"NFCFileCleanup conectado - Limpieza programada para {self.delay_seconds//1000} segundos")
        except Exception as e:
            print(f"Error al conectar NFCFileCleanup: {e}")
    
    @Slot()
    def schedule_cleanup(self):
        print(f"Tarjeta retirada - Limpieza programada en {self.delay_seconds//1000} segundos...")
        self.cleanup_timer.start(self.delay_seconds)
    
    def cancel_cleanup(self):
        if self.cleanup_timer.isActive():
            self.cleanup_timer.stop()
            print("Limpieza cancelada")
    
    @Slot()
    def cleanup_files(self):
        print("Ejecutando limpieza de archivos JSON...")
        
        for filename in self.files_to_clean:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Archivo eliminado: {filename}")
            except Exception as e:
                print(f"Error al eliminar {filename}: {e}")
    
    def set_delay(self, seconds):
        self.delay_seconds = seconds * 1000
        print(f"Tiempo de limpieza cambiado a {seconds} segundos")
    
    def manual_cleanup(self):
        self.cleanup_files()