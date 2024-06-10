import pytest
from datetime import datetime, timezone, timedelta
from Operacoes_class.conta import Conta  

class TestConta:
    def test_init_extrato_empty(self):
        # Test case: Initialize a new account with an empty extrato list
        conta = Conta()
        assert conta.extrato == []

    def test_init_saldo_zero(self):
        # Test case: Initialize a new account with a zero balance
        conta = Conta()
        assert conta.saldo == 0

    def test_init_saldo_custom(self):
        # Test case: Initialize a new account with a custom balance
        custom_balance = 1000
        conta = Conta(custom_balance)
        assert conta.saldo == custom_balance

    def test_init_qtde_saques_zero(self):
        # Test case: Initialize a new account with zero saques
        conta = Conta()
        assert conta.qtde_saques_realizados == 0

    def test_init_data_ultimo_saque_none(self):
        # Test case: Initialize a new account with no last withdrawal date
        conta = Conta()
        assert conta.data_ultimo_saque is None