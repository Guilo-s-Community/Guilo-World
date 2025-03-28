
from datetime import datetime
import os
import math


#Dicionário com o produto e preço.
PRODUTOS = {
    1: {
        "nome": "X-salada",
        "preço": 10.0
    },
    2: {
        "nome": "X-burger ",
        "preço": 10.0
    },
    3: {
        "nome": "Cachorro quente ",
        "preço": 7.5
    },
    4: {
        "nome": "Misto quente",
        "preço": 8.0
    },
    5: {
        "nome": "Salada de frutas",
        "preço": 5.5
    },
    6: {
        "nome": "Refrigerante",
        "preço": 4.5
    },
    7: {
        "nome": "Suco natural",
        "preço": 6.25
    },
}


#Criar o arquivo dos pedidos.
ARQUIVO_PEDIDOS = "pedidos.txt"
if not os.path.isfile(ARQUIVO_PEDIDOS):
    open(ARQUIVO_PEDIDOS, "x").close()

#Função principal onde chama as opções.
def main():
    while True:
        print()
        print("1 - Novo pedido")
        print("2 - Cancelar pedido")
        print("3 - Inserir produto")  # No pedido
        print("4 - Cancelar produto")  # Do pedido
        print("5 - Valor do pedido")
        print("6 - Extrato do pedido")
        print()
        print("0 - Sair")

        escolha = input("Digite o codigo que deseja:\n-> ")
        if escolha == "0":
            break
        if escolha == "1":
            novo_pedido()
        if escolha == "2":
            cancela_pedido()
        if escolha == "3":
            insere_produto()
        if escolha == "4":
            cancela_produto()
        if escolha == "5":
            valor_do_pedido()
        if escolha == "6":
            extrato_do_pedido()


#Criar novo pedido por cpf.
def novo_pedido():
    #Usuário insere as informações.
    print()
    print("1 - Novo pedido")
    print()
    nome = input("Nome: ")
    cpf = input("Cpf: ")
    senha = input("Senha: ")

    usuarios = ler_usuarios()

    #Verifica se já existe pedido com cpf cadastrado.E cria o usuario e o pedido
    if cpf not in usuarios:
        criar_usuario(cpf, nome, senha)
        menu_pedido(cpf, nome)
    else:
        print("Já existe um pedido com este CPF.")
        return


#Função para cancelar pedido
def cancela_pedido():
    #informar o login para cancelar o pedido.
    print()
    print("2 - Cancela pedido")
    print()
    cpf = input("Cpf: ")
    senha = input("Senha: ")

    #Verifica se existe o login cadastrado para cancelar o pedido.
    usuario = login(cpf, senha)
    if usuario != False:
        print()
        print("Pedido Cancelado!")
        excluir_usuario(cpf)

#Função para inserir um produto no pedido.
def insere_produto():
    #informar o login para adicionar um produto.
    print()
    print("3 - Insere produto")
    print()
    cpf = input("Cpf: ")
    senha = input("Senha: ")

    #Verifica se existe o login cadastrado para adicionar um produto.
    usuario = login(cpf, senha)
    if usuario != False:
        menu_pedido(cpf, usuario["nome"])

#Função para cancelar um produto do pedido.
def cancela_produto():
    #Informar o login para cancelar um produto do pedido.
    print()
    print("4 - Cancela produto")
    print()
    cpf = input("Cpf: ")
    senha = input("Senha: ")
    #Verifica se existe o login cadastrado para cancelar um produto do pedido.
    #Se existe, libera para cancelar.
    usuario = login(cpf, senha)
    if usuario != False:
        for codigo, produto in PRODUTOS.items():
            print(f'{codigo} - {produto["nome"]:17} {produto["preço"]:5.2f}')
        print()
        codigo = int(input("Código do produto\n-> "))
        quantidade = int(input("Quantidade\n-> "))
        #Verifica se foi cancelado 0.
        if quantidade == 0:
            print("Digite um número maior que zero.")
            return
        #Cancela o produto do pedido
        quantidade_no_pedido = 0
        for produto in usuario["produtos"]:
            if produto["codigo"] == codigo:
                quantidade_no_pedido += produto["quantidade"]
        #Verifica se tentou cancelar uma quantidade maior que existe.
        if quantidade > quantidade_no_pedido:
            print("Quantidade maior que no pedido")
            return

        adicionar_produto(cpf, codigo, -quantidade)

#Função para verificar o valor do pedido.
def valor_do_pedido():
    #Informar o login.
    print()
    print("5 - Valor a pagar")
    print()
    cpf = input("Cpf: ")
    senha = input("Senha: ")
    #Verifica o login para calcular o valor do pedido
    usuario = login(cpf, senha)
    if usuario != False:
        total = calcula_total(usuario)
        print()
        print(f"Valor a pagar R$: {total}")

