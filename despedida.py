from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QFont, QCursor
from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint

class VentanaDespedida(QWidget):
    def __init__(self):  
        super().__init__()
        self.initUI()
        self.dragging = False
        self.offset = QPoint()

    def moveToCenter(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):
        self.setWindowTitle('¡Hasta pronto!')
        
        self.setGeometry(450, 400, 450, 250)  
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.mensaje = QLabel("¡Gracias por usar\nnuestro servicio!")
        self.mensaje.setAlignment(Qt.AlignCenter)

        font = QFont("Segoe UI", 25, QFont.Bold)
        self.mensaje.setFont(font)
        self.mensaje.setStyleSheet("""
            color: #ffffff;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(75, 108, 183, 200),
                                            stop:1 rgba(24, 40, 72, 200));
            border-radius: 15px;
            padding: 20px;
        """)
        layout.addWidget(self.mensaje)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)

        QTimer.singleShot(3000, self.iniciarCierre)
        self.animarAparicion()

    def animarAparicion(self):
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()

    def iniciarCierre(self):
        self.anim_cierre = QPropertyAnimation(self, b"windowOpacity")
        self.anim_cierre.setDuration(1000)
        self.anim_cierre.setStartValue(1)
        self.anim_cierre.setEndValue(0)
        self.anim_cierre.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim_cierre.finished.connect(self.close)
        self.anim_cierre.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
