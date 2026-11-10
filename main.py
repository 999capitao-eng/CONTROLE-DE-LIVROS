
import sys
from PySide6.QtWidgets import QApplication
from views.janela_principal import JanelaPrincipal
from db import conectar, preparar_banco

conn = conectar()
preparar_banco(conn)

app = QApplication(sys.argv)

janela = JanelaPrincipal(conn)
janela.show()

resultado = app.exec()

conn.close()
sys.exit(resultado)
