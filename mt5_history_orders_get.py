import MetaTrader5 as mt5
import pandas as pd
import datetime

from main_functions import *

# Inicialização ======================================
intialize_mt5()
symbol = set_symbol("ITUB4")

# obtemos o número de ordens no histórico dado um filtro de group
# from_date e to_date ja foram definidos no inicio do artigo
from_date=datetime(2020,1,1)
to_date=datetime.now()

# definimos o grupo de pesquisa
group_search = "*USD*"

history_orders=mt5.history_orders_get(from_date, to_date, group=group_search)
if history_orders==None:
    print(f"Sem history orders com o group={group_search}, error code={mt5.last_error()}")
elif len(history_orders)>0:
    print(f"history_orders_get({from_date}, {to_date}, group={group_search})={len(history_orders)}")


# é possivel definir por position ticket e organizar em um df, mas como isso ja foi feito no subtitulo anterior
# não inclui no artigo
