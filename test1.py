import MetaTrader5 as mt5
import json
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time

teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials_test.json')
not_teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials.json')

is_test = False
FILE_PATH = teste_path if is_test else not_teste_path
# Inicialização ======================================
with open(FILE_PATH) as f:
    credentials = json.load(f)
# Caso o mt5 nao inicialize, quit()
if not mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'], path="C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe"):
    print("initialize() failed, error code = ", mt5.last_error())
    mt5.shutdown(); quit()

symbol = 'PETR4'
symbol_info = mt5.symbol_info(symbol)

mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'])
# Recapitulação ======================================
'''
PRIMEIRO DE TUDO:
Existem duas funções muito semelhantes dentro da biblioteca do mt5, sendo elas:
- copy_rates_ -> from or range          *recebe barras do mt5
- copy_ticks_ -> from or from_pos       *recebe ticks do mt5

TICKS X BARRAS
Os ticks se formam apenas com base em um número de transações, os gráficos de tempo formam
uma nova barra/vela com base em um determinado período de tempo [timeframes].
Dos Ticks se formam as barras.

copy_rates_from_pos -> recebe as velas do mt5 a partir da data específicada
copy_rates_from_pos(
   symbol,       # nome do ativo
   timeframe,    # período gráfico
   date_from,    # data de abertura da barra inicial
   count         # número de barras
   )

copy_ticks_from -> recebe os ticks do mt5 a partir da data específicada
copy_ticks_from(
   symbol,       # nome do ativo
   date_from,    # data a partir da qual são solicitados os ticks
   count,        # número de ticks solicitados
   flags         # combinação de sinalizadores que definem o tipo de ticks solicitados
   )
'''

petr_df = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, time.time(), 100)
petr_df = pd.DataFrame(petr_df)
# Converte o tipo de formato da data ...
petr_df['time'] = pd.to_datetime(petr_df['time'], unit='s')


# Funções relacionadas ao book ======================
''' Market Book
market_book_add -> Recebe eventos sobre mudanças no livro de ofertas
market_book_add(
   symbol      # nome do ativo
)

market_book_get -> Retorna uma tupla desde o log de BookInfo contendo o tipo de pedido, preço e volume em lotes.
market_book_get(
   symbol      # nome do ativo
)

market_book_release -> Cancela a subscrição para receber eventos sobre alterações no livro de ofertas.
Basicamente o anti market_book_add
market_book_release(
   symbol      # nome do instrumento financeiro
)
'''


# Funções relacionadas a ordens ====================== 
'''
orders_total() -> Retorna o valor total de ordens ativas

orders_get() -> Essa função tem 3 situações possíveis porém retorna quais são as ordens ativas.
1. Ordens por ativo
orders_get(
    symbol      # nome do ativo
)
2. Ordens por grupo filtrado de ativos
orders_get(
    group       # grupo de ativos
)
3. Por bilhete de ordem
orders_get(
    ticket      # bilhete
)
Em suma, retorna informações na forma de tuplas nomeadas. Em caso de erro retorna None
Exemplo abaixo:
'''
# exibimos informações sobre ordens ativas do ativo GBPUSD
orders=mt5.orders_get(symbol="GBPUSD")  # relação libra esterlina/dólar
if orders is None:
    print('Sem orders de GBPUSD, código de erro=', mt5.last_error())
else:
    print('Total de orders:',len(orders))
    # exibimos todas as ordens ativas
    for order in orders:
        print(order)

# obtemos uma lista de ordens com base em ativos cujos nomes contenham "*GBP*"
gbp_orders=mt5.orders_get(group="*GBP*")
if gbp_orders is None:
    print('Sem orders do group="*GBP*", código de erro=', mt5.last_error())
else:
    print('orders_get(group="*GBP*")=', len(gbp_orders))
    # exibimos essas posições como uma tabela usando pandas.DataFrame
    df=pd.DataFrame(list(gbp_orders),columns=gbp_orders[0]._asdict().keys())
    df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial', 'price_stoplimit'], axis=1, inplace=True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    print(df)

# OBSERVAÇÃO:  
'''
O parâmetro group permite filtrar ordens por ativos, é permitido usar '*' no início e no final da linha.
O parâmetro group pode conter várias condições, separadas por vírgulas. 
A condição pode ser especificada como uma máscara usando '*'. Para exclusões, pode-se usar o ativo de negação lógica '!'. 
Neste caso, todas as condições são aplicadas sequencialmente, ou seja, primeiro deve-se especificar as condições para inclusão no grupo e, em seguida, a condição de exclusão. 
Por exemplo, group="*, !EUR" significa que primeiro é necessário selecionar as ordens de todos os ativos e, em seguida, excluir as que contêm o ativo "EUR" no nome.
'''

