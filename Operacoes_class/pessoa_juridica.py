from Operacoes_class.conta import Conta
import sqlite3
from tabulate import tabulate



class PessoaJuridica(Conta):
    def __init__(self, razao_social, cnpj, saldo=0):
        super().__init__(saldo)
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.id_pj = None
        self.senha = None
        self.agencia = None
        self.saldo = saldo

    def criar_pessoa_juridica(self,senha, agencia):
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        try:
            
            cursor.execute("""
                INSERT INTO PessoaJuridica (razao_social, cnpj, senha, agencia)
                VALUES (?, ?, ?, ?)
            """, (self.razao_social, self.cnpj, senha, agencia))

            # Recupera o ID da pj recém-inserida
            self.id_pj = cursor.lastrowid

            cursor.execute("""
                SELECT agencia, numero_conta 
                FROM Contas
                WHERE id_pj = ?
            """, (self.id_pj,))
            conta_info = cursor.fetchone()

            agenc = conta_info[0]
            numero_conta = conta_info[1]
            conn.commit()
            print("Pessoa jurídica criada com sucesso!")

            print("Conta criada com sucesso!")
            print("Detalhes:")
            table_data = [
                ["Cliente", self.razao_social],
                ["CPF", self.cnpj],
                ["Conta", numero_conta],
                ["Agência", agenc]
            ]
            print(tabulate(table_data, headers=["Informação", "Dados"], tablefmt="grid"))
        except sqlite3.IntegrityError:
            print("CNPJ já cadastrado no sistema!")
        finally:
            conn.close()
    def logar_pessoa_juridica(self, agencia, conta, cnpj, senha):
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        try:
        
            cursor.execute("""
                SELECT Contas.id_conta, Contas.saldo
                FROM Contas
                INNER JOIN PessoaJuridica ON Contas.id_pj = PessoaJuridica.id_pj
                WHERE PessoaJuridica.cnpj = ? AND Contas.agencia = ? AND Contas.numero_conta = ?
            """, (cnpj, agencia, conta))
            resultado = cursor.fetchone()

            if resultado is not None:
                self.id_conta = resultado[0]
                self.saldo = resultado[1]

                cursor.execute("""
                    SELECT senha
                    FROM PessoaJuridica
                    WHERE cnpj = ?
                """, (cnpj,))
                senha_banco = cursor.fetchone()[0]

                if senha_banco == senha:
                    self.agencia = agencia
     
                    print("Login realizado com sucesso!")
                    return True
                else:
                    print("Senha incorreta.")
                    return False
            else:
                print("CNPJ, agência ou número de conta inválidos.")
                return False

        except Exception as e:
            print(f"Erro durante o login: {e}")
            return False

        finally:
            conn.close()









