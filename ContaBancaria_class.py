class ContaBancaria:
    
    LIMITE_SAQUE = 3
    LIMITE_POR_SAQUE_PADRAO = 500

    def __init__(self, saldo=0, limite_por_saque=None):
        self.saldo = saldo
        self.extrato = []
        self.qtde_saques_realizados = 0
        self.limite_por_saque = limite_por_saque if limite_por_saque is not None else ContaBancaria.LIMITE_POR_SAQUE_PADRAO

    def sacar(self, valor):
        if self.qtde_saques_realizados >= ContaBancaria.LIMITE_SAQUE:
            print("Você atingiu o limite diário de saques.")
        elif valor > self.limite_por_saque:
            print(f"O valor máximo para saque é de R$ {self.limite_por_saque:.2f}.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f}")
            self.qtde_saques_realizados += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    
    def extrato_conta(self):
        if not self.extrato:
            print("Não foram realizadas movimentações.")
            return

        print("Extrato da conta:")
        for movimentacao in self.extrato:
            print(movimentacao)
        
        print(f"Saldo atual da conta: R$ {self.saldo:.2f}")
        
    def depositar(self, valor):
        if valor <= 0:
            print("O valor do depósito deve ser positivo.")
            return
        
        self.saldo += valor
        self.extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
