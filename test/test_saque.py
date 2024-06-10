import pytest
import sqlite3
from Operacoes_class.saque import Saque
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

def test_saque_valor_dentro_limite(conta_existente):
    saque = Saque(conta_existente, 200.00)
    assert saque.realizar_saque() == True
    assert conta_existente.saldo == 800.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 800.00

def test_saque_valor_acima_limite(conta_existente, capsys):
    saque = Saque(conta_existente, 600.00)
    assert saque.realizar_saque() == False
    assert conta_existente.saldo == 1000.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 1000.00

    captured = capsys.readouterr()
    assert "O valor máximo para saque é de R$ 500.00." in captured.out

def test_saque_saldo_insuficiente(conta_existente, capsys):
    saque = Saque(conta_existente, 1200.00)
    saque.limite_por_saque = 2000.00  # Ajustar o o limite para testar saldo insuficiente
    assert saque.realizar_saque() == False
    assert conta_existente.saldo == 1000.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 1000.00

    captured = capsys.readouterr()
    assert "Saldo insuficiente." in captured.out

def test_limite_diario_saques(conta_existente, capsys):
    saque = Saque(conta_existente, 200.00)
    # Realizar 3 saques dentro do limite permitido
    for _ in range(3):
        assert saque.realizar_saque() == True

    assert conta_existente.saldo == 400.00

    # Tentando realizar um quarto saque no mesmo dia
    assert saque.realizar_saque() == False
    assert conta_existente.saldo == 400.00

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM Contas WHERE id_conta = 1")
    saldo = cursor.fetchone()[0]
    conn.close()
    assert saldo == 400.00

    captured = capsys.readouterr()
    assert "Você atingiu o limite diário de 3 de saques." in captured.out