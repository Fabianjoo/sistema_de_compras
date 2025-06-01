import mysql.connector
import sys

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="loja"
)

cursor = conexao.cursor()
carrinho = []

def adicionar_produtos():
    # Produtos disponíveis com nome, preço e estoque limite
    produtos_disponiveis = {
        "celular": (1500.00, 20),
        "notebook": (3000.00, 10),
        "fones": (200.00, 50),
        "carregador": (80.00, 35)
    }

    # Mostra os produtos disponíveis (somente print)
    print("\nProdutos disponíveis:")
    for nome, (preco, estoque) in produtos_disponiveis.items():
        print(f"- {nome} | R$ {preco:.2f} | Estoque disponível: {estoque}")

    nome = input("\nDigite o nome do produto que deseja adicionar ao banco: ").lower()

    if nome not in produtos_disponiveis:
        print("Produto inválido. Esse produto não está disponível para cadastro.\n")
        return

    preco, estoque_disponivel = produtos_disponiveis[nome]

    try:
        quantidade = int(input("Digite a quantidade que deseja adicionar: "))
    except ValueError:
        print("Quantidade inválida.\n")
        return

    if quantidade > estoque_disponivel:
        print(f"Erro: Estoque máximo permitido é {estoque_disponivel}. Tente novamente.\n")
        return

    cursor.execute(
        "INSERT INTO titens (nome, preco, quantidade) VALUES (%s, %s, %s)",
        (nome, preco, quantidade)
    )
    conexao.commit()

    print(f"{quantidade}x {nome} inseridos no banco com sucesso!\n")

def retirar_produto():
    cursor.execute("SELECT nome, preco, quantidade FROM titens")
    produtos = cursor.fetchall()

    if not produtos:
        print("O carrinho está vazio.\n")
        return

    print("Itens no carrinho:")
    for nome, preco, quantidade in produtos:
        print(f"- {nome} (x{quantidade}) - R$ {preco:.2f} cada")

    nome_remover = input("Digite o nome do produto que deseja remover: ").lower()

    # Verifica se o produto existe
    produto_encontrado = None
    for p in produtos:
        if p[0].lower() == nome_remover:
            produto_encontrado = p
            break

    if not produto_encontrado:
        print("Produto não encontrado no carrinho.\n")
        return

    try:
        quantidade_remover = int(input("Digite a quantidade que deseja remover: "))
    except ValueError:
        print("Quantidade inválida.\n")
        return

    nome_produto, preco_produto, quantidade_estoque = produto_encontrado

    if quantidade_remover > quantidade_estoque:
        print(f"Quantidade inválida. O carrinho tem apenas {quantidade_estoque} unidades desse produto.\n")
        return

    nova_quantidade = quantidade_estoque - quantidade_remover

    if nova_quantidade > 0:
        cursor.execute("UPDATE titens SET quantidade = %s WHERE nome = %s", (nova_quantidade, nome_produto))
    else:
        cursor.execute("DELETE FROM titens WHERE nome = %s", (nome_produto,))

    conexao.commit()
    print(f"{quantidade_remover}x {nome_produto} removidos do carrinho.\n")


def concluir_compra():
    cursor.execute("SELECT * FROM titens")
    produtos = cursor.fetchall()
    if not produtos:
        print("Não há produtos no carrinho!")
        return
    
    print("Compra finalizada com sucesso!")
    
    # Limpa a tabela titens no banco (zera o carrinho)
    cursor.execute("DELETE FROM titens")
    conexao.commit()
    
    sair()


def limpar_carrinho():
    confirmar = input("Tem certeza que deseja limpar todo o carrinho? (s/n): ").lower()
    if confirmar == 's':
        cursor.execute("DELETE FROM titens")
        conexao.commit()
        print("Carrinho limpo com sucesso.\n")
    else:
        print("Operação cancelada.\n")


def mostrar_itens():
    cursor.execute("SELECT nome, preco, quantidade FROM titens")
    resultados = cursor.fetchall()

    if not resultados:
        print("Não há itens cadastrados no banco de dados!")
        return

    print("\nItens cadastrados no banco:")
    for nome, preco, quantidade in resultados:
        total = preco * quantidade
        print(f"- {nome} (x{quantidade}) - Total = R$ {total:.2f}")


def sair():
    print("Encerrando o programa. Até mais!")
    sys.exit()

while True:
    print("\nSeja bem-vindo ao sistema de compras!")
    print("1 - Adicionar Produtos")
    print("2 - Retirar Produto")
    print("3 - Concluir Compra")
    print("4 - Limpar Carrinho")
    print("5 - Mostrar Itens")
    print("6 - Sair")
    opcao = input("Digite uma opção: ")

    if opcao == "1":
        adicionar_produtos()
    elif opcao == "2":
        retirar_produto()
    elif opcao == "3":
        concluir_compra()
    elif opcao == "4":
        limpar_carrinho()
    elif opcao == "5":
        mostrar_itens()
    elif opcao == "6":
        sair()
    else:
        print("Opção inválida. Tente novamente.\n")
