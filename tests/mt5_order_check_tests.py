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
 
# preparamos a solicitação ============================
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
order_result_log(result) 

# concluímos a conexão ao terminal MetaTrader 5
# mt5.shutdown()