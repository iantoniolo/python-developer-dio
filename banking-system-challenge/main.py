print(
"""
-------- SISTEMA BANCÁRIO --------

    [1]: Visualizar saldo
    [2]: Depositar
    [3]: Sacar
    [4]: Visualizar extrato
    [0]: Sair

----------------------------------
"""
)

saldo = 0
saque = 1
extrato = []

VALOR_LIMITE_SAQUE = 500
QTD_LIMITE_SAQUE = 3

while True:
    
    opcao = int(input('\nDigite o número referente a operação em que deseja realizar: '))

    if opcao == 1:
        print(f"Saldo disponível: R${saldo},00")

    elif opcao == 2:
        identificador_deposito = 1 
        valor_deposito = int(input('Qual valor (R$) deseja depositar em sua conta? Digite apenas números: '))
        saldo += valor_deposito
        extrato.append(f"Depósito {identificador_deposito}: R${valor_deposito},00")
        identificador_deposito += 1
        print("Depósito concluído com sucesso.")

    elif opcao == 3:
        if saque <= QTD_LIMITE_SAQUE:
            valor_saque = int(input('Qual valor (R$) deseja sacar de sua conta? Digite apenas números: '))
            if valor_saque <= saldo:
                saldo -= valor_saque
                extrato.append(f"Saque {saque}: R${valor_saque},00")
                saque += 1
                print("Saque concluído com sucesso. Retire seu dinheiro na boca do caixa.")
            elif valor_saque > saldo:
                print("Saldo insuficiente. Não foi possível realizar a operação.")
        else:
            print("Limite diário de saques atingido. Tente novamente após 24 horas.")
        
    elif opcao == 4:
        
        print("------ EXTRATO ------")
    
        for e in extrato:
            print(e)

        print("---------------------")
        
    elif opcao == 0:
        print("Obrigado por utilizar nosso sistema. Volte sempre!")
        break

    else:
        print("Opção inválida.")
