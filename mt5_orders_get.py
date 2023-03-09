import MetaTrader5 as mt5
import pandas as pd

from main_functions import *

# Inicialização ======================================
intialize_mt5()
symbol = set_symbol("ITUB4")

# exibimos informações sobre ordens ativas do símbolo ITUB4
orders = mt5.orders_get(symbol=symbol)
if orders is None:
    print(f"Sem orders em {symbol}, error code={mt5.last_error()}")
else:
    print(f"Total orders em {symbol}: {len(orders)}")
    # exibimos todas as ordens ativas
    for order in orders:
        print(order)
 
# definimos o grupo de pesquisa
group_search = "*USD*"

# obtemos uma lista de ordens com base em símbolos cujos nomes contenham "*BRL*"
gbp_orders=mt5.orders_get(group=group_search)
if gbp_orders is None:
    print(f"No orders with group={group_search}, error code={mt5.last_error()}")
else:
    print(f"orders_get(group={group_search})={len(gbp_orders)}")
    # exibimos essas posições como uma tabela usando pandas.DataFrame
    df=pd.DataFrame(list(gbp_orders),columns=gbp_orders[0]._asdict().keys())
    df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial', 'price_stoplimit'], axis=1, inplace=True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
 
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()