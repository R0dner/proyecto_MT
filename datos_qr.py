import json
import requests
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtSvg import QSvgRenderer
import qrcode
from PIL import Image
import io
import time
import os

# Función para convertir imagen PIL a QImage para PySide2
def pil_to_qimage(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_data = buffer.getvalue()
    qimage = QImage.fromData(img_data)
    return qimage

# Función para descargar una imagen desde una URL
def download_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            return pil_to_qimage(img)
        else:
            print(f"Error al descargar imagen: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al descargar imagen: {e}")
        return None

class QRDatosManager:
    def __init__(self):
        # URL base para la API
        self.base_url = "https://serviciosvirtual-test.miteleferico.bo"
        self.api_url = f"{self.base_url}/api/v1/payment/registrar-deuda-mobile"
        self.datos_recarga = {}
        self.qr_url = None
        self.correo_temporal = None  # Para almacenar el correo temporalmente sin guardarlo
        self.api_response = None  # Para almacenar la respuesta completa de la API
        # Token de autenticación - Puedes establecerlo aquí o a través de un método
        self.auth_token = None
    
    def set_auth_token(self, token):
        """Establece el token de autenticación para las solicitudes API"""
        self.auth_token = token
        return True
    
    def recopilar_datos(self, uid, documento, razon_social, complemento, correo, monto):
        self.correo_temporal = correo
        
        self.datos_recarga = {
            "uid": uid.replace("UID: ", ""),  
            "documento": documento,
            "razon_social": razon_social,
            "complemento": complemento,
            "monto": monto,
            "timestamp": int(time.time())
        }
        
        # Guardar localmente en un archivo JSON para utilizarlo en la solicitud
        with open("ultima_recarga.json", "w") as f:
            json.dump(self.datos_recarga, f, indent=4)
            
        return self.datos_recarga
    
    def cargar_datos_recarga(self):
        """Carga los datos del archivo ultima_recarga.json"""
        try:
            if os.path.exists("ultima_recarga.json"):
                with open("ultima_recarga.json", "r") as f:
                    self.datos_recarga = json.load(f)
                return True
            else:
                print("Archivo ultima_recarga.json no encontrado")
                return False
        except Exception as e:
            print(f"Error al cargar datos de recarga: {e}")
            return False
    
    def enviar_solicitud(self):
        """Envía los datos guardados en 'ultima_recarga.json' a la API y espera la URL del QR como respuesta"""
        try:
            # Cargar los datos del archivo JSON
            if not self.cargar_datos_recarga():
                return False, "No se pudieron cargar los datos de recarga"

            # Verificar que el token esté configurado
            if not self.auth_token:
                return False, "Token de autenticación no configurado"

            # Construir el payload usando los campos requeridos por la API
            datos_para_api = {
                "monto": self.datos_recarga.get("monto", ""),
                "nit": self.datos_recarga.get("documento", ""),
                "razon_social": self.datos_recarga.get("razon_social", ""),
                "uid": self.datos_recarga.get("uid", "")
            }

            # Incluir el token en los headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"  # Añadir token en formato Bearer
            }
            
            respuesta = requests.post(self.api_url, json=datos_para_api, headers=headers)

            if respuesta.status_code == 200:
                self.api_response = respuesta.json()
                
                # Verificar si la respuesta tiene el formato esperado
                if self.api_response.get("success") and "data" in self.api_response:
                    data = self.api_response["data"]
                    self.qr_url = data.get("qr_simple_url", "")
                    
                    # Guardar la respuesta completa para uso posterior
                    with open("ultima_respuesta_api.json", "w") as f:
                        json.dump(self.api_response, f, indent=4)
                    
                    return True, self.qr_url
                else:
                    return False, "Formato de respuesta de API inesperado"
            else:
                return False, f"Error {respuesta.status_code}: {respuesta.text}"

        except Exception as e:
            print(f"Error al enviar solicitud: {e}")
            return False, str(e)
    
    def generar_qr_basado_en_respuesta(self):
        """Descarga y muestra la imagen QR desde qr_simple_url en lugar de generar un nuevo QR"""
        try:
            if self.qr_url and self.api_response and "data" in self.api_response:
                # Usar directamente la URL del QR proporcionada por la API
                qr_simple_url = self.api_response["data"].get("qr_simple_url", "")
                
                if qr_simple_url:
                    # Descargar la imagen QR desde la URL
                    qr_image = download_image_from_url(qr_simple_url)
                    if qr_image:
                        return qr_image, self.api_response["data"]
                    else:
                        # Si falla la descarga, generamos un QR temporal como respaldo
                        print("Fallo al descargar QR, generando uno temporal...")
                        return self.generar_qr_temporal(), self.api_response["data"]
            
            return None, None
        except Exception as e:
            print(f"Error al generar QR basado en respuesta: {e}")
            return None, None
    
    def generar_qr_temporal(self):
        """Genera un QR temporal con los datos de ultima_recarga.json mientras se espera la respuesta de la API"""
        if not self.datos_recarga:
            if not self.cargar_datos_recarga():
                return None
        
        # Crear un código QR temporal basado en los datos recopilados
        data = json.dumps(self.datos_recarga)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        # Convertir la imagen PIL a QImage usando la función auxiliar
        return pil_to_qimage(img)


