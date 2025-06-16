from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import QPixmap
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtGui import QPainter, QPixmap, QColor, QPen
from PySide2.QtCore import QByteArray, Qt, QRectF
from PySide2.QtWidgets import QGraphicsBlurEffect
from PySide2.QtCore import QPropertyAnimation
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import (QDialog, QVBoxLayout, QFrame, QLabel, QProgressBar, 
                               QApplication, QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PySide2.QtGui import QColor
import os
import re
from datos_qr import solicitar_recarga
from nfc_monitor import NFCMonitorSingleton
from estilos_generales import (ENCABEZADO_COLOR_PRIMARIO,BOTONES_ACCIONES,
                               BOTONES_ACCIONES_HOVER,BOTONES_ACCIONES_PRESSED,GRADIENTE_INICIO,GRADIENTE_FINAL)

class VirtualKeyboard(QDialog):
    def __init__(self, parent=None, target_widget=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.shift_pressed = False
        self.caps_lock = False
        self.key_buttons = []
        self.is_closing = False
        self.manually_closed_signal = None
        self.setupUI()
        
        self.installEventFilter(self)
        QApplication.instance().installEventFilter(self)
        
    def setupUI(self):
        self.setWindowTitle("Teclado Virtual")
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(450, 280)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 12px;
                border: 2px solid #3498db;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5d6d7e, stop:1 #34495e);
                color: white;
                border: 1px solid #7f8c8d;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 2px;
                min-width: 28px;
                min-height: 28px;
                margin: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7f8c8d, stop:1 #5d6d7e);
                border: 1px solid #3498db;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #3498db);
                border: 1px solid #85c1e9;
            }
            QPushButton[special="true"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                font-size: 10px;
            }
            QPushButton[special="true"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton[special="true"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1b4f72, stop:1 #2980b9);
            }
            QPushButton[close="true"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                font-size: 11px;
                font-weight: bold;
                color: white;
            }
            QPushButton[close="true"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
            QPushButton[close="true"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a93226, stop:1 #922b21);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(6, 6, 6, 6)
        row1_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '⌫']
        row1_layout = self.create_row(row1_keys, key_width=30)
        layout.addLayout(row1_layout)
        row2_keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
        row2_layout = self.create_row(row2_keys, key_width=30)
        layout.addLayout(row2_layout)
        row3_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', ';', "'"]
        row3_layout = self.create_row(row3_keys, key_width=30)
        layout.addLayout(row3_layout)
        row4_keys = ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
        row4_layout = self.create_row(row4_keys, key_width=30)
        layout.addLayout(row4_layout)
        row5_keys = ['@', '#', '$', '%', '&', '*', '(', ')', '_', '+', '{', '}']
        row5_layout = self.create_row(row5_keys, key_width=30)
        layout.addLayout(row5_layout)
        row6_layout = QHBoxLayout()
        row6_layout.setSpacing(2)
        self.space_btn = QPushButton("Espacio")
        self.space_btn.setProperty("special", "true")
        self.space_btn.setFixedSize(200, 28)
        self.space_btn.clicked.connect(self.space_pressed)
        row6_layout.addWidget(self.space_btn)
        row6_layout.addSpacing(10)
        self.close_btn = QPushButton("✕ CERRAR")
        self.close_btn.setProperty("close", "true")
        self.close_btn.setFixedSize(100, 28)
        self.close_btn.clicked.connect(self.close_keyboard_from_button)  
        row6_layout.addWidget(self.close_btn)
        
        layout.addLayout(row6_layout)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if not self.is_closing:
                if not self.geometry().contains(event.globalPos()):
                    if self.target_widget:
                        target_global_rect = QRect(
                            self.target_widget.mapToGlobal(self.target_widget.rect().topLeft()),
                            self.target_widget.size()
                        )
                        if not target_global_rect.contains(event.globalPos()):
                            QTimer.singleShot(50, self.close_keyboard_manually)
                    else:
                        QTimer.singleShot(50, self.close_keyboard_manually)
        
        return super().eventFilter(obj, event)
    
    def create_row(self, keys, key_width=30):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(1)
        
        for key in keys:
            if key == '⌫':
                btn = QPushButton(key)
                btn.setProperty("special", "true")
                btn.setFixedSize(key_width + 10, 28)
                btn.clicked.connect(self.backspace)
            elif key == 'Enter':
                btn = QPushButton(key)
                btn.setProperty("special", "true")
                btn.setFixedSize(key_width + 15, 28)
                btn.clicked.connect(self.enter_pressed)
            elif key == 'Shift':
                btn = QPushButton(key)
                btn.setProperty("special", "true")
                btn.setFixedSize(key_width + 15, 28)
                btn.setCheckable(True)
                btn.toggled.connect(self.toggle_shift)
                self.shift_btn = btn
            elif key == '↑':
                btn = QPushButton(key)
                btn.setProperty("special", "true")
                btn.setFixedSize(key_width, 28)
                btn.clicked.connect(self.move_cursor_up)
            else:
                btn = QPushButton(key.upper() if self.shift_pressed or self.caps_lock else key)
                btn.setFixedSize(key_width, 28)
                btn.clicked.connect(lambda checked=False, k=key: self.key_pressed(k))
                btn.original_key = key
                self.key_buttons.append(btn)
            
            row_layout.addWidget(btn)
            
        return row_layout
    
    def key_pressed(self, key):
        if key.isalpha():
            char = key.upper() if self.shift_pressed or self.caps_lock else key
        else:
            shift_chars = {
                '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
                '-': '_', '=': '+', '[': '{', ']': '}',
                ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
                '\\': '|'
            }
            if self.shift_pressed and key in shift_chars:
                char = shift_chars[key]
            else:
                char = key
                
        self.insert_text(char)
        
        if self.shift_pressed and not self.caps_lock:
            self.shift_pressed = False
            if hasattr(self, 'shift_btn'):
                self.shift_btn.setChecked(False)
            self.update_key_labels()
    
    def space_pressed(self):
        self.insert_text(" ")
    
    def enter_pressed(self):
        self.insert_text("\n")
    
    def toggle_shift(self, checked):
        self.shift_pressed = checked
        self.update_key_labels()
        
    def toggle_caps(self, checked):
        self.caps_lock = checked
        self.update_key_labels()
    
    def move_cursor_left(self):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.target_widget.setTextCursor(cursor)
    
    def move_cursor_right(self):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.movePosition(QTextCursor.Right)
            self.target_widget.setTextCursor(cursor)
    
    def move_cursor_up(self):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.movePosition(QTextCursor.Up)
            self.target_widget.setTextCursor(cursor)
    
    def move_cursor_down(self):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.movePosition(QTextCursor.Down)
            self.target_widget.setTextCursor(cursor)
        
    def update_key_labels(self):
        for btn in self.key_buttons:
            if hasattr(btn, 'original_key'):
                key = btn.original_key
                if key.isalpha():
                    if self.shift_pressed or self.caps_lock:
                        btn.setText(key.upper())
                    else:
                        btn.setText(key.lower())
                else:
                    shift_chars = {
                        '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                        '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
                        '-': '_', '=': '+', '[': '{', ']': '}',
                        ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
                        '\\': '|'
                    }
                    if self.shift_pressed and key in shift_chars:
                        btn.setText(shift_chars[key])
                    else:
                        btn.setText(key)
    
    def insert_text(self, text):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.insertText(text)
            self.target_widget.setTextCursor(cursor)
            
    def backspace(self):
        if self.target_widget:
            cursor = self.target_widget.textCursor()
            cursor.deletePreviousChar()
            self.target_widget.setTextCursor(cursor)
    
    def close_keyboard_from_button(self):
        if not self.is_closing:
            QTimer.singleShot(50, self.close_keyboard_manually)
    
    def close_keyboard_manually(self):
        if self.is_closing:
            return
            
        if self.manually_closed_signal:
            self.manually_closed_signal()
            
        self.close_keyboard()
    
    def close_keyboard(self):
        if self.is_closing:
            return
            
        self.is_closing = True
        
        QApplication.instance().removeEventFilter(self)
        
        if self.target_widget and hasattr(self.target_widget, 'keyboard'):
            self.target_widget.keyboard = None
            
        self.close()
        self.deleteLater()
        
    def closeEvent(self, event):
        QApplication.instance().removeEventFilter(self)
        
        if self.target_widget and hasattr(self.target_widget, 'keyboard'):
            self.target_widget.keyboard = None
        event.accept()


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard = None
        self.focus_timer = QTimer()
        self.focus_timer.setSingleShot(True)
        self.focus_timer.timeout.connect(self.delayed_keyboard_check)
        self.keyboard_manually_closed = False
        
    def focusInEvent(self, event):
        super().focusInEvent(event)
        if not self.keyboard_manually_closed:
            self.show_keyboard()
        
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focus_timer.start(150)
        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.keyboard_manually_closed:
            self.keyboard_manually_closed = False
            self.show_keyboard()
        
    def delayed_keyboard_check(self):
        current_focus = QApplication.focusWidget()
        
        if isinstance(current_focus, (QPushButton, CustomTextEdit)):
            return
            
        if self.keyboard and self.keyboard.isVisible():
            keyboard_widgets = self.keyboard.findChildren(QPushButton)
            if current_focus in keyboard_widgets:
                return
                
        if not self.keyboard_manually_closed:
            self.hide_keyboard()
        
    def show_keyboard(self):
        if hasattr(self.parent(), 'close_all_keyboards'):
            self.parent().close_all_keyboards()
            
        if not self.keyboard or not self.keyboard.isVisible():
            if self.keyboard:
                self.keyboard.close()
                
            self.keyboard = VirtualKeyboard(self.parent(), self)
            self.keyboard.manually_closed_signal = self.on_keyboard_manually_closed
            self.position_keyboard_fixed()
            self.keyboard.show()
        
    def on_keyboard_manually_closed(self):
        self.keyboard_manually_closed = True
        
    def position_keyboard_fixed(self):
        if not self.keyboard:
            return
            
        parent_window = self.window()
        fixed_x = 80  
        fixed_y = 600  

        parent_pos = parent_window.mapToGlobal(QPoint(0, 0))

        final_x = parent_pos.x() + fixed_x
        final_y = parent_pos.y() + fixed_y
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        if final_x + self.keyboard.width() > screen_geometry.right():
            final_x = screen_geometry.right() - self.keyboard.width() - 10
            
        if final_x < screen_geometry.left():
            final_x = screen_geometry.left() + 10
            
        if final_y + self.keyboard.height() > screen_geometry.bottom():
            final_y = screen_geometry.bottom() - self.keyboard.height() - 10
            
        if final_y < screen_geometry.top():
            final_y = screen_geometry.top() + 10
            
        self.keyboard.move(final_x, final_y)
        
    def hide_keyboard(self):
        if self.keyboard and not self.keyboard.is_closing:
            self.keyboard.close_keyboard()
            
    def close_all_keyboards(self):
        if self.keyboard and not self.keyboard.is_closing:
            self.keyboard.close_keyboard()
            
class Ui_Recarga(QObject):
    def __init__(self):
        super().__init__()
        self.nfc_monitor = NFCMonitorSingleton.get_instance()
        self.nfc_monitor.card_removed.connect(self.handle_card_removal)
        self.nfc_monitor.card_error.connect(self.show_error_message)

    def handle_card_removal(self):
        self.show_error_message("Se ha retirado la tarjeta\nCerrando ventana de recarga...")

    def show_error_message(self, message):          
        # Mostrar mensaje de error con el estilo del monitor NFC
        self.nfc_monitor.show_auto_close_message(message)

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.nfc_monitor = NFCMonitorSingleton.get_instance()
        self.nfc_monitor.register_window(MainWindow)
        MainWindow.destroyed.connect(lambda: self.nfc_monitor.unregister_window(MainWindow))
        
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
        self.encabezado.setStyleSheet(f"""
            QFrame#encabezado {{
                background-color: {ENCABEZADO_COLOR_PRIMARIO};
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }}
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
        self.recargaOk.setStyleSheet(f"""
            QPushButton {{
                background-color: {BOTONES_ACCIONES};  
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
        self.recargaOk.clicked.connect(self.handle_recarga_ok)
        
        self.fondoMontos.raise_()
        self.fondoFactura.raise_()
        self.tituloPrincipal.raise_()
        self.volver.raise_()
        self.recargaOk.raise_()
        self.tarjeta.raise_()
        
        self.NumeroCiEdit = CustomTextEdit(self.centralwidget)
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
        
        self.ComplementoEdit = CustomTextEdit(self.centralwidget)
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
        
        self.RazonSocialEdit = CustomTextEdit(self.centralwidget)
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
        
        self.CorreoEdit = CustomTextEdit(self.centralwidget)
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

    def close_all_keyboards(self):
        for widget in [self.NumeroCiEdit, self.ComplementoEdit, 
                      self.RazonSocialEdit, self.CorreoEdit]:
            if hasattr(widget, 'hide_keyboard'):
                widget.hide_keyboard()

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

    def show_confirmation_dialog(self, uid, numero_ci, razon_social, monto, correo, complemento=""):
        self.apply_blur_effect(self.centralwidget)
        pago_dialog = QDialog(self.centralwidget)
        pago_dialog.setFixedSize(750, 500)
        pago_dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        pago_dialog.setStyleSheet("""
        QDialog {
            background-color: #F5F5F5;
            border-radius: 10px;
            border: 1px solid #CFD8DC;
        }
        """)

        # Configurar el monitor NFC para cerrar la ventana automáticamente
        try:
            from nfc_monitor import NFCMonitorSingleton
            nfc_monitor = NFCMonitorSingleton.get_instance()
            nfc_monitor.register_window(pago_dialog)
            
            # Conectar la señal de tarjeta removida para cerrar el diálogo
            def close_on_card_removal():
                print("Confirmation Dialog: Tarjeta removida detectada - Cerrando ventana de confirmación")
                self.close_dialog_and_remove_blur(pago_dialog)
            
            nfc_monitor.card_removed.connect(close_on_card_removal)
            print("Ventana de confirmación registrada con el monitor NFC")
        except Exception as e:
            print(f"Advertencia: No se pudo conectar con el monitor NFC: {e}")

        # Sobrescribir el método closeEvent del diálogo para desregistrar la ventana
        original_close_event = pago_dialog.closeEvent
        def custom_close_event(event):
            try:
                if 'nfc_monitor' in locals():
                    nfc_monitor.unregister_window(pago_dialog)
                    print("Ventana de confirmación desregistrada del monitor NFC")
            except Exception as e:
                print(f"Error al desregistrar ventana: {e}")
            
            # Llamar al método original
            original_close_event(event)
        
        pago_dialog.closeEvent = custom_close_event

        header = QLabel(pago_dialog)
        header.setGeometry(0, 0, 750, 60)
        header.setStyleSheet("background-color: #2C3E50;")
        
        title = QLabel("Solicitud de Recarga", header)
        title.setGeometry(0, 0, 750, 60)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        message = QLabel("Se está solicitando una nueva recarga \n Verifique si los datos están correctos:", pago_dialog)
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
        
        def balance_text_lines(text, max_chars_per_line=27):

            if len(text) <= max_chars_per_line:
                return text
            mid_point = len(text) // 2
            split_pos = -1
            search_range = min(8, mid_point) 
            
            for i in range(search_range):
                if mid_point - i > 0 and text[mid_point - i] == ' ':
                    split_pos = mid_point - i
                    break
                if mid_point + i < len(text) and text[mid_point + i] == ' ':
                    split_pos = mid_point + i
                    break
            if split_pos == -1:
                split_pos = text.rfind(' ', 0, max_chars_per_line)
                if split_pos == -1:
                    split_pos = max_chars_per_line
            
            line1 = text[:split_pos].strip()
            line2 = text[split_pos:].strip()
            
            return f"{line1}\n{line2}"
        
        max_chars_per_line = 27  
        invoice_data = f"{numero_ci} - {razon_social}"
        invoice_data_display = balance_text_lines(invoice_data, max_chars_per_line)

        # Etiquetas de título
        QLabel("Datos de Factura:", self.tarjeta).setGeometry(QRect(50, 30, 150, 20))
        QLabel("Monto de Recarga:", self.tarjeta).setGeometry(QRect(380, 30, 150, 20))
        QLabel("Número de Tarjeta:", self.tarjeta).setGeometry(QRect(50, 120, 150, 20))

        # Datos principales
        datosFactura_label = QLabel(invoice_data_display, self.tarjeta)
        datosFactura_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        datosFactura_label.setGeometry(QRect(50, 50, 280, 60)) 
        datosFactura_label.setWordWrap(True)
        datosFactura_label.setAlignment(Qt.AlignTop)

        monto_label = QLabel(f"Bs. {monto}", self.tarjeta)
        monto_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        monto_label.setGeometry(QRect(380, 50, 150, 30)) 

        uid_label = QLabel(f"{uid}", self.tarjeta)
        uid_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        uid_label.setGeometry(QRect(50, 140, 450, 30))  

        teleferico_label = QLabel(self.tarjeta)
        teleferico_label.setGeometry(QRect(420, 120, 80, 60))
        
        teleferico_svg = """
        <svg fill="#f3f2f2" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        stroke="#f3f2f2"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" 
        stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M45.0625 1.875L28.40625 5.96875L20.75 7.875C21.492188 
        7.582031 22 6.84375 22 6C22 4.894531 21.105469 4 20 4C18.894531 4 18 4.894531 18 6C18 7.105469 18.894531 8 20 8C20.136719 
        8 20.277344 7.996094 20.40625 7.96875L4.4375 11.9375L4.9375 13.875L24.5 9.03125C25.335938 10.523438 27.484375 15.21875 
        24.46875 20L18 20L18 22L32 22L32 20L26.71875 20C29.121094 15.222656 27.488281 10.609375 26.46875 8.53125L45.5625 3.8125 Z M 
        28.40625 5.96875C29.316406 5.78125 30 4.964844 30 4C30 2.894531 29.105469 2 28 2C26.894531 2 26 2.894531 26 4C26 5.105469
        26.894531 6 28 6C28.136719 6 28.277344 5.996094 28.40625 5.96875 Z M 13.34375 24L13.0625 24.28125C13.0625 24.28125 
        12 25.328125 11 27.28125C10 29.234375 9 32.164063 9 36C9 39.835938 10 42.765625 11 44.71875C12 46.671875 13.0625
        47.71875 13.0625 47.71875L13.34375 48L36.65625 48L36.96875 47.71875C36.96875 47.71875 41 43.570313 41 36C41 28.429688
        36.96875 24.28125 36.96875 24.28125L36.65625 24 Z M 14.25 26L24 26L24 35L11.03125 35C11.175781 32.007813 11.960938 
        29.765625 12.75 28.21875C13.527344 26.699219 14.097656 26.15625 14.25 26 Z M 26 26L35.71875 26C36.039063 26.332031 
        38.691406 29.171875 38.96875 35L26 35 Z M 11.03125 37L38.96875 37C38.691406 42.828125 36.039063 45.667969 35.71875
        46L14.25 46C14.097656 45.84375 13.527344 45.300781 12.75 43.78125C11.960938 42.234375 11.175781 39.992188 11.03125 37Z">
        </path></g></svg>
        """
        try:
            svg_renderer = QSvgRenderer(QByteArray(teleferico_svg.encode()))
            pixmap = QPixmap(80, 60)
            pixmap.fill(Qt.transparent) 
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing) 
            svg_renderer.render(painter)
            painter.end()
            teleferico_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error al renderizar SVG: {e}")
            teleferico_label.setText("🚠")
            teleferico_label.setStyleSheet("color: white; font-size: 24px;")
            teleferico_label.setAlignment(Qt.AlignCenter)

        for label in self.tarjeta.findChildren(QLabel)[:3]: 
            label.setStyleSheet("color: #BDC3C7; font-size: 18px; font-weight: normal;")
            
        Cancelar = QPushButton("  Cancelar", pago_dialog)
        Cancelar.setFixedSize(200, 50)
        Cancelar.setStyleSheet("""
        QPushButton {
            background-color: #E74C3C;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #C0392B;
        }
        """)
        Cancelar.setGeometry(105, 400, 250, 50)
        Cancelar.clicked.connect(lambda: self.close_dialog_and_remove_blur(pago_dialog))
        
        cancel_svg = """
        <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="#ffffff"/>
        </svg>
        """
        # icono SVG al botón Cancelar
        self.add_svg_icon(Cancelar, cancel_svg)
        
        PagoTarjeta = QPushButton("Solicitar Recarga", pago_dialog)
        PagoTarjeta.setFixedSize(250, 50)
        PagoTarjeta.setStyleSheet("""
        QPushButton {
            background-color: #27AE60;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2ECC71;
        }
        """)
        PagoTarjeta.setGeometry(410, 400, 250, 50)
        
        PagoTarjeta.clicked.connect(lambda: self.procesar_recarga(
            pago_dialog, uid, numero_ci, razon_social, complemento, correo, monto
        ))
        
        card_svg = """
        <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z" fill="#f8f1f1"/>
        </svg>
        """
        # icono SVG al botón PagoTarjeta
        self.add_svg_icon(PagoTarjeta, card_svg)

        pago_dialog.exec_()
    
    def procesar_recarga(self, dialog, uid, numero_ci, razon_social, complemento, correo, monto):
        dialog.close()
        self.apply_blur_effect(self.centralwidget)
        result = solicitar_recarga(
            uid, 
            numero_ci, 
            razon_social, 
            complemento, 
            correo, 
            monto, 
            self.centralwidget
        )
        
        self.remove_blur_effect(self.centralwidget)
        
        if result:  
            self.show_payment_confirmation()
        
        return result
        
    def show_payment_confirmation(self):
            self.apply_blur_effect(self.centralwidget)

            dialog = QDialog(self.MainWindow)
            dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            dialog.setModal(True)
            dialog.setFixedSize(500, 420)
            
            parent_geometry = self.MainWindow.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - 500) // 2
            y = parent_geometry.y() + (parent_geometry.height() - 420) // 2

            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            main_frame = QFrame()
            main_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f8f9fa, stop:1 #e9ecef);
                    border-radius: 24px;
                    border: 1px solid #dee2e6;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                }
            """)
            layout.addWidget(main_frame)
            frame_layout = QVBoxLayout(main_frame)
            frame_layout.setContentsMargins(50, 50, 50, 50)
            frame_layout.setSpacing(30)

            icon_container = QFrame()
            icon_container.setFixedSize(100, 100)
            icon_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #4CAF50, stop:1 #45a049);
                    border-radius: 50px;
                    border: none;
                }
            """)

            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel("✓")
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 48px;
                    font-weight: bold;
                    background: none;
                    border: none;
                }
            """)
            icon_layout.addWidget(icon_label)
            
            icon_center_layout = QHBoxLayout()
            icon_center_layout.addStretch()
            icon_center_layout.addWidget(icon_container)
            icon_center_layout.addStretch()
            frame_layout.addLayout(icon_center_layout)

            title_label = QLabel("¡Recarga Exitosa!")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFixedHeight(70)  
            title_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 34px;
                    font-weight: 700;
                    background: none;
                    border: none;
                    margin: 5px 0;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    padding: 8px 0;
                }
            """)
            frame_layout.addWidget(title_label)

            message_label = QLabel("La transaccion se completo correctamete. \nSu saldo esta siendo actualizado.")
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setFixedHeight(60)  
            message_label.setStyleSheet("""
                QLabel {
                    color: #6c757d;
                    font-size: 16px;
                    background: none;
                    border: none;
                    line-height: 26px;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    font-weight: 400;
                    padding: 10px 0;
                }
            """)
            frame_layout.addWidget(message_label)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFixedHeight(1)
            separator.setStyleSheet("""
                QFrame {
                    background-color: #e9ecef;
                    border: none;
                    margin: 15px 40px;
                }
            """)
            frame_layout.addWidget(separator)
            
            countdown_label = QLabel("Esta ventana se cerrará en 4 segundos...")
            countdown_label.setAlignment(Qt.AlignCenter)
            countdown_label.setFixedHeight(40) 
            countdown_label.setStyleSheet("""
                QLabel {
                    color: #868e96;
                    font-size: 14px;
                    background: none;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 20px;
                    background-color: #f8f9fa;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    font-weight: 500;
                }
            """)
            frame_layout.addWidget(countdown_label)

            progress_container = QFrame()
            progress_container.setFixedHeight(8)
            progress_container.setStyleSheet("""
                QFrame {
                    background-color: #e9ecef;
                    border-radius: 4px;
                    border: none;
                    margin: 10px 60px;
                }
            """)
            
            progress_bar = QProgressBar(progress_container)
            progress_bar.setRange(0, 4)
            progress_bar.setValue(0)
            progress_bar.setFixedHeight(8)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: transparent;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #4CAF50, stop:1 #45a049);
                    border-radius: 4px;
                }
            """)
            
            progress_layout = QHBoxLayout(progress_container)
            progress_layout.setContentsMargins(0, 0, 0, 0)
            progress_layout.addWidget(progress_bar)
            
            frame_layout.addWidget(progress_container)

            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(30)
            shadow_effect.setXOffset(0)
            shadow_effect.setYOffset(8)
            shadow_effect.setColor(QColor(0, 0, 0, 80))
            dialog.setGraphicsEffect(shadow_effect)
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()

            self.countdown_timer = QTimer()
            self.countdown_seconds = 4
            
            def update_countdown():
                if self.countdown_seconds > 0:
                    countdown_label.setText(f"Esta ventana se cerrará en {self.countdown_seconds} segundos...")
                    progress_bar.setValue(4 - self.countdown_seconds)
                    self.countdown_seconds -= 1
                else:
                    self.countdown_timer.stop()
                    dialog.close()
                    self.remove_blur_effect(self.centralwidget)
                    self.MainWindow.close()
            
            self.countdown_timer.timeout.connect(update_countdown)
            self.countdown_timer.start(1000)

            self.auto_close_timer = QTimer()
            self.auto_close_timer.setSingleShot(True)
            
            def close_dialog_and_window():
                dialog.close()
                self.remove_blur_effect(self.centralwidget)
                self.MainWindow.close()
            
            self.auto_close_timer.timeout.connect(close_dialog_and_window)
            self.auto_close_timer.start(4000)
            self.loading_dialog = dialog

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
            complemento = self.ComplementoEdit.toPlainText() if hasattr(self, 'ComplementoEdit') else ""
            
            self.show_confirmation_dialog(uid, numero_ci, razon_social, monto, correo, complemento)

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

    def abrir_qr_con_blur(self, pago_dialog, monto):
        # Apply blur to the main window instead of the pago_dialog
        self.apply_blur_effect(self.centralwidget)
        
        # Close the confirmation dialog
        pago_dialog.close()
        
        # Create the QR dialog
        qr_dialog = pago_dialog(monto, parent=self.centralwidget)
        
        # Connect the dialog's close event to remove blur
        qr_dialog.finished.connect(lambda: self.remove_blur_effect(self.centralwidget))
        
        # Show the QR
        qr_dialog.exec_()

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