'''
As duas funções abaixo possuem ORDER_TYPE(s) de fato eu não sei o que cada uma significa afundo, mas anotei o identificador e a descrição até pro Tadewald explicar:

order_calc_margin -> Retorna o tamanho da margem na moeda (real) da conta para a operação de negociação específicada
A função permite estimar a margem necessária para o tipo de ordem especificado na conta corrente e no ambiente de mercado atual,
excluindo os pedidos pendentes atuais e as posições abertas.
order_calc_margin(
   action,      # tipo de ordem (ORDER_TYPE_BUY ou ORDER_TYPE_SELL)
   symbol,      # nome do ativo
   volume,      # volume
   price        # preço de abertura
   )

order_calc_profit -> Retorna o valor do lucro na moeda da conta para a operação de negociação especificada.
order_calc_profit(
   action,          # tipo de ordem (ORDER_TYPE_BUY ou ORDER_TYPE_SELL)
   symbol,          # nome do ativo
   volume,          # volume
   price_open,      # preço de abertura
   price_close      # preço de fechamento
   )

ORDER_TYPES:

ORDER_TYPE_BUY                  Ordem de mercado para compra
ORDER_TYPE_SELL                 Ordem de mercado para venda
ORDER_TYPE_BUY_LIMIT            Ordem pendente Buy Limit
ORDER_TYPE_SELL_LIMIT           Ordem pendente Sell Limit
ORDER_TYPE_BUY_STOP             Ordem pendente Buy Stop
ORDER_TYPE_SELL_STOP            Ordem pendente Sell Stop
ORDER_TYPE_BUY_STOP_LIMIT       Ao atingir o preço da ordem, uma ordem Buy Limit é colocada segundo o preço Stop Limit
ORDER_TYPE_SELL_STOP_LIMIT      Ao atingir o preço da ordem, é colocada uma ordem pendente Sell Limit de acordo com o preço StopLimit
ORDER_TYPE_CLOSE_BY             Ordem de fechamento da posição oposta

Exemplo abaixo:
'''

# EXEMPLO DE order_calc_profit ====================
# obtemos a moeda da conta
account_currency=mt5.account_info().currency
print("Moeda utilizada:",account_currency)
 
# fazemos uma lista de símbolos
symbols = ("EURUSD","GBPUSD","USDJPY")
# avaliamos valores de lucro para compras e vendas
lot=1.0             # lot = volume
distance=300        # distance = preço de abertura

# iterando por cada ativo
for symbol in symbols:
    symbol_info=mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol,"não encontrado, pulado")
        continue
    if not symbol_info.visible:
        print(symbol, "não está visível para o mt5, tentando deixá-lo on")
        if not mt5.symbol_select(symbol,True):
            print(f"symbol_select({symbol}) falhou, pulado")
            continue

    # Separando as informações do ativo específico (lembrando que estamos iterando)
    point=mt5.symbol_info(symbol).point
    symbol_tick=mt5.symbol_info_tick(symbol)
    ask=symbol_tick.ask
    bid=symbol_tick.bid

    # Lucro de compra
    buy_profit=mt5.order_calc_profit(mt5.ORDER_TYPE_BUY,symbol,lot,ask,ask+distance*point)
    if buy_profit != None:
        print(f"\tBuy {symbol} {lot} lot: profit on {distance} points => {buy_profit} {account_currency}")
    else:
        print("order_calc_profit(ORDER_TYPE_BUY) falhou, error code =", mt5.last_error())

    # Lucro de venda
    sell_profit=mt5.order_calc_profit(mt5.ORDER_TYPE_SELL,symbol,lot,bid,bid-distance*point)
    if sell_profit != None:
        print(f"\tSell {symbol} {lot} lots: profit on {distance} points => {sell_profit} {account_currency}")
    else:
        print("order_calc_profit(ORDER_TYPE_SELL) falhou, error code =", mt5.last_error())
# ======================================

'''
Assim como no processo de margem, utilizariamos variáveis como a moeda corrente, ativos a serem analisados, volume e preço de abertura. 
Digamos que nesse exemplo o lot=0.1:
'''
# EXEMPLO DE order_calc_margin ====================
action=mt5.ORDER_TYPE_BUY
lot=0.1
for symbol in symbols:
    symbol_info=mt5.symbol_info(symbol)
    # inserir aqui verificação de ativo <- 

    # Calculo de margem
    ask=mt5.symbol_info_tick(symbol).ask
    margin=mt5.order_calc_margin(action,symbol,lot,ask)
    if margin != None:
        print(f"{symbol} buy {lot} lot margin: {margin} {account_currency}")
    else:
        print("order_calc_margin falhou: , error code =", mt5.last_error())
# ======================================

# Repetir o porocess

'''
As duas funções abaixo necessitam de uma 'estrutura de solicitação' que é a seguinte:

order_check -> Verifica que há fundos suficientes para realizar a operação de negociação requerida
order_check(
   request      # estrutura da solicitação
   )
order_send -> Envia do terminal para o servidor de negociação uma solicitação para concluir uma operação de negociação
order_send(
   request      # estrutura da solicitação
   )
'''



# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()

