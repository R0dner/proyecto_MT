from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsBlurEffect,
                               QPushButton, QLabel, QScrollArea, QWidget, QGridLayout)
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtCore import QByteArray
import sys
import threading
import time
import os
from PantallaRecarga import Ui_Recarga # type: ignore
from PantallaMovimientos import Ui_Movimientos #type: ignore
from PySide2.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide2.QtGui import QFont, QColor
from smartcard.CardMonitoring import CardMonitor
from NFCHandler import Lectura
from despedida import VentanaDespedida
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PySide2.QtGui import QPainter, QPixmap
from nfc_monitor import NFCMonitorSingleton
from estilos_generales import (ENCABEZADO_COLOR_PRIMARIO,BOTONES_ACCIONES,BOTONES_ACCIONES_HOVER,
                               BOTONES_ACCIONES_PRESSED,GRADIENTE_FINAL,GRADIENTE_INICIO)

class CustomMessageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.content_frame = QFrame(self)
        content_layout = QVBoxLayout(self.content_frame)

        message_label = QLabel("No puede realizar transacciones \n de recarga debido al estado \n de su tarjeta.")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("""
            color: #34495e;
            font-size: 20px;
            font-weight: bold;
            border: none;
        """)

        warning_icon = QLabel()
        warning_icon.setPixmap(self.render_svg(self.get_warning_svg(), QSize(52, 52)))
        warning_icon.setAlignment(Qt.AlignCenter)

        ok_button = QPushButton("Aceptar")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2574a9;
            }
        """)
        ok_button.clicked.connect(self.accept)

        content_layout.addWidget(message_label)
        content_layout.addWidget(warning_icon)
        content_layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            }
        """)

        layout.addWidget(self.content_frame)
        self.setFixedSize(400, 280)

    def get_warning_svg(self):
        return '''
        <svg viewBox="0 0 22 22" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(0 -1030.362)">
                <path style="fill:#ffc35a;fill-opacity:1;stroke:none;" d="m11 1032.362-10 18h20zm0 2 8 15H3z"/>
                <path style="fill:#373737;fill-opacity:.94117647;stroke:none;" d="M10 1046.362h2v2h-2z"/>
                <path style="fill:#373737;fill-opacity:.94117647;stroke:none;" d="M10 1045.362h2v-6h-2z"/>
            </g>
        </svg>
        '''

    def render_svg(self, svg_content, size):
        renderer = QSvgRenderer(svg_content.encode('utf-8'))
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

class CustomInfoDialog(QDialog):
    def __init__(self, mensaje, icono='info', parent=None, auto_close=False, close_time=3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.auto_close = auto_close
        self.close_time = close_time
        self.setup_ui(mensaje, icono)

    def setup_ui(self, mensaje, icono):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        icono_label = QLabel()
        icon_size = QSize(72, 72)
        
        if icono == 'error':
            svg_content = '''
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill="#e74c3c" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            '''
        else:  
            svg_content = '''
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill="#3498db" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            '''
        
        icono_label.setPixmap(self.render_svg(svg_content, icon_size))
        icono_label.setAlignment(Qt.AlignCenter)
        mensaje_label = QLabel(mensaje)
        mensaje_label.setAlignment(Qt.AlignCenter)
        mensaje_label.setWordWrap(True)
        mensaje_label.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 22px;
                font-weight: bold;
                border: none;
                padding: 0 10px;
            }
        """)
        
        close_button = QPushButton("Aceptar")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2574a9;
            }
        """)
        close_button.clicked.connect(self.close_with_animation)

        content_layout.addWidget(icono_label, 0, Qt.AlignCenter)
        content_layout.addWidget(mensaje_label, 0, Qt.AlignCenter)
        content_layout.addWidget(close_button, 0, Qt.AlignCenter)

        self.content_frame.setStyleSheet("""
            QFrame#contentFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            }
        """)

        layout.addWidget(self.content_frame)
        self.setFixedSize(450, 350)

    def render_svg(self, svg_content, size):
        renderer = QSvgRenderer(svg_content.encode('utf-8'))
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def showEvent(self, event):
        # Animación de entrada
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        if self.auto_close:
            QTimer.singleShot(self.close_time, self.close_with_animation)

    def close_with_animation(self):
        # Animación de salida
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()

