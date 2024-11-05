from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from iframe import Iframe
from PySide2.QtGui import QPixmap
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtGui import QPainter, QPixmap, QColor, QPen
from PySide2.QtCore import QByteArray, Qt, QRectF
from PySide2.QtWidgets import QGraphicsBlurEffect
from PySide2.QtCore import QPropertyAnimation
import os
import re

class Ui_Recarga(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 1024)
        MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.fondoRecarga = QFrame(self.centralwidget)
        self.fondoRecarga.setObjectName(u"fondoRecarga")
        self.fondoRecarga.setGeometry(QRect(-15.4, -13.09, 12780, 1024))        
        self.fondoRecarga.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"                            stop:0 #E0E0E0, stop:1 #F5F5F5);")
        self.fondoRecarga.setFrameShape(QFrame.StyledPanel)
        self.fondoRecarga.setFrameShadow(QFrame.Raised)
       
        self.encabezado = QFrame(self.fondoRecarga)
        self.encabezado.setObjectName(u"encabezado")
        self.encabezado.setGeometry(QRect(20, 20, 1240, 65))
        self.encabezado.setStyleSheet(u"""
            QFrame#encabezado {
                background-color: #2C3E50;
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }
        """)
        self.encabezado.setFrameShape(QFrame.StyledPanel)
        self.encabezado.setFrameShadow(QFrame.Raised)
       
        self.tituloPrincipal = QLabel(self.encabezado)
        self.tituloPrincipal.setObjectName(u"tituloPrincipal")
        self.tituloPrincipal.setGeometry(QRect(420, 0, 505.4, 70.59)) 
        self.tituloPrincipal.setStyleSheet(u"color: #ECF0F1;\n"
"font-size: 20pt;\n"
"font-weight: bold;\n"
"background: none;")

        self.fondoPasos = QFrame(self.fondoRecarga)
        self.fondoPasos.setObjectName(u"fondoPasos")
        self.fondoPasos.setGeometry(QRect(70, 110, 530, 200))       
        self.fondoPasos.setStyleSheet(u"background-color: #ECEFF1;\n"
"border: 1px solid #CFD8DC;\n"
"border-radius: 10px;\n"
"border: 1px solid #CFD8DC;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoPasos.setFrameShape(QFrame.StyledPanel)
        self.fondoPasos.setFrameShadow(QFrame.Raised)

        self.encabezadoPasos = QFrame(self.fondoPasos)
        self.encabezadoPasos.setObjectName(u"encabezadoPasos")
        self.encabezadoPasos.setGeometry(QRect(0, 0, 530, 35))
        self.encabezadoPasos.setStyleSheet(u"""
            QFrame#encabezadoPasos {
                background-color: #2C3E50;
                border-radius: 30px;
            }
        """)
        self.encabezadoPasos.setFrameShape(QFrame.StyledPanel)
        self.encabezadoPasos.setFrameShadow(QFrame.Raised)
        
        self.tituloPasos = QLabel(self.encabezadoPasos)
        self.tituloPasos.setObjectName(u"titulo")
        self.tituloPasos.setGeometry(QRect(0, 0, 530, 35))
        self.tituloPasos.setStyleSheet(u"""
            QLabel#titulo {
        background-color: transparent;
        border: none;
        color: #ECF0F1;
        font-size: 19px;
        font-weight: bold;
        qproperty-alignment: AlignCenter;
            }
        """)  
        
        self.paso1 = QLabel(self.fondoPasos)
        self.paso1.setObjectName(u"paso1")
        self.paso1.setGeometry(QRect(60, 45, 43, 35))
        self.paso1.setStyleSheet(u"""
            QLabel#paso1 {
                background-color: #2C3E50;
                color: #FFFFFF;
                font-size: 21px;
                font-weight: bold;
                padding: 8px;
                border-radius: 17.5px;
                border: 1px solid #BDC3C7;
                min-height: 17.5px;
            }
        """)
        
        self.paso1Text = QLabel(self.fondoPasos)
        self.paso1Text.setObjectName(u"paso1Text")
        self.paso1Text.setGeometry(QRect(120, 45, 400, 35))
        self.paso1Text.setStyleSheet(u"""
            QLabel#paso1Text {
                background-color: Transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
        """)
        
        self.paso2 = QLabel(self.fondoPasos)
        self.paso2.setObjectName(u"paso2")
        self.paso2.setGeometry(QRect(60, 95, 43, 35))
        self.paso2.setStyleSheet(u"""
            QLabel#paso2 {
                background-color: #2C3E50;
                color: #FFFFFF;
                font-size: 21px;
                font-weight: bold;
                padding: 8px;
                border-radius: 17.5px;
                border: 1px solid #BDC3C7;
                min-height: 17.5px;
            }
        """)
        
        self.paso2Text = QLabel(self.fondoPasos)
        self.paso2Text.setObjectName(u"paso1Text")
        self.paso2Text.setGeometry(QRect(120, 95, 400, 35))
        self.paso2Text.setStyleSheet(u"""
            QLabel#paso1Text {
                background-color: Transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
        """)
        
        self.paso3 = QLabel(self.fondoPasos)
        self.paso3.setObjectName(u"paso3")
        self.paso3.setGeometry(QRect(60, 145, 43, 35))
        self.paso3.setStyleSheet(u"""
            QLabel#paso3 {
                background-color: #2C3E50;
                color: #FFFFFF;
                font-size: 21px;
                font-weight: bold;
                padding: 8px;
                border-radius: 17.5px;
                border: 1px solid #BDC3C7;
                min-height: 17.5px;
            }
        """)
        
        self.paso3Text = QLabel(self.fondoPasos)
        self.paso3Text.setObjectName(u"paso1Text")
        self.paso3Text.setGeometry(QRect(120, 145, 400, 35))
        self.paso3Text.setStyleSheet(u"""
            QLabel#paso1Text {
                background-color: Transparent;
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
        """)

        self.tarjeta = QWidget(self.fondoRecarga)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setGeometry(QRect(640, 110, 550, 200))
        self.tarjeta.setStyleSheet("""
    QWidget#tarjeta {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 #2C3E50, stop:1 #34495e);
        border-radius: 15px;
        color: white;
    }
""")
        
        self.IconoLogo = QLabel(self.tarjeta)
        self.IconoLogo.setObjectName(u"iconoLogo")
        self.IconoLogo.setGeometry(QRect(470, 125, 60, 60))
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
        
        self.tipoTarjeta = QLabel(self.tarjeta)
        self.tipoTarjeta.setObjectName(u"tipoTarjeta")
        self.tipoTarjeta.setGeometry(QRect(30, 10, 280, 40))
        self.tipoTarjeta.setStyleSheet(u"""
            QLabel#tipoTarjeta {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: bold;
            }
        """)         
        
        self.estado = QLabel(self.tarjeta)
        self.estado.setObjectName(u"estadoTarjeta")
        self.estado.setGeometry(QRect(440, 10, 100, 40))
        self.estado.setStyleSheet(u"""
            QLabel#estadoTarjeta {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: bold;
            }
        """) 
        
        self.uid = QLabel(self.tarjeta)
        self.uid.setObjectName(u"uid")
        self.uid.setGeometry(QRect(30, 115, 350, 40))
        self.uid.setStyleSheet(u"""
        QLabel#uid {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 18px;
        font-weight: bold;
        }
        """)
       
        self.nombre = QLabel(self.tarjeta)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setGeometry(QRect(30, 147, 350, 40))
        self.nombre.setStyleSheet(u"""
            QLabel#nombre {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 18px;
        font-weight: bold;
            }
        """)
        
        self.saldo = QLabel(self.tarjeta)
        self.saldo.setObjectName(u"saldo")
        self.saldo.setGeometry(QRect(200, 60, 300, 50))
        self.saldo.setStyleSheet(u"""
            QLabel#saldo {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 49px;
        font-weight: bold;
            }
        """)
        
        self.monedaSaldo = QLabel(self.tarjeta)
        self.monedaSaldo.setObjectName(u"moneda")
        self.monedaSaldo.setGeometry(QRect(335, 85, 170, 50))
        self.monedaSaldo.setStyleSheet(u"""
            QLabel#moneda {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 27px;
        font-weight: bold;
            }
        """)
        
        self.fondoMontos = QFrame(self.fondoRecarga)
        self.fondoMontos.setObjectName(u"fondoMontos")
        self.fondoMontos.setGeometry(QRect(70, 333.2, 1149.4, 167.79))       
        self.fondoMontos.setStyleSheet(u"background-color: #ECEFF1;\n"
"border: 1px solid #CFD8DC;\n"
"border-radius: 10px;\n"
"border: 1px solid #CFD8DC;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoMontos.setFrameShape(QFrame.StyledPanel)
        self.fondoMontos.setFrameShadow(QFrame.Raised)
       
        self.pasoTituloMontos = QLabel(self.fondoMontos)
        self.pasoTituloMontos.setObjectName(u"1")
        self.pasoTituloMontos.setGeometry(QRect(330, 12, 38, 35))
        self.pasoTituloMontos.setStyleSheet(u"""
            QLabel#1 {
                background-color: #2C3E50;
                color: #FFFFFF;
                font-size: 19px;
                font-weight: bold;
                padding: 8px;
                border-radius: 17.5px;
                border: 1px solid #BDC3C7;
                min-height: 20px;
            }
        """)
       
        self.tituloMontos = QLabel(self.fondoMontos)
        self.tituloMontos.setObjectName(u"tituloMontos")
        self.tituloMontos.setGeometry(QRect(380, 11, 449.4, 36.89))     
        self.tituloMontos.setStyleSheet(u"QLabel {\n"
"    color: #455A64;\n"
"    font-size: 17pt;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}")      
        
        self.monto1 = QPushButton(self.fondoMontos)
        self.monto1.setObjectName(u"monto1")
        self.monto1.setGeometry(QRect(112, 57, 88, 88))               
        self.monto1.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
              
        self.monto2 = QPushButton(self.fondoMontos)
        self.monto2.setObjectName(u"monto2")
        self.monto2.setGeometry(QRect(266, 57, 88, 88))     
        self.monto2.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
       
        self.monto3 = QPushButton(self.fondoMontos)
        self.monto3.setObjectName(u"monto3")
        self.monto3.setGeometry(QRect(434,57, 88, 88))         
        self.monto3.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
        
        self.monto4 = QPushButton(self.fondoMontos)
        self.monto4.setObjectName(u"monto4")
        self.monto4.setGeometry(QRect(588, 57, 88, 88))
        self.monto4.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
        
        self.monto5 = QPushButton(self.fondoMontos)
        self.monto5.setObjectName(u"monto5")
        self.monto5.setGeometry(QRect(756, 57, 88, 88))
        self.monto5.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
        
        self.monto6 = QPushButton(self.fondoMontos)
        self.monto6.setObjectName(u"monto6")
        self.monto6.setGeometry(QRect(924, 57, 88, 88))
        self.monto6.setStyleSheet(u"""
QPushButton {
    background-color: #FFFFFF;
    border: 2px solid #B0BEC5;
    border-radius: 44px;
    color: #37474F;
    padding: 9px;
    font-weight: bold;
    text-align: center;
    font-size: 19px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: #FFFFFF;
    border-color: #90A4AE;
}

QPushButton:pressed, QPushButton:checked {
    background-color: #1976D2;
    color: #FFFFFF;
    border-color: #1565C0;
    font-size: 25px;
    border-width: 3px;
}
""")
        
        self.fondoFactura = QFrame(self.fondoRecarga)
        self.fondoFactura.setObjectName(u"frame")
        self.fondoFactura.setGeometry(QRect(70, 523.6, 1149.4, 393.89))
        self.fondoFactura.setStyleSheet(u"background-color: #ECEFF1;\n"
"border: 1px solid #CFD8DC;\n"
"border-radius: 10px;\n"
"border: 1px solid #CFD8DC;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoFactura.setFrameShape(QFrame.StyledPanel)
        self.fondoFactura.setFrameShadow(QFrame.Raised)
       
        self.pasoTituloFactura = QLabel(self.fondoFactura)
        self.pasoTituloFactura.setObjectName(u"1")
        self.pasoTituloFactura.setGeometry(QRect(290, 12, 38, 35))
        self.pasoTituloFactura.setStyleSheet(u"""
            QLabel#1 {
                background-color: #2C3E50;
                color: #FFFFFF;
                font-size: 19px;
                font-weight: bold;
                padding: 8px;
                border-radius: 17.5px;
                border: 1px solid #BDC3C7;
                min-height: 20px;
            }
        """)
       
        self.TituloFactura = QLabel(self.fondoFactura)
        self.TituloFactura.setObjectName(u"TituloFactura")
        self.TituloFactura.setGeometry(QRect(340, 11, 490, 36.89))
        self.TituloFactura.setStyleSheet(u"QLabel {\n"
"    color: #455A64;\n"
"    font-size: 17pt;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}")
        
        self.IconoDocIden = QLabel(self.fondoFactura)
        self.IconoDocIden.setObjectName(u"IconoDocIden")
        self.IconoDocIden.setGeometry(QRect(550, 95.2, 58, 48))
        svg_content = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-id-card">
            <path d="M16 10h2"/>
            <path d="M16 14h2"/>
            <path d="M6.17 15a3 3 0 0 1 5.66 0"/>
            <circle cx="9" cy="11" r="2"/>
            <rect x="2" y="5" width="20" height="14" rx="2"/>
        </svg>
        '''
        svg_renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        
        size = min(self.IconoDocIden.width(), self.IconoDocIden.height())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        background_color = QColor("#2C3E50")  
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_size = size * 0.6  
        svg_pos = (size - svg_size) / 2

        svg_renderer.render(painter, QRectF(svg_pos, svg_pos, svg_size, svg_size))
        painter.end()
        
        self.IconoDocIden.setPixmap(pixmap)
        self.IconoDocIden.setScaledContents(True)
        
        self.IconoNit = QLabel(self.fondoFactura)
        self.IconoNit.setObjectName(u"IconoNit")
        self.IconoNit.setGeometry(QRect(550, 95.2, 58, 48))        
        Nit_svg_content = '''
        <svg fill="#FFFFFF" height="200px" width="200px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier"> <g> <g> <path d="M486.881,68.409H25.119C11.268,68.409,0,79.677,0,93.528v324.944c0,13.851,11.268,25.119,25.119,25.119h94.419 c4.428,0,8.017-3.588,8.017-8.017c0-4.428-3.588-8.017-8.017-8.017H25.119c-5.01,0-9.086-4.076-9.086-9.086V93.528 c0-5.01,4.076-9.086,9.086-9.086h461.762c5.01,0,9.086,4.076,9.086,9.086v324.944c0,5.01-4.076,9.086-9.086,9.086H154.037 c-4.428,0-8.017,3.588-8.017,8.017c0,4.428,3.588,8.017,8.017,8.017h332.844c13.851,0,25.119-11.268,25.119-25.119V93.528 C512,79.677,500.732,68.409,486.881,68.409z"></path> </g> </g> 
            <g> <g> <path d="M452.676,111.165h-59.858c-4.428,0-8.017,3.588-8.017,8.017s3.588,8.017,8.017,8.017h59.858 c0.294,0,0.534,0.241,0.534,0.534v256.534c0,0.294-0.241,0.534-0.534,0.534H59.324c-0.294,0-0.534-0.241-0.534-0.534V127.733 c0-0.294,0.241-0.534,0.534-0.534h298.934c4.428,0,8.017-3.588,8.017-8.017s-3.588-8.017-8.017-8.017H59.324 c-9.136,0-16.568,7.432-16.568,16.568v256.534c0,9.136,7.432,16.568,16.568,16.568h393.353c9.136,0,16.568-7.432,16.568-16.568 V127.733C469.244,118.597,461.812,111.165,452.676,111.165z"></path> </g> </g> 
            <g> <g> <path d="M207.441,272.112c13.73-12.429,22.371-30.382,22.371-50.317c0-37.426-30.448-67.875-67.875-67.875 s-67.875,30.448-67.875,67.875c0,19.935,8.641,37.888,22.372,50.317l-21.943,64.316c-1.139,3.344,0.042,7.04,2.912,9.101 c2.87,2.061,6.748,2,9.554-0.15l14.926-11.44l4.822,18.179c0.905,3.414,3.94,5.834,7.469,5.956 c0.094,0.003,0.188,0.005,0.281,0.005c3.417,0,6.475-2.173,7.586-5.428l19.897-58.32l19.897,58.32 c1.111,3.255,4.167,5.428,7.586,5.428c0.093,0,0.187-0.002,0.281-0.005c3.531-0.122,6.565-2.542,7.469-5.956l4.822-18.179 l14.926,11.44c2.819,2.16,6.839,2.182,9.681,0.053c2.749-2.059,3.892-5.753,2.783-9.004L207.441,272.112z M135.415,322.416 c-1.014-3.823-1.707-7.895-5.845-9.579c-2.708-1.102-5.674-0.586-7.989,1.132c-1.134,0.842-2.244,1.72-3.365,2.579l11.884-34.831 c5.304,2.829,11.026,4.967,17.047,6.311L135.415,322.416z M161.937,273.637c-28.585,0-51.841-23.256-51.841-51.841 s23.256-51.841,51.841-51.841c28.585,0,51.841,23.256,51.841,51.841S190.523,273.637,161.937,273.637z M202.293,313.969 c-2.315-1.718-5.281-2.234-7.989-1.132c-4.137,1.684-4.83,5.756-5.845,9.579l-11.732-34.388c6.02-1.344,11.743-3.481,17.047-6.311 l11.884,34.831C204.537,315.689,203.428,314.811,202.293,313.969z"></path> </g> </g> 
            <g> <g> <path d="M161.937,179.574c-23.281,0-42.221,18.941-42.221,42.221s18.941,42.221,42.221,42.221s42.221-18.941,42.221-42.221 S185.218,179.574,161.937,179.574z M161.937,247.983c-14.441,0-26.188-11.747-26.188-26.188s11.747-26.188,26.188-26.188 s26.188,11.747,26.188,26.188S176.378,247.983,161.937,247.983z"></path> </g> </g> 
            <g> <g> <path d="M409.921,230.881h-17.102c-4.428,0-8.017,3.588-8.017,8.017s3.588,8.017,8.017,8.017h17.102 c4.428,0,8.017-3.588,8.017-8.017S414.349,230.881,409.921,230.881z"></path> </g> </g> 
            <g> <g> <path d="M298.756,282.188h-25.653c-4.428,0-8.017,3.588-8.017,8.017c0,4.428,3.588,8.017,8.017,8.017h25.653 c4.428,0,8.017-3.588,8.017-8.017C306.772,285.776,303.184,282.188,298.756,282.188z"></path> </g> </g> 
            <g> <g> <path d="M367.165,230.881h-25.653c-4.428,0-8.017,3.588-8.017,8.017s3.588,8.017,8.017,8.017h25.653 c4.428,0,8.017-3.588,8.017-8.017S371.593,230.881,367.165,230.881z"></path> </g> </g> 
            <g> <g> <path d="M315.858,230.881h-42.756c-4.428,0-8.017,3.588-8.017,8.017s3.588,8.017,8.017,8.017h42.756 c4.428,0,8.017-3.588,8.017-8.017S320.286,230.881,315.858,230.881z"></path> </g> </g> 
            <g> <g> <path d="M409.921,282.188h-85.511c-4.428,0-8.017,3.588-8.017,8.017c0,4.428,3.588,8.017,8.017,8.017h85.511 c4.428,0,8.017-3.588,8.017-8.017C417.937,285.776,414.349,282.188,409.921,282.188z"></path> </g> </g> 
            <g> <g> <path d="M397.094,153.921H285.929c-11.493,0-20.843,9.351-20.843,20.843s9.351,20.843,20.843,20.843h111.165 c11.493,0,20.843-9.351,20.843-20.843S408.587,153.921,397.094,153.921z M397.094,179.574H285.929c-2.652,0-4.81-2.158-4.81-4.81 s2.158-4.81,4.81-4.81h111.165c2.652,0,4.81,2.158,4.81,4.81S399.746,179.574,397.094,179.574z"></path> </g> </g> 
            <g> <g> <path d="M341.511,333.495h-68.409c-4.428,0-8.017,3.588-8.017,8.017c0,4.428,3.588,8.017,8.017,8.017h68.409 c4.428,0,8.017-3.588,8.017-8.017C349.528,337.083,345.94,333.495,341.511,333.495z"></path> </g> </g> 
            <g> <g> <path d="M409.921,333.495h-42.756c-4.428,0-8.017,3.588-8.017,8.017c0,4.428,3.588,8.017,8.017,8.017h42.756 c4.428,0,8.017-3.588,8.017-8.017C417.937,337.083,414.349,333.495,409.921,333.495z"></path> </g> </g> </g>
        </svg>
        '''
        Nit_svg_renderer = QSvgRenderer(QByteArray(Nit_svg_content.encode()))

        size = min(self.IconoNit.width(), self.IconoNit.height())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        background_color = QColor("#2C3E50")
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_size = size * 0.6  
        svg_pos = (size - svg_size) / 2

        Nit_svg_renderer.render(painter, QRectF(svg_pos, svg_pos, svg_size, svg_size))
        painter.end()
        
        self.IconoNit.setPixmap(pixmap)
        self.IconoNit.setScaledContents(True)
        self.IconoNit.hide()
        
        self.IconoComple = QLabel(self.fondoFactura)
        self.IconoComple.setObjectName(u"IconoComple")
        self.IconoComple.setGeometry(QRect(903, 95.2, 58, 48))      
        Comple_svg_content = '''
        <svg viewBox="0 0 24 24" id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" fill="#FFFFFF">
            <g id="SVGRepo_bgCarrier" stroke-width="0">
            </g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round">
            </g><g id="SVGRepo_iconCarrier">
            <defs><style>.cls-1{fill:none;stroke:#FFFFFF;stroke-miterlimit:10;stroke-width:1.91px;}</style></defs>
            <rect class="cls-1" x="1.5" y="4.36" width="21" height="15.27"></rect>
            <line class="cls-1" x1="4.36" y1="8.18" x2="12" y2="8.18"></line>
            <line class="cls-1" x1="4.36" y1="12" x2="12" y2="12"></line>
            <line class="cls-1" x1="4.36" y1="15.82" x2="10.09" y2="15.82"></line>
            <rect class="cls-1" x="14.86" y="8.18" width="3.82" height="3.82"></rect></g>
        </svg>
        '''
        Comple_svg_renderer = QSvgRenderer(QByteArray(Comple_svg_content.encode()))

        size = min(self.IconoComple.width(), self.IconoComple.height())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        background_color = QColor("#2C3E50") 
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_size = size * 0.6 
        svg_pos = (size - svg_size) / 2

        Comple_svg_renderer.render(painter, QRectF(svg_pos, svg_pos, svg_size, svg_size))
        painter.end()
        
        self.IconoComple.setPixmap(pixmap)
        self.IconoComple.setScaledContents(True)
        
        self.IconoRazonSoc = QLabel(self.fondoFactura)
        self.IconoRazonSoc.setObjectName(u"IconoRazonSoc")
        self.IconoRazonSoc.setGeometry(QRect(550, 203, 58, 48))
        Razon_svg_content = '''
        <svg fill="#FFFFFF" height="200px" width="200px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 508 508" xml:space="preserve">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier"> <g> 
            <g> <path d="M467.2,146H332.4v-24.2c0-7.8-6.3-14.1-14.1-14.1h-22V14.1C296.3,6.3,290,0,282.2,0h-56.4c-7.8,0-14.1,6.3-14.1,14.1v93.6 h-22c-7.8,0-14.1,6.3-14.1,14.1V146H40.8C18.3,146,0,164.3,0,186.8v280.5C0,489.7,18.3,508,40.8,508h426.4 c22.5,0,40.8-18.3,40.8-40.8V186.8C508,164.3,489.7,146,467.2,146z M239.9,28.2h28.2v79.5h-28.2V28.2z M203.8,135.9h100.4v38.4 H203.8V135.9z M479.8,467.2L479.8,467.2c0,6.9-5.6,12.6-12.6,12.6H40.8c-6.9,0-12.6-5.6-12.6-12.6V186.8c0-6.9,5.6-12.6,12.6-12.6 h134.8v14.3c0,7.8,6.3,14.1,14.1,14.1h128.6c7.8,0,14.1-6.3,14.1-14.1v-14.3h134.8c6.9,0,12.6,5.6,12.6,12.6V467.2z">
            </path> </g> </g> 
            <g> <g> <path d="M188.6,239.9H79.1c-7.8,0-14.1,6.3-14.1,14.1v117.8c0,7.8,6.3,14.1,14.1,14.1h109.5c7.8,0,14.1-6.3,14.1-14.1V254 C202.7,246.2,196.4,239.9,188.6,239.9z M174.4,357.7H93.2v-89.6h81.2V357.7z"></path> </g> </g> <g> <g> 
            <path d="M428.9,239.9H261.3c-7.8,0-14.1,6.3-14.1,14.1s6.3,14.1,14.1,14.1h167.6c7.8,0,14.1-6.3,14.1-14.1 C443,246.2,436.7,239.9,428.9,239.9z"></path> </g> </g> <g> <g> 
            <path d="M428.9,325.2H261.3c-7.8,0-14.1,6.3-14.1,14.1s6.3,14.1,14.1,14.1h167.6c7.8,0,14.1-6.3,14.1-14.1 C443,331.6,436.7,325.2,428.9,325.2z"></path> </g> </g> 
            <g> <g> <path d="M428.9,410.6H79.1c-7.8,0-14.1,6.3-14.1,14.1c0,7.8,6.3,14.1,14.1,14.1h349.8c7.8,0,14.1-6.3,14.1-14.1 C443,416.9,436.7,410.6,428.9,410.6z"></path> </g> </g> </g>
        </svg>
        '''
        Razon_svg_renderer = QSvgRenderer(QByteArray(Razon_svg_content.encode()))

        size = min(self.IconoRazonSoc.width(), self.IconoRazonSoc.height())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        background_color = QColor("#2C3E50") 
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_size = size * 0.6 
        svg_pos = (size - svg_size) / 2

        Razon_svg_renderer.render(painter, QRectF(svg_pos, svg_pos, svg_size, svg_size))
        painter.end()
        
        self.IconoRazonSoc.setPixmap(pixmap)
        self.IconoRazonSoc.setScaledContents(True)
        
        self.IconoCorreo = QLabel(self.fondoFactura)
        self.IconoCorreo.setObjectName(u"IconoCorreo")
        self.IconoCorreo.setGeometry(QRect(550, 313, 58, 48))
        Correo_svg_content = '''
        <svg height="186px" width="186px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-46.08 -46.08 604.16 604.16" xml:space="preserve" fill="#000000" stroke="#000000" stroke-width="1.0240019999999999">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#303030" stroke-width="2.0480039999999997"></g>
            <g id="SVGRepo_iconCarrier"> <polygon style="fill:#f8f7f7;" points="470.638,192.171 470.638,214.3 375.914,292.619 256,391.772 136.087,292.619 41.362,214.3 41.362,192.171 256,14.714 "></polygon> 
            <path style="fill:#ffffff;" d="M480.014,225.64c3.381-2.796,5.338-6.954,5.338-11.34v-22.129c0-4.386-1.957-8.544-5.338-11.34 L265.376,3.375c-5.44-4.499-13.311-4.499-18.751,0L31.987,180.832c-3.381,2.796-5.338,6.954-5.338,11.34V214.3 c0,0.026,0.004,0.051,0.004,0.078v279.015v0.138v3.756c0,8.126,6.589,14.713,14.713,14.713h429.267 c8.125,0,14.713-6.587,14.713-14.713v-3.893V315.927c0-8.126-6.589-14.713-14.713-14.713c-8.125,0-14.713,6.587-14.713,14.713 v146.209L324.954,353.849L480.014,225.64z M256,372.68l-23.507-19.436l-81.693-67.55v-87.078h210.4v87.078l-81.693,67.55L256,372.68 z M56.08,245.562L187.046,353.85L56.08,462.137C56.08,462.137,56.08,245.562,56.08,245.562z M256,33.805l199.925,165.292v8.276 l-65.298,53.991v-77.461c0-8.126-6.589-14.713-14.713-14.713H136.087c-8.125,0-14.713,6.587-14.713,14.713v77.463L56.08,207.378 V201.4c0-0.029-0.004-0.057-0.004-0.085v-2.217L256,33.805z M434.458,482.574H77.543l132.593-109.632l36.489,30.171 c2.721,2.25,6.047,3.374,9.375,3.374c3.328,0,6.655-1.126,9.375-3.374l36.489-30.171L434.458,482.574z"></path> </g>
        </svg>
        '''
        Correo_svg_renderer = QSvgRenderer(QByteArray(Correo_svg_content.encode()))

        size = min(self.IconoCorreo.width(), self.IconoCorreo.height())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        background_color = QColor("#2C3E50") 
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        svg_size = size * 0.6 
        svg_pos = (size - svg_size) / 2

        Correo_svg_renderer.render(painter, QRectF(svg_pos, svg_pos, svg_size, svg_size))
        painter.end()
        
        self.IconoCorreo.setPixmap(pixmap)
        self.IconoCorreo.setScaledContents(True)
        
        self.DocIenRaButt = QRadioButton(self.fondoFactura)
        self.DocIenRaButt.setObjectName(u"DocIenRaButt")
        self.DocIenRaButt.setGeometry(QRect(144, 142.8, 365.4, 36.89))
        self.DocIenRaButt.setStyleSheet(u"QRadioButton {\n"
"    color: #455A64;\n"
"    font-size: 23px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;\n"
"    padding: 8px; \n"
"    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);\n"
"	border: none;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 10px;\n"
"    background-color: #f2f2f2;\n"
"    border: 2px solid #cccccc;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #2980b9;\n"
"    border-color: #2980b9;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border-color: #7fb3d5;\n"
"}\n"
"\n"
"QRadioButton::indicator:pressed {\n"
"    background-color: #1f618d;\n"
"    border-color: #1f618d;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    background-color: #f2f2f2;\n"
"    border-color: #e6e6e6;\n"
"}\n"
"")
        self.DocIenRaButt.setChecked(True)
        
        self.NitRadButt = QRadioButton(self.fondoFactura)
        self.NitRadButt.setObjectName(u"NitRadButt")
        self.NitRadButt.setGeometry(QRect(144, 238, 127.4, 36.89))
        self.NitRadButt.setStyleSheet(u"QRadioButton {\n"
"    color: #455A64;\n"
"    font-size: 23px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;\n"
"    padding: 8px; \n"
"    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);\n"
"	border:none;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 10px;\n"
"    background-color: #f2f2f2;\n"
"    border: 2px solid #cccccc;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #2980b9;\n"
"    border-color: #2980b9;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border-color: #7fb3d5;\n"
"}\n"
"\n"
"QRadioButton::indicator:pressed {\n"
"    background-color: #1f618d;\n"
"    border-color: #1f618d;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    background-color: #f2f2f2;\n"
"    border-color: #e6e6e6;\n"
"}")
        
        self.volver = QPushButton(self.fondoRecarga)
        self.volver.setObjectName(u"volver")
        self.volver.setGeometry(QRect(293, 940, 323, 61))
        self.volver.clicked.connect(MainWindow.close)
        self.volver.setStyleSheet(u"""
            QPushButton {
                background-color: #0C1C23;  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 22px;           
                font-weight: bold;        
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }

            QPushButton:hover {
                background-color: #213138; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }

            QPushButton:pressed {
                background-color: #213138;   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }
        """)

        self.recargaOk = QPushButton(self.fondoRecarga)
        self.recargaOk.setObjectName(u"recarga")
        self.recargaOk.setGeometry(QRect(675, 940, 323, 61))      
        self.recargaOk.setStyleSheet(u"""
            QPushButton {
                background-color: #2C3E50;  
                color: #FFFFFF;            
                border: none;               
                border-radius: 25px;        
                padding: 12px 24px;        
                font-family: 'Arial', sans-serif; 
                font-size: 22px;           
                font-weight: bold;        
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; 
                cursor: pointer;           
            }

            QPushButton:hover {
                background-color: #34495E; 
                transform: translateY(-3px); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); 
            }

            QPushButton:pressed {
                background-color: #1ABC9C;   
                transform: translateY(1px);   
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }
        """)
        self.recargaOk.clicked.connect(self.handle_recarga_ok)
        
        self.fondoMontos.raise_()
        self.fondoFactura.raise_()
        self.tituloPrincipal.raise_()
        self.volver.raise_()
        self.recargaOk.raise_()
        self.tarjeta.raise_()
        
        self.NumeroCiEdit = QTextEdit(self.centralwidget)
        self.NumeroCiEdit.setObjectName(u"NumeroCi")
        self.NumeroCiEdit.setGeometry(QRect(696, 618.8, 220, 47)) 
        self.NumeroCiEdit.setStyleSheet(u"""
            QTextEdit#NumeroCi {
                background-color: #FFFFFF;
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
                padding: 7px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)
        
        self.ComplementoEdit = QTextEdit(self.centralwidget)
        self.ComplementoEdit.setObjectName(u"ComplementoEdit")
        self.ComplementoEdit.setGeometry(QRect(1040, 618.8, 120, 47))
        self.ComplementoEdit.setStyleSheet(u"""
            QTextEdit#ComplementoEdit {
                background-color: #FFFFFF;
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
                padding: 7px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)
        
        self.RazonSocialEdit = QTextEdit(self.centralwidget)
        self.RazonSocialEdit.setObjectName(u"RazonSocialEdit")
        self.RazonSocialEdit.setGeometry(QRect(696, 725.9, 365, 47))      
        self.RazonSocialEdit.setStyleSheet(u"""
            QTextEdit#RazonSocialEdit {
                background-color: #FFFFFF;
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
                padding: 7px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)
        
        self.CorreoEdit = QTextEdit(self.centralwidget)
        self.CorreoEdit.setObjectName(u"CorreoEdit")
        self.CorreoEdit.setGeometry(QRect(696, 833, 365, 47))
        self.CorreoEdit.setStyleSheet(u"""
            QTextEdit#CorreoEdit {
                background-color: #FFFFFF;
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
                padding: 7px;
                border-radius: 10px;
                border: 1px solid #BDC3C7;
            }
        """)        

        self.DocumentoIden = QLabel(self.centralwidget)
        self.DocumentoIden.setObjectName(u"DocumentoIden")
        self.DocumentoIden.setGeometry(QRect(700, 583.1, 253.4, 23.8))
        self.DocumentoIden.setStyleSheet(u"color: #455A64;\n"
"    font-size: 22px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;")
        
        self.Complemento = QLabel(self.centralwidget)
        self.Complemento.setObjectName(u"Complemento")
        self.Complemento.setGeometry(QRect(1020, 583.1, 253.4, 23.8))
        self.Complemento.setStyleSheet(u"color: #455A64;\n"
"    font-size: 22px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;")
        
        self.RazonSocial = QLabel(self.centralwidget)
        self.RazonSocial.setObjectName(u"RazonSocial")
        self.RazonSocial.setGeometry(QRect(700, 690.2, 253.4, 23.8))
        self.RazonSocial.setStyleSheet(u"color: #455A64;\n"
"    font-size: 22px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;")
        
        self.Correo = QLabel(self.centralwidget)
        self.Correo.setObjectName(u"Correo")
        self.Correo.setGeometry(QRect(700, 797.3, 253.4, 23.8))
        self.Correo.setStyleSheet(u"color: #455A64;\n"
"    font-size: 22px; \n"
"    font-family: Arial, sans-serif;\n"
"    font-weight: bold;")
        

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        self.monto1.setCheckable(True)
        self.monto2.setCheckable(True)
        self.monto3.setCheckable(True)
        self.monto4.setCheckable(True)
        self.monto5.setCheckable(True)
        self.monto6.setCheckable(True)
        
        self.monto1.clicked.connect(lambda: self.toggle_monto_buttons(self.monto1))
        self.monto2.clicked.connect(lambda: self.toggle_monto_buttons(self.monto2))
        self.monto3.clicked.connect(lambda: self.toggle_monto_buttons(self.monto3))
        self.monto4.clicked.connect(lambda: self.toggle_monto_buttons(self.monto4))
        self.monto5.clicked.connect(lambda: self.toggle_monto_buttons(self.monto5))
        self.monto6.clicked.connect(lambda: self.toggle_monto_buttons(self.monto6)) 
        
        QMetaObject.connectSlotsByName(MainWindow)
        
        self.DocIenRaButt.toggled.connect(self.toggle_documento_identidad)
        self.NitRadButt.toggled.connect(self.toggle_nit)

    def actualizar_etiquetas(self, datos_tarjeta):
        self.tipoTarjeta.setText(datos_tarjeta['profile_name'])
        self.estado.setText(datos_tarjeta['card_status'])
        self.uid.setText(f"UID: {datos_tarjeta['uid']}")
        nombre_completo = f"{datos_tarjeta.get('name', '')} {datos_tarjeta.get('last_name', '')}".strip()
        self.nombre.setText(nombre_completo)
        self.saldo.setText(f"{datos_tarjeta['balance']}")
        self.NumeroCiEdit.setText(f"{datos_tarjeta['document']}")
        self.RazonSocialEdit.setText(f"{datos_tarjeta['social_reason']}")
        self.monedaSaldo.setText("Bs")

    def show_confirmation_dialog(self, uid, numero_ci, razon_social, monto):
        self.apply_blur_effect(self.centralwidget)
        pago_dialog = QDialog(self.centralwidget)
        pago_dialog.setFixedSize(750, 500)
        pago_dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        pago_dialog.setStyleSheet("""
            QDialog {
                border: 2px solid #2C3E50;
                border-radius: 10px;
            }
        """)

        header = QLabel(pago_dialog)
        header.setGeometry(0, 0, 750, 60)
        header.setStyleSheet("background-color: #2C3E50;")
        
        title = QLabel("Solicitud de Recarga", header)
        title.setGeometry(0, 0, 750, 60)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        message = QLabel("Se esta solicitando una nueva recarga \n Verifique si los datos estan correctos :", pago_dialog)
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("font-size: 22px; color: #2C3E50;")
        message.setGeometry(50, 90, 650, 50)

        self.tarjeta = QWidget(pago_dialog)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setGeometry(100, 170, 550, 200)
        self.tarjeta.setStyleSheet("""
            QWidget#tarjeta {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2C3E50, stop:1 #34495e);
                border-radius: 15px;
                color: white;
            }
        """)
        
        uid_label = QLabel(f" {uid}", self.tarjeta)
        datosFactura_label = QLabel(f" {numero_ci} - {razon_social}", self.tarjeta)
        monto_label = QLabel(f"Bs. {monto}", self.tarjeta)

        uid_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        datosFactura_label.setStyleSheet("color: white; font-size: 21px;")
        monto_label.setStyleSheet("color: white; font-size: 21px;")

        uid_label.setGeometry(QRect(140, 130, 300, 40))
        datosFactura_label.setGeometry(QRect(50, 60, 200, 30))
        monto_label.setGeometry(QRect(345, 60, 70, 30))

        QLabel("Numero de Tarjeta :", self.tarjeta).setGeometry(QRect(200, 110, 150, 20))
        QLabel("Datos de Factura :", self.tarjeta).setGeometry(QRect(90, 40, 150, 20))
        QLabel("Monto de Recarga :", self.tarjeta).setGeometry(QRect(310, 40, 150, 20))

        for label in self.tarjeta.findChildren(QLabel)[3:]:
            label.setStyleSheet("color: white; font-size: 18px;")
            
        Cancelar = QPushButton("  Cancelar", pago_dialog)
        Cancelar.setFixedSize(200, 50)
        Cancelar.setStyleSheet("""
            QPushButton {
                background-color: #C21807;
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
        Cancelar.setGeometry(105, 400, 250, 50)
        Cancelar.clicked.connect(lambda: self.close_dialog_and_remove_blur(pago_dialog))
        
        cancel_svg = """
        <svg viewBox="0 0 1024 1024" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg" fill="#ffffff" stroke="#ffffff">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier"><path d="M704 288h-281.6l177.6-202.88a32 32 0 0 0-48.32-42.24l-224 256a30.08 30.08 0 0 0-2.24 3.84 32 32 0 0 0-2.88 4.16v1.92a32 32 0 0 0 0 5.12A32 32 0 0 0 320 320a32 32 0 0 0 0 4.8 32 32 0 0 0 0 5.12v1.92a32 32 0 0 0 2.88 4.16 30.08 30.08 0 0 0 2.24 3.84l224 256a32 32 0 1 0 48.32-42.24L422.4 352H704a224 224 0 0 1 224 224v128a224 224 0 0 1-224 224H320a232 232 0 0 1-28.16-1.6 32 32 0 0 0-35.84 27.84 32 32 0 0 0 27.84 35.52A295.04 295.04 0 0 0 320 992h384a288 288 0 0 0 288-288v-128a288 288 0 0 0-288-288zM103.04 760a32 32 0 0 0-62.08 16A289.92 289.92 0 0 0 140.16 928a32 32 0 0 0 40-49.92 225.6 225.6 0 0 1-77.12-118.08zM64 672a32 32 0 0 0 22.72-9.28 37.12 37.12 0 0 0 6.72-10.56A32 32 0 0 0 96 640a33.6 33.6 0 0 0-9.28-22.72 32 32 0 0 0-10.56-6.72 32 32 0 0 0-34.88 6.72A32 32 0 0 0 32 640a32 32 0 0 0 2.56 12.16 37.12 37.12 0 0 0 6.72 10.56A32 32 0 0 0 64 672z" fill="#ffffff"></path></g>
        </svg>"""
        self.add_svg_icon(Cancelar, cancel_svg)
        
        PagoTarjeta = QPushButton("Solicitar Recarga", pago_dialog)
        PagoTarjeta.setFixedSize(250, 50)
        PagoTarjeta.setStyleSheet("""
            QPushButton {
                background-color: #008000;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007300;
            }
        """)
        PagoTarjeta.setGeometry(410, 400, 250, 50)
        #PagoTarjeta.clicked.connect(lambda: self.abrir_iframe(pago_dialog))
        
        card_svg = """
        <svg fill="#f8f1f1" viewBox="0 0 512 512" enable-background="new 0 0 512 512" id="Credit_x5F_card" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" stroke="#f8f1f1">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier"> <g> <path d="M127.633,215.98h215.568c29.315,0,53.166,23.851,53.166,53.166v14.873h38.061c22.735,0,41.166-18.432,41.166-41.167 v-69.608H127.633V215.98z"></path> 
            <path d="M434.428,74.2H168.799c-22.735,0-41.166,18.431-41.166,41.166v17.479h347.961v-17.479 C475.594,92.631,457.163,74.2,434.428,74.2z"></path> 
            <path d="M343.201,227.98H77.572c-22.735,0-41.166,18.431-41.166,41.166v127.487c0,22.735,18.431,41.166,41.166,41.166h265.629 c22.736,0,41.166-18.431,41.166-41.166V269.146C384.367,246.412,365.938,227.98,343.201,227.98z M131.542,329.846 c0,4.92-3.989,8.909-8.909,8.909H75.289c-4.92,0-8.908-3.989-8.908-8.909v-29.098c0-4.921,3.988-8.909,8.908-8.909h47.344 c4.92,0,8.909,3.988,8.909,8.909V329.846z M300.961,413.039c-10.796,0-19.548-8.752-19.548-19.549s8.752-19.549,19.548-19.549 c10.797,0,19.549,8.752,19.549,19.549S311.758,413.039,300.961,413.039z M345.271,413.039c-10.797,0-19.549-8.752-19.549-19.549 s8.752-19.549,19.549-19.549c10.796,0,19.548,8.752,19.548,19.549S356.067,413.039,345.271,413.039z"></path> </g> </g>
        </svg>"""
        self.add_svg_icon(PagoTarjeta, card_svg)
        
        #PagoQR = QPushButton("  Pago por QR", pago_dialog)
        #PagoQR.setFixedSize(250, 50)
        #PagoQR.setStyleSheet("""
        #    QPushButton {
         #       background-color: #008000 ;
          #      color: white;
           #     border: none;
            #    border-radius: 25px;
             #   font-size: 18px;
              #  font-weight: bold; 
           # }
            #QPushButton:hover {
             #   background-color: #007300;
            #}
       # """)
        #PagoQR.setGeometry(410, 400, 250, 50)

        #qr_svg = """
        #<svg fill="#ffffff" viewBox="0 -0.09 122.88 122.88" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="enable-background:new 0 0 122.88 122.7" xml:space="preserve" stroke="#ffffff">
         #   <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          #  <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
           # <g id="SVGRepo_iconCarrier"> <style type="text/css">.st0{fill-rule:evenodd;clip-rule:evenodd;}</style> 
            #<g> <path class="st0" d="M0.18,0h44.63v44.45H0.18V0L0.18,0z M111.5,111.5h11.38v11.2H111.5V111.5L111.5,111.5z M89.63,111.48h11.38 v10.67H89.63h-0.01H78.25v-21.82h11.02V89.27h11.21V67.22h11.38v10.84h10.84v11.2h-10.84v11.2h-11.21h-0.17H89.63V111.48 L89.63,111.48z M55.84,89.09h11.02v-11.2H56.2v-11.2h10.66v-11.2H56.02v11.2H44.63v-11.2h11.2V22.23h11.38v33.25h11.02v11.2h10.84 v-11.2h11.38v11.2H89.63v11.2H78.25v22.05H67.22v22.23H55.84V89.09L55.84,89.09z M111.31,55.48h11.38v11.2h-11.38V55.48 L111.31,55.48z M22.41,55.48h11.38v11.2H22.41V55.48L22.41,55.48z M0.18,55.48h11.38v11.2H0.18V55.48L0.18,55.48z M55.84,0h11.38 v11.2H55.84V0L55.84,0z M0,78.06h44.63v44.45H0V78.06L0,78.06z M10.84,88.86h22.95v22.86H10.84V88.86L10.84,88.86z M78.06,0h44.63 v44.45H78.06V0L78.06,0z M88.91,10.8h22.95v22.86H88.91V10.8L88.91,10.8z M11.02,10.8h22.95v22.86H11.02V10.8L11.02,10.8z"></path> 
            #</g> </g>
        #</svg>"""
        
        #self.add_svg_icon(PagoQR, qr_svg)

        pago_dialog.exec_()

    def handle_recarga_ok(self):
        monto = self.obtener_monto_seleccionado()
        correo = self.CorreoEdit.toPlainText()
        
        if monto == "0":
            self.mensaje_advertencia()
        elif not correo:
            self.mensaje_advertencia_correo()
        elif not self.es_correo_valido(correo):
            self.mensaje_advertencia_correo_no_valido()
        else:
            uid = self.uid.text()
            numero_ci = self.NumeroCiEdit.toPlainText()
            razon_social = self.RazonSocialEdit.toPlainText()
            self.show_confirmation_dialog(uid, numero_ci, razon_social, monto)

    def es_correo_valido(self, correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, correo))
    
    def mensaje_advertencia_correo_no_valido(self, message="El correo introducido no es valido"):
        self.apply_blur_effect(self.centralwidget)

        msg = QDialog(self.centralwidget)
        msg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        msg.setModal(True)

        layout = QVBoxLayout(msg)

        icon_label = QLabel()
        icon = msg.style().standardIcon(QStyle.SP_MessageBoxWarning)
        icon_label.setPixmap(icon.pixmap(32, 32))

        text_label = QLabel(message)
        text_label.setAlignment(Qt.AlignCenter)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(msg.accept)

        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        layout.addWidget(text_label)
        layout.addWidget(ok_button, alignment=Qt.AlignHCenter)

        msg.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                msg.sizeHint(),
                self.centralwidget.geometry()
            )
        )

        msg.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #2C3E50;
                border-radius: 10px;
            }
            QLabel {
                color: #2C3E50;
                font-size: 20px;
                padding: 10px;
            }
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)

        msg.exec_()
        self.remove_blur_effect(self.centralwidget)
            
    def mensaje_advertencia_correo(self, message="Por favor, llene el campo de correo electronico."):
        self.apply_blur_effect(self.centralwidget)

        msg = QDialog(self.centralwidget)
        msg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        msg.setModal(True)

        layout = QVBoxLayout(msg)

        icon_label = QLabel()
        icon = msg.style().standardIcon(QStyle.SP_MessageBoxWarning)
        icon_label.setPixmap(icon.pixmap(32, 32))

        text_label = QLabel(message)
        text_label.setAlignment(Qt.AlignCenter)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(msg.accept)

        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        layout.addWidget(text_label)
        layout.addWidget(ok_button, alignment=Qt.AlignHCenter)

        msg.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                msg.sizeHint(),
                self.centralwidget.geometry()
            )
        )

        msg.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #2C3E50;
                border-radius: 10px;
            }
            QLabel {
                color: #2C3E50;
                font-size: 20px;
                padding: 10px;
            }
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)

        msg.exec_()
        self.remove_blur_effect(self.centralwidget)

    def mensaje_advertencia(self):
        self.apply_blur_effect(self.centralwidget)
        
        msg = QDialog(self.centralwidget)
        msg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        msg.setModal(True)
        
        layout = QVBoxLayout(msg)
        
        icon_label = QLabel()
        icon = msg.style().standardIcon(QStyle.SP_MessageBoxWarning)
        icon_label.setPixmap(icon.pixmap(32, 32))
        
        text_label = QLabel("Por favor, seleccione un monto antes de continuar.")
        text_label.setAlignment(Qt.AlignCenter)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(msg.accept)
        
        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        layout.addWidget(text_label)
        layout.addWidget(ok_button, alignment=Qt.AlignHCenter)
        
        msg.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                msg.sizeHint(),
                self.centralwidget.geometry()
            )
        )
        
        msg.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #2C3E50;
                border-radius: 10px;
            }
            QLabel {
                color: #2C3E50;
                font-size: 20px;
                padding: 10px;
            }
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
      
        msg.exec_()
        self.remove_blur_effect(self.centralwidget)

    def apply_blur_effect(self, widget):
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(0)
        widget.setGraphicsEffect(self.blur_effect)
        
        self.blur_animation = QPropertyAnimation(self.blur_effect, b"blurRadius")
        self.blur_animation.setDuration(300)
        self.blur_animation.setStartValue(0)
        self.blur_animation.setEndValue(5)
        self.blur_animation.start()

    def remove_blur_effect(self, widget):
        if hasattr(self, 'blur_animation'):
            self.blur_animation.setDirection(QPropertyAnimation.Backward)
            self.blur_animation.finished.connect(lambda: widget.setGraphicsEffect(None))
            self.blur_animation.start()
        
    def close_dialog_and_remove_blur(self, dialog):
        dialog.close()
        self.remove_blur_effect(self.centralwidget)

    def obtener_monto_seleccionado(self):
        if self.monto1.isChecked():
            return "5"
        elif self.monto2.isChecked():
            return "10"
        elif self.monto3.isChecked():
            return "20"
        elif self.monto4.isChecked():
            return "30"
        elif self.monto5.isChecked():
            return "50"
        elif self.monto6.isChecked():
            return "100"
        else:
            return "0"  

    def abrir_iframe(self, dialog):
        dialog.close()
        self.remove_blur_effect(self.centralwidget)
        self.iframe_window = Iframe()
        
        main_window_rect = self.centralwidget.geometry()
        main_window_center = main_window_rect.center()
        
        iframe_x = main_window_center.x() - (self.iframe_window.width() // 2)
        iframe_y = main_window_center.y() - (self.iframe_window.height() // 2)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        iframe_x = max(screen_geometry.left(), min(iframe_x, screen_geometry.right() - self.iframe_window.width()))
        iframe_y = max(screen_geometry.top(), min(iframe_y, screen_geometry.bottom() - self.iframe_window.height()))

        self.iframe_window.move(iframe_x, iframe_y)
        self.apply_blur_effect(self.centralwidget)

        self.iframe_window.closeEvent = self.on_iframe_close

        self.iframe_window.show()

    def on_iframe_close(self, event):
        self.remove_blur_effect(self.centralwidget)
        event.accept()

    def apply_blur_effect(self, widget):
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(0)
        widget.setGraphicsEffect(self.blur_effect)
        
        self.blur_animation = QPropertyAnimation(self.blur_effect, b"blurRadius")
        self.blur_animation.setDuration(300)
        self.blur_animation.setStartValue(0)
        self.blur_animation.setEndValue(5)
        self.blur_animation.start()

    def remove_blur_effect(self, widget):
        if hasattr(self, 'blur_animation'):
            self.blur_animation.setDirection(QPropertyAnimation.Backward)
            self.blur_animation.finished.connect(lambda: widget.setGraphicsEffect(None))
            self.blur_animation.start()

    def add_svg_icon(self, button, svg_content):
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        pixmap = QPixmap(30, 30)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter, QRectF(pixmap.rect()))
        painter.end()
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(30, 30))
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tituloPasos.setText(QCoreApplication.translate("MainWindow", u" Recarga en 3 Simples Pasos :", None))
        self.paso1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.paso1Text.setText(QCoreApplication.translate("MainWindow", u"Selecciona el Monto a Recargar", None))
        self.paso2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.paso2Text.setText(QCoreApplication.translate("MainWindow", u"Introduce tus Datos para la Factura", None))
        self.paso3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.paso3Text.setText(QCoreApplication.translate("MainWindow", u"Presiona Recargar tu tarjeta", None))
        self.tipoTarjeta.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.estado.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.uid.setText(QCoreApplication.translate("MainWindow", u"UID:", None))
        self.saldo.setText(QCoreApplication.translate("MainWindow", u"  ", None))
        self.monedaSaldo.setText(QCoreApplication.translate("MainWindow", u" Bs ", None))
        self.pasoTituloMontos.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.tituloMontos.setText(QCoreApplication.translate("MainWindow", u"Elige el monto de tu recarga", None))
        self.monto1.setText(QCoreApplication.translate("MainWindow", u"Bs \n 5 ", None))
        self.monto2.setText(QCoreApplication.translate("MainWindow", u"Bs \n 10 ", None))
        self.monto3.setText(QCoreApplication.translate("MainWindow", u"Bs \n 20 ", None))
        self.monto4.setText(QCoreApplication.translate("MainWindow", u"Bs \n 30 ", None))
        self.monto5.setText(QCoreApplication.translate("MainWindow", u"Bs \n 50 ", None))
        self.monto6.setText(QCoreApplication.translate("MainWindow", u"Bs \n 100 ", None))
        self.DocIenRaButt.setText(QCoreApplication.translate("MainWindow", u"Documento de Identidad", None))
        self.NitRadButt.setText(QCoreApplication.translate("MainWindow", u"NIT", None))
        self.TituloFactura.setText(QCoreApplication.translate("MainWindow", u"Ingresa los datos para tu factura", None))
        self.pasoTituloFactura.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.tituloPrincipal.setText(QCoreApplication.translate("MainWindow", u"RECARGA TU CREDITO", None))
        self.volver.setText(QCoreApplication.translate("MainWindow", u"  Atras", None))
        self.recargaOk.setText(QCoreApplication.translate("MainWindow", u"  Recargar tu Tarjeta", None))
        self.DocumentoIden.setText(QCoreApplication.translate("MainWindow", u"Documento de Identidad", None))
        self.Complemento.setText(QCoreApplication.translate("MainWindow", u"Complemento", None))
        self.Correo.setText(QCoreApplication.translate("MainWindow", u"Correo", None))
        self.RazonSocial.setText(QCoreApplication.translate("MainWindow", u"Razon social", None))
        
        volver_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" x2="9" y1="12" y2="12"/>
        </svg>
        '''
        volver_icon_color = "#FFFFFF"  
        volver_svg_content = volver_svg_template.format(color=volver_icon_color)

        volver_svg_renderer = QSvgRenderer(QByteArray(volver_svg_content.encode()))
        volver_pixmap = QPixmap(40, 40)
        volver_pixmap.fill(Qt.transparent)
        volver_painter = QPainter(volver_pixmap)
        volver_svg_renderer.render(volver_painter)
        volver_painter.end()

        volver_icon = QIcon(volver_pixmap)
        self.volver.setIcon(volver_icon)
        self.volver.setIconSize(QSize(40, 40))
        
        recargaOk_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-hand-coins">
            <path d="M11 15h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 17"/>
            <path d="m7 21 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/>
            <path d="m2 16 6 6"/>
            <circle cx="16" cy="9" r="2.9"/><circle cx="6" cy="5" r="3"/>
        </svg>
        '''
        recargaOk_icon_color = "#FFFFFF"  
        recargaOk_svg_content = recargaOk_svg_template.format(color=recargaOk_icon_color)

        recargaOk_svg_renderer = QSvgRenderer(QByteArray(recargaOk_svg_content.encode()))
        recargaOk_pixmap = QPixmap(40, 40)
        recargaOk_pixmap.fill(Qt.transparent)
        recargaOk_painter = QPainter(recargaOk_pixmap)
        recargaOk_svg_renderer.render(recargaOk_painter)
        recargaOk_painter.end()

        recargaOk_icon = QIcon(recargaOk_pixmap)
        self.recargaOk.setIcon(recargaOk_icon)
        self.recargaOk.setIconSize(QSize(40, 40))
     
    def toggle_documento_identidad(self, checked):
        if checked:
            self.NumeroCiEdit.show()
            self.DocumentoIden.show()
            self.IconoDocIden.show()
            self.IconoComple.show()
            self.IconoNit.hide()
            
            self.DocumentoIden.setGeometry(QRect(700, 583.1, 253.4, 23.8))
            self.NumeroCiEdit.setGeometry(QRect(696, 618.8, 220, 47))
            self.IconoDocIden.setGeometry(QRect(550, 95.2, 58, 48))
            
            self.Complemento.setText("Complemento")
            self.Complemento.show()
            self.Complemento.setGeometry(QRect(1020, 583.1, 253.4, 23.8))
            self.ComplementoEdit.setGeometry(QRect(1040, 618.8, 120, 47))
            self.ComplementoEdit.show()
            self.IconoComple.setGeometry(QRect(903, 95.2, 58, 48))
            
            self.RazonSocial.setGeometry(QRect(700, 690.2, 254.3, 23.8))
            self.RazonSocialEdit.setGeometry(QRect(696, 725.9, 365, 47))
            self.IconoRazonSoc.setGeometry(QRect(550, 203, 58, 48))
            self.Correo.setGeometry(QRect(700, 797.3, 253.4, 23.8))
            self.IconoCorreo.setGeometry(QRect(550, 313, 58, 48))
            
       
    def toggle_monto_buttons(self, button):
        buttons = [self.monto1, self.monto2, self.monto3, self.monto4, self.monto5, self.monto6]
        for btn in buttons:
           if btn != button:
                btn.setChecked(False)
        button.setChecked(True)      
        
                
    def toggle_nit(self, checked):
        if checked:
            self.NumeroCiEdit.show()
            self.DocumentoIden.hide()
            self.IconoDocIden.hide()
            self.IconoComple.hide()
            self.IconoNit.show()
            
            self.Complemento.hide()
            self.ComplementoEdit.hide()
            
            self.DocumentoIden.setText("NIT")
            self.DocumentoIden.show()
            self.DocumentoIden.setGeometry(QRect(700, 583.1, 253.4, 23.8))
            self.NumeroCiEdit.setGeometry(QRect(696, 618.8, 365.4, 47))
            self.IconoNit.setGeometry(QRect(550, 96, 58, 48))
            
            self.RazonSocial.setGeometry(QRect(700, 690.2, 254.3, 23.8))
            self.RazonSocialEdit.setGeometry(QRect(696, 725.9, 365, 47))
            self.IconoRazonSoc.setGeometry(QRect(550, 203, 58, 48))
            self.Correo.setGeometry(QRect(700, 797.3, 253.4, 23.8))
            self.IconoCorreo.setGeometry(QRect(550, 313, 58, 48))
            
  
    # retranslateUi