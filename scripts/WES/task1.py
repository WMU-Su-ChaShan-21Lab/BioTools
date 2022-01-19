import functools
import os
import re
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


@click.command()
@click.option('--input_dir', '-i', type=str, required=True, help='输入文件夹')
@click.option('--output_dir', '-o', type=str, default=None, help='输出文件夹')
@click.option('--limit', '-l', type=int, default=None, help='限制读取的文件数')
@print_accurate_execute_time
def task1(input_dir, output_dir, limit):
    start = time.perf_counter()
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
    wes_all = dict()
    wes_count_change = []
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
                        site=row[1]
                        p_value = int(row[2])
                        if p_value >= 10:
                            # 使用集合方法
                            if wes_all.get(ch, None):
                                wes_all[ch] += [site]
                            else:
                                wes_all[ch] = [site]
                    for key, value in wes_all.items():
                        wes_all[key] = list(set(value))
                    wes_count_change += [str(sum([len(value) for key, value in wes_all.items()])) + '\n']
                    print(f'{rows_text} 计算耗费时间:{(time.perf_counter() - cal_time) * 1000}ms')
                    print(f'{rows_text} 循环耗费总时间:{(time.perf_counter() - read_file_time) * 1000}ms')
                    print(f'已经耗费时间: {(time.perf_counter() - start) * 1000}ms')
                else:
                    stop = True
                    print(f'{file_name} 读取并比对完毕，共耗费时间{(time.perf_counter() - start) * 1000}ms')
    print(f'文件全部读取处理完毕，共耗费时间{(time.perf_counter() - start) * 1000}ms')
    print('开始写入文件')
    file_write_time = time.perf_counter()
    file_write_name = os.path.join(output_dir, 'count_change.txt')
    with open(file_write_name, 'w') as w:
        w.write('change:\n')
        w.writelines(wes_count_change)
        w.write('unique:\n')
        w.writelines([key + ':' + '\n' + '\n'.join(value) + '\n' for key, value in wes_all.items()])
    print(f'文件写入完成，耗费时间{(time.perf_counter() - file_write_time) * 1000}ms')
    print(f'任务完成，共耗费时间{(time.perf_counter() - start) * 1000}ms')


if __name__ == '__main__':
    """
    说明：任务1
    
    参数：
    input_dir:输入文件存放的文件夹
    output_dir:输出文件存放的文件夹，默认会生成输入文件夹下面的outputs空文件夹
    limit:只处理文件夹中前n个文件
    
    使用：python3 ./task1.py --input_dir=输入文件夹 --output_dir=输出文件夹 --limit=10
    """
    task1()
