import sys
from PyQt5.QtWidgets import QApplication
from comfyui.widgets import CWindow, CButton

app = QApplication(sys.argv)

# Crear una ventana
window = CWindow("Mi primera ventana ComfyUI", width=400, height=300)

# Agregar un botón
button = CButton("Presióname")
window.set_central_widget(button)

window.show()
sys.exit(app.exec_())

