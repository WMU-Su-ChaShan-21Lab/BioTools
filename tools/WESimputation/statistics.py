# -*- encoding: utf-8 -*-
"""
@File Name      :   statistics.py    
@Create Time    :   2022/5/8 17:00
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

import math
import multiprocessing
import os
import sys
import time
from shutil import rmtree

import click
import pandas as pd

module_path = os.path.dirname(__file__)
root_path = os.path.dirname(os.path.dirname(module_path))
sys.path.append(root_path)

from tools.WESimputation import chromosome_sizes


def handle_chromosome(output_dir_path, dir_paths: list, chromosome: str, up_range: int, down_range: int):
    try:
        start_time = time.time()
        dfs = []
        for dir_path in dir_paths:
            dir_name = os.path.basename(dir_path)
            file_path = os.path.join(dir_path, dir_name + '.' + chromosome + '.filter.txt.gz')
            if not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, sep='\t', compression='gzip')
            df = df[df['POS'] >= up_range, df['POS'] < down_range]
            dfs.append(df)
        if len(dfs) >= 2:
            all_df = pd.concat(dfs)
        elif len(dfs) == 1:
            all_df = dfs[0]
            print(f'{chromosome}-{up_range}-{down_range} only one file found')
        else:
            print(f'{chromosome}-{up_range}-{down_range} no file found')
            return
        group_by = ['#CHROM', 'POS']
        all_df_sum = all_df.groupby(group_by)['INFO'].agg('sum').reset_index().rename(columns={'INFO': 'SUM'})
        all_df_count = all_df.groupby(group_by).size().reset_index().rename(columns={0: 'COUNT'})
        all_df = pd.merge(all_df_sum, all_df_count, on=group_by)
        all_df['MEAN'] = all_df['SUM'] / all_df['COUNT']
        all_df.to_csv(os.path.join(output_dir_path, f'{chromosome}-{up_range}-{down_range}.statistics.txt.gz'),
                      sep='\t', index=False, compression='gzip')
        print(f'{chromosome}-{up_range}-{down_range} done:{time.time() - start_time}')
    except Exception as e:
        print(f'{chromosome}-{up_range}-{down_range} error:{e}')


@click.command()
@click.option('--input_dir_path', '-i', type=str, required=True, help='Input dir')
@click.option('--chromosome_num', '-c', type=str, help='Chromosome')
@click.option('--size', '-s', type=int, default=10000000, help='Size')
@click.option('up_group_num', '-u', type=int, default=0, help='Up group number')
@click.option('down_group_num', '-d', type=int, default=None, help='Down group number')
@click.option('--auto_generate', '-a', is_flag=True, help='Auto generate scripts')
@click.option('--generate_group_num', '-g', type=int, default=1, help='Auto generate group by')
def main(input_dir_path, chromosome_num: str, size: int, up_group_num: int, down_group_num: int,
         auto_generate, generate_group_num: int):
    """
    up_group_num 应该遵循python的列表规则从0开始，如果从一开始代码改动比较麻烦
    """
    if not os.path.exists(input_dir_path) or not os.path.isdir(input_dir_path):
        raise Exception('Input dir not exists or not a dir')
    output_dir_path = os.path.join(input_dir_path, 'statistics')
    if os.path.exists(output_dir_path):
        rmtree(output_dir_path)
    os.makedirs(output_dir_path, exist_ok=True)
    if auto_generate:
        for chromosome, limit in chromosome_sizes.items():
            group_num = math.ceil(limit / size)
            for i in range(0, group_num, generate_group_num):
                with open(os.path.join(output_dir_path, f'statistics-{chromosome}-{i}-{i + generate_group_num}.sh'),
                          'w') as f:
                    f.write(
                        f'python3 {__file__} -i {input_dir_path} -c {chromosome.replace("chr", "")} -s {size} -u {i} -d {i + generate_group_num}')
        return
    chromosome = 'chr' + chromosome_num
    chromosome_size = chromosome_sizes.get_chromosome_size(chromosome, None)
    if not chromosome_size:
        raise Exception('Chromosome not exists')
    group_num = math.ceil(chromosome_size // size)
    if up_group_num < 0 or down_group_num < 0:
        raise Exception('Up group number or down group number must be greater than 0')
    if up_group_num > group_num:
        raise Exception('Up group number is too large')
    if not down_group_num or down_group_num > group_num:
        down_group_num = group_num
    dir_names = os.listdir(input_dir_path)
    dir_paths = [os.path.join(input_dir_path, dir_name) for dir_name in dir_names]
    dir_paths = [dir_path for dir_path in dir_paths if os.path.isdir(dir_path)]

    processes = []
    for group in range(up_group_num, down_group_num):
        up_range = group * size
        down_range = up_range + size
        p = multiprocessing.Process(target=handle_chromosome,
                                    args=(output_dir_path, dir_paths, chromosome, up_range, down_range), daemon=True)
        processes.append(p)
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
