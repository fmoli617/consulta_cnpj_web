''' 
'''
__author__ = 'fernando.silva'
__version__ = '1.0'

import os, sys
import datetime as dt
import pandas as pd
from app.configurations import AppConfig
from app.loggers import AppLogger
from service.query_cnpj import QueryCnpjWeb
from service.gerar_relatorio import create_relatorio

def main():
    logger = AppLogger.instance()
    logger.info(f'\n>Inicio da execucao')
    logger.info(f'>{dt.datetime.now().strftime("%Y:%m:%d %H:%M:%S")}')
    
    #========================================================================================================================================>
    
    # Buscar lista de CNPJ
    list_cnpj = pd.read_csv(os.path.join('..\input', 'data.csv'), usecols=['CNPJs'])['CNPJs'].tolist()
    
    # PARA CADA CNPJ, PROCESSAR A CONSULTA WEB
    # Criar uma variavel com o cabecalho para armazernar os resultados da pesquisa e posteriormente gerar relatorio
    list_result = [
        [   'CNPJ UTILIZADO NA CONSULTA',
            'STATUS DA CONSULTA',
            'NÚMERO DE INSCRIÇÃO-INFO', 
            'DATA DE ABERTURA',
            'NOME EMPRESARIAL',
            'TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)',
            'PORTE',
            'CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL',
            'CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS',
            'CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA',
            'LOGRADOURO',
            'NÚMERO',
            'COMPLEMENTO',
            'CEP',
            'BAIRRO/DISTRITO',
            'MUNICÍPIO',
            'UF',
            'ENDEREÇO ELETRÔNICO',
            'TELEFONE',
            'ENTE FEDERATIVO RESPONSÁVEL (EFR)',
            'SITUAÇÃO CADASTRAL',
            'DATA DA SITUAÇÃO CADASTRAL',
            'MOTIVO DE SITUAÇÃO CADASTRAL',
            'SITUAÇÃO ESPECIAL',
            'DATA DA SITUAÇÃO ESPECIAL'
        ]
        
    ]
    
    qtd = len(list_cnpj)
    i = 0
    
    for cnpj in list_cnpj:
        i += 1
        logger.info(f'\n>Item {i} de {qtd} -> CNPJ: {cnpj}')
        
        # Extrair informações
        result = QueryCnpjWeb(cnpj).run()

        # Adicionar resultado
        list_result.append(result)
        
        # Gerar relatorio
        create_relatorio(list_result, os.path.join('..\output', 'result.xlsx'))
 

    #========================================================================================================================================>

    logger.info(f'\n>Termino')
    logger.info(f'>{dt.datetime.now().strftime("%Y:%m:%d %H:%M:%S")}')

if __name__ == '__main__':
    # FORCANDO A CONFIGURAÇÃO DE CODIFICACAO PARA UTF-8
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    # ALTERA O DIRETORIO ATUAL PARA O DIRETORIO DE EXECUÇÃO
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # INICIALIZA ARQUIVO DE CONFIGURAÇÃO
    AppConfig.setup(config_filename='./app_config.yaml')

    # INICIALIZA LOGGER
    log_filename = os.path.basename(__file__).lower().replace('.py', '.log')
    logger = AppLogger.setup(log_filename=log_filename)
    
    # EXECUTAR ATIVIDADE
    try:
        main()
        sys_exit = 0
    except Exception as e:
       logger.error(f'Falha: {e} \n')
       sys_exit = 1