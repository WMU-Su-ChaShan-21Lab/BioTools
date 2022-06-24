# -*- encoding: utf-8 -*-
"""
@File Name      :   compare.py    
@Create Time    :   2021/12/27 18:32
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import gzip
from itertools import islice


def compare_keys(read1_file_path, read2_file_path):
    """
    load read1 and read2 file, and check if the key of read1 and read2 is same
    :param read1_file_path:
    :param read2_file_path:
    :return: 查看两个文件是否每一行的key都一一对应

    """
    with gzip.open(read1_file_path, 'rb') as read1_file, gzip.open(read2_file_path, 'rb') as read2_file:
        stop = False
        same_list = []
        count = 0
        while not stop:
            count += 1
            read1_lines = list(islice(read1_file, 4))
            read2_lines = list(islice(read2_file, 4))
            if read2_lines and read1_lines and read1_lines[0].split()[0] == read2_lines[0].split()[0]:
                same_list.append(read1_lines[0].split()[0])
            else:
                stop = True
    return all(same_list)
