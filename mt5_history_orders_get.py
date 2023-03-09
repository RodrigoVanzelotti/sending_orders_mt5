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
group_search = "*USD*"

history_orders=mt5.history_orders_get(from_date, to_date, group=group_search)
if history_orders==None:
    print(f"Sem history orders com o group={group_search}, error code={mt5.last_error()}")
elif len(history_orders)>0:
    print(f"history_orders_get({from_date}, {to_date}, group={group_search})={len(history_orders)}")


# é possivel definir por position ticket e organizar em um df, mas como isso ja foi feito no subtitulo anterior
# não inclui no artigo

# exibimos todas as ordens históricas segundo o bilhete da posição
position_id = 530218319         # é preciso coletar o numero dessa position
position_history = mt5.history_orders_get(position=position_id)
if position_history == None:
    print(f"Sem orders com a position #{position_id}\nerror code = {mt5.last_error()}")
else:
    print(f"Total history orders on position #{position_id}: {len(position_history)}")

   # exibimos todas as ordens históricas que possuem o bilhete da posição especificado
    for position_order in position_history:        
        print(position_order)

    # exibimos essas posições como uma tabela usando DataFrame
    df=pd.DataFrame(list(position_history),columns=position_history[0]._asdict().keys())
    df.drop(['time_expiration','type_time','state','position_by_id','reason','volume_current','price_stoplimit','sl','tp'], axis=1, inplace=True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
    print(df)
 
# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()