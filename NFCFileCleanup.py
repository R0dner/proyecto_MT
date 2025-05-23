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
        self.cleanup_timer.setSingleShot(True)  # Solo ejecutar una vez
        self.cleanup_timer.timeout.connect(self.cleanup_files)
        
        if self.nfc_monitor:
            self.connect_to_monitor()
    
    def connect_to_monitor(self):
        """Conecta las señales del monitor NFC para limpiar archivos"""
        try:
            self.nfc_monitor.card_removed.connect(self.schedule_cleanup)
            print(f"NFCFileCleanup conectado - Limpieza programada para {self.delay_seconds//1000} segundos")
        except Exception as e:
            print(f"Error al conectar NFCFileCleanup: {e}")
    
    @Slot()
    def schedule_cleanup(self):
        """Programa la limpieza de archivos después del tiempo definido"""
        print(f"Tarjeta retirada - Limpieza programada en {self.delay_seconds//1000} segundos...")
        self.cleanup_timer.start(self.delay_seconds)
    
    def cancel_cleanup(self):
        """Cancela la limpieza programada (útil si se vuelve a insertar la tarjeta)"""
        if self.cleanup_timer.isActive():
            self.cleanup_timer.stop()
            print("Limpieza cancelada")
    
    @Slot()
    def cleanup_files(self):
        """Limpia los archivos JSON cuando se retira la tarjeta"""
        print("Ejecutando limpieza de archivos JSON...")
        
        for filename in self.files_to_clean:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Archivo eliminado: {filename}")
            except Exception as e:
                print(f"Error al eliminar {filename}: {e}")
    
    def set_delay(self, seconds):
        """Cambia el tiempo de retraso para la limpieza"""
        self.delay_seconds = seconds * 1000
        print(f"Tiempo de limpieza cambiado a {seconds} segundos")
    
    def manual_cleanup(self):
        """Permite ejecutar la limpieza manualmente"""
        self.cleanup_files()