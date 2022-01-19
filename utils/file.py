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
from itertools import islice
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


def read_dir_files_name(file_dir):
    """
    只处理一层文件夹
    """
    file_names = []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        names = os.listdir(file_dir)
        for name in names:
            if os.path.isfile(os.path.join(file_dir, name)):
                file_names.append(name)
    return file_names


def remove_file(file_path):
    """
    有文件就删除文件，没有文件就什么都不做
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def read_n_lines_each_time(file_path: str, per: int=1000)->Iterable[List[str]]:
    with open(file_path, 'r') as f:
        stop = False
        while not stop:
            lines = list(islice(f, per))
            if lines:
                yield lines
            else:
                stop = True

# 这种方法比list(islice(f, n))慢三分之一，猜测是因为for循环的速度慢
def read_n_lines_each_time2(file_path: str, n: int) -> Iterable[List[str]]:
    i = 0
    lines = []
    with open(file_path, 'r', encoding='utf8') as f:
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


def count_file_lines(file_path,per=1000):
    """
    计算文件行数
    """
    with open(file_path,'r')as f:
        stop = False
        count = 0
        while not stop:
            lines=list(islice(f,per))
            if lines:
                count += len(list(lines))
                print(f'读取了{count}行')
            else:
                stop=True
        return count
