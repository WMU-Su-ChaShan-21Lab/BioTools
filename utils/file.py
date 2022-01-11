# -*- encoding: utf-8 -*-
"""
@File Name      :   file.py    
@Create Time    :   2021/12/31 15:02
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
from typing import List, Iterable

def make_dir(make_dir_path: str) -> bool:
    """
    没有就创建这个文件夹，有就直接返回True
    """
    # 为了防止是WindowsPath而报错，先转换一下
    path = str(make_dir_path).strip()
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(str(e))
            return False
    return True

def remove_file(file_path):
    """
    有文件就删除文件，没有文件就什么都不做
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


# 这种方法比list(islice(f, n))慢三分之一，猜测是因为for循环的速度慢
def read_n_lines_each_time(path: str, n: int) -> Iterable[List[str]]:
    i = 0
    lines = []
    with open(path, mode='r', encoding='utf8') as f:
        for line in f:
            i += 1
            lines.append(line.strip())
            if i >= n:
                yield lines
                # reset buffer
                i = 0
                lines.clear()
    # remaining lines
    if i > 0:
        yield lines
