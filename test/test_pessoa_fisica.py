import pytest
from Bank.pessoa_fisica import PessoaFisica
import sqlite3



def consultar_numero_conta(cpf):
    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT numero_conta
        FROM Contas
        INNER JOIN PessoaFisica ON Contas.id_pf = PessoaFisica.id_pf
        WHERE PessoaFisica.cpf = ?
    """, (cpf,))
    numero_conta = cursor.fetchone()[0]
    conn.close()
    return numero_conta

@pytest.fixture
def pessoa_fisica():
    return PessoaFisica("Fulano de Tal", "72355678913")

def test_criar_pessoa_fisica(pessoa_fisica, capsys):
    pessoa_fisica.criar_pessoa_fisica("senha123", 1)

    captured = capsys.readouterr()

    assert "Pessoa física criada com sucesso!" in captured.out
    assert "Conta criada com sucesso!" in captured.out
    assert "Cliente" in captured.out
    assert "CPF" in captured.out
    assert "Conta" in captured.out
    assert "Agência" in captured.out

def test_logar_pessoa_fisica_sucesso(pessoa_fisica):
    numero_conta_esperado = consultar_numero_conta("72355678913")

    assert pessoa_fisica.logar_pessoa_fisica(1, numero_conta_esperado, "72355678913", "senha123") == True
def test_logar_pessoa_fisica_cpf_invalido(pessoa_fisica):
    numero_conta_esperado = consultar_numero_conta("72355678913")
    assert pessoa_fisica.logar_pessoa_fisica(1, numero_conta_esperado, "72355678912", "senha123") == False

def test_logar_pessoa_fisica_agencia_invalida(pessoa_fisica):
    numero_conta_esperado = consultar_numero_conta("72355678913")
    assert pessoa_fisica.logar_pessoa_fisica(2, numero_conta_esperado, "72355678913", "senha123") == False

def test_logar_pessoa_fisica_conta_invalida(pessoa_fisica):
    assert pessoa_fisica.logar_pessoa_fisica(1, 2, "72355678913", "senha123") == False

def test_logar_pessoa_fisica_senha_incorreta(pessoa_fisica):
    numero_conta_esperado = consultar_numero_conta("72355678913")

    assert pessoa_fisica.logar_pessoa_fisica(1, numero_conta_esperado, "72355678913", "senha_incorreta") == False
