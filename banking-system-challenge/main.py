from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        self.conta = conta
        self.transacao = transacao

    def adicionar_conta(self, conta):
        self.conta = conta

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self.saldo = 0.00
        self.numero = 1
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self, valor):
        return self._valor
    
    @property
    def nova_conta(self, cliente, numero):
        return 
    
    @property
    def sacar(self, valor):
        return 
    
    @property
    def depositar(self, valor):
        return 
    
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transcao(self, transacao):
        self.transacao = transacao

class Transacao(ABC):
    @abstractmethod
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Sacar(Transacao):
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass

def menu():
    print(
"""
-------- SISTEMA BANCÁRIO --------

    [1]: Cadastrar usuário
    [2]: Criar conta
    [3]: Visualizar saldo
    [4]: Depositar
    [5]: Sacar
    [6]: Visualizar extrato
    [7]: Listar usuários
    [8]: Listar contas
    [0]: Sair

----------------------------------
"""
)

def visualizar_saldo(saldo):
    print(f"Saldo disponível: R${saldo:.2f}")

def depositar(saldo, extrato, deposito):
    valor_deposito = int(input('Qual valor (R$) deseja depositar em sua conta? Digite apenas números: '))
    extrato += f"\nDepósito {deposito}: R${valor_deposito:.2f}"
    saldo += valor_deposito
    deposito += 1
    print("Depósito concluído com sucesso.")
    return saldo, extrato, deposito

def sacar(saque, saldo, extrato, QTD_LIMITE_SAQUE, VALOR_LIMITE_SAQUE):
    if saque <= QTD_LIMITE_SAQUE:
        valor_saque = int(input('Qual valor (R$) deseja sacar de sua conta? Digite apenas números: '))
        if valor_saque <= saldo and valor_saque <= VALOR_LIMITE_SAQUE:
            saldo -= valor_saque
            extrato += f"\nSaque {saque}: R${valor_saque:.2f}"
            saque += 1
            print("Saque concluído com sucesso. Retire seu dinheiro na boca do caixa.")
            return saque, saldo, extrato
        elif valor_saque > saldo:
            print("Saldo insuficiente. Não foi possível realizar a operação.")
            return saque, saldo, extrato
        elif valor_saque > VALOR_LIMITE_SAQUE:
            print(f"Não foi possível realizar a operação. O valor limite para saque é {VALOR_LIMITE_SAQUE}")
            return saque, saldo, extrato
    else:
        print("Limite diário de saques atingido. Tente novamente após 24 horas.")
        return saque, saldo, extrato

def visualizar_extrato(saldo, extrato):
    print(f"""
--------- EXTRATO ---------
    {extrato}

---------------------------
Saldo da conta: R${saldo:.2f}
---------------------------
""")
    
def criar_usuario(usuarios):
    nome = input("Seu nome (completo): ")
    cpf = input("CPF (Somente números): ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Rua: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    sigla_estado = input("Sigla do estado: ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla_estado}"

    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    if usuarios:
        cpf_filtrado = []
        for u in usuarios:
            cpf_filtrado.append(u["cpf"])
            
        if usuario["cpf"] not in cpf_filtrado:
            print("Checando CPF...")
            usuarios.append(usuario)
            print("CPF Disponível. Usuário cadastrado")
        else:
            print("Falha ao cadastrar. CPF indisponível!")
    else:
        print("Checando CPF...")
        print("CPF Disponível. Usuário cadastrado")
        usuarios.append(usuario)

def criar_conta(usuarios, contas, numero_conta, AGENCIA):
    cpf = input("A qual CPF você deseja atrelar sua conta? ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario.setdefault("contas", [])
            usuario["contas"].append({"agencia": AGENCIA, "numero_conta": numero_conta})
            print("Conta criada com sucesso!")
            contas.append({"agencia": AGENCIA, "numero_conta": numero_conta, "cpf_usuario": cpf})
            numero_conta += 1
            break

    else:
        print("Não existe um usuário atrelado a esse CPF.")

    return numero_conta

def main():

    saldo = 0
    saque = 1
    deposito = 1
    extrato = ""
    usuarios = []
    contas = []
    numero_conta = 1

    VALOR_LIMITE_SAQUE = 500
    QTD_LIMITE_SAQUE = 3
    AGENCIA = "0001"

    menu()

    while True:

        opcao = int(input("\n=> Digite o número referente a operação em que deseja realizar: "))

        if opcao == 1:
            criar_usuario(usuarios=usuarios)

        elif opcao == 2:
            numero_conta = criar_conta(usuarios, contas, numero_conta, AGENCIA=AGENCIA)

        elif opcao == 3:
            visualizar_saldo(saldo=saldo)

        elif opcao == 4:
            saldo, extrato, deposito = depositar(saldo,extrato,deposito)

        elif opcao == 5:
            saque, saldo, extrato = sacar(saque=saque,saldo=saldo,extrato=extrato,QTD_LIMITE_SAQUE=QTD_LIMITE_SAQUE,VALOR_LIMITE_SAQUE=VALOR_LIMITE_SAQUE)
            
        elif opcao == 6:
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == 7:
            print(usuarios) if usuarios else print("Sem registros de usuários.")

        elif opcao == 8:
            print(contas) if contas else print("Sem registros de contas.")
            
        elif opcao == 0:
            print("Obrigado por utilizar nosso sistema. Volte sempre!")
            break

        else:
            print("Opção inválida.")

main()