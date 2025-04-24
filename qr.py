import sys
import qrcode
import tempfile
from PySide2.QtWidgets import (QDialog, QLabel, QPushButton, QMessageBox)
from PySide2.QtGui import QPixmap, QFont, QMouseEvent
from PySide2.QtCore import Qt, QTimer, QPoint

class QRDialog(QDialog):
    def __init__(self, payment_data, parent=None, segunda3=None):
        super().__init__(parent)
        self.segunda3 = segunda3
        self.parent_widget = parent
        self.setWindowTitle("Solicitud de Recarga")
        self.setFixedSize(500, 650)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self._drag_position = None
        
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F4F8;
                border-radius: 15px;
            }
        """)

        self.header = QLabel(self)
        self.header.setText("Escanea para Recargar")
        self.header.setGeometry(0, 0, 500, 50)
        self.header.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            font-size: 24px; 
            font-weight: bold; 
            qproperty-alignment: AlignCenter;
        """)
        self.header.mousePressEvent = self.mousePressEvent
        self.header.mouseMoveEvent = self.mouseMoveEvent

        qr_label = QLabel(self)
        qr_pixmap = QPixmap(self.generate_qr_data(payment_data))
        qr_label.setPixmap(qr_pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        qr_label.setAlignment(Qt.AlignCenter)
        qr_label.setGeometry(75, 100, 350, 350)

        monto_label = QLabel(f"Monto: Bs. {payment_data}", self)
        monto_label.setGeometry(0, 470, 500, 50)
        monto_label.setStyleSheet("""
            font-size: 20px; 
            color: #34495E; 
            qproperty-alignment: AlignCenter;
        """)

        self.contador_label = QLabel(self)
        self.contador_label.setGeometry(0, 520, 500, 50)
        self.contador_label.setStyleSheet("""
            font-size: 18px; 
            color: #7F8C8D; 
            qproperty-alignment: AlignCenter;
        """)

        self.tiempo_restante = 20
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_contador)
        self.timer.start(1000)

        Cancelar = QPushButton("Cancelar", self)
        Cancelar.setFixedSize(200, 50)
        Cancelar.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        Cancelar.setGeometry(150, 570, 200, 50)
        Cancelar.clicked.connect(self.volver_segunda3)
    
    def generate_qr_data(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#2C3E50", back_color="white")
        temp_qr = tempfile.mktemp('.png')
        img.save(temp_qr)
        
        return temp_qr
    
    def actualizar_contador(self):
        self.tiempo_restante -= 1
        self.contador_label.setText(f"La ventana se cerrará en {self.tiempo_restante} segundos")
        
        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()
    
    def volver_segunda3(self):
        # Stop the timer
        self.timer.stop()
        
        # Close the dialog (which will trigger the finished signal)
        self.close()

def open_qr_payment(monto, segunda3=None):
    qr_dialog = QRDialog(monto, segunda3=segunda3)
    qr_dialog.setGeometry(380, 200, 500, 600)  
    return qr_dialog.exec_()