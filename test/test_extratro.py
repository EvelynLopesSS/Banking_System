import pytest
from Bank.conta import Conta
from Bank.extrato import Extrato

@pytest.fixture
def conta_existente():
    conta = Conta()
    conta.id_conta = 1  # ID da conta existente no banco de dados
    conta.saldo = 1000.00
    return conta

def test_gerar_extrato(conta_existente, capsys):
    extrato = Extrato(conta_existente)
    extrato.gerar_extrato()

    # Verificando a saída padrão
    captured = capsys.readouterr()
    assert "Operação: EXTRATO" in captured.out
    assert "Depósito" in captured.out
    assert "Saque" in captured.out
    assert "Transferência (Saída)" in captured.out
    # Verificar se a string não está presente na saída, pois a conta 1 não tem essa operação
    assert "Transferência (Entrada)" not in captured.out  