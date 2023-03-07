import MetaTrader5 as mt5
import time
import json
import os
from datetime import datetime

from main_functions import *


# Inicialização ======================================
intialize_mt5()
symbol = set_symbol("ITUB4")
        
# ORDER_CHECK() ======================================
# preparamos a solicitação -> order_check()
point = mt5.symbol_info(symbol).point
ask = mt5.symbol_info_tick(symbol).ask

# estabelecer o volume aqui para mitigar erros
volume = 100.0
check_volume(volume, symbol)

request = {
    "action": mt5.TRADE_ACTION_DEAL,            # TRADE_ACTION_DEAL -> Ordem imediata
    "symbol": symbol,
    "volume": volume,                           
    "type": mt5.ORDER_TYPE_BUY,                 # ORDER_TYPE_BUY -> Ordem para compra
    "price": ask,                               # preço ask
    "sl": ask-100*point,
    "tp": ask+100*point,
    "deviation": 10,
    "magic": 234000,
    "comment": "asimov python script",
    "type_time": mt5.ORDER_TIME_GTC,            # ORDER_TIME_GTC -> A ordem permanecerá na fila até ser tirada
    "type_filling": mt5.ORDER_FILLING_RETURN,   # ORDER_FILLING RETURN -> No caso de uma execução parcial, a ordem de mercado ou limit com um volume residual não é retirada e continua
}

# verificamos e exibimos o resultado como está
result = mt5.order_check(request)._asdict()
print(result['retcode'], result['comment'])

# ORDER_SEND() =======================================
# Primeiro executamos uma ordem de compra do ativo, damos 2 segundos e o vendemos
# ORDEM DE COMPRA =====================
volume = 100.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

# estrutura de request igual à utilizada no order_check()
request = {
    "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
    "symbol": symbol,
    "volume": volume,
    "type": mt5.ORDER_TYPE_BUY,         # ordem de mercado para compra
    "price": price,                     # preço ask
    "sl": price - 100 * point,          # não é necessário
    "tp": price + 100 * point,          # não é necessário
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

print(f"1. order_send(): by {symbol} {volume} lots at {price} desvio={deviation} points")
print("2. order_send() executada:")
print(f"   posição aberta: POSITION_TICKET={position_id}")

# tempo de processamento e redefinição da posição
time.sleep(2)
print(f"   timer 2s antes de fechar a posição #{position_id}")

# ORDEM DE FECHAMENTO =================
price = mt5.symbol_info_tick(symbol).bid
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
    "symbol": symbol,
    "volume": volume,
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
print(f"3. close position #{position_id}: sell {symbol} {volume} lots at {price} desvio={deviation} points")
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"4. order_send falhou, retcode={result.retcode}")
    print("   resultado",result)
else:
    print(f"4. posição #{position_id} closed, {result}")
    order_result_log(result)


# Quantas Ordens? ====================================
date_from=datetime(2020,1,1)
date_to=datetime.now()
history_orders=mt5.history_orders_total(date_from, date_to)
if history_orders>0:
    print("Total history orders=",history_orders)
else:
    print("Orders not found in history")


# Como consultar uma ordem específica ================
# Existem 3 maneiras:
#       1. Bilhete de posição
mt5.positions_get()
#       2. Bilhete da ordem
mt5.positions_get(ticket=position_id)
# order = pending order
# position = opened order
#       3. dates and group -> datetime
date_from = datetime(2020,1,1)
date_to = datetime.now()
mt5.history_orders_get(
    date_from, date_to #, group -> optional
)







# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()



# CÓDIGO PRO ARTIGO
1.
import MetaTrader5 as mt5
from datetime import datetime

date_from = datetime(2020,1,1)
date_to = datetime.now()

# Todas as funções aqui retornaram um inteiro
mt5.orders_total()                              # Total de ordens
mt5.positions_total()                           # Total de posições
mt5.history_orders_total(date_from, date_to)    # Total de ordens no histórico de negociação
mt5.history_deals_total(date_from, date_to)     # Total de transações no histórico de negociação (deals)

2.
