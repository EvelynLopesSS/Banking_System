from Operacoes_class.conta import Conta
from tabulate import tabulate
import sqlite3



class Extrato:
    def __init__(self, conta: Conta):
        self.conta = conta

    def gerar_extrato(self):
        headers = ["Data", "Operação", "Valor"]
        data = []

        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        # Consultando depósitos
        cursor.execute("""
            SELECT data_hora, 'Depósito' AS Operacao, valor
            FROM Depositos
            WHERE id_conta = ?
        """, (self.conta.id_conta,))
        depositos = cursor.fetchall()

        # Consultando saques
        cursor.execute("""
            SELECT data_hora, 'Saque' AS Operacao, valor
            FROM Saques
            WHERE id_conta = ?
        """, (self.conta.id_conta,))
        saques = cursor.fetchall()

        # Consultando transferências (origem)
        cursor.execute("""
            SELECT data_hora, 'Transferência (Saída)' AS Operacao, valor
            FROM Transferencias
            WHERE id_conta_origem = ?
        """, (self.conta.id_conta,))
        transferencias_saida = cursor.fetchall()

        # Consultando transferências (destino)
        cursor.execute("""
            SELECT data_hora, 'Transferência (Entrada)' AS Operacao, valor
            FROM Transferencias
            WHERE id_conta_destino = ?
        """, (self.conta.id_conta,))
        transferencias_entrada = cursor.fetchall()

        # Consultando empréstimos
        cursor.execute("""
            SELECT data_hora, 'Empréstimo' AS Operacao, valor
            FROM Emprestimos
            WHERE id_conta = ?
        """, (self.conta.id_conta,))
        emprestimos = cursor.fetchall()

        conn.close()

        # Adicionar os dados das movimentações ao extrato
        data.extend(depositos)
        data.extend(saques)
        data.extend(transferencias_saida)
        data.extend(transferencias_entrada)
        data.extend(emprestimos)

        data.sort(key=lambda x: x[0])

        # Adicionar saldo final ao extrato
        data_hora_final = self.conta.validar_data_hora()
        data.append([data_hora_final, "Saldo Final", self.conta.saldo])

        linha = "-" * 20
        print(f"{linha * 2}\n")
        print("\033[1mOperação: EXTRATO\033[0m\n")
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"{linha * 2}")