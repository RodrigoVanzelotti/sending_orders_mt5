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

# Seguir daqui amanha
'''
1. Precisa definir o symbol?
2. Seguir transcrevendo código relativo a positions
3. Documentação de oq falta cobrir está no notion
https://www.notion.so/Posi-es-e-Hist-rico-de-Orders-no-MetaTrader5-45e89d87f4604f90b91c3cd0a17f1336
4. Fazer a classe e conversar com o Adri na quinta ao invés de quarta
5. Avisar o Lucas que um dos artigos ta pronto
'''

