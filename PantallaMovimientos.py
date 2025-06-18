from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import QSvgRenderer
import os
from smartcard.Card import Card
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
from PySide2.QtWidgets import *
from PySide2.QtGui import QPixmap
from NFCHandler import Lectura
from estilos_generales import (ENCABEZADO_COLOR_PRIMARIO,BOTONES_ACCIONES,
                               BOTONES_ACCIONES_HOVER,BOTONES_ACCIONES_PRESSED,GRADIENTE_INICIO,GRADIENTE_FINAL)

class Ui_Movimientos(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 1024)
        MainWindow.setFixedSize(1280, 1024)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.fondoUltimosMov = QFrame(self.centralwidget)
        self.fondoUltimosMov.setObjectName(u"fondoUltimosMov")
        self.fondoUltimosMov.setGeometry(QRect(0, 0, 1280, 1024))
        self.fondoUltimosMov.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"                            stop:0 #E0E0E0, stop:1 #F5F5F5);")
        self.fondoUltimosMov.setFrameShape(QFrame.StyledPanel)
        self.fondoUltimosMov.setFrameShadow(QFrame.Raised)
        
        self.fondoTabla = QFrame(self.fondoUltimosMov)
        self.fondoTabla.setObjectName(u"fondoTabla")
        self.fondoTabla.setGeometry(QRect(50, int(400/1024*1024), int(1170/1280*1280), int(600/1024*1024)))
        self.fondoTabla.setStyleSheet(u"background-color: #E9EDF0;\n"
"border: 2px solid #AEB6BF;\n"
"border-radius: 10px;\n"
"border: 2px solid #AEB6BF;\n"
"box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);")
        self.fondoTabla.setFrameShape(QFrame.StyledPanel)
        self.fondoTabla.setFrameShadow(QFrame.Raised)
        
        self.movimientos = QTableWidget(self.fondoTabla)
        if (self.movimientos.columnCount() < 8):
            self.movimientos.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.movimientos.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.movimientos.rowCount() < 15):
            self.movimientos.setRowCount(15)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9= QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10= QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11= QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(5, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(6, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(7, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(8, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(9, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(10, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(11, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(12, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(13, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.movimientos.setVerticalHeaderItem(14, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()

        __qtablewidgetitem23.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.movimientos.setItem(0, 0, __qtablewidgetitem23)
        self.movimientos.setObjectName(u"movimientos")
        self.movimientos.setGeometry(QRect(45, 35, int(1080/1280*1280), int(478/1024*1024)))
        self.movimientos.setRowCount(15)
        self.movimientos.setColumnCount(8)
        altura_fila = int((self.movimientos.height() - self.movimientos.horizontalHeader().height()) / 8)
        for i in range(40):
                self.movimientos.setRowHeight(i, altura_fila)
        self.setAnchosColumnasProporcionales()
        self.movimientos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.movimientos.setSelectionMode(QAbstractItemView.NoSelection)

        header = self.movimientos.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #34495E;
                color: #ECF0F1;
                padding: 5px;
                border: none;
                border-right: 1px solid #7F8C8D;
                border-bottom: 3px solid #2C3E50;
                font-weight: bold;
                font-size: 18px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QHeaderView::section:hover {
                background-color: #2980B9;
            }
            QHeaderView::section:nth-child(1) { background-color: #27AE60; }
            QHeaderView::section:nth-child(2) { background-color: #8E44AD; }
            QHeaderView::section:nth-child(3) { background-color: #E74C3C; }
            QHeaderView::section:nth-child(4) { background-color: #F39C12; }
            QHeaderView::section:nth-child(5) { background-color: #3498DB; }
            QHeaderView::section:nth-child(6) { background-color: #1ABC9C; }
            QHeaderView::section:nth-child(7) { background-color: #1ABC9C; }
        """)

        vertical_header = self.movimientos.verticalHeader()
        vertical_header.setStyleSheet("""
            QHeaderView::section {
                background-color: #2C3E50;
                color: #ECF0F1;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #34495E;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                qproperty-alignment: AlignCenter;
            }
            QHeaderView::section:hover {
                background-color: #34495E;
            }
        """)

        table_style = """
            QTableWidget#movimientos {
                background-color: #FFFFFF;
                border: 2px solid #BDC3C7;  
                border-radius: 15px;
                gridline-color: #E0E0E0;
                alternate-background-color: #ECF0F1; 
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 19px;            
            }
            QTableWidget::item {
                border: none;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: transparent;
            }
        """
        scrollbar_style = """
            QScrollBar:vertical {
                border: none;
                background: #2C3E50;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #34495E;
                min-height: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #3498DB;
            }

            QScrollBar::sub-line:vertical {
                border: none;
                background-color: #2C3E50;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical {
                border: none;
                background-color: #2C3E50;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                border: none;
                background: #2C3E50;
                height: 14px;
                margin: 0px 15px 0 15px;
                border-radius: 0px;
            }

            QScrollBar::handle:horizontal {
                background-color: #34495E;
                min-width: 30px;
                border-radius: 7px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #3498DB;
            }

            QScrollBar::sub-line:horizontal {
                border: none;
                background-color: #2C3E50;
                width: 15px;
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:horizontal {
                border: none;
                background-color: #2C3E50;
                width: 15px;
                border-top-right-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }

            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                background: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """
        self.movimientos.setStyleSheet(table_style + scrollbar_style)
       
        self.tarjeta = QWidget(self.fondoUltimosMov)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setGeometry(QRect(370, 120, 550, 250))
        self.tarjeta.setStyleSheet(f"""
    QWidget#tarjeta {{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                            stop: 0 {GRADIENTE_INICIO}, stop: 1 {GRADIENTE_FINAL});
        border-radius: 15px;
        color: white;
    }}
""")
        
        self.IconoLogo = QLabel(self.tarjeta)
        self.IconoLogo.setObjectName(u"iconoLogo")
        self.IconoLogo.setGeometry(QRect(460, 158, 70, 70))
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
        self.tipoTarjeta.setGeometry(QRect(30, 20, 280, 40))
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
        self.estado.setGeometry(QRect(410, 15, 200, 40))
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
        self.uid.setGeometry(QRect(30, 147, 350, 40))
        self.uid.setStyleSheet(u"""
        QLabel#uid {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: bold;
        }
        """)
       
        self.nombre = QLabel(self.tarjeta)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setGeometry(QRect(30, 187, 400, 40))
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
        self.saldo.setGeometry(QRect(190, 70, 200, 50))
        self.saldo.setStyleSheet(u"""
            QLabel#saldo {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 50px;
        font-weight: bold;
            }
        """)
        
        self.monedaSaldo = QLabel(self.tarjeta)
        self.monedaSaldo.setObjectName(u"moneda")
        self.monedaSaldo.setGeometry(QRect(335, 90, 100, 50))
        self.monedaSaldo.setStyleSheet(u"""
            QLabel#moneda {
        background-color: transparent;
        color: #FFFFFF;
        font-size: 27px;
        font-weight: bold;
            }
        """)
        
        self.encabezado = QFrame(self.fondoUltimosMov)
        self.encabezado.setObjectName(u"encabezado")
        self.encabezado.setGeometry(QRect(0, 20, 1280, 80))
        self.encabezado.setStyleSheet(f"""
            QFrame#encabezado {{
                background-color: {ENCABEZADO_COLOR_PRIMARIO};
                border: none;
                border-radius: 20px;
                padding: 15px;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 20px;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
        """)
        self.encabezado.setFrameShape(QFrame.StyledPanel)
        self.encabezado.setFrameShadow(QFrame.Raised)
        
        self.titulo = QLabel(self.encabezado)
        self.titulo.setObjectName(u"titulo")    
        self.titulo.setGeometry(QRect(0, 0, 1280, 80))
        self.titulo.setStyleSheet(u"QLabel#titulo {\n"
"    color: #FFFFFF; \n"
"    font-family: 'Arial Black', sans-serif; \n"
"    font-size: 25px;\n"
"    font-weight: bold; \n"
"    padding: 5px;\n"
"    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); \n"
"    letter-spacing: 1px; \n"
"    text-transform: uppercase;\n"
"	 background : none; \n"
"    qproperty-alignment: AlignCenter;"
"}")
       
        self.atras = QPushButton(self.fondoUltimosMov)
        self.atras.setObjectName(u"atras")
        self.atras.setGeometry(QRect(540, 930, 220, 50))
        self.atras.clicked.connect(MainWindow.close)
        self.atras.setStyleSheet(f"""
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
        
        self.etiqueta_nombre = self.nombre
        self.etiqueta_uid = self.uid
        self.etiqueta_saldo = self.saldo
        self.etiqueta_tipoTarjeta = self.tipoTarjeta
        self.etiqueta_estado = self.estado
        
        self.init_nfc_reader()

        if hasattr(self, 'nfc_reader'):
            self.nfc_reader.tabla_movimientos = self.movimientos
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    
    def init_nfc_reader(self):
        try:
            self.nfc_reader = Lectura(self.movimientos)
            self.cardmonitor = CardMonitor()
            self.cardmonitor.addObserver(self.nfc_reader)
            
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_ui)
            self.update_timer.start(1000)  
            
        except Exception as e:
            print(f"Error al inicializar el lector NFC: {e}")
            
    def update_ui(self):
        if hasattr(self, 'nfc_reader') and self.nfc_reader.is_data_ready():
            card_data = self.nfc_reader.get_card_data()
            if card_data:
                self.actualizar_etiquetas(card_data)

                self.movimientos.viewport().update()            
            
    def check_card_data(self):

        if hasattr(self, 'nfc_reader') and self.nfc_reader.is_data_ready():
            card_data = self.nfc_reader.get_card_data()
            if card_data:
                self.actualizar_etiquetas(card_data)

    def closeEvent(self, event):
        if hasattr(self, 'cardmonitor') and hasattr(self, 'nfc_reader'):
            self.cardmonitor.deleteObserver(self.nfc_reader)
        event.accept()
        
    def actualizar_etiquetas(self, datos_tarjeta):
        if datos_tarjeta:
            nombre_completo = f"{datos_tarjeta.get('name', '')} {datos_tarjeta.get('last_name', '')}".strip()
            self.nombre.setText(nombre_completo)
            self.uid.setText(f"UID: {datos_tarjeta.get('uid', '')}")
            self.saldo.setText(str(datos_tarjeta.get('balance', '')))
            self.tipoTarjeta.setText(datos_tarjeta.get('profile_name', ''))
            self.estado.setText(datos_tarjeta.get('card_status', ''))

    def setAnchosColumnasProporcionales(self):
        header = self.movimientos.horizontalHeader()

        anchos_columnas = [120, 100, 2, 190, 220, 90, 100, 120] 

        header.setStretchLastSection(False)

        for i, ancho in enumerate(anchos_columnas):
            header.setSectionResizeMode(i, QHeaderView.Fixed)
            self.movimientos.setColumnWidth(i, ancho)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtablewidgetitem = self.movimientos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"FECHA", None));
        ___qtablewidgetitem1 = self.movimientos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"HORA", None));
        ___qtablewidgetitem2 = self.movimientos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"", None));
        ___qtablewidgetitem3 = self.movimientos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"LINEA", None));
        ___qtablewidgetitem4 = self.movimientos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"ESTACION", None));
        ___qtablewidgetitem5 = self.movimientos.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"MONTO", None))
        ___qtablewidgetitem6 = self.movimientos.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"SALDO", None));
        ___qtablewidgetitem7 = self.movimientos.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"ACCION", None));
        ___qtablewidgetitem8 = self.movimientos.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"  1", None));
        ___qtablewidgetitem9 = self.movimientos.verticalHeaderItem(1) 
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"  2", None));
        ___qtablewidgetitem10 = self.movimientos.verticalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"  3", None));
        ___qtablewidgetitem11 = self.movimientos.verticalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"  4", None));
        ___qtablewidgetitem12 = self.movimientos.verticalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"  5", None));
        ___qtablewidgetitem13 = self.movimientos.verticalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"  6", None));
        ___qtablewidgetitem14 = self.movimientos.verticalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"  7", None));
        ___qtablewidgetitem15 = self.movimientos.verticalHeaderItem(7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"  8", None));
        ___qtablewidgetitem16 = self.movimientos.verticalHeaderItem(8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"  9", None));
        ___qtablewidgetitem17 = self.movimientos.verticalHeaderItem(9)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u" 10", None));
        ___qtablewidgetitem18 = self.movimientos.verticalHeaderItem(10)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u" 11", None));
        ___qtablewidgetitem19 = self.movimientos.verticalHeaderItem(11)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u" 12", None));
        ___qtablewidgetitem20 = self.movimientos.verticalHeaderItem(12)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u" 13", None));
        ___qtablewidgetitem21 = self.movimientos.verticalHeaderItem(13)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u" 14", None));
        ___qtablewidgetitem22 = self.movimientos.verticalHeaderItem(14)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u" 15", None));

        __sortingEnabled = self.movimientos.isSortingEnabled()
        self.movimientos.setSortingEnabled(False)
        self.movimientos.setSortingEnabled(__sortingEnabled)

        self.tipoTarjeta.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.estado.setText(QCoreApplication.translate("MainWindow", u" ", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.uid.setText(QCoreApplication.translate("MainWindow", u"UID:", None))
        self.saldo.setText(QCoreApplication.translate("MainWindow", u"  ", None))
        self.monedaSaldo.setText(QCoreApplication.translate("MainWindow", u" Bs ", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"TUS MOVIMIENTOS MAS RECIENTES", None))
        self.atras.setText(QCoreApplication.translate("MainWindow", u"  ATRAS", None))
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(current_dir, 'imagenes2')

        atras_svg_template = '''
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" x2="9" y1="12" y2="12"/>
        </svg>
        '''
        atras_icon_color = "#FFFFFF" 
        atras_svg_content = atras_svg_template.format(color=atras_icon_color)

        atras_svg_renderer = QSvgRenderer(QByteArray(atras_svg_content.encode()))
        atras_pixmap = QPixmap(40, 40)
        atras_pixmap.fill(Qt.transparent)
        atras_painter = QPainter(atras_pixmap)
        atras_svg_renderer.render(atras_painter)
        atras_painter.end()
        atras_icon = QIcon(atras_pixmap)
        self.atras.setIcon(atras_icon)
        self.atras.setIconSize(QSize(30, 30))

