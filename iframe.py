import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtCore import QByteArray, Qt, QRectF
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Qt


class Iframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowTitle("Pago en línea")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()

        self.volver = QPushButton("Salir")
        self.volver.setFixedSize(150, 50)  
        self.volver.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 18px ;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #ff4d4d;
            }
        """)
        self.volver.clicked.connect(self.close_iframe)

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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.volver, 0, Qt.AlignCenter)
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.browser.load("https://pagos.libelula.bo/?id=e4c9734d-7477-4daf-8425-faff2c0c656b")  

    def close_iframe(self):
        self.browser.load("about:blank")
        self.close()  
