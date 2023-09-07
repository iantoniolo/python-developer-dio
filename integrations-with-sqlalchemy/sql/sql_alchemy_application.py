"""
    Desafio de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM
"""

import sqlalchemy

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select 

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(11), unique=True)
    email = Column(String(30), unique=True)
    

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, conta={self.conta})"


class Conta(Base):
    __tablename__ = "conta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Float)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero})"
    

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)
session = Session(engine)

def menu():
    opcao = int(input(
"""
Cadastro de Clientes

[1] Cadastrar conta
[2] Buscar cliente
[3] Buscar contas de um cliente
[4] Ordenar contas
[5] Verificar dados bancários dos clientes
[6] Verificar quantidade de clientes
[0] Sair

=> Qual opção você deseja? """
))
    return opcao

while True:

    opcao = menu()

    if opcao == 1:

        nome = input("Nome: ").lower()
        cpf = input("CPF (Digite apenas números): ")
        email = input("E-mail: ")
        saldo = float(input("Saldo da conta: "))

        cliente_existente = session.query(Cliente).filter_by(cpf=cpf).first()

        if cliente_existente:
            cliente = cliente_existente
            print("\nCliente já cadastrado.")
        else:
            cliente = Cliente(
                nome=nome,
                cpf=cpf,
                email=email,
            )
            
            session.add(cliente)
            session.commit()

        numero_conta = 1

        conta = Conta(
            tipo="conta corrente",
            agencia="0001",
            numero=numero_conta,
            cliente=cliente,
            saldo=saldo
        )

        numero_conta += 1

        session.add(conta)
        session.commit()
        print("\nCadastro concluído com sucesso.")

    elif opcao == 2:
        cpf_cliente = input("Digite o CPF do cliente: ")
        stmt_cliente = select(Cliente).where(Cliente.cpf == cpf_cliente)
        cliente = session.execute(stmt_cliente).scalar()
        if cliente:
            print(cliente)
        else:
            print("\nCliente não encontrado.")

    elif opcao == 3:
        cpf_cliente = input("\nDigite o CPF do cliente: ")

        cliente = session.query(Cliente).filter_by(cpf=cpf_cliente).first()

        if cliente:
            contas = cliente.conta

            if contas:
                for conta in contas:
                    print(conta)
            else:
                print("\nCliente não possui contas.")
        else:
            print("\nCliente não encontrado.")

    elif opcao == 4:
        stmt_order = session.query(Cliente).join(Conta).order_by(Conta.numero)
        for result in stmt_order:
            print(result)

    elif opcao == 5:
        stmt_join = session.query(Cliente.cpf, Conta.tipo, Conta.agencia, Conta.numero).join(Conta).all()
        for result in stmt_join:
            print(f"\nCPF: {result[0]}, Tipo de Conta: {result[1]}, Agência: {result[2]}, Número da Conta: {result[3]}")

    elif opcao == 6:
        stmt_count = select(func.count("*")).select_from(Cliente)
        for result in session.scalars(stmt_count):
            print(f"\nTotal de clientes cadastrados: {result}")

    elif opcao == 0:
        break

    else:
        print("Opção inválida.")

