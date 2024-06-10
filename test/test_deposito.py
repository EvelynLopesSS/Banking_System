import pytest
import sqlite3
from Operacoes_class.deposito import Deposito
from Operacoes_class.conta import Conta

@pytest.fixture
def conta_existente():
    conta = Conta()
    conta.id_conta = 1  # ID da conta existente no banco de dados

    # Ajustar o saldo da conta existente para um valor conhecido
    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Contas SET saldo = 1000.00 WHERE id_conta = 1")
    conn.commit()
    conn.close()

    conta.saldo = 1000.00
    return conta

def test_deposito_valor_positivo_conta_existente(conta_existente):
    deposito = Deposito(conta_existente, 500.00)
    deposito.realizar_deposito()
    assert conta_existente.saldo == 1500.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 1500.00


def test_deposito_valor_negativo_conta_existente(conta_existente, capsys):
    deposito = Deposito(conta_existente, -100.00)
    deposito.realizar_deposito()
    assert conta_existente.saldo == 1000.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 1000.00

    captured = capsys.readouterr()
    assert "Valor inválido para depósito." in captured.out
