from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def __str__(self):
        return f"Nome: {self.nome}\nCPF: {self.cpf}\nData de Nascimento: {self.data_nascimento}\nEndereço: {self._endereco}"

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0.00
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor) -> bool:
        if valor < self.saldo:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True

        elif valor > self.saldo:
            print("Saldo insuficiente")
        
        else: 
            print("Valor inválido.")

        return False
    
    def depositar(self, valor) -> bool:
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso")
            return True
        else:
            print("Valor inválido")
            return False
        
    def __str__(self):
        return f"Cliente: {self.cliente.nome}\nAgência: {self.agencia}\nConta corrente: {self.numero}\nSaldo: R${self.saldo:.2f}\n"

class ContaCorrente(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self._limite = 500
        self._limite_saque = 3
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saque(self):
        return self._limite_saque
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__])

        print(f"Numero saques {numero_saques}")
    
        if valor > self.limite:
            print("Valor de saque excedeu o limite de R$500,00. Por favor, tente novamente.")

        elif numero_saques >= self.limite_saque:
            print("Limite de saques excedido. Tente novamente, após 24 horas.")
            
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"Cliente: {self.cliente.nome}\nAgência: {self.agencia}\nConta corrente: {self.numero}\n"
    
class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    print(
"""
-------- SISTEMA BANCÁRIO --------

    [1]: Cadastrar cliente
    [2]: Criar conta
    [3]: Depositar
    [4]: Sacar
    [5]: Visualizar extrato
    [6]: Listar clientes
    [7]: Listar contas
    [0]: Sair

----------------------------------
"""
)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\nCliente não possui conta.")
        return

    return cliente._contas[0]

def introducao_opcoes(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        segunda_tentativa = int(input(f"O CPF informado não está atrelado a nenhum cliente.\nSe deseja realizar um novo cadastro, aperte 2.\ne para sair, tecle 1: "))
        
        if segunda_tentativa == 2:
            criar_conta(clientes, contas)
        elif segunda_tentativa == 1:
            return
        else:
            print("Valor informado inválido")
            return
        
    return cliente

def depositar(clientes, contas):
    cliente = introducao_opcoes(clientes, contas)

    valor_deposito = float(input('Qual valor deseja depositar em sua conta? Digite apenas números: '))
    deposito = Deposito(valor_deposito)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, deposito)
    

def sacar(clientes, contas):
    cliente = introducao_opcoes(clientes, contas)

    valor_saque = int(input('Qual valor deseja sacar de sua conta? Digite apenas números: '))
    saque = Saque(valor_saque)

    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return

    cliente.realizar_transacao(conta, saque)

def visualizar_extrato(clientes, contas):
    cliente = introducao_opcoes(clientes, contas)
    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return
        
    print("\n------------ EXTRATO ------------")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Extrato sem registros."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print("---------------------------------")
    print(f"\nSaldo atual: R${conta.saldo:.2f}")
    print("---------------------------------")

def criar_conta(clientes, contas):
    numero_conta = len(contas) + 1
    cliente = introducao_opcoes(clientes, contas)
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("Conta criada com sucesso")

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("CPF inválido. Cliente já cadastrado.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso")

def main():

    clientes = []
    contas = []

    menu()

    while True:

        opcao = int(input("\n=> Digite o número referente a operação em que deseja realizar: "))

        if opcao == 1:
            cadastrar_cliente(clientes)

        elif opcao == 2:
            criar_conta(clientes, contas)

        elif opcao == 3:
            depositar(clientes, contas)

        elif opcao == 4:
            sacar(clientes, contas)
            
        elif opcao == 5:
            visualizar_extrato(clientes, contas)

        elif opcao == 6:
            [print(cliente) for cliente in clientes] if clientes else print("Sem registros de usuários.")

        elif opcao == 7:
            [print(conta) for conta in contas] if contas else print("Sem registros de contas.")
            
        elif opcao == 0:
            print("Obrigado por utilizar nosso sistema. Volte sempre!")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