#Função para pedir o extrato do pedido.
def extrato_do_pedido():
    #Informar o login.
    print()
    print("6 - Extrato do pedido")
    cpf = input("Cpf: ")
    senha = input("Senha: ")
    #Se existir, ir para função que mostra o extrato.
    usuario = login(cpf, senha)
    if usuario != False:
        mostra_extrato(cpf, usuario)



#Função fazer o pedido.
def menu_pedido(cpf, nome):
    while True:
        print(f"Olá {nome}.")
        for codigo, produto in PRODUTOS.items():
            print(f'{codigo} - {produto["nome"]:17} {produto["preço"]:5.2f}')
        print()

        codigo = input("Digite o código do produto!\n-> ")
        quantidade = input("Digite a quantidade!\n-> ")

        adicionar_produto(cpf, codigo, quantidade)

        if input("Deseja pedir outro? (S/N) ").lower() != "s":
            break

#Função para ler os usuarios/pedidos do arquivo.
def ler_usuarios():
    f = open(ARQUIVO_PEDIDOS, "r")
    conteudo = f.read()
    f.close()

    pedidos = dict()
    for pedido_arquivo in conteudo.split('\n\n'):
        if pedido_arquivo == '':
            continue

        linhas = pedido_arquivo.splitlines()

        cpf = linhas[0]
        nome = linhas[1]
        senha = linhas[2]
        produtos = linhas[3:]

        pedidos[cpf] = {
            "nome": nome,
            "senha": senha,
            "produtos": []
        }
        for produto in produtos:
            codigo_str, quantidade_str = produto.split(",")
            codigo = int(codigo_str)
            quantidade = int(quantidade_str)

            pedidos[cpf]["produtos"].append({
                "codigo": codigo,
                "quantidade": quantidade,
            })

    return pedidos

#Função para escrever o usuario criado.
def escrever_usuarios(pedidos):
    #As informações do usuario sao:nome,cpf,senha e o pedido.
    pedidos_arquivos = []

    for cpf, usuario in pedidos.items():
        pedido_arquivo = f"{cpf}\n{usuario['nome']}\n{usuario['senha']}"

        for cod_qtd in usuario["produtos"]:
            codigo = cod_qtd["codigo"]
            quantidade = cod_qtd["quantidade"]
            pedido_arquivo += f"\n{codigo},{quantidade}"

        pedidos_arquivos.append(pedido_arquivo)

    conteudo = '\n\n'.join(pedidos_arquivos)

    f = open(ARQUIVO_PEDIDOS, "w")
    f.write(conteudo)
    f.close()

#Função para criar o usuário.
def criar_usuario(cpf, nome, senha):
    pedidos = ler_usuarios()

    if cpf not in pedidos:
        pedidos[cpf] = {
            "nome": nome,
            "senha": senha,
            "produtos": []
        }
        escrever_usuarios(pedidos)

#Função para adicionar produto.
def adicionar_produto(cpf, codigo, quantidade):
    pedidos = ler_usuarios()

    pedidos[cpf]["produtos"].append({
        "codigo": codigo,
        "quantidade": quantidade
    })

    escrever_usuarios(pedidos)

#Função para excluir usuário.
def excluir_usuario(cpf):
    usuarios = ler_usuarios()

    usuarios.pop(cpf)

    escrever_usuarios(usuarios)

#Função para fazer o login.
def login(cpf, senha):
    usuarios = ler_usuarios()
    #verifica se o cpf ja existe.
    if cpf not in usuarios:
        print("CPF não cadastrado!")
        return False
    #Verifica se a senha do cpf cadastrado está certa.
    if senha != usuarios[cpf]["senha"]:
        print("Senha incorreta!")
        return False

    return usuarios[cpf]

#Função apenas para calcular o total do pedido.
def calcula_total(usuario):
    soma = 0
    for produto in usuario["produtos"]:
        soma += PRODUTOS[produto["codigo"]]["preço"] * produto["quantidade"]

    return soma

#Função que mostra o extrato.
def mostra_extrato(cpf, usuario):
    print(f"Nome: {usuario['nome']}")
    print(f"CPF: {cpf}")

    total = calcula_total(usuario)
    print(f"Total: R$ {total:.2f}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    print("Itens do pedido:")
    print("Qtd.", "Produto".ljust(19, ' '), "Unitário ", "Saldo  ")
    for produto in usuario["produtos"]:
        qtd = produto["quantidade"]
        info_produto = PRODUTOS[produto["codigo"]]

        cancelado = ""
        if qtd < 0:
            cancelado = "---> Cancelado"

        print("{:2d}x  {:19} {:8.2f} {:+7.2f} {:5}".format(
                abs(qtd),
                info_produto["nome"],
                info_produto["preço"],
                info_produto["preço"] * qtd,
                cancelado
            )
        )


if __name__ == "__main__":
    main()
