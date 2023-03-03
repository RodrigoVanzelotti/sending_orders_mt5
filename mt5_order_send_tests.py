import MetaTrader5 as mt5
import json
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time

def error_quit(message=None):
    print(message)
    mt5.shutdown(); quit()

def order_result_log(result_object):
    print(f"2. order_send falhou, retcode={result.retcode}")
    # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result_object._asdict()
    for field in result_dict.keys():
        print(f"   {field}={result_dict[field]}")
        #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print(f"\ttraderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
 

teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials_test.json')
not_teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials.json')

is_test = True
FILE_PATH = teste_path if is_test else not_teste_path

# Inicialização ======================================
with open(FILE_PATH) as f:
    credentials = json.load(f)
# Caso o mt5 nao inicialize, quit()
if not mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'], path="C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe"):
    error_quit(f"initialize() failed, error code = {mt5.last_error()}")

account_currency = mt5.account_info().currency
print("Moeda corrente:",account_currency)

# preparamos o ativo
symbol = "ITUB4"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    error_quit(f"{symbol} não foi encontrado, não é possível chamar order_check()")
 
# se o símbolo não estiver disponível no MarketWatch, adicionamos
if not symbol_info.visible:
    print(symbol, "não está visível, tentando conectar...")
    if not mt5.symbol_select(symbol,True):
        error_quit(f"symbol_select({symbol}) falhou, exit")
 
# ORDEM DE COMPRA ==================================
lot = 100.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,         # ordem de mercado para compra
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "asimov python script open",
    "type_time": mt5.ORDER_TIME_GTC,            # A ordem permanecerá na fila até ser tirada
    "type_filling": mt5.ORDER_FILLING_RETURN,   # Ordem manual
}
 
# enviamos a solicitação de negociação
result = mt5.order_send(request)

# verificamos o resultado da execução
if result.retcode != mt5.TRADE_RETCODE_DONE:
    order_result_log(result); error_quit()
 
# resultados da ordem de compra
position_id = result.order
print('POSIÇÃO:', position_id)

print(f"1. order_send(): by {symbol} {lot} lots at {price} desvio={deviation} points")
print("2. order_send() executada:")
print(f"   posição aberta: POSITION_TICKET={position_id}")
print(f"   timer 2s antes de fechar a posição #{position_id}")

# tempo de processamento e redefinição da posição
time.sleep(2)
position_id = result.order
print('POSIÇÃO:', position_id)

# ORDEM DE FECHAMENTO ============================
price = mt5.symbol_info_tick(symbol).bid
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,        # ordem de mercado para venda
    "position": position_id,            # ticket
    "price": price,                     # preço bid
    "deviation": deviation,             
    "magic": 234000,
    "comment": "asimov python script close",
    "type_time": mt5.ORDER_TIME_GTC,    # A ordem permanecerá na fila até ser tirada
    "type_filling": mt5.ORDER_FILLING_RETURN,   # Ordem manual
}

# enviamos a solicitação de negociação
result = mt5.order_send(request)

# verificamos o resultado da execução
print(f"3. close position #{position_id}: sell {symbol} {lot} lots at {price} desvio={deviation} pontos")
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"4. order_send falhou, retcode={result.retcode}")
    print("   resultado",result)
else:
    print(f"4. posição #{position_id} closed, {result}")
   # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result._asdict()
    for field in result_dict.keys():
        print(f"   {field}={result_dict[field]}")
        #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print(f"       traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
 
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()