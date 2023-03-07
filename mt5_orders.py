import MetaTrader5 as mt5
import time
import json
import os
from datetime import datetime

# Funções para diminuir repetições de código
def error_quit(message):
    print(message)
    mt5.shutdown(); quit()

def order_result_log(result_object):
    # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result_object._asdict()
    for field in result_dict.keys():
        print(f"   {field}={result_dict[field]}")
        #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print(f"\ttraderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
 
def check_volume(vol, symbol):
    maxvol = mt5.symbol_info(symbol).volumehigh
    minvol = mt5.symbol_info(symbol).volumelow
    if volume < minvol or volume > maxvol:
        error_quit(f'Volume Selecionado: {volume}\nVolume Mínimo: {minvol}\nVolume Máximo: {maxvol}')


# Estabelecendo o path e se estamos em um ambiente de testes
teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials_test.json')
not_teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials.json')

is_test = True              # NOTE é um ambiente de teste?
FILE_PATH = teste_path if is_test else not_teste_path

# Inicialização ======================================
with open(FILE_PATH) as f:
    credentials = json.load(f)
# Caso o mt5 nao inicialize, quit()
if not mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'], path="C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe"):
    error_quit(f"initialize() falhou, error code = {mt5.last_error()}")
    
# preparamos o ativo
symbol="ITUB4"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    error_quit(f"{symbol} não foi encontrado, não é possível chamar order_check()")
   
 
# se o símbolo não estiver disponível no MarketWatch, adicionamos
if not symbol_info.visible:
    print(symbol, "não está visível, tentando conectar...")
    if not mt5.symbol_select(symbol,True):
        error_quit(f"symbol_select({symbol}) falhou, exiting...")
        
# ORDER_CHECK() ======================================
# preparamos a solicitação -> order_check()
point = mt5.symbol_info(symbol).point       # não sei o que o point significa NOTE perguntar pro T.
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
    "type_filling": mt5.ORDER_FILLING_RETURN,   # ORDER_FILLING RETURN -> 
}

# verificamos e exibimos o resultado como está
result = mt5.order_check(request)._asdict()
print(result['retcode'], result['comment'])



# ORDER_SEND() =======================================
# Primeiro executamos uma ordem de compra do ativo, damos 2 segundos e o vendemos
# ORDEM DE COMPRA =====================
lot = 100.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,    # ação imediata de transação
    "symbol": symbol,
    "volume": lot,
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

print(f"1. order_send(): by {symbol} {lot} lots at {price} desvio={deviation} points")
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
print(f"3. close position #{position_id}: sell {symbol} {lot} lots at {price} desvio={deviation} points")
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"4. order_send falhou, retcode={result.retcode}")
    print("   resultado",result)
else:
    print(f"4. posição #{position_id} closed, {result}")
    order_result_log(result)


# Quantas Ordens? ====================================
from_date=datetime(2020,1,1)
to_date=datetime.now()
history_orders=mt5.history_orders_total(from_date, datetime.now())
if history_orders>0:
    print("Total history orders=",history_orders)
else:
    print("Orders not found in history")


# Como consultar uma ordem específica ================
# Existem 3 maneiras:
#       1. Bilhete de posição
mt5.positions_get(position='aaaa')
#       2. Bilhete da ordem
mt5.positions_get(ticket=position_id)
# order = pending order
# position = opened order
#       3. dates and group -> datetime
from_date=datetime(2020,1,1)
to_date=datetime.now()
mt5.history_orders_get(
    from_date, to_date #, group -> optional
    
)







# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()
