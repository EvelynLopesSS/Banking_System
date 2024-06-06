
from datetime import datetime, timezone,timedelta

class Conta:
    def __init__(self, saldo=0):
        self.saldo = saldo
        self.extrato = []
        self.saldo_inicial = saldo  
        self.qtde_saques_realizados = 0  # Contador de saques na conta
        self.data_ultimo_saque = None  # Data do último saque
        self.id_conta = None
        
  



    def validar_data_hora(self):
        timezone_pb = timezone(timedelta(hours=-3))
        return datetime.now(timezone_pb).strftime("%d/%m/%Y %H:%M:%S %Z%z") 
    





        
        