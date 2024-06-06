from Operacoes_class.conta import Conta
from datetime import datetime
import sqlite3

class Saque:
    def __init__(self, conta: Conta, valor, limite_saque=3, limite_por_saque=500):
        self.conta = conta
        self.valor = valor
        self.limite_saque = limite_saque
        self.limite_por_saque = limite_por_saque



    def realizar_saque(self):
        data_atual = self.conta.validar_data_hora()

        if self.conta.data_ultimo_saque is not None and data_atual == self.conta.data_ultimo_saque:
            if self.conta.qtde_saques_realizados >= self.limite_saque:
                print(f"Você atingiu o limite diário de {self.limite_saque} de saques.")
                return False
        else:
            self.conta.qtde_saques_realizados = 0  # Reinicia a contagem se for um novo dia

        if self.valor > self.limite_por_saque:
            print(f"O valor máximo para saque é de R$ {self.limite_por_saque:.2f}.")
            return False
        elif self.valor > self.conta.saldo:
            print("Saldo insuficiente.")
            return False
        else:
            self.conta.saldo -= self.valor
            data_hora = self.conta.validar_data_hora()
            self.conta.extrato.append(f"{data_hora}: Saque: R$ {self.valor:.2f}")
            self.conta.qtde_saques_realizados += 1
            self.conta.data_ultimo_saque = data_atual  # Atualiza a data do último saque

            linha = "-" * 20
            print(f"{linha * 2}\n")
            print("\033[1mOperação: SAQUE\033[0m\n")
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso.\n")
            print(f"{linha * 2}")

            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Contas
                SET saldo = saldo - ?
                WHERE id_conta = ?
            """, (self.valor, self.conta.id_conta))

            cursor.execute("""
                INSERT INTO Saques (id_conta, valor, data_hora)
                VALUES (?, ?, ?)
            """, (self.conta.id_conta, self.valor, data_hora))
            conn.commit()
            conn.close()

            return True
    
                