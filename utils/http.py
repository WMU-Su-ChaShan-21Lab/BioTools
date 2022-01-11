# -*- encoding: utf-8 -*-
"""
@File Name      :   https.py    
@Create Time    :   2022/1/11 11:16
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

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = Session()
# 设置失败后进行重访问，最大5次
session.mount('https://', HTTPAdapter(max_retries=Retry(total=5,
                                                        allowed_methods=frozenset(['GET', 'POST']))))
