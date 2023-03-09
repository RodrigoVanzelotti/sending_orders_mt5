import MetaTrader5 as mt5
import pandas as pd
import datetime

from main_functions import *

# Inicialização ======================================
intialize_mt5()

# obtemos o número de ordens no histórico dado um filtro de group
# from_date e to_date ja foram definidos no inicio do artigo
from_date = datetime(2020,1,1)
to_date = datetime.now()

# definimos o grupo de pesquisa
group_search = "*,!*EUR*,!*GBP*"

# obtemos transações cujos símbolos não contêm "EUR" nem "GBP"
deals = mt5.history_deals_get(from_date, to_date, group=group_search)
if deals == None:
    print(f"Sem deals, error code={mt5.last_error()}")
else:
    print(f"history_deals_get(from_date, to_date, group={group_search}) = {len(deals)}")
    # exibimos todas as transações recebidos como estão
    for deal in deals:
        print("\t", deal)

    # exibimos essas transações como uma tabela usando DataFrame
    df=pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df)
 
# obtemos todas as transações que pertencem à posição 530218319
position_id=530218319
position_deals = mt5.history_deals_get(position=position_id)

# checando se existem position_deals
if position_deals == None:
    print(f"Sem deals com a position #{position_id}")
    print(f"error code = {mt5.last_error()}")
elif len(position_deals) > 0:
    print(f"Deals com a position id #{position_id}: {len(position_deals)}")

    # exibimos essas transações como uma tabela usando DataFrame
    df=pd.DataFrame(list(position_deals),columns=position_deals[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # print(df)
 
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()