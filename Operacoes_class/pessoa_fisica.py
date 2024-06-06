from Operacoes_class.conta import Conta
import sqlite3
from tabulate import tabulate




class PessoaFisica(Conta):
    def __init__(self, nome, cpf, saldo=None):
        super().__init__(saldo)

        self.nome = nome
        self.conta = None
        self.cpf = cpf
        self.id_pf = None
        self.senha = None
        self.agencia = None
        self.saldo = saldo

    def criar_pessoa_fisica(self, senha, agencia):
        """Cria uma pessoa física no banco de dados e associa uma conta a ela."""
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        try:
            
            cursor.execute("""
                INSERT INTO PessoaFisica (nome, cpf, senha, agencia)
                VALUES (?, ?, ?, ?)
            """, (self.nome, self.cpf, senha, agencia))

            # Recupera o ID da pessoa física recém-inserida
            self.id_pf = cursor.lastrowid
            

            # Consulta a tabela Contas para obter os dados da conta
            cursor.execute("""
                SELECT agencia, numero_conta 
                FROM Contas
                WHERE id_pf = ?
            """, (self.id_pf,))
            conta_info = cursor.fetchone()

            agenc = conta_info[0]
            numero_conta = conta_info[1]
            conn.commit()
            print("Pessoa física criada com sucesso!")

            print("Conta criada com sucesso!")
            print("Detalhes:")
            table_data = [
                ["Cliente", self.nome],
                ["CPF", self.cpf],
                ["Conta", numero_conta],
                ["Agência", agenc]
            ]
            print(tabulate(table_data, headers=["Informação", "Dados"], tablefmt="grid"))

        except sqlite3.IntegrityError:
            print("CPF já cadastrado no sistema!")
        finally:
            conn.close()
    def logar_pessoa_fisica(self, agencia, conta, cpf, senha):

            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    SELECT Contas.id_conta, Contas.saldo
                    FROM Contas
                    INNER JOIN PessoaFisica ON Contas.id_pf = PessoaFisica.id_pf
                    WHERE PessoaFisica.cpf = ? AND Contas.agencia = ? AND Contas.numero_conta = ?
                """, (cpf, agencia, conta))
                resultado = cursor.fetchone()

                if resultado is not None:
                    self.id_conta = resultado[0]
                    self.saldo = resultado[1]

                    cursor.execute("""
                        SELECT senha
                        FROM PessoaFisica
                        WHERE cpf = ?
                    """, (cpf,))
                    senha_banco = cursor.fetchone()[0]

                    if senha_banco == senha:
                        self.agencia = agencia
                        print("Login realizado com sucesso!")
                        return True
                    else:
                        print("Senha incorreta.")
                        return False
                else:
                    print("CPF, agência ou número de conta inválidos.")
                    return False

            except Exception as e:
                print(f"Erro durante o login: {e}")
                return False

            finally:
                conn.close()