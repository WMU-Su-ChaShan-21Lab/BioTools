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

from typing import List, Iterable


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
