# -*- encoding: utf-8 -*-
"""
@File Name      :   filter.py    
@Create Time    :   2021/12/27 18:35
@Description    :   
@Version        :   v1.0
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import functools
import gzip
import os
import time
from itertools import islice

import click


# 更精确的运行时间记录
def print_accurate_execute_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'函数 {func.__name__} 耗时 {(end - start) * 1000} ms')
        return res

    return wrapper


def any_equal(filtered_str, rule_list):
    return any([filtered_str == rule for rule in rule_list])


def any_include(filtered_str, rule_list):
    return any([rule in filtered_str for rule in rule_list])


@click.command()
@click.option('--read1_file_path', '-r1', type=str, required=True, help='read1 file')
@click.option('--read2_file_path', '-r2', type=str, help='read2 file')
@click.option('--operation', '-op', type=str, default=None, help="operation method, can only input 'tile' and 'reads'")
@click.option('--tile', '-t', is_flag=True, help='operate tile, cover --operation')
@click.option('--reads', '-r', is_flag=True, help='operate reads, cover --operation')
@click.option('--filter_file_path', '-f', type=str, required=True, help='filter rules file path')
@click.option('--output-dir', '-o', type=str, default='',
              help='Output directory path, according to input files to generate files. ' +
                   'If not given, generate file in script run directory')
@click.option('--output-prefix', '-p', type=str, default='', help='Output file prefix')
@print_accurate_execute_time
def filter_fastq(read1_file_path, read2_file_path, operation, tile, reads, filter_file_path, output_dir, output_prefix):
    """
    filter fastq files（过滤fastq文件）\n
    用法\n
    :param read1_file_path:read1文件路径，必选\n
    :param read2_file_path:read2文件路径，可选\n
    :param tile:操作tile\n
    :param reads:操作reads\n
    :param operation:需要进行的操作，只能输入 'tile' 或者 'reads'（命令行中不需要带引号），
    可以和 --tile 和 --reads 选项同时使用，会被这两个选项覆盖\n
    :param filter_file_path:需要进行过滤的规则文件路径，必选\n
    :param output_dir:输出文件也是gzip压缩文件\n
    :param output_prefix:输出文件前缀\n
    :return:无返回值\n
    """
    if tile:
        operation = 'tile'
    if reads:
        operation = 'reads'
    if not operation:
        print('not choose operation method')
        return False
    elif operation != 'tile' and operation != 'reads':
        print('operation must be tile or read')
        return False
    print(f'operation is {operation}')
    if not os.path.exists(filter_file_path) or not os.path.isfile(filter_file_path):
        print('filter file not exist')
        return False
    with open(filter_file_path, 'rb') as filter_file:
        filter_rules = filter_file.read().splitlines()
        print(f'filter_rules:{filter_rules}')
    # 只有一个r1文件
    if read1_file_path and not read2_file_path:
        if not os.path.exists(read1_file_path) or not os.path.isfile(read1_file_path):
            print('r1 file not exist')
            return False
        if output_prefix:
            read1_output_file_path = output_prefix + '.r1.fastq.gz'
        else:
            read1_output_file_path = os.path.join(output_dir, os.path.basename(read1_file_path).split('.')[
                0] + '.filter_' + operation + '.fq.gz')
        with gzip.open(read1_file_path, 'rb') as read1_file, \
                gzip.open(read1_output_file_path, 'wb') as read1_output_file:
            stop = False
            while not stop:
                lines = list(islice(read1_file, 4))
                if lines:
                    if operation == 'tile' and not any_equal(lines[0].split(":")[4], filter_rules):
                        read1_output_file.writelines(lines)
                    elif operation == 'reads' and not any_include(lines[1], filter_rules):
                        read1_output_file.writelines(lines)
                else:
                    stop = True
    # 有r1，r2两个文件
    if read1_file_path and read2_file_path:
        if not os.path.exists(read1_file_path) or not os.path.isfile(read1_file_path):
            print('r1 file not exist')
            return False
        if not os.path.exists(read2_file_path) or not os.path.isfile(read2_file_path):
            print('r2 file not exist')
            return False
        if output_prefix:
            read1_output_file_path = output_prefix + '.r1.fastq.gz'
            read2_output_file_path = output_prefix + '.r2.fastq.gz'
        else:
            read1_output_file_path = os.path.join(output_dir, os.path.basename(read1_file_path).split('.')[
                0] + '.filter_' + operation + '.fq.gz')
            read2_output_file_path = os.path.join(output_dir, os.path.basename(read2_file_path).split('.')[
                0] + '.filter_' + operation + '.fq.gz')
        with gzip.open(read1_file_path, 'rb') as read1_file, gzip.open(read2_file_path, 'rb') as read2_file, \
                gzip.open(read1_output_file_path, 'wb') as read1_output_file, \
                gzip.open(read2_output_file_path, 'wb') as read2_output_file:
            stop = False
            count = 0
            while not stop:
                read1_lines = list(islice(read1_file, 4))
                read2_lines = list(islice(read2_file, 4))
                count += 1
                if count % 100000 == 0:
                    print(f'read {count} lines')
                if read1_lines and read2_lines:
                    if operation == 'tile' and (not any_equal(read1_lines[0].split(":")[4], filter_rules)
                                                and not any_equal(read2_lines[0].split(":")[4], filter_rules)):
                        read1_output_file.writelines(read1_lines)
                        read2_output_file.writelines(read2_lines)
                    elif operation == 'reads' and (not any_include(read1_lines[1], filter_rules)
                                                   and not any_include(read2_lines[1], filter_rules)):
                        read1_output_file.writelines(read1_lines)
                        read2_output_file.writelines(read2_lines)
                else:
                    stop = True


if __name__ == '__main__':
    """
    本脚本在python3.8环境下测试通过，预计Python3.6版本以上都不会出现问题
    注意：本脚本需要安装click包
    帮助：python3 filter.py --help
    """
    filter_fastq()
