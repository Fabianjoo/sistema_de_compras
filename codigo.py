import mysql.connector
import sys

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="loja"
)
cursor = conexao.cursor()

def cadastrar_produto():
    nome = input("Nome do produto: ").lower()
    descricao = input("Descrição do produto: ")
    try:
        preco = float(input("Preço: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Preço ou quantidade inválidos.\n")
        return

    cursor.execute("INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (%s, %s, %s, %s)",
                   (nome, descricao, preco, quantidade))
    conexao.commit()
    print(f"Produto '{nome}' cadastrado com sucesso!\n")

def deletar_produto():
    nome = input("Digite o nome do produto para deletar: ").lower()
    cursor.execute("DELETE FROM produtos WHERE nome = %s", (nome,))
    conexao.commit()
    print(f"Produto '{nome}' deletado, se existia.\n")

def comprar_produto():
    nome = input("Nome do produto que deseja comprar: ").lower()
    try:
        quantidade = int(input("Quantidade a comprar: "))
    except ValueError:
        print("Quantidade inválida.\n")
        return

    cursor.execute("SELECT quantidade FROM produtos WHERE nome = %s", (nome,))
    resultado = cursor.fetchone()

    if resultado:
        estoque_atual = resultado[0]
        if quantidade > estoque_atual:
            print(f"Estoque insuficiente. Disponível: {estoque_atual}\n")
        else:
            novo_estoque = estoque_atual - quantidade
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE nome = %s", (novo_estoque, nome))
            conexao.commit()
            print(f"Compra de {quantidade}x '{nome}' realizada com sucesso.\n")
    else:
        print("Produto não encontrado.\n")

def aplicar_desconto():
    nome = input("Nome do produto para aplicar desconto: ").lower()
    try:
        desconto = float(input("Valor do desconto (em reais): "))
    except ValueError:
        print("Valor inválido.\n")
        return

    cursor.execute("SELECT preco FROM produtos WHERE nome = %s", (nome,))
    resultado = cursor.fetchone()

    if resultado:
        preco_atual = resultado[0]
        novo_preco = max(0, preco_atual - desconto)
        cursor.execute("UPDATE produtos SET preco = %s WHERE nome = %s", (novo_preco, nome))
        conexao.commit()
        print(f"Desconto aplicado! Novo preço: R$ {novo_preco:.2f}\n")
    else:
        print("Produto não encontrado.\n")

def listar_produtos():
    cursor.execute("SELECT nome, descricao, preco, quantidade FROM produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.\n")
    else:
        print("\nProdutos cadastrados:")
        for nome, descricao, preco, quantidade in produtos:
            print(f"- {nome} | {descricao} | R$ {preco:.2f} | Estoque: {quantidade}")

def sair():
    print("Encerrando o sistema.")
    sys.exit()

# Menu principal
while True:
    print("\n--- Menu Estoque ---")
    print("1 - Cadastrar produto")
    print("2 - Deletar produto")
    print("3 - Comprar produto")
    print("4 - Aplicar desconto")
    print("5 - Listar produtos")
    print("6 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_produto()
    elif opcao == "2":
        deletar_produto()
    elif opcao == "3":
        comprar_produto()
    elif opcao == "4":
        aplicar_desconto()
    elif opcao == "5":
        listar_produtos()
    elif opcao == "6":
        sair()
    else:
        print("Opção inválida.\n")
