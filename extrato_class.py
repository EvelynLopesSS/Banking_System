class ContaBancariaExtrato:
    def __init__(self, saldo=0, limite_por_saque=None):
        self.saldo = saldo
        self.extrato = []
        self.qtde_saques_realizados = 0
        self.limite_por_saque = limite_por_saque

    def extrato_conta(self):
        if not self.extrato:
            print("Não foram realizadas movimentações.")
            return

        print("Extrato da conta:")
        for movimentacao in self.extrato:
            print(movimentacao)
        
        print(f"Saldo atual da conta: R$ {self.saldo:.2f}")
