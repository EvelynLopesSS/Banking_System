

import sqlite3

def criar_banco_de_dados():
    """Cria as tabelas do banco de dados SQLite."""

    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE PessoaFisica (
        id_pf INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(255) NOT NULL,
        cpf VARCHAR(11) UNIQUE NOT NULL,
        senha VARCHAR(8) NOT NULL,
        agencia INTEGER NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)           

    cursor.execute("""
    CREATE TABLE PessoaJuridica (
        id_pj INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social VARCHAR(255) NOT NULL,
        cnpj VARCHAR(18) UNIQUE NOT NULL,
        senha VARCHAR(8) NOT NULL,
        agencia INTEGER NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)   

    cursor.execute("""
    CREATE TABLE Contas (
        id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
        agencia INTEGER NOT NULL,
        numero_conta INTEGER NOT NULL,
        saldo DECIMAL(10,2) DEFAULT 0,
        id_pf INTEGER,
        id_pj INTEGER,
        FOREIGN KEY (id_pf) REFERENCES PessoaFisica(id_pf),
        FOREIGN KEY (id_pj) REFERENCES PessoaJuridica(id_pj),
        UNIQUE (agencia, numero_conta)
    );
    """)  

    # Criando Triggers para gerar um numero_conta e  garantir que o número da conta seja único na mesma agência
    cursor.execute("""
    CREATE TRIGGER gerar_conta_pf
    AFTER INSERT ON PessoaFisica
    BEGIN
        INSERT INTO Contas (agencia, numero_conta, id_pf)
        VALUES (NEW.agencia, 
                (SELECT COALESCE(MAX(numero_conta), 0) + 1 FROM Contas WHERE agencia = NEW.agencia),
                NEW.id_pf);
    END;
    """)

    # Trigger para gerar número de conta para Pessoa Jurídica
    cursor.execute("""
    CREATE TRIGGER gerar_conta_pj
    AFTER INSERT ON PessoaJuridica
    BEGIN
        INSERT INTO Contas (agencia, numero_conta, id_pj)
        VALUES (NEW.agencia, 
                (SELECT COALESCE(MAX(numero_conta), 0) + 1 FROM Contas WHERE agencia = NEW.agencia),
                NEW.id_pj);
    END;
    """)



    cursor.execute("""
    CREATE TABLE Depositos (
        id_deposito INTEGER PRIMARY KEY AUTOINCREMENT,
        id_conta INTEGER,
        valor DECIMAL(10,2) NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_conta) REFERENCES Contas(id_conta)
    );
    """) 

    cursor.execute("""
    CREATE TABLE Saques (
        id_saque INTEGER PRIMARY KEY AUTOINCREMENT,
        id_conta INTEGER,
        valor DECIMAL(10,2) NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_conta) REFERENCES Contas(id_conta)
    );
    """) 

    cursor.execute("""
    CREATE TABLE Transferencias (
        id_transferencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_conta_origem INTEGER,
        id_conta_destino INTEGER,
        valor DECIMAL(10,2) NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_conta_origem) REFERENCES Contas(id_conta),
        FOREIGN KEY (id_conta_destino) REFERENCES Contas(id_conta)
    );
    """) 

    cursor.execute("""
    CREATE TABLE Emprestimos (
        id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_conta INTEGER,
        valor DECIMAL(10,2) NOT NULL,
        juros DECIMAL(4,2) NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_vencimento DATETIME,
        FOREIGN KEY (id_conta) REFERENCES Contas(id_conta)
    );
    """) 

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco_de_dados()
    print("Banco de dados criado com sucesso!")