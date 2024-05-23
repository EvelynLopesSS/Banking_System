class ContaBancariaDeposito:
    def __init__(self, saldo=0, limite_por_saque=None):
        self.saldo = saldo
        self.extrato = []
        self.qtde_saques_realizados = 0
        self.limite_por_saque = limite_por_saque

    def depositar(self, valor):
        if valor <= 0:
            print("O valor do depósito deve ser positivo.")
            return
        
        self.saldo += valor
        self.extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
