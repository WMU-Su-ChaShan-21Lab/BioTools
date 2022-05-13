# -*- encoding: utf-8 -*-
"""
@File Name      :   filter.py    
@Create Time    :   2022/5/8 12:35
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
import time
from shutil import rmtree

import click
import pandas as pd


def handle_sample(dir_path):
    try:
        start = time.perf_counter()
        dir_name = os.path.basename(dir_path)
        file_paths = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path) if
                      'filter' not in file_name]
        dfs = []
        for file_path in file_paths:
            df = pd.read_csv(file_path, sep='\t', skiprows=112, compression='gzip')
            df = df[['#CHROM', 'POS', 'INFO']][df['INFO'].str.contains('DP=')]
            df['INFO'] = df['INFO'].str.split(';').str[0].str.replace('DP=', '')
            filtered_file_name = os.path.join(dir_path, os.path.basename(file_path).replace('vcf.gz', 'filter.txt.gz'))
            df.to_csv(filtered_file_name, sep='\t', index=False, compression='gzip')
            dfs.append(df)
            print(f'{dir_name}:{file_path}处理完成')
            print(f'耗时:{time.perf_counter() - start}')
        if len(dfs) >= 2:
            all_df = pd.concat(dfs)
        elif len(dfs) == 1:
            all_df = dfs[0]
            print(f'{dir_name} only one file found')
        else:
            print(dir_name + ' no file')
            return
        all_filtered_file_name = os.path.join(dir_path, dir_name + '.all.filter.txt.gz')
        all_df.to_csv(all_filtered_file_name, sep='\t', index=False, compression='gzip')
        print(dir_name, 'done')
        print(f'耗时:{time.perf_counter() - start}')
    except Exception as e:
        print(e)
        print(dir_path, 'failed')


def handle_dirs(dir_paths):
    for dir_path in dir_paths:
        if os.path.isdir(dir_path):
            handle_sample(dir_path)


def handle_tasks(dir_paths, task_num=10):
    dir_count = len(dir_paths)
    print('总共有', dir_count, '个文件夹')
    if dir_count < task_num:
        task_num = dir_count
        print(f'进程数量超过要处理的文件夹数量，已经自动更正为{task_num}')
    groups = [dir_paths[i:i + task_num] for i in range(0, dir_count, task_num)]

    processes = []
    for group in groups:
        p = multiprocessing.Process(target=handle_dirs, args=(group,), daemon=True)
        processes.append(p)
    for process in processes:
        process.start()
    for process in processes:
        process.join()


@click.command()
@click.option('--input_dir', '-i', type=str, required=True, help='Input dir')
@click.option('--task_num', '-t', type=int, default=10, help='Task group num')
@click.option('--node_num', '-n', type=int, default=10, help='Node group num')
@click.option('--group', '-g', type=int, help='Node group')
@click.option('--auto_generate', '-a', is_flag=True, help='Auto generate scripts')
def main(input_dir, task_num=10, node_num=10, group=0, auto_generate=False):
    scripts_dir_path = os.path.join(input_dir, 'filter')
    if os.path.exists(scripts_dir_path):
        rmtree(scripts_dir_path)
    os.makedirs(scripts_dir_path, exist_ok=True)
    if auto_generate:
        for i in range(node_num):
            with open(os.path.join(scripts_dir_path, f'filter-{i}.sh'), 'w') as f:
                f.write(f'python {__file__} -i {input_dir} -n {node_num} -g {i} -t {task_num}')
        return
    dir_names = os.listdir(input_dir)
    dir_paths = [os.path.join(input_dir, dir_name) for dir_name in dir_names]
    dir_paths = [dir_path for dir_path in dir_paths if os.path.isdir(dir_path)]
    dir_count = len(dir_paths)
    print('总共有', dir_count, '个文件夹')
    group_num = math.ceil(dir_count // node_num)
    up = group * group_num
    down = (group + 1) * group_num
    print(f'handle {up} to {down}')
    handle_tasks(dir_paths[up:down], task_num=task_num)


if __name__ == '__main__':
    main()
