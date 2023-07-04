import time
from data_access.web import WebAccess

class QueryCnpjWeb():
    """ Representa... """
    
    def __init__(self, cnpj: str):
        """ Construtor da classe """
        self._cnpj = cnpj
        
    
    def clear_data_extract(self, data_query):
        """ """
        
        for i in range(len(data_query)):
            # Altera o valor da string na posição i
            info_temp = data_query[i].replace("\t","").replace("*","").strip()
            if info_temp == "":
                info_temp = "N/A"
            data_query[i] = info_temp
        
        list_clear = [
            f'{self._cnpj}', # VALOR ORIGINAL
            f'{data_query[27]}', # STATUS DA CONSULTA
            f'{data_query[2]}-{data_query[3]}', # NÚMERO DE INSCRIÇÃO/INFO
            f'{data_query[5]}', # DATA DE ABERTURA
            f'{data_query[6]}', # NOME EMPRESARIAL
            f'{data_query[7]}', # TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)
            f'{data_query[8]}', # PORTE
            f'{data_query[9]}', # CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL
            f'{data_query[10]}', # CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS
            f'{data_query[11]}', # CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA
            f'{data_query[12]}', # LOGRADOURO
            f'{data_query[13]}', # NÚMERO
            f'{data_query[14]}', # COMPLEMENTO
            f'{data_query[15]}', # CEP
            f'{data_query[16]}', # BAIRRO/DISTRITO
            f'{data_query[17]}', # MUNICÍPIO
            f'{data_query[18]}', # UF
            f'{data_query[19]}', # ENDEREÇO ELETRÔNICO
            f'{data_query[20]}', # TELEFONE
            f'{data_query[21]}', # ENTE FEDERATIVO RESPONSÁVEL (EFR)
            f'{data_query[22]}', # SITUAÇÃO CADASTRAL
            f'{data_query[23]}', # DATA DA SITUAÇÃO CADASTRAL
            f'{data_query[24]}', # MOTIVO DE SITUAÇÃO CADASTRAL
            f'{data_query[25]}', # SITUAÇÃO ESPECIAL
            f'{data_query[26]}' # DATA DA SITUAÇÃO ESPECIAL
        ]
        
        return list_clear
        
    def run(self):
        """ """
        # Abrir web
        dao_web = WebAccess()
        dao_web.open()
        
        # Informar o cnpj
        dao_web.write_js(self._cnpj, '#cnpj')
        
        # Quebrar o recaptha manualmente
        input("Aperte Enter apos a solucao do recaptha e abertura da situacao cadastral")
        
        # Extrair informações
        data_query = dao_web.list_info_extract_table("td[style='border:solid windowtext .5pt; padding:5.65pt 5.65pt 5.65pt 5.65pt']")
        
        # Fechar browser
        dao_web.close()
        
        # Retornar dados tratados
        return self.clear_data_extract(data_query)