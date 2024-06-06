# 💰 Sistema Bancário em Python

Este projeto é uma implementação básica de um sistema bancário que permite realizar operações de depósito, saque, transferência,  geração de extrato com as movimentações realizadas.


## 📂 Estrutura do Projeto

O projeto é dividido em classes para representar as operações bancárias e um arquivo principal (menu.py) para interagir com o usuário. As classes estão organizadas na pasta Operacoes_class:

- `Operacoes_class/pessoa_fisica.py`: Classe para representar contas pessoa física.
- `Operacoes_class/pessoa_juridica.py`: Classe para representar contas pessoa jurídica.
- `Operacoes_class/extrato.py`: Classe para gerar extratos de contas.
- `Operacoes_class/deposito.py`: Classe para realizar depósitos em contas.
- `Operacoes_class/saque.py`: Classe para realizar saques em contas.
- `Operacoes_class/transferencia.py`: Classe para realizar transferências entre contas.

A criação do Banco de Dados e os triggers estão separados :
- Database/database.py: Script para criar o banco de dados SQLite e as tabelas necessárias.



## ⚙️ Funcionalidades

### 1. 👤 Criação de Conta
- Permite a criação de dois tipos de conta: Pessoa Jurídica e Pessoa Fisíca.

### 2. 📥 Depósito
- Permite depositar valores positivos na conta bancária.
- Todos os depósitos são armazenados e exibidos na operação de extrato.

### 3. 📤 Saque
- Permite realizar até 3 saques diários.
- Limite máximo de R$ 500,00 por saque.
- Caso o usuário não tenha saldo suficiente, o sistema exibe uma mensagem de saldo insuficiente.
- Todos os saques são armazenados e exibidos na operação de extrato.

### 4. 📄 Extrato
- Lista todos os depósitos, saques e transferências realizados na conta.
- Exibe o saldo final da conta.
- Se não houver movimentações, exibe a mensagem: "Não foram realizadas movimentações."
- Os valores são exibidos no formato `R$ xxx,xx`.
- Exemplo: 1500.45 = R$ 1500,45

## 👁️ Testes Unitários
Este projeto inclui uma suíte abrangente de testes unitários para garantir que cada componente individual do código funcione conforme o esperado. Os testes unitários são escritos utilizando a biblioteca pytest.

## 📋 Requisitos
- sqlite3
- datetime
- tabulate


## 🚀 Como Executar
Execute o arquivo:

`python menu.py`
