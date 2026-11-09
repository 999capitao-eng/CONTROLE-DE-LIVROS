from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)


class JanelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Livros")
        self.resize(800, 600)

        self.livros = []
        self.id_atual = 1

        self.criar_tela()

    def criar_tela(self):

        layout = QVBoxLayout()

        titulo = QLabel("SISTEMA DE CADASTRO DE LIVROS")
        layout.addWidget(titulo)

        # Campos
        formulario = QFormLayout()

        self.titulo = QLineEdit()
        self.autor = QLineEdit()
        self.ano = QLineEdit()
        self.isbn = QLineEdit()

        formulario.addRow("Título:", self.titulo)
        formulario.addRow("Autor:", self.autor)
        formulario.addRow("Ano:", self.ano)
        formulario.addRow("ISBN:", self.isbn)

        layout.addLayout(formulario)

        # Botoes de cadastro
        botoes = QHBoxLayout()

        cadastrar = QPushButton("Cadastrar")
        cadastrar.clicked.connect(self.cadastrar)

        atualizar = QPushButton("Atualizar")
        atualizar.setEnabled(False)

        excluir = QPushButton("Excluir")
        excluir.setEnabled(False)

        limpar = QPushButton("Limpar")
        limpar.clicked.connect(self.limpar)

        botoes.addWidget(cadastrar)
        botoes.addWidget(atualizar)
        botoes.addWidget(excluir)
        botoes.addWidget(limpar)

        layout.addLayout(botoes)

        # Pesquisa
        layout.addWidget(QLabel("Pesquisar livro:"))

        pesquisa_layout = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Digite o título ou autor")

        pesquisar = QPushButton("Pesquisar")
        pesquisar.clicked.connect(self.pesquisar)

        mostrar = QPushButton("Mostrar todos")
        mostrar.clicked.connect(self.mostrar_todos)

        pesquisa_layout.addWidget(self.pesquisa)
        pesquisa_layout.addWidget(pesquisar)
        pesquisa_layout.addWidget(mostrar)

        layout.addLayout(pesquisa_layout)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Título", "Autor", "Ano", "ISBN"]
        )

        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabela.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabela.itemSelectionChanged.connect(self.selecionar)

        layout.addWidget(self.tabela)

        self.setLayout(layout)

    # Cadastrar livro
    def cadastrar(self):

        titulo = self.titulo.text().strip()
        autor = self.autor.text().strip()
        ano = self.ano.text().strip()
        isbn = self.isbn.text().strip()

        if titulo == "" or autor == "":
            QMessageBox.warning(
                self, "Aviso", "Preencha o título e o autor."
            )
            return

        if not ano.isdigit():
            QMessageBox.warning(
                self, "Aviso", "O ano deve ser numérico."
            )
            return

        livro = {
            "id": self.id_atual,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "isbn": isbn
        }

        self.livros.append(livro)
        self.id_atual += 1

        self.mostrar_todos()
        self.limpar()

        QMessageBox.information(
            self, "Sucesso", "Livro cadastrado!"
        )

    # Mostrar livros na tabela
    def mostrar_todos(self):

        self.pesquisa.clear()
        self.tabela.setRowCount(0)

        for livro in self.livros:

            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            self.tabela.setItem(linha, 0, QTableWidgetItem(str(livro["id"])))
            self.tabela.setItem(linha, 1, QTableWidgetItem(livro["titulo"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(livro["autor"]))
            self.tabela.setItem(linha, 3, QTableWidgetItem(livro["ano"]))
            self.tabela.setItem(linha, 4, QTableWidgetItem(livro["isbn"]))

    # Pesquisar por titulo ou autor
    def pesquisar(self):

        termo = self.pesquisa.text().lower()

        self.tabela.setRowCount(0)

        for livro in self.livros:

            if termo in livro["titulo"].lower() or termo in livro["autor"].lower():

                linha = self.tabela.rowCount()
                self.tabela.insertRow(linha)

                self.tabela.setItem(linha, 0, QTableWidgetItem(str(livro["id"])))
                self.tabela.setItem(linha, 1, QTableWidgetItem(livro["titulo"]))
                self.tabela.setItem(linha, 2, QTableWidgetItem(livro["autor"]))
                self.tabela.setItem(linha, 3, QTableWidgetItem(livro["ano"]))
                self.tabela.setItem(linha, 4, QTableWidgetItem(livro["isbn"]))

    # Selecionar livro
    def selecionar(self):

        linha = self.tabela.currentRow()

        if linha >= 0:

            id_livro = int(self.tabela.item(linha, 0).text())

            for livro in self.livros:

                if livro["id"] == id_livro:
                    self.titulo.setText(livro["titulo"])
                    self.autor.setText(livro["autor"])
                    self.ano.setText(livro["ano"])
                    self.isbn.setText(livro["isbn"])
                    break

    # Limpar campos
    def limpar(self):

        self.titulo.clear()
        self.autor.clear()
        self.ano.clear()
        self.isbn.clear()
        self.pesquisa.clear()
        self.tabela.clearSelection()