class Ui_MainWindow3(QObject):
    
    def __init__(self):
        super().__init__()
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(0)
        self.nfc_monitor = NFCMonitorSingleton.get_instance()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
                    
        MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        MainWindow.resize(1280, 1024)
        self.MainWindow = MainWindow
        self.nfc_monitor.register_window(self.MainWindow)
        self.nfc_monitor.card_removed.connect(self.handle_card_removed)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setGraphicsEffect(self.blur_effect)
        
        self.fondoSegunda = QFrame(self.centralwidget)
        self.fondoSegunda.setObjectName(u"fondoSegunda")    
        self.fondoSegunda.setGeometry(QRect(0, 0, 1280, 1024))
        self.fondoSegunda.setStyleSheet(u"""
            QFrame#fondoSegunda {
                background-color: #E9EDF0;
            }
        """)
        self.fondoSegunda.setFrameShape(QFrame.StyledPanel)
        self.fondoSegunda.setFrameShadow(QFrame.Raised)
        
        self.encabezado = QFrame(self.fondoSegunda)
        self.encabezado.setObjectName(u"encabezado")
        self.encabezado.setGeometry(QRect(20, 20, 1240, 80))
        self.encabezado.setStyleSheet(f"""
            QFrame#encabezado {{
                background-color: {ENCABEZADO_COLOR_PRIMARIO};
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }}
        """)
        #66999B 124661 color sugerido
        self.encabezado.setFrameShape(QFrame.StyledPanel)
        self.encabezado.setFrameShadow(QFrame.Raised)
       
        self.titulo = QLabel(self.encabezado)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setGeometry(QRect(0, 0, 1240, 80))
        self.titulo.setStyleSheet(u"""
            QLabel#titulo {
                color: #ECF0F1; 
                font-family: 'Arial', sans-serif; 
                font-size: 35px;
                font-weight: bold; 
                letter-spacing: 1px; 
                qproperty-alignment: AlignCenter;
            }
        """)
                
        self.fondoTarjeta = QFrame(self.fondoSegunda)
        self.fondoTarjeta.setObjectName(u"fondoTarjeta")
        self.fondoTarjeta.setGeometry(QRect(40, 120, 1200, 400))
        self.fondoTarjeta.setStyleSheet(u"background-color: #E9EDF0;\n"
"border: 2px solid #AEB6BF;\n"
"border-radius: 10px;\n"
"border: 2px solid #AEB6BF;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoTarjeta.setLayout(QVBoxLayout())
        
        self.encabezadoBotones = QFrame(self.fondoSegunda)
        self.encabezadoBotones.setObjectName(u"encabezadoBotones")
        self.encabezadoBotones.setGeometry(QRect(20, 540, 1250, 70))
        self.encabezadoBotones.setStyleSheet(F"""
            QFrame#encabezadoBotones {{
                background-color: {ENCABEZADO_COLOR_PRIMARIO};
                border-radius: 30px;
            }}
        """)
        self.encabezadoBotones.setFrameShape(QFrame.StyledPanel)
        self.encabezadoBotones.setFrameShadow(QFrame.Raised)
        
        self.tituloBotones = QLabel(self.encabezadoBotones)
        self.tituloBotones.setObjectName(u"tituloBotones")
        self.tituloBotones.setGeometry(QRect(0, 0,1250, 70))
        self.tituloBotones.setStyleSheet(u"""
            QLabel#tituloBotones {
                color: #ECF0F1; 
                font-family: 'Arial', sans-serif; 
                font-size: 35px;
                font-weight: bold; 
                letter-spacing: 1px; 
                qproperty-alignment: AlignCenter;
            }
        """)
        
        self.fondoBotones = QFrame(self.fondoSegunda)
        self.fondoBotones.setObjectName(u"fondoBotones")
        self.fondoBotones.setGeometry(QRect(40, 630, 1200, 350))
        self.fondoBotones.setStyleSheet(u"background-color: #E9EDF0;\n"
"border: 2px solid #AEB6BF;\n"
"border-radius: 10px;\n"
"border: 2px solid #AEB6BF;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoBotones.setLayout(QVBoxLayout())
        
        self.Umovimientos = QPushButton(self.fondoBotones)
        self.Umovimientos.setObjectName(u"Umovimientos")
        self.Umovimientos.setGeometry(QRect(150, 70, 380, 80))
        self.Umovimientos.setStyleSheet(f"""
            QPushButton {{
                background-color: {BOTONES_ACCIONES};  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 23px;           
                font-weight: bold;        
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }}

            QPushButton:hover {{
                background-color: {BOTONES_ACCIONES_HOVER}; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }}

            QPushButton:pressed {{
                background-color: {BOTONES_ACCIONES_PRESSED};   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }}
        """)
        self.Umovimientos.clicked.connect(self.mostrar_ventana_movimientos)
        
        self.lector_nfc = Lectura()
        self.monitor_tarjeta = CardMonitor()
        self.monitor_tarjeta.addObserver(self.lector_nfc)
        
        self.hilo_nfc = threading.Thread(target=self.verificar_datos_tarjeta, daemon=True)
        self.hilo_nfc.start()
        
        self.RecargaCredito = QPushButton(self.fondoBotones)
        self.RecargaCredito.setObjectName(u"RecargaCredito")
        self.RecargaCredito.setGeometry(QRect(700, 70, 300, 80))
        self.RecargaCredito.setStyleSheet(f"""
            QPushButton {{
                background-color: {BOTONES_ACCIONES};  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 23px;           
                font-weight: bold;        
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23);
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }}

            QPushButton:hover {{
                background-color: {BOTONES_ACCIONES_HOVER}; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }}

            QPushButton:pressed {{
                background-color: {BOTONES_ACCIONES_PRESSED};   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }}
        """)
        self.RecargaCredito.clicked.connect(self.verificar_estado_tarjeta)
        
        self.salir = QPushButton(self.fondoBotones)
        self.salir.setObjectName(u"salir")
        self.salir.setGeometry(QRect(700, 200, 300, 80))
        self.salir.setLayoutDirection(Qt.LeftToRight)
        self.salir.setStyleSheet(f"""
            QPushButton {{
                background-color: {BOTONES_ACCIONES};  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 23px;           
                font-weight: bold;        
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }}

            QPushButton:hover {{
                background-color: {BOTONES_ACCIONES_HOVER}; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }}

            QPushButton:pressed {{
                background-color: {BOTONES_ACCIONES_PRESSED};   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }}
        """)
        self.MainWindow = MainWindow
        self.salir.clicked.connect(self.mostrar_ventana_despedida)  
        self.MainWindow = MainWindow

        self.salir.clicked.connect(self.mostrar_ventana_despedida) 
        
        
        self.actualizar = QPushButton(self.fondoBotones)
        self.actualizar.setObjectName(u"actualizar")
        self.actualizar.setGeometry(QRect(150, 200, 380, 80))
        self.actualizar.clicked.connect(self.refresh_window)
        self.actualizar.setLayoutDirection(Qt.LeftToRight)
        self.actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {BOTONES_ACCIONES};  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 23px;           
                font-weight: bold;        
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }}

            QPushButton:hover {{
                background-color: {BOTONES_ACCIONES_HOVER}; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }}

            QPushButton:pressed {{
                background-color: {BOTONES_ACCIONES_PRESSED};   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }}
        """)

        self.tarjeta = QWidget(self.fondoTarjeta)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setGeometry(QRect(665, 85, 470, 270))
        self.tarjeta.setStyleSheet(f"""
            QWidget#tarjeta {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                            stop: 0 {GRADIENTE_INICIO}, stop: 1 {GRADIENTE_FINAL});
                border-radius: 20px;
                border: 1px solid #2980B9; 
            }}
        """)       
        
        self.tarjetaInterior = QWidget(self.tarjeta)
        self.tarjetaInterior.setObjectName(u"borde")
        self.tarjetaInterior.setGeometry(QRect(30, 30, 410, 210))
        self.tarjetaInterior.setStyleSheet("""
            QWidget#borde {
                background-color: transparent;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 25px;
                line-height: 60px;
            }
        """)

        self.IconoLogo = QLabel(self.tarjetaInterior)
        self.IconoLogo.setObjectName(u"iconoLogo")
        self.IconoLogo.setGeometry(QRect(340, 18, 55, 55))
        size = 60
        svg_content = '''
<svg version="1.1" viewBox="0 0 1042 1043" width="1280" height="1280" xmlns="http://www.w3.org/2000/svg">
<path transform="translate(496,67)" d="m0 0h47l33 3 35 6 32 8 33 11 29 12 16 8 19 10 19 12 12 8 15 11 14 11 14 12 12 11 23 23 7 8 11 13 11 15v2l-19 13-6 4-3-1-10-13-11-13-11-12-23-23-11-9-3-1v2l11 9 16 15 11 11 7 8 13 15 12 16 11-7 14-10 5-2 11 15 3 6-13 10-19 13-7 5-5-5-12-17-10-13-11-13-9-10-12-13-13-12-15-13-20-15-21-14-15-9-29-15-27-11-30-10-24-6-28-5-27-3-22-1h-13l-34 2-28 4-29 6-27 8-27 10-24 11-28 15-27 18-17 13-13 11-12 11-23 23-9 11-10 12-13 18-8 12-4-2-19-13-18-13 7-11 10-14 10-13 11-13 7-8 9-10 22-22 8-7 13-11 20-15 17-12 27-16 23-12 25-11 27-10 27-8 31-7 26-4 18-2zm-17 3 3 32-34 5-27 6-28 8-9 4 2 3 21-7 32-8 30-5 17-2-1-16-2-20zm99 12-4 37 4 1 3-28v-6l28 5 32 8 33 11 5 1 1-3-25-9-27-8-27-6-19-3zm-131 2-29 6-28 8-23 8-17 7 1 6 12 28 3-1-3-9-9-22 9-3 31-11 34-9 20-4 2-1-1-3zm145 23-1 3 44 11 30 10 25 10 5-11 8-20v-2l-3-1-11 27v2l-34-13-29-9-32-7zm-324 39-2 2 12 16 7 10v2l-14 10-16 13-11 10-8 7-18 18-7 8v2l3 1 12-13 23-23 11-9 12-10 18-13v-3l-13-18-7-10zm505 14-8 11-10 16-2 5 3 1 10-16 8-12 8 6 13 10 15 13 7 7 8 7 7 7 7 8 8 9 3-1-2-4-14-15-22-22-11-9-9-8-17-13zm-518 10-11 9-14 12-7 7-8 7-7 7-7 8-11 12-9 11 5 5 17 13 4 3 4-1-5-5-19-14 2-4 12-14 14-15 15-15 8-7 13-11 6-5z" fill="#fff"/>
<path transform="translate(120,318)" d="m0 0 6 2 29 14 9 4-1 6-10 22-11 30-8 29-6 29-3 21-2 25v41l2 26 5 33 7 30 8 26 11 28 3 7v3l-27 13-3-1-11-26-9-25-8-29-3-13-3-1 10 37 10 30 12 28 1 4 28-13 5-2 10 19 15 26 13 19 10 13 9 11 12 14 26 26 11 9 13 11 18 13 19 12 21 12 27 13 26 10 25 8 30 7 26 4 23 3v45l-1 5-30-3-30-5-30-7-29-9-28-11-28-13-22-12-24-15-19-14-16-13-11-9-17-16-16-16-7-8-12-14-13-17-3-5 11-9 14-10 4-1 14 18 11 13 11 12 10 11 8 7 7 7 6 5h2l-1-3-8-7-12-11-13-13-7-8-12-14-15-20h-3l-18 13-10 7h-2l-10-15-7-11-12-21-14-28-11-27-11-33-9-36-6-37-2-18-1-19v-40l2-28 5-35 6-28 9-31 9-25 13-30zm-18 45-1 3 31 12-12 37-7 28-5 29v5h3l3-16 7-34 8-27 8-24-12-5-20-8zm2 28-7 25-6 28-4 28-2 24 30 3h7v-3l-15-2-18-1 4-35 5-28 8-32 1-6zm10 193-35 6 1 3 16-2 17-3 4 23 8 32 10 30 5 12h4l-11-30-8-28-6-27-3-16zm68 211v4l13 16 12 14 15 16 8 8 8 7 11 10 5 2 9-10 9-11 5-6-1-3h-2l-8 10-11 13-1 2-4-2-11-10-8-7-20-20-7-8-11-13-9-12zm167 104-14 33v2l3 1 13-30h4l21 9 33 11 28 7 11 2v-4l-34-8-26-8-28-11-9-4zm114 24-1 1-3 25v6l-28-5-34-9-26-9-7-3-4 1v2l27 10 26 8 31 7 12 2h6l4-35z" fill="#fff"/>
<path transform="translate(922,321)" d="m0 0h2l10 22 11 29 8 26 6 24 5 26 4 33 1 13v55l-3 32-5 30-6 27-9 30-10 27-13 29-2 2-29-17 1-5 11-25 11-31 10-37h-3l-3 15-10 33-8 21-11 25-1 5 21 12 10 6-2 6-12 22-12 19-12 17-14 18-12 14-11 12-27 27-11 9-13 11-12 9-4-1-11-18-6-9 1-3 12-9 16-13 12-11 10-9 9-9 14-16-2-2-9 11-27 27-11 9-9 8-19 14 2 5 11 18 6 9-2 4-15 10-15 9-18 10-24 12-27 11-30 10-28 7-27 5h-3l-5-24-1-11 7-2 26-5 30-8 31-11 3-2v-2l-26 10-31 9-29 6-15 2 2 8 5 28v3l-36 4-3-1-4-49 36-4 27-5 28-7 32-11 23-10 16-8 19-10 27-18 17-13 11-9 12-11 8-7 12-12 7-8 13-15 6-8 8 6 15 14 2 1-2 5-12 14-7 8-9 10-20 20-8 7-11 9v3l11-9 12-11 10-9 9-9 7-8 10-11 11-14 3-4-9-9-16-14h-2l2-4 20-30 13-23 13-27 9-23 9-27 7-28 6-36 2-22v-55l-4-36-6-31-8-29-10-28-11-25v-4l33-16zm9 50-28 10-5 2v3l9-2 23-8 3 11 8 28 6 27 5 33 3-1v-8l-5-30-7-30-8-26-3-9zm-12 47 6 32 4 36 1 36 1 1 37 1v-4l-34-1v-17l-2-30-5-35-4-19zm-3 172-1 3 9 2 23 3-6 28-7 25-8 24-7 17v4h3l12-31 9-30 7-30 1-10-32-5zm-223 298-2 1 1 5 12 25-6 2-20 9-24 9-25 8-19 5v3l9-1 31-9 27-10 24-11 7-4-2-6-12-26z" fill="#fff"/>
<path transform="translate(307,416)" d="m0 0h165l1 74 3 5 5 4 11 3 7 1h45l15-3 7-4 4-7 1-73h164l-5 6-10 5-10 2h-127v384l-11 9h-1l-1-315-7 4h-2v320l-10 9h-2v-327l-2 1h-9v337l-11 9h-1v-345h-10v345l-8-6-4-4v-336h-9l-1 326-5-2-8-7-1-320-8-4v315l-4-2-9-8v-383h-127l-12-3-10-6z" fill="#fff"/>
<path transform="translate(277,323)" d="m0 0h489l7 3 5 8 1 3v9l5 1 8 7 4 9 1 14-1 5h-550v-17l3-9 6-7 6-3h2l1-11 3-6 5-5zm12 6-7 4-2 2-7 2-3 4v7l4 8 6 5 5 5 1 4h470l3-6 8-6 4-6 1-3v-9l-4-4-7-2-5-4-2-1h-10l-6 4-2 2-430 1-2-4-6-3zm488 23-6 8-10 6-2 4h25l-2-5-8-4h7l7 2-2-6-5-4zm-513 0-6 4-4 5 1 3 7-3h7l-8 3-3 6h25l-1-4-9-5-8-9z" fill="#fff"/>
<path transform="translate(289,393)" d="m0 0h209l8 4 6 7 3 10v22l-2 23h16l-2-28v-14l2-10 5-8 8-5 3-1h209l-4 6-6 7h-195l-7 2-3 6v22l1 34h-37v-57l-2-5-8-2h-195l-9-11z" fill="#fff"/>
<path transform="translate(289,331)" d="m0 0h9l6 4 3 5v7h428v-6l4-6 3-3 3-1h8l5 3 4 5 1 2v8l-4 6-3 3-3 1h-464l-6-4-3-4-1-8 3-7 5-4zm2 7-4 3v8l4 3h5l4-4v-6l-4-4zm456 0-5 5 1 6 4 3 6-1 3-4-1-6-4-3z" fill="#fff"/>
<path transform="translate(316,301)" d="m0 0h410l7 8 2 4h-428l6-8z" fill="#fff"/>
<path transform="translate(545,426)" d="m0 0h19l5 5v27l-5 5h-18l-5-4-1-3v-23l3-5zm4 6-2 2v21l3 2h10l3-3v-20l-2-2z" fill="#fff"/>
<path transform="translate(478,426)" d="m0 0h19l4 4 1 2v25l-4 5-2 1h-18l-5-6v-26zm4 6-3 3v18l4 4h9l4-4v-17l-3-4z" fill="#fff"/>
<path transform="translate(504,479)" d="m0 0h34v10h-34z" fill="#fff"/>
<path transform="translate(837,769)" d="m0 0" fill="#fff"/>
</svg>

        '''.format(size, size)
        svg_renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QColor("#2C3E50"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_renderer.render(painter, QRectF(0, 0, size, size))
        painter.end()

        self.IconoLogo.setPixmap(pixmap)
        self.IconoLogo.setScaledContents(True)
        self.IconoLogo.setAutoFillBackground(False)
        self.IconoLogo.setAttribute(Qt.WA_TranslucentBackground)
        
        self.tituloSaldo = QLabel(self.tarjetaInterior)
        self.tituloSaldo.setObjectName(u"tituloSaldo")
        self.tituloSaldo.setGeometry(QRect(20, 15, 200, 40))
        self.tituloSaldo.setStyleSheet(u"""
            QLabel#tituloSaldo {
                background: transparent;
                color: #ECF0F1; 
                border: none;
                font-family: 'Arial', sans-serif; 
                font-size: 22px;
                font-weight: bold; 
                letter-spacing: 1px; 
            }
        """)
        
        self.nombreUsuario = QLabel(self.fondoTarjeta)
        self.nombreUsuario.setObjectName(u"nombre")
        self.nombreUsuario.setGeometry(QRect(80, 10, 500, 40))
        self.nombreUsuario.setStyleSheet(u"""
            QLabel#nombre {
                background-color: transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
        """)

        self.editNombreUsuario = QLabel(self.fondoTarjeta)
        self.editNombreUsuario.setObjectName(u"nombreUsuario")
        self.editNombreUsuario.setGeometry(QRect(80, 55, 500, 40))
        self.editNombreUsuario.setStyleSheet(u"""
            QLabel#nombreUsuario {
                background-color: #FFFFFF;
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                padding: 4px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)
        
        self.Ci = QLabel(self.fondoTarjeta)
        self.Ci.setObjectName(u"CI")
        self.Ci.setGeometry(QRect(80, 100, 500, 40))
        self.Ci.setStyleSheet(u"""
            QLabel#CI {
                background-color: transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
        """)
        
        self.CiEdit = QLabel(self.fondoTarjeta)
        self.CiEdit.setObjectName(u"CIEdit")
        self.CiEdit.setGeometry(QRect(80, 145, 500, 40))
        self.CiEdit.setStyleSheet(u"""
            QLabel#CIEdit {
                background-color: #FFFFFF;
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                padding: 4px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)

        self.numeroTarjeta = QLabel(self.fondoTarjeta)
        self.numeroTarjeta.setObjectName(u"numeroTarjeta")
        self.numeroTarjeta.setGeometry(QRect(80, 190, 500, 40))
        self.numeroTarjeta.setStyleSheet(u"""
            QLabel#numeroTarjeta {
                background-color: transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
        """)

        self.numeroTarjetaEdit = QLabel(self.fondoTarjeta)
        self.numeroTarjetaEdit.setObjectName(u"numeroTarjetaEdit")
        self.numeroTarjetaEdit.setGeometry(QRect(80, 235, 500, 40))
        self.numeroTarjetaEdit.setStyleSheet(u"""
            QLabel#numeroTarjetaEdit {
                background-color: #FFFFFF;
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)

        self.estado = QLabel(self.fondoTarjeta)
        self.estado.setObjectName(u"estadoTarjeta")
        self.estado.setGeometry(QRect(80, 280, 500, 40))
        self.estado.setStyleSheet(u"""
            QLabel#estadoTarjeta {
                background-color: transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
        """)
        
        self.estadoEdit = QLabel(self.fondoTarjeta)
        self.estadoEdit.setObjectName(u"estadoTarjetaEdit")
        self.estadoEdit.setGeometry(QRect(80, 325, 500, 40))
        self.estadoEdit.setStyleSheet(u"""
            QLabel#estadoTarjetaEdit {
                background-color: #FFFFFF;
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                padding: 4px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)

        self.saldo = QLabel(self.tarjetaInterior)
        self.saldo.setObjectName(u"saldo")
        self.saldo.setGeometry(QRect(35, 60, 330, 120))
        self.saldo.setStyleSheet(u"""
            QLabel#saldo {
                background-color: transparent;
                color: #FFFFFF;
                font-size: 75px;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
        """)  
        self.saldo.setAlignment(Qt.AlignCenter)

        self.moneda = QLabel(self.tarjetaInterior)
        self.moneda.setObjectName(u"moneda")
        self.moneda.setGeometry(QRect(310, 135, 100, 50))
        self.moneda.setStyleSheet(u"""
            QLabel#moneda {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 44px;
                font-weight: bold;
            }
        """)   

        font = QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(87)
        self.moneda.setFont(font)

        self.posicion_original_saldo = self.saldo.geometry()
        
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.actualizar_posiciones)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def handle_card_removed(self):

        if hasattr(self, 'ventana_recarga') and self.ventana_recarga:
            self.ventana_recarga.close()
            
        if hasattr(self, 'ventana_movimientos') and self.ventana_movimientos:
            self.ventana_movimientos.close()

    def mostrar_ventana_despedida(self):
        self.ventana = VentanaDespedida()
        self.ventana.show()
        self.MainWindow.close()

    def ajustar_saldo(self, nuevo_texto):
        self.saldo.setText(nuevo_texto)
        self.update_timer.start(100) 

    def mostrar_ventana_despedida(self):
        self.ventana = VentanaDespedida()
        self.ventana.show()
        self.MainWindow.close()

    def actualizar_posiciones(self):
        texto_saldo = self.saldo.text()

        font = self.saldo.font()
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(texto_saldo)
        text_height = font_metrics.height()

        new_width = min(max(text_width + 20, 100), self.posicion_original_saldo.width())  
        new_height = min(text_height + 20, self.posicion_original_saldo.height())  
        new_x = self.posicion_original_saldo.x() + (self.posicion_original_saldo.width() - new_width) / 2
        new_y = self.posicion_original_saldo.y() + (self.posicion_original_saldo.height() - new_height) / 2

        self.saldo.setGeometry(QRect(int(new_x), int(new_y), int(new_width), int(new_height)))

    def mostrar_mensaje_temporal(self, mensaje, duracion_ms, icono='info'):

        msg = QLabel(self.centralwidget)
        msg.setObjectName("mensajeTemporal")
        msg.setAlignment(Qt.AlignCenter)

        if icono == 'error':
            color_fondo = "#e74c3c"  
            svg_icon = '''
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill="#fff" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            '''
        elif icono == 'info':
            color_fondo = "#3498db"  
            svg_icon = '''
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path fill="#fff" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            '''
        else:
            color_fondo = "#2C3E50"  
            svg_icon = ''
        
        # Configuracion del estilo
        msg.setStyleSheet(f"""
            QLabel#mensajeTemporal {{
                background-color: {color_fondo};
                color: white;
                padding: 20px;
                border-radius: 15px;
                font-family: 'Arial', sans-serif;
                font-size: 18px;
                font-weight: bold;
                min-width: 300px;
                border: none;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }}
        """)

        layout = QHBoxLayout(msg)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        if svg_icon:
            icon_label = QLabel()
            renderer = QSvgRenderer(QByteArray(svg_icon.encode('utf-8')))
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)

        text_label = QLabel(mensaje)
        text_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(text_label)

        msg.adjustSize()
        x_pos = (self.centralwidget.width() - msg.width()) // 2
        y_pos = (self.centralwidget.height() - msg.height()) // 2
        msg.move(x_pos, y_pos)

        msg.setWindowOpacity(0)
        msg.show()
        
        fade_in = QPropertyAnimation(msg, b"windowOpacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QEasingCurve.OutCubic)

        fade_out = QPropertyAnimation(msg, b"windowOpacity")
        fade_out.setDuration(300)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.InCubic)

        seq = QSequentialAnimationGroup()
        seq.addAnimation(fade_in)
        seq.addPause(duracion_ms)
        seq.addAnimation(fade_out)

        seq.finished.connect(msg.deleteLater)
        seq.start()

    def mostrar_ventana_movimientos(self):
        datos_tarjeta = self.lector_nfc.get_card_data()
        if not datos_tarjeta:
            self.blur_effect.setBlurRadius(10)
            
            dialog = CustomInfoDialog("No se detectó la tarjeta", icono='error', parent=self.centralwidget)
            dialog.finished.connect(lambda: self.blur_effect.setBlurRadius(0))
            dialog.exec_()
            return
            
        uid = datos_tarjeta.get('uid', '')
            
        movimientos = self.lector_nfc.get_movements_from_api(uid)
            
        if not movimientos or len(movimientos) == 0:

            self.blur_effect.setBlurRadius(10)
            
            dialog = CustomInfoDialog("No tiene movimientos recientes", icono='info', parent=self.centralwidget)
            dialog.finished.connect(lambda: self.blur_effect.setBlurRadius(0))
            dialog.exec_()
            return
        self.ventana_movimientos = QMainWindow()
        self.ui_movimientos = Ui_Movimientos()
        self.ui_movimientos.setupUi(self.ventana_movimientos)
        self.ventana_movimientos.show()
        self.actualizar_etiquetas_movimientos()
        self.nfc_monitor.register_window(self.ventana_movimientos)

    def mostrar_mensaje_temporal(self, mensaje, duracion_ms=3000, icono='info'):
        self.blur_effect.setBlurRadius(10)
        
        dialog = CustomInfoDialog(
            mensaje, 
            icono=icono, 
            parent=self.centralwidget,
            auto_close=True,
            close_time=duracion_ms
        )
        dialog.finished.connect(lambda: self.blur_effect.setBlurRadius(0))
        dialog.exec_()

    def verificar_datos_tarjeta(self):
        while True:
            if self.lector_nfc.is_data_ready():
                datos_tarjeta = self.lector_nfc.get_card_data()
                if datos_tarjeta:
                    QMetaObject.invokeMethod(self, "actualizar_etiquetas_movimientos", Qt.QueuedConnection)
            time.sleep(0.5)
            
    @Slot()
    def actualizar_etiquetas_movimientos(self):
        if hasattr(self, 'ui_movimientos'):
            datos_tarjeta = self.lector_nfc.get_card_data()
            if datos_tarjeta:
                nombre_completo = f"{datos_tarjeta.get('name', '')} {datos_tarjeta.get('last_name', '')}".strip()
                self.ui_movimientos.nombre.setText(nombre_completo)
                self.ui_movimientos.uid.setText(f"UID: {datos_tarjeta.get('uid', '')}")
                self.ui_movimientos.saldo.setText(datos_tarjeta.get('balance', ''))
                self.ui_movimientos.tipoTarjeta.setText(datos_tarjeta.get('profile_name', ''))
                self.ui_movimientos.estado.setText(datos_tarjeta.get('card_status', ''))    
   
   
    def closeEvent(self, event):
        if hasattr(self, 'nfc_monitor'):
            self.nfc_monitor.unregister_window(self.MainWindow)

        self.monitor_tarjeta.deleteObserver(self.lector_nfc)
        super().closeEvent(event)
        
    def verificar_estado_tarjeta(self):
        estado_tarjeta = self.estadoEdit.text().strip().upper()
        if estado_tarjeta == "ACTIVA":
            self.mostrar_ventana_recarga()
        else:
            self.mostrar_mensaje_error()
        
    def mostrar_ventana_recarga(self):
        self.ventana_recarga = QMainWindow()
        self.ui_recarga = Ui_Recarga()
        self.ui_recarga.setupUi(self.ventana_recarga)
        self.ui_recarga.recarga_completada.connect(self.refresh_window)
        self.ventana_recarga.show()
        self.actualizar_etiquetas_recarga()
        self.nfc_monitor.register_window(self.ventana_recarga)
        
    def mostrar_mensaje_error(self):
        self.blur_effect.setBlurRadius(5)

        dialog = CustomMessageDialog(self.centralwidget)
        dialog.finished.connect(self.remove_blur)
        dialog.exec_()

    def remove_blur(self):
        self.blur_effect.setBlurRadius(0)
        
    @Slot()
    def actualizar_etiquetas_recarga(self):
        if hasattr(self, 'ui_recarga'):
            datos_tarjeta = self.lector_nfc.get_card_data()
            if datos_tarjeta:
                self.ui_recarga.tipoTarjeta.setText(datos_tarjeta['profile_name'])
                self.ui_recarga.estado.setText(datos_tarjeta['card_status'])
                self.ui_recarga.uid.setText(f"UID: {datos_tarjeta['uid']}")
                nombre_completo = f"{datos_tarjeta.get('name', '')} {datos_tarjeta.get('last_name', '')}".strip()
                self.ui_recarga.nombre.setText(nombre_completo)
                self.ui_recarga.saldo.setText(f"{datos_tarjeta['balance']}")
                self.ui_recarga.NumeroCiEdit.setText(f"{datos_tarjeta['document']}")
                self.ui_recarga.RazonSocialEdit.setText(f"{datos_tarjeta['social_reason']}")
        
    def closeEvent(self, event):
        self.monitor_tarjeta.deleteObserver(self.lector_nfc)
        super().closeEvent(event)
        
    def refresh_window(self):
        try:
            self.actualizar.setEnabled(False)
            self.actualizar.setText("Actualizando...")

            if hasattr(self.lector_nfc, 'read_card'):
                # Limpiar datos existentes
                with self.lector_nfc.lock:
                    self.lector_nfc.card_data = None
                    self.lector_nfc.movements_data = None
                self.lector_nfc.data_ready.clear()              
                # Realizar nueva lectura
                self.lector_nfc.read_card()

                if self.lector_nfc.data_ready.wait(3):  
                    datos_tarjeta = self.lector_nfc.get_card_data()
                    
                    if datos_tarjeta:
                        self.actualizar_interfaz(datos_tarjeta)
                        
                        if hasattr(self, 'ui_movimientos'):
                            self.actualizar_etiquetas_movimientos()
                        if hasattr(self, 'ui_recarga'):
                            self.actualizar_etiquetas_recarga()
                    else:
                        self.mostrar_mensaje_temporal("No se pudo leer la tarjeta", 2000, 'error')
                else:
                    self.mostrar_mensaje_temporal("Tiempo de espera agotado", 2000, 'error')
            else:
                print("El lector NFC no tiene el método read_card")
                self.mostrar_mensaje_temporal("Error en el lector NFC", 2000, 'error')
                    
        except Exception as e:
            print(f"Error al actualizar: {e}")
            self.mostrar_mensaje_temporal("Error al actualizar", 2000, 'error')
        finally:
            self.actualizar.setEnabled(True)
            self.actualizar.setText("Actualizar Saldo")

    def actualizar_interfaz(self, datos_tarjeta):
        
        nombre_completo = f"{datos_tarjeta.get('name', '')} {datos_tarjeta.get('last_name', '')}".strip()
        self.editNombreUsuario.setText(nombre_completo)
        self.CiEdit.setText(f" {datos_tarjeta.get('document', '')}")
        self.numeroTarjetaEdit.setText(f"UID: {datos_tarjeta.get('uid', '')}")
        self.estadoEdit.setText(f" {datos_tarjeta.get('card_status', '')}")
        self.saldo.setText(datos_tarjeta.get('balance', '0'))
        self.ajustar_saldo(datos_tarjeta.get('balance', '0'))
        self.titulo.setText(datos_tarjeta.get('profile_name', ''))
        self.moneda.setText("Bs")

    def mostrar_mensaje_temporal(self, mensaje, duracion_ms):

        msg = QLabel(mensaje, self.centralwidget)
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        """)
        msg.setGeometry(QRect(400, 400, 400, 60))
        msg.show()
        QTimer.singleShot(duracion_ms, msg.deleteLater)

    def show_movi_message(self):
        self.movi_window = QMainWindow()
        self.ui2_recarga = Ui_Movimientos()
        self.ui2_recarga.setupUi(self.movi_window)
        self.movi_window.show()
        
    def show_recharge_message(self):
        self.recarga_window = QMainWindow()
        self.ui_recarga = Ui_Recarga()
        self.ui_recarga.setupUi(self.recarga_window)
        self.recarga_window.show()
    
    def update_uid(self, uid):
            
        self.numeroTarjetaEdit.setText(f"UID:   {uid}")
        
    def update_name(self, name, last_name):
        self.editNombreUsuario.setText(f" {name} {last_name}")
        
    def update_document(self, document):
        self.CiEdit.setText(f" {document}")
        
    def update_card_status(self, card_status):
        self.estadoEdit.setText(f" {card_status}")
    
    def update_nameTarjeta(self, status):
        self.estadoEdit.setText(f" {status}")    

    def update_balance(self, balance):
        self.saldo.setText(balance)
        
    def update_profile(self, profile_name):
        self.titulo.setText(profile_name)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.tituloSaldo.setText(QCoreApplication.translate("MainWindow", u" SALDO ACTUAL", None))
        self.tituloBotones.setText(QCoreApplication.translate("MainWindow", u" OPCIONES", None))
        self.Umovimientos.setText(QCoreApplication.translate("MainWindow", u"   Movimientos", None))
        self.RecargaCredito.setText(QCoreApplication.translate("MainWindow", u"  Recarga Credito", None))
        self.salir.setText(QCoreApplication.translate("MainWindow", u"  Salir", None))
        self.actualizar.setText(QCoreApplication.translate("MainWindow", u"  Actualizar Saldo", None))
        self.nombreUsuario.setText(QCoreApplication.translate("MainWindow", u"Nombre Usuario", None))
        self.editNombreUsuario.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.Ci.setText(QCoreApplication.translate("MainWindow", u" CI  ", None))
        self.CiEdit.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.numeroTarjeta.setText(QCoreApplication.translate("MainWindow", u"Numero de Tarjeta     ", None))
        self.numeroTarjetaEdit.setText(QCoreApplication.translate("MainWindow", u"  ", None))
        self.estado.setText(QCoreApplication.translate("MainWindow", u" Estado de la Tarjeta   ", None))
        self.estadoEdit.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.moneda.setText(QCoreApplication.translate("MainWindow", u"  Bs", None))
        self.saldo.setText(QCoreApplication.translate("MainWindow", u" ", None))
        
        umovimientos_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-table-properties">
            <path d="M15 3v18"/>
            <rect width="18" height="18" x="3" y="3" rx="2"/>
            <path d="M21 9H3"/><path d="M21 15H3"/>
        </svg>
        '''

        umovimientos_icon_color = "#FFFFFF"  
        umovimientos_svg_content = umovimientos_svg_template.format(color=umovimientos_icon_color)

        umovimientos_svg_renderer = QSvgRenderer(QByteArray(umovimientos_svg_content.encode()))
        umovimientos_pixmap = QPixmap(40, 40)
        umovimientos_pixmap.fill(Qt.transparent)
        umovimientos_painter = QPainter(umovimientos_pixmap)
        umovimientos_svg_renderer.render(umovimientos_painter)
        umovimientos_painter.end()

        umovimientos_icon = QIcon(umovimientos_pixmap)
        self.Umovimientos.setIcon(umovimientos_icon)
        self.Umovimientos.setIconSize(QSize(40, 40))
        
        recarga_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wallet">
            <path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/>
            <path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>
        </svg>
        '''

        recarga_icon_color = "#FFFFFF"  
        recarga_svg_content = recarga_svg_template.format(color=recarga_icon_color)

        recarga_svg_renderer = QSvgRenderer(QByteArray(recarga_svg_content.encode()))
        recarga_pixmap = QPixmap(40, 40)
        recarga_pixmap.fill(Qt.transparent)
        recarga_painter = QPainter(recarga_pixmap)
        recarga_svg_renderer.render(recarga_painter)
        recarga_painter.end()

        recarga_icon = QIcon(recarga_pixmap)
        self.RecargaCredito.setIcon(recarga_icon)
        self.RecargaCredito.setIconSize(QSize(40, 40))
        
        salir_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" x2="9" y1="12" y2="12"/>
        </svg>
        '''
        salir_icon_color = "#FFFFFF" 
        salir_svg_content = salir_svg_template.format(color=salir_icon_color)

        salir_svg_renderer = QSvgRenderer(QByteArray(salir_svg_content.encode()))
        salir_pixmap = QPixmap(40, 40)
        salir_pixmap.fill(Qt.transparent)
        salir_painter = QPainter(salir_pixmap)
        salir_svg_renderer.render(salir_painter)
        salir_painter.end()

        salir_icon = QIcon(salir_pixmap)
        self.salir.setIcon(salir_icon)
        self.salir.setIconSize(QSize(40, 40))
        
        svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-refresh-cw">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
            <path d="M21 3v5h-5"/>
            <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
            <path d="M8 16H3v5"/>
        </svg>
        '''
        icon_color = "#FFFFFF" 
        svg_content = svg_template.format(color=icon_color)

        svg_renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        refresh_icon = QIcon(pixmap)
        self.actualizar.setIcon(refresh_icon)
        self.actualizar.setIconSize(QSize(40, 40))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    screen = app.primaryScreen()
    screen_geometry = screen.geometry()
    print(f"Resolución de pantalla: {screen_geometry.width()}x{screen_geometry.height()}")
    
    MainWindow = QMainWindow()
    ui = Ui_MainWindow3()
    ui.setupUi(MainWindow)

    MainWindow.show()
    
    window_size = MainWindow.size()
    MainWindow.move(
        (screen_geometry.width() - window_size.width()) // 2,
        (screen_geometry.height() - window_size.height()) // 2
    )
    
    sys.exit(app.exec_())