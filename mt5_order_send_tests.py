import MetaTrader5 as mt5
import json
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time

from main_functions import *

# Inicialização ======================================
intialize_mt5()
symbol = set_symbol("ITUB4")

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
    order_result_log(result)
    
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()