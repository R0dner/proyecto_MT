from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QFont, QCursor
from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint

class VentanaDespedida(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.offset = QPoint()
        
        self.gradient_animation = QTimer(self)
        self.gradient_animation.timeout.connect(self.updateGradient)
        self.gradient_animation.start(100)
        self.gradient_angle = 0
    
    def updateGradient(self):
        self.gradient_angle = (self.gradient_angle + 5) % 360
        style = f"""
            color: #2C3E50;
            background: qconicalgradient(cx:0.5, cy:0.5, angle:{self.gradient_angle},
                stop:0 #F5F7FA,
                stop:0.33 #E6E9ED,
                stop:0.66 #D7DDE4,
                stop:1 #F5F7FA);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        """
        self.mensaje.setStyleSheet(style)
    
    def initUI(self):
        self.setWindowTitle('¡Hasta pronto!')
        self.setGeometry(450, 400, 450, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.mensaje = QLabel("¡Gracias por usar \n nuestro servicio!")
        self.mensaje.setAlignment(Qt.AlignCenter)
        
        font = QFont("Segoe UI", 24, QFont.DemiBold)
        self.mensaje.setFont(font)
        
        self.mensaje.setStyleSheet("""
            color: #2C3E50;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #F5F7FA,
                stop:0.5 #E6E9ED,
                stop:1 #D7DDE4);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        """)
        
        main_layout.addWidget(self.mensaje)
        self.setLayout(main_layout)
        
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
    
    def closeEvent(self, event):
        self.gradient_animation.stop()
        super().closeEvent(event)