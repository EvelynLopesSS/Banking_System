from ContaBancaria_class  import ContaBancaria

def main():
    saldo_inicial = float(input("Informe o saldo inicial da conta: "))
    conta = ContaBancaria(saldo_inicial)

    while True:
        print("\nMenu de Operações:")
        print("1. Sacar")
        print("2. Depositar")
        print("3. Extrato")
        print("4. Início")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            valor = float(input("Digite o valor para saque: R$ "))
            conta.sacar(valor)
        elif opcao == '2':
            valor = float(input("Digite o valor para depósito: R$ "))
            conta.depositar(valor)
        elif opcao == '3':
            conta.extrato_conta()
        elif opcao == '4':
            print("Retornando ao início.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
