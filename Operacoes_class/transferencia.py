import sqlite3
from Operacoes_class.conta import Conta
from datetime import datetime

class Transferencia:
    def __init__(self, conta_origem: Conta, agencia_destino, numero_conta_destino, valor):
        self.conta_origem = conta_origem
        self.agencia_destino = agencia_destino
        self.numero_conta_destino = numero_conta_destino
        self.valor = valor

    def realizar_transferencia(self):
        if self.valor <= 0:
            print("Valor inválido para transferência.")
            return False

        if self.conta_origem.saldo < self.valor:
            print("Saldo insuficiente na conta de origem.")
            return False

        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        try:

            # Verificar se a conta de destino existe
            cursor.execute("""
                SELECT id_conta, saldo
                FROM Contas
                WHERE agencia = ? AND numero_conta = ?
            """, (self.agencia_destino, self.numero_conta_destino))
            resultado_destino = cursor.fetchone()

            if resultado_destino is None:
                print("Conta de destino não encontrada.")
                return False

            id_conta_destino = resultado_destino[0]
            saldo_destino = resultado_destino[1]

            # Atualizando saldos no banco de dados
            cursor.execute("""
                UPDATE Contas
                SET saldo = saldo - ?
                WHERE id_conta = ?
            """, (self.valor, self.conta_origem.id_conta))

            cursor.execute("""
                UPDATE Contas
                SET saldo = saldo + ?
                WHERE id_conta = ?
            """, (self.valor, id_conta_destino))

            # Inserindo registro de transferência
            data_hora = self.conta_origem.validar_data_hora()
            cursor.execute("""
                INSERT INTO Transferencias (id_conta_origem, id_conta_destino, valor, data_hora)
                VALUES (?, ?, ?, ?)
            """, (self.conta_origem.id_conta, id_conta_destino, self.valor, data_hora))

            conn.commit()

            self.conta_origem.saldo -= self.valor
            self.conta_origem.extrato.append(f"{data_hora}: Transferência Enviada: R$ {self.valor:.2f}")

            linha = "-" * 20
            print(f"{linha * 2}\n")
            print("=== Comprovante de Transferência ===")
            print(f"Data/Hora: {data_hora}")
            print("Conta de Destino:")
            print(f"- Agência: {self.agencia_destino}")
            print(f"- Número da Conta: {self.numero_conta_destino}")
            print(f"Valor transferido: R$ {self.valor:.2f}")
            print("=====================================")

            return True

        except Exception as e:
            print(f"Erro ao realizar transferência: {e}")
            return False

        finally:
            conn.close()



