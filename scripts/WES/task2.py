# -*- encoding: utf-8 -*-
"""
@File Name      :   task2.py    
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

import functools
import multiprocessing
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


@print_accurate_execute_time
def task2(input_dir, output_dir, file_names, file_block):
    start = time.perf_counter()
    wes_all_sum = dict()
    for file_name in file_names:
        print(f'开始读取 {file_name}')
        per = 100000000
        with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as f:
            stop = False
            count = 0
            while not stop:
                count += 1
                read_file_time = time.perf_counter()
                rows_text = f'{file_name}文件的第{(count - 1) * per}-{count * per}行'
                print(f'正在读取 {rows_text}')
                lines = list(islice(f, per))
                print(f'{rows_text} 读取花费时间:{(time.perf_counter() - read_file_time) * 1000}ms')
                cal_time = time.perf_counter()
                if lines:
                    for line in lines:
                        row = line.strip().split('\t')
                        if len(row) <= 2:
                            continue
                        ch = row[0]
                        site = row[1]
                        p_value = int(row[2])
                        if wes_all_sum.get(ch, {}):
                            if wes_all_sum[ch].get(site, {}):
                                wes_all_sum[ch][site] += p_value
                            else:
                                wes_all_sum[ch][site] = p_value
                        else:
                            wes_all_sum[ch] = {}
                            wes_all_sum[ch][site] = p_value
                    # union_dict_use_for(wes_all_sum, {
                    #     ":".join(line.replace('\n', '').split('\t')[0:2]): line.replace('\n', '').split('\t')[2] for
                    #     line in lines})
                    print(f'{rows_text} 计算耗费时间:{(time.perf_counter() - cal_time) * 1000}ms')
                    print(f'{rows_text} 循环耗费时间:{(time.perf_counter() - read_file_time) * 1000}ms')
                    print(f'{file_block} 这部分文件已经耗费时间:{(time.perf_counter() - start) * 1000}ms')
                else:
                    stop = True
                    print(f'{file_name} 读取并比对完毕，共耗费时间{(time.perf_counter() - start) * 1000}ms')
    print(f'{file_block} 这部分文件全部读取处理完毕，共耗费时间{(time.perf_counter() - start) * 1000}ms')
    print(f'{file_block} 这部分文件结果开始写入文件')
    file_write_time = time.perf_counter()
    file_write_name = os.path.join(output_dir, file_block + '_' + 'sum.txt')
    with open(file_write_name, 'w') as w:
        # w.writelines(['\t'.join(key.split(':')) + '\t' + str(value) + '\n' for key, value in wes_all_sum.items()])
        w.writelines(
            [chr_key + '\t' + site_key + '\t' + str(site_value) + '\n' for chr_key, chr_value in wes_all_sum.items() for
             site_key, site_value in chr_value.items()])
    print(f'{file_block} 这部分文件结果写入完成，耗费时间{(time.perf_counter() - file_write_time) * 1000}ms')
    print(f'{file_block} 这部分文件任务完成，共耗费时间{(time.perf_counter() - start) * 1000}ms')


@click.command()
@click.option('--input_dir', '-i', type=str, required=True, help='输入文件夹')
@click.option('--process_num', '-p', type=int, required=True, default=3, help='进程数')
@click.option('--output_dir', '-o', type=str, default=None, help='输出文件夹')
@click.option('--limit', '-l', type=int, default=None, help='限制读取的文件数')
def multi_task2(input_dir, process_num=3, output_dir=None, limit=None):
    if os.path.exists(input_dir) and os.path.isdir(input_dir):
        file_names = []
        names = os.listdir(input_dir)
        for name in names:
            if os.path.isfile(os.path.join(input_dir, name)):
                file_names.append(name)
    else:
        print('dir not exists or is not a dir')
        return False
    file_names = file_names[:limit]
    if not output_dir:
        output_dir = os.path.join(input_dir, 'outputs')
    make_dir(output_dir)
    files_count = len(file_names)
    if files_count < process_num:
        process_num = files_count // 200
        print(f'进程数量超过文件数量，已经自动更正')
    quotient = files_count // process_num
    remainder = files_count % process_num
    remainder_count = remainder

    processes = []
    for i in range(process_num):
        if remainder_count > 0:
            file_start = i * (quotient + 1)
            file_end = (i + 1) * (quotient + 1)
            remainder_count -= 1
            process = multiprocessing.Process(
                target=task2,
                args=(input_dir, output_dir, file_names[file_start:file_end], str(file_start) + '-' + str(file_end)),
                daemon=True)
        else:
            file_start = i * quotient + remainder
            file_end = (i + 1) * quotient + remainder
            process = multiprocessing.Process(
                target=task2,
                args=(input_dir, output_dir, file_names[file_start:file_end], str(file_start) + '-' + str(file_end)),
                daemon=True)
        # print(file_start, '-', file_end)
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    """
    说明：
    1.脚本使用multiprocessing模块，每个进程负责读取一部分文件，并计算每个文件的结果，最后将结果写入文件
    2.生成的部分文件可以再调用一次这个脚本，直到最后的进程数限制为1
    
    参数：
    input_dir:输入文件存放的文件夹
    process_num:总进程数，即分成多少块进行处理
    output_dir:输出文件存放的文件夹，默认会生成输入文件夹下面的outputs空文件夹
    limit:只处理文件夹中前n个文件
    
    使用方法：
    方法1.不使用click模块
    把click相关的内容全部注释（即@click开头的装饰器）
    在主程序中使用函数：multi_task2(input_dir='输入文件夹路径', process_num=10)
    
    方法2.安装并使用click模块，使用命令行的方式调用
    将click相关内容全部取消注释
    主程序只需要写上multi_task2()
    在命令行中调用：python3 ./task2 --input_dir=输入文件夹路径 --process_num=10 --output_dir=输出文件夹路径（非必须）
    
    """
    print('CPU核心数量:' + str(multiprocessing.cpu_count()))
    # multi_task2(input_dir='D:\Server\simplify', process_num=3)
    multi_task2()
    print('所有任务处理完成')
