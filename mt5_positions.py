import MetaTrader5 as mt5
import pandas as pd

from main_functions import *

# Inicialização ======================================
intialize_mt5()
symbol = set_symbol("ITUB4")

# obtemos as posições abertas com base no ativo escolhido (ITUB4)
positions=mt5.positions_get(symbol=symbol)
if positions == None:
    print(f"Sem positions em {symbol}, error code={mt5.last_error()}")
else:
    # imprimimos todas as posições abertas
    print(f"Total de positions com ITUB4 = {len(positions)}")
    for position in positions:
        print(position)
 
# definimos o grupo de pesquisa
group_search = "*USD*"

# obtemos uma lista de posições com base em símbolos cujos nomes contenham "*USD*"
'''
Lembrando que a pesquisa por grupo permite várias condições separadas por vírgulas. 
A condição pode ser especificada como uma máscara usando '*'. 
Para exclusões, pode-se usar o símbolo de negação lógica '!'. 
Neste caso, todas as condições são aplicadas sequencialmente, ou seja, primeiro deve-se especificar as condições para inclusão no grupo e, em seguida, 
a condição de exclusão. Por exemplo, group="*, !ITUB" significa que primeiro é necessário selecionar as posições de todos os símbolos e, em seguida, 
excluir as que contêm o símbolo "ITUB" no nome.deve-se especificar as condições para inclusão no grupo e, em seguida, a condição de exclusão. 
Por exemplo, group="*, !ITUB" significa que primeiro é necessário selecionar as posições de todos os símbolos e, em seguida, excluir as que contêm o símbolo "ITUB" no nome.
'''
usd_positions=mt5.positions_get(group="group_search")
if usd_positions==None:
    print(f"Sem positions com o parâmetro group={group_search}, error code={mt5.last_error()}")
else:
    print(f"positions_get(group={group_search})={len(usd_positions)}")
    # exibimos essas posições como uma tabela usando pandas.DataFrame
    df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
 
# A pesquisa por bilhete necessita de um número específico de operação, porém o padrão seria
# mt5.positions_get(ticket=0000000)

# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()
