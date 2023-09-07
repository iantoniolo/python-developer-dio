import pprint
import pymongo as pyM

from secrets import URL_CLUSTER

client = pyM.MongoClient(URL_CLUSTER)

db = client.sistema_bancario
clientes = db.bank

def menu():
    opcao = int(input(
"""
Cadastro de Clientes

[1] Cadastrar conta
[2] Listar clientes
[3] Ordenar clientes
[4] Excluir conta de um cliente
[0] Sair

=> Qual opção você deseja? """
))
    return opcao

numero_conta = 1

while True:

    opcao = menu()

    if opcao == 1:

        nome = input("Nome: ")
        cpf = input("CPF (somente números): ")
        email = input("E-mail: ")
        saldo = float(input("Saldo da conta: "))

        cliente = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "tipo_conta": "conta_corrente",
            "agencia": "0001",
            "numero_conta": numero_conta
        }

        numero_conta += 1
            
        clientes.insert_one(cliente)

        print("\nConta criada com sucesso.")

    elif opcao == 2:
        num_clientes = clientes.count_documents({})
        if num_clientes == 0:
            print("\nNão existem clientes registrados para listar.")
        else:
            print("\nDocumentos presentes na coleção posts")
            for cliente in clientes.find():
                pprint.pprint(cliente)

    elif opcao == 3:
        num_clientes = clientes.count_documents({})
        if num_clientes == 0:
            print("\nNão existem clientes registrados para ordenar.")
        else:
            tipo_ordenacao = input("""Escolha o tipo de ordenação (nome, cpf, email, numero_conta): """)
            print("\nRecuperando infos da coleção post de maneira ordenada")
            for cliente in clientes.find({}).sort(tipo_ordenacao):
                pprint.pprint(cliente)

    elif opcao == 4:
        cpf_cliente = input("\nDigite o CPF do cliente que deseja encerrar a conta: ")
        cliente_existente = clientes.find_one({"cpf": cpf_cliente})
    
        if cliente_existente:
            clientes.delete_one({"cpf": cpf_cliente})
            print(f"\nCliente excluído com sucesso.")
        else:
            print(f"\nCliente com o CPF mencionado não foi encontrado.")

    elif opcao == 0:
        break

    else:
        print("Opção inválida.")