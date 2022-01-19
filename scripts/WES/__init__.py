# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/1/13 14:35
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

import os
from itertools import islice

if __name__ == '__main__':
    # 用于简化文件，测试任务程序是否正确
    files_dir = ''
    file_names = os.listdir(files_dir)

    for file_name in file_names:
        with open(os.path.join(files_dir, file_name), 'r') as r, open(os.path.join(files_dir, 'simplify', file_name),
                                                                      'w') as w:
            lines = list(islice(r, 1000000))
            w.writelines(lines)
