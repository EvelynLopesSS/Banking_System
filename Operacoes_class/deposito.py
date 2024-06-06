from Operacoes_class.conta import Conta
from datetime import datetime
import sqlite3



class Deposito:
    def __init__(self, conta: Conta, valor):
        self.conta = conta
        self.valor = valor
        

    def realizar_deposito(self):
        if self.valor > 0:
            self.conta.saldo += self.valor
            data_hora = self.conta.validar_data_hora()

            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Contas
                SET saldo = saldo + ?
                WHERE id_conta = ?
            """, (self.valor, self.conta.id_conta))

            cursor.execute("""
                INSERT INTO Depositos (id_conta, valor, data_hora)
                VALUES (?, ?, ?)
            """, (self.conta.id_conta, self.valor, data_hora))
            
            conn.commit()
            conn.close()
            
            self.conta.extrato.append(f"{data_hora}: Depósito: R$ {self.valor:.2f}")
            linha = "-" * 20
            print(f"{linha * 2}\n")
            print("\033[1mOperação: DEPÓSITO\033[0m\n")
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso.\n")
            print(f"{linha * 2}")
        else:
            print("Valor inválido para depósito.")