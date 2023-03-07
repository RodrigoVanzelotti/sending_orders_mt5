import MetaTrader5 as mt5
import json
import os

# Funções para diminuir repetições de código ====================

def intialize_mt5(test=True):
    # Estabelecendo o path e se estamos em um ambiente de testes
    teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials_test.json')
    not_teste_path = os.path.normpath(r'C:\Users\rodri\OneDrive\Área de Trabalho\credentials.json')

    is_test = test              # NOTE é um ambiente de teste?
    FILE_PATH = teste_path if is_test else not_teste_path

    # Inicialização
    with open(FILE_PATH) as f:
        credentials = json.load(f)
    # Caso o mt5 nao inicialize, quit()
    if not mt5.initialize(login=credentials['loginJson'], password=credentials['passwordJson'], server=credentials['serverJson'], path="C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe"):
        error_quit(f"initialize() falhou, error code = {mt5.last_error()}")
    
    account_currency = mt5.account_info().currency
    print("Moeda corrente:", account_currency)
        
def set_symbol(symb):
    # preparamos o ativo
    symbol = symb
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        error_quit(f"{symbol} não foi encontrado, não é possível chamar order_check()")
    
    # se o símbolo não estiver disponível no MarketWatch, adicionamos
    '''
    MarketWatch é um site que fornece informações financeiras, notícias de negócios, análises e dados do mercado de ações. 
    Junto com The Wall Street Journal e Barron's, é uma subsidiária da Dow Jones & Company, propriedade da News Corp
    '''
    if not symbol_info.visible:
        print(symbol, "não está visível, tentando conectar...")
        if not mt5.symbol_select(symbol,True):
            error_quit(f"symbol_select({symbol}) falhou, exiting...")
    
    return symbol

def error_quit(message):
    print(message)
    mt5.shutdown(); quit()

def order_result_log(result_object):
    # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result_object._asdict()
    for field in result_dict.keys():
        print(f"\t{field}={result_dict[field]}")
        #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print(f"\t\ttraderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
 
def check_volume(vol, symbol):
    maxvol = mt5.symbol_info(symbol).volumehigh
    minvol = mt5.symbol_info(symbol).volumelow
    if vol < minvol or vol > maxvol:
        error_quit(f'Volume Selecionado: {vol}\nVolume Mínimo: {minvol}\nVolume Máximo: {maxvol}')