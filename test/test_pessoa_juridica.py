import sqlite3
import pytest
from Bank.pessoa_juridica import PessoaJuridica


def consultar_numero_conta(cnpj):
    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT numero_conta
        FROM Contas
        INNER JOIN PessoaJuridica ON Contas.id_pj = PessoaJuridica.id_pj
        WHERE PessoaJuridica.cnpj = ?
    """, (cnpj,))
    numero_conta = cursor.fetchone()[0]
    conn.close()
    return numero_conta

# Fixtures
@pytest.fixture
def pessoa_juridica():
    return PessoaJuridica("Empresa XYZ", "12245678000190")

# Testes
def test_criar_pessoa_juridica_sucesso(pessoa_juridica):
    assert pessoa_juridica.criar_pessoa_juridica("senha123", 1) is None
    

def test_criar_pessoa_juridica_cnpj_existente(pessoa_juridica, capsys):
    pessoa_juridica.criar_pessoa_juridica("outra_senha", 1)
    captured = capsys.readouterr()
    assert "CNPJ já cadastrado no sistema!" in captured.out

def test_logar_pessoa_juridica_sucesso(pessoa_juridica):
    numero_conta_esperado = consultar_numero_conta("12245678000190")
    assert pessoa_juridica.logar_pessoa_juridica(1, numero_conta_esperado, "12245678000190", "senha123") == True

def test_logar_pessoa_juridica_cnpj_invalido(pessoa_juridica):
    assert not pessoa_juridica.logar_pessoa_juridica(1, 123, "12345678000191", "senha456")

def test_logar_pessoa_juridica_senha_incorreta(pessoa_juridica):
    numero_conta_esperado = consultar_numero_conta("12245678000190")
    assert not pessoa_juridica.logar_pessoa_juridica(1, numero_conta_esperado, "12245678000190", "senha_incorreta")

def test_logar_pessoa_juridica_agencia_invalida(pessoa_juridica):
    numero_conta_esperado = consultar_numero_conta("12245678000190")
    assert not pessoa_juridica.logar_pessoa_juridica(2, numero_conta_esperado, "12245678000190", "senha123")

def test_logar_pessoa_juridica_conta_invalida(pessoa_juridica):
    assert not pessoa_juridica.logar_pessoa_juridica(1, 999999, "12245678000190", "senha123")