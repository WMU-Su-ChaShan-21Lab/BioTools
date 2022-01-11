# -*- encoding: utf-8 -*-
"""
@File Name      :   url.py    
@Create Time    :   2022/1/11 10:34
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode, unquote


def url_query_dict(url: str):
    return parse_qs(urlparse(url).query)


def un_url_query_dict(params_dict: dict, if_quote=False):
    """
    url_query_dict函数的逆
    """
    return urlencode(params_dict, doseq=True) if if_quote else unquote(urlencode(params_dict, doseq=True))


def url_query_list(url: str):
    return parse_qsl(urlparse(url).query)


def un_url_query_list(params_list: list, if_quote=False):
    """
    url_query_list函数的逆
    """
    return urlencode(params_list) if if_quote else unquote(urlencode(params_list))
