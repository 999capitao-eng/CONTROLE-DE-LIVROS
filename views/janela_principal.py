
import sqlite3

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)


class JanelaPrincipal(QWidget):

    def __init__(self, conn):
        super().__init__()

        self.conn = conn
        self.id_selecionado = None

        self.setWindowTitle("Cadastro de Livros")
        self.resize(800, 600)

        self.criar_tela()
        self.mostrar_todos()

    def criar_tela(self):

        layout = QVBoxLayout()

        titulo = QLabel("SISTEMA DE CADASTRO DE LIVROS")
        layout.addWidget(titulo)

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

        botoes = QHBoxLayout()

        cadastrar = QPushButton("Cadastrar")
        cadastrar.clicked.connect(self.cadastrar)

        self.atualizar = QPushButton("Atualizar")
        self.atualizar.setEnabled(False)
        self.atualizar.clicked.connect(self.atualizar_livro)

        self.excluir = QPushButton("Excluir")
        self.excluir.setEnabled(False)
        self.excluir.clicked.connect(self.excluir_livro)

        limpar = QPushButton("Limpar")
        limpar.clicked.connect(self.limpar)

        botoes.addWidget(cadastrar)
        botoes.addWidget(self.atualizar)
        botoes.addWidget(self.excluir)
        botoes.addWidget(limpar)

        layout.addLayout(botoes)

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

        if not titulo or not autor or not ano or not isbn:
            QMessageBox.warning(
                self, "Aviso", "Preencha todos os campos."
            )
            return

        if not ano.isdigit():
            QMessageBox.warning(
                self, "Aviso", "O ano deve ser numérico."
            )
            return

        try:
            self.conn.execute(
                """
                INSERT INTO livro (titulo, autor, ano, isbn)
                VALUES (?, ?, ?, ?)
                """,
                (titulo, autor, int(ano), isbn)
            )

            self.conn.commit()

            self.mostrar_todos()
            self.limpar()

            QMessageBox.information(
                self, "Sucesso", "Livro cadastrado!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self, "Aviso", "Esse ISBN já está cadastrado."
            )

    # Mostrar todos os livros
    def mostrar_todos(self):

        self.pesquisa.clear()
        self.tabela.setRowCount(0)

        livros = self.conn.execute(
            "SELECT * FROM livro ORDER BY id"
        ).fetchall()

        self.exibir_livros(livros)

    # Exibir livros na tabela
    def exibir_livros(self, livros):

        self.tabela.setRowCount(0)

        for livro in livros:

            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            self.tabela.setItem(
                linha, 0, QTableWidgetItem(str(livro["id"]))
            )
            self.tabela.setItem(
                linha, 1, QTableWidgetItem(livro["titulo"])
            )
            self.tabela.setItem(
                linha, 2, QTableWidgetItem(livro["autor"])
            )
            self.tabela.setItem(
                linha, 3, QTableWidgetItem(str(livro["ano"]))
            )
            self.tabela.setItem(
                linha, 4, QTableWidgetItem(livro["isbn"])
            )

    # Pesquisar livro
    def pesquisar(self):

        termo = self.pesquisa.text().strip()

        livros = self.conn.execute(
            """
            SELECT * FROM livro
            WHERE titulo LIKE ? OR autor LIKE ?
            ORDER BY id
            """,
            (f"%{termo}%", f"%{termo}%")
        ).fetchall()

        self.exibir_livros(livros)

    # Selecionar livro
    def selecionar(self):

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        self.id_selecionado = int(
            self.tabela.item(linha, 0).text()
        )

        livro = self.conn.execute(
            "SELECT * FROM livro WHERE id = ?",
            (self.id_selecionado,)
        ).fetchone()

        if livro:
            self.titulo.setText(livro["titulo"])
            self.autor.setText(livro["autor"])
            self.ano.setText(str(livro["ano"]))
            self.isbn.setText(livro["isbn"])

            self.atualizar.setEnabled(True)
            self.excluir.setEnabled(True)

    # Atualizar livro
    def atualizar_livro(self):

        if self.id_selecionado is None:
            return

        titulo = self.titulo.text().strip()
        autor = self.autor.text().strip()
        ano = self.ano.text().strip()
        isbn = self.isbn.text().strip()

        if not titulo or not autor or not ano or not isbn:
            QMessageBox.warning(
                self, "Aviso", "Preencha todos os campos."
            )
            return

        if not ano.isdigit():
            QMessageBox.warning(
                self, "Aviso", "O ano deve ser numérico."
            )
            return

        try:
            self.conn.execute(
                """
                UPDATE livro
                SET titulo = ?, autor = ?, ano = ?, isbn = ?
                WHERE id = ?
                """,
                (titulo, autor, int(ano), isbn, self.id_selecionado)
            )

            self.conn.commit()

            self.mostrar_todos()
            self.limpar()

            QMessageBox.information(
                self, "Sucesso", "Livro atualizado!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self, "Aviso", "Esse ISBN já está cadastrado."
            )

    # Excluir livro
    def excluir_livro(self):

        if self.id_selecionado is None:
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar",
            "Deseja realmente excluir este livro?"
        )

        if resposta == QMessageBox.StandardButton.Yes:

            self.conn.execute(
                "DELETE FROM livro WHERE id = ?",
                (self.id_selecionado,)
            )

            self.conn.commit()

            self.mostrar_todos()
            self.limpar()

    # Limpar campos
    def limpar(self):

        self.titulo.clear()
        self.autor.clear()
        self.ano.clear()
        self.isbn.clear()
        self.pesquisa.clear()

        self.id_selecionado = None

        self.tabela.clearSelection()

        self.atualizar.setEnabled(False)
        self.excluir.setEnabled(False)
