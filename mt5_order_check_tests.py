import MetaTrader5 as mt5
import json
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time


teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials_test.json')
not_teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials.json')

is_test = True
FILE_PATH = teste_path if is_test else not_teste_path

# Inicialização ======================================
with open(FILE_PATH) as f:
    credentials = json.load(f)
# Caso o mt5 nao inicialize, quit()
if not mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'], path="C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe"):
    print("initialize() failed, error code = ", mt5.last_error())
    mt5.shutdown(); quit()

account_currency=mt5.account_info().currency
print("Moeda corrente:", account_currency)
 
# preparamos o ativo
symbol="PETR4"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "não foi encontrado, não é possível chamar order_check()")
    mt5.shutdown()
    quit()
 
# se o símbolo não estiver disponível no MarketWatch, adicionamos
'''
MarketWatch é um site que fornece informações financeiras, notícias de negócios, análises e dados do mercado de ações. 
Junto com The Wall Street Journal e Barron's, é uma subsidiária da Dow Jones & Company, propriedade da News Corp
'''
if not symbol_info.visible:
    print(symbol, "não está visível, tentando conectar...")
    if not mt5.symbol_select(symbol,True):
        print(f"symbol_select({symbol}) falhou, exit")
        mt5.shutdown()
        quit()
 
# preparamos a solicitação
point = mt5.symbol_info(symbol).point
ask = mt5.symbol_info_tick(symbol).ask
request = {
    "action": mt5.TRADE_ACTION_DEAL,            # TRADE_ACTION_DEAL -> Ordem imediata
    "symbol": symbol,
    "volume": 3.0,
    "type": mt5.ORDER_TYPE_BUY,                 # ORDER_TYPE_BUY -> Ordem para compra
    "price": ask,
    "sl": ask-100*point,
    "tp": ask+100*point,
    "deviation": 10,
    "magic": 234000,
    "comment": "asimov python script",
    "type_time": mt5.ORDER_TIME_GTC,            # ORDER_TIME_GTC -> A ordem permanecerá na fila até ser tirada
    "type_filling": mt5.ORDER_FILLING_RETURN,   # ORDER_FILLING RETURN -> Não entendi NOTE perguntar pro T
}

# verificamos e exibimos o resultado como está
result = mt5.order_check(request)
print(result)
# solicitamos o resultado na forma de um dicionário e exibimos elemento por elemento
result_dict=result._asdict()
for field in result_dict.keys():
    print(f"   {field}={result_dict[field]}")
    # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
    if field=="request":
        traderequest_dict=result_dict[field]._asdict()
        for tradereq_filed in traderequest_dict:
            print(f"       traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
 
# O request enviado esta armazendado no request, caso queira checar
# request_trade = result._asdict()['request']

# concluímos a conexão ao terminal MetaTrader 5
# mt5.shutdown()