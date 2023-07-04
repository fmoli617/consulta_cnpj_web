import os
import yaml
import warnings
from functools import reduce

class ConfigBase(dict):
    """ Metaclass para a classe de configurações """

    # atributos extras que podemos acrescentar no nosso objeto de configuração
    extra_attributes = {'config_filename': None}

    def __init__(self, *args, **kwargs):
        """ Construtor (o mesmo de um dict()) """
        super().__init__()
        # recarrega dados do arquivo de configuração
        self.reload()

    def setup(self, config_filename='./app_config.yaml'):
        """
        Inicializa configurações

        :param config_filename: caminho do arquivo de configuração
        """
        # ao atribuir internamente, todos os dados serão lidos
        self.config_filename = config_filename

    def reload(self):
        """
        Recarrega dados do arquivo
        """
        # limpa dados atuais
        self.clear()

        config_filename = self.extra_attributes['config_filename']

        if config_filename is None:
            return

        try:
            # carrega arquivo de configuração
            with open(config_filename, encoding='utf8') as f:
                configurations = yaml.safe_load(f)

            self.update(configurations)
        except TypeError:
            pass
        except:
            def warning_format(message, category, filename, lineno, file=None, line=None):
                return f'{os.path.basename(filename)}:{lineno}: {category.__name__}: {message}\n'
            warnings.formatwarning = warning_format
            warnings.warn(f'Arquivo de configuração "{config_filename}" não encontrado.')

    def __getattr__(self, name):
        """ Getter como atributo """
        if name in self.extra_attributes:
            return self.extra_attributes[name]
        else:
            return self.get(name, None)

    def __setattr__(self, name, value):
        """ Setter como atributo """
        if name in self.extra_attributes:
            self.extra_attributes[name] = value
            # se atribuirmos um novo valor à chave config_filename, atualizamos com os dados do arquivo
            if name == 'config_filename':
                self.reload()
        else:
            self[name] = value

    def __delattr__(self, name):
        """ Deleter de atributo """
        if name not in self.extra_attributes:
            del self[name]

    def __dir__(self):
        """ Lista membros da classe """
        dir_list = super().__dir__()
        # estendemos com os atributos extras
        dir_list.extend(self.extra_attributes.keys())
        # estendemos com as atributos do arquivo de configuração
        dir_list.extend(self.keys())
        return sorted(dir_list)

class AppConfig(metaclass=ConfigBase):
    """ Representa o arquivo de configuração """
    pass

def get_configuration_by_path(path: str, sep: str = '/'):
    """
    Retorna configuração a partir de um caminho hierárquico.

    :param path: caminho onde a configuração desejada se encontra
    :param sep: separador do caminho. default: '/'
    :return: valor associado a essa configuração
    """
    return reduce(lambda k, v: k[v], path.split(sep), AppConfig)
