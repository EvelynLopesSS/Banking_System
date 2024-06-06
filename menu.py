from Operacoes_class.pessoa_fisica import PessoaFisica
from Operacoes_class.pessoa_juridica import PessoaJuridica
from Operacoes_class.extrato import Extrato
from Operacoes_class.deposito import Deposito
from Operacoes_class.saque import Saque
from Operacoes_class.transferencia import Transferencia
import subprocess
import os


def verificar_banco_de_dados():
    return os.path.exists("banco_de_dados.db")

def criar_banco_de_dados():
    subprocess.run(["python", "Database/database.py"])

def main():
    if verificar_banco_de_dados():
        print("Banco de dados encontrado.")
    else:
        print("Banco de dados não encontrado. Criando banco de dados...")
        criar_banco_de_dados()

    while True:
        print("\n=== Menu ===\n")
        print("1. Criar Conta")
        print("2. Entrar na Conta")
        print("3. Sair")

        opcao_menu = input("Selecione uma opção: ")

        if opcao_menu == '1':
            print("\n=== Tipo de Conta ===\n")
            print("1. PF")
            print("2. PJ")

            opcao_tipo_conta = input("Selecione o tipo de conta: ")

            if opcao_tipo_conta == '1':
                nome = input("Digite seu nome: ")
                cpf = input("Digite seu CPF: ")
                senha = input("Digite sua senha (mínimo 8 caracteres): ")
                agencia = int(input("Digite a agência desejada: "))
                pf = PessoaFisica(nome, cpf)
                pf.criar_pessoa_fisica(senha, agencia)

            elif opcao_tipo_conta == '2':
                razao_social = input("Digite a razão social: ")
                cnpj = input("Digite o CNPJ: ")
                senha = input("Digite sua senha (mínimo 8 caracteres): ")
                agencia = int(input("Digite a agência desejada: "))
                pj = PessoaJuridica(razao_social, cnpj)
                pj.criar_pessoa_juridica(senha, agencia)

            else:
                print("Opção inválida.")

        elif opcao_menu == '2':
            print("\n=== Tipo de Conta ===\n")
            print("1. PF")
            print("2. PJ")

            opcao_tipo_conta = input("Selecione o tipo de conta: ")

            if opcao_tipo_conta == '1':
                agencia = int(input("Digite sua agência: "))
                numero_conta = int(input("Digite seu número de conta: "))
                cpf = input("Digite seu CPF: ")
                senha = input("Digite sua senha: ")
                pf = PessoaFisica(None, cpf)  # instância da classe PF sem nome
                if pf.logar_pessoa_fisica(agencia, numero_conta, cpf, senha):
                    conta_pf = pf  # Guarda a conta PF para usar no menu interno
                    menu_interno(conta_pf) 

            elif opcao_tipo_conta == '2':
                agencia = int(input("Digite sua agência: "))
                numero_conta = int(input("Digite seu número de conta: "))
                cnpj = input("Digite seu CNPJ: ")
                senha = input("Digite sua senha: ")
                pj = PessoaJuridica(None, cnpj)  #  instância da classe PF sem nome
                if pj.logar_pessoa_juridica(agencia, numero_conta, cnpj, senha):
                    conta_pj = pj  # Guarda a conta PF para usar no menu interno
                    menu_interno(conta_pj) 

            else:
                print("Opção inválida.")

        elif opcao_menu == '3':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_interno(conta):
    """Menu interno para operações bancárias."""
    while True:
        print("\n=== Menu ===")
        print("1. Sacar")
        print("2. Depósito")
        print("3. Extrato")
        print("4. Transferir")
        print("5. Sair")
        
        opcao_menu_interno = input("Selecione uma opção: ")

        if opcao_menu_interno == '1':
            valor = float(input("Digite o valor do saque: "))
            saque = Saque(conta, valor)
            saque.realizar_saque()

        elif opcao_menu_interno == '2':
            valor = float(input("Digite o valor do depósito: "))
            deposito = Deposito(conta, valor)
            deposito.realizar_deposito()

        elif opcao_menu_interno == '3':
            extrato = Extrato(conta)
            extrato.gerar_extrato()

        elif opcao_menu_interno == '4':
            agencia_destino = input("Digite a agência de destino: ")
            numero_conta_destino = input("Digite o número da conta de destino: ")
            valor_transferencia = float(input("Digite o valor da transferência: "))

            transferencia = Transferencia(conta, agencia_destino, numero_conta_destino, valor_transferencia)
            transferencia.realizar_transferencia()
        
        elif opcao_menu_interno == '5':
            print("Voltando ao menu principal...")
            break
if __name__ == "__main__":
    main()