class QRRechargeDialog(QDialog):
    def __init__(self, datos_manager, parent=None):
        super().__init__(parent)
        self.datos_manager = datos_manager
        self.setup_ui()
        self.show_loading_qr()
        
        # Iniciar proceso de solicitud en un hilo separado
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_qr_status)
        self.timer.start(500)  # Verificar cada 500ms
        
    def setup_ui(self):
        self.setWindowTitle("Código QR para Recarga")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #CFD8DC;
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Encabezado
        header = QLabel("Escanea el código QR")
        header.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        
        # Contenedor del QR
        self.qr_container = QLabel()
        self.qr_container.setFixedSize(300, 300)
        self.qr_container.setStyleSheet("background-color: white; border: 1px solid #CFD8DC;")
        self.qr_container.setAlignment(Qt.AlignCenter)
        
        # Estado
        self.status_label = QLabel("Generando código QR...")
        self.status_label.setStyleSheet("color: #455A64; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Información adicional
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #455A64; font-size: 12px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        # Botón Cerrar
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(header)
        layout.addWidget(self.qr_container, 0, Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addWidget(self.info_label)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
    def show_loading_qr(self):
        """Muestra un indicador de carga mientras se genera el QR"""
        loading_gif = QMovie("loading.gif")
        if QFile("loading.gif").exists():
            self.qr_container.setMovie(loading_gif)
            loading_gif.start()
        else:
            self.qr_container.setText("Cargando...")
            self.qr_container.setStyleSheet("background-color: white; font-size: 20px;")
    
    def show_qr_image(self, qr_image):
        """Muestra la imagen QR en el diálogo"""
        if isinstance(qr_image, QImage):
            pixmap = QPixmap.fromImage(qr_image)
        else:
            pixmap = QPixmap(qr_image)
        
        scaled_pixmap = pixmap.scaled(
            self.qr_container.width(), 
            self.qr_container.height(),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        self.qr_container.setPixmap(scaled_pixmap)
    
    def check_qr_status(self):
        """Verifica si ya tenemos la respuesta de la API y muestra el QR"""
        if self.datos_manager.qr_url:
            self.timer.stop()
            
            qr_image, api_data = self.datos_manager.generar_qr_basado_en_respuesta()
            
            if qr_image:
                self.show_qr_image(qr_image)
                
                # Mostrar información del pago
                if api_data:
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']}")
                    
                    # Mostrar información adicional como código de recaudación
                    info_text = f"Código de recaudación: {api_data.get('codigo_recaudacion', 'N/A')}\n"
                    info_text += f"ID Transacción: {api_data.get('id_transaccion', 'N/A')}"
                    self.info_label.setText(info_text)
            else:
                # Si falló la generación del QR basado en la respuesta, usamos el temporal
                temp_qr = self.datos_manager.generar_qr_temporal()
                if temp_qr:
                    self.show_qr_image(temp_qr)
                    self.status_label.setText(f"Monto: Bs. {self.datos_manager.datos_recarga['monto']} (QR temporal)")
                else:
                    self.status_label.setText("Error al generar el código QR")


def solicitar_recarga(uid="", documento="", razon_social="", complemento="", correo="", monto="", auth_token="", parent_widget=None):
    """Función principal para iniciar el proceso de recarga"""
    # Crear instancia del gestor de datos
    datos_manager = QRDatosManager()
    
    # Configurar el token de autenticación
    if auth_token:
        datos_manager.set_auth_token(auth_token)
    else:
        QMessageBox.warning(
            parent_widget,
            "Advertencia",
            "No se ha proporcionado un token de autenticación",
            QMessageBox.Ok
        )
        return False
    
    # Verificar si tenemos datos proporcionados o debemos cargar desde el archivo
    if uid and documento and razon_social and monto:
        # Recopilar datos y guardarlos en 'ultima_recarga.json'
        datos_manager.recopilar_datos(uid, documento, razon_social, complemento, correo, monto)
    else:
        # Cargar datos del archivo JSON
        if not datos_manager.cargar_datos_recarga():
            QMessageBox.critical(
                parent_widget,
                "Error de Carga",
                "No se pudieron cargar los datos de recarga del archivo ultima_recarga.json",
                QMessageBox.Ok
            )
            return False
    
    # Enviar solicitud a la API
    success, message = datos_manager.enviar_solicitud()
    
    if success:
        dialog = QRRechargeDialog(datos_manager, parent_widget)
        return dialog.exec_()
    else:
        QMessageBox.critical(
            parent_widget,
            "Error de Conexión",
            f"No se pudo conectar con el servidor: {message}",
            QMessageBox.Ok
        )
        return False


# Para uso directo en pruebas
if __name__ == "__main__":
    app = QApplication([])
    
    # Ejemplo de cómo proporcionar el token de autenticación
    mi_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ1LCJkbmkiOiI2MDUxOTQ5IiwiZmlyc3RfbmFtZSI6Ikpvc2UgTHVpcyIsImxhc3RfbmFtZSI6IlphbW9yYSIsImNlbGxwaG9uZSI6Nzk1MTE4MTAsInNlY3JldCI6IjExNmJlMDE1MGE5MWFjMmNmYzg2MzgwNjU0NTFmNzVkIiwiaWF0IjoxNzQ2NjQ4ODE4LCJleHAiOjE3NzgxODQ4MTh9.z5zp5EuMFJz35UQ8Xv5eO7S4yM6bWvrMGCOh-QclTk8"  # Reemplaza con tu token real
    
    solicitar_recarga(
        auth_token=mi_token,
        parent_widget=None
    )
    
    app.exec_()