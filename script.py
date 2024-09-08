
import pyodbc
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def conectar():
   conexao = pyodbc.connect (
    "DRIVER={SQL Server};"
    "SERVER=;"
    "DATABASE=MINI_EMPRESA;"
    
)   
   return print("conexao bem sucedida")
conectar()


# Função para conectar ao banco de dados SQL Server
def conectar():
    try:
        conexao = pyodbc.connect(
             "DRIVER={SQL Server};"
             "SERVER=;"
              "DATABASE=MINI_EMPRESA;"
        )
        return conexao
    except pyodbc.Error as e:
        messagebox.showerror("Erro de conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de produtos, se não existir
def criar_tabela_produtos():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Produtos' and xtype='U')
        CREATE TABLE Produtos (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nome NVARCHAR(100) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            quantidade_estoque INT NOT NULL
        )
        ''')
        conexao.commit()
        conexao.close()

# Função para adicionar um produto ao banco de dados
def adicionar_produto(nome, preco, quantidade):
    if not nome or not preco or not quantidade:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute('''
            INSERT INTO Produtos (nome, preco, quantidade_estoque) VALUES (?, ?, ?)
            ''', (nome, float(preco), int(quantidade)))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            listar_produtos()
        except pyodbc.Error as e:
            messagebox.showerror("Erro ao adicionar produto", f"Erro: {e}")
        finally:
            conexao.close()

# Função para listar produtos usando pandas
def listar_produtos():
    conexao = conectar()
    if conexao:
        try:
            # Ler dados do banco de dados para um DataFrame do pandas
            query = "SELECT * FROM Produtos"
            df = pd.read_sql(query, conexao)

            # Limpar a Treeview antes de listar
            for row in tree.get_children():
                tree.delete(row)

            # Inserir dados na Treeview
            for index, row in df.iterrows():
                tree.insert("", "end", values=(row['id'], row['nome'], row['preco'], row['quantidade_estoque']))
        except pyodbc.Error as e:
            messagebox.showerror("Erro ao listar produtos", f"Erro: {e}")
        finally:
            conexao.close()

# Criar a janela principal
janela = tk.Tk()
janela.title("Gerenciador de Produtos")

# Criar widgets
label_nome = tk.Label(janela, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=10)

entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_preco = tk.Label(janela, text="Preço:")
label_preco.grid(row=1, column=0, padx=10, pady=10)

entry_preco = tk.Entry(janela)
entry_preco.grid(row=1, column=1, padx=10, pady=10)

label_quantidade = tk.Label(janela, text="Quantidade:")
label_quantidade.grid(row=2, column=0, padx=10, pady=10)

entry_quantidade = tk.Entry(janela)
entry_quantidade.grid(row=2, column=1, padx=10, pady=10)

botao_adicionar = tk.Button(janela, text="Adicionar Produto", command=lambda: adicionar_produto(entry_nome.get(), entry_preco.get(), entry_quantidade.get()))
botao_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

# Criar uma Treeview para mostrar os produtos
colunas = ("ID", "Nome", "Preço", "Quantidade")
tree = ttk.Treeview(janela, columns=colunas, show='headings')
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Preço", text="Preço")
tree.heading("Quantidade", text="Quantidade")
tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Inicializar a interface
criar_tabela_produtos()
listar_produtos()

# Executar a interface
janela.mainloop()



