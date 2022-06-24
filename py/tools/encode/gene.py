# -*- encoding: utf-8 -*-
"""
@File Name      :   gene.py    
@Create Time    :   2022/5/20 23:32
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
import re
import threading
from queue import Queue

import click
import requests

thread_lock = threading.Lock()
que = Queue()
max_connections = 10
sem = threading.BoundedSemaphore(max_connections)

base_url = "https://www.ncbi.nlm.nih.gov/gene/"


def get_human_gene_name(mouse_gene_name, html):
    human_gene_name_texts_re = re.compile(r'(<tr class="rprt">){1}.*<em>Homo sapiens</em>')
    human_gene_name_texts = human_gene_name_texts_re.search(html)
    if human_gene_name_texts:
        human_gene_name_text = human_gene_name_texts.group(0)
        human_gene_name_re = re.compile(r'<a href=.*><span class="highlight" style="background-color:">(.*)</span></a>')
        human_gene_names = human_gene_name_re.search(human_gene_name_text)
        try:
            human_gene_name = human_gene_names.group(1)
            return mouse_gene_name, human_gene_name
        except Exception as e:
            human_gene_name_re = re.compile(r'<a href=.*>(.*)</a>')
            human_gene_names = human_gene_name_re.search(human_gene_name_text)
            try:
                human_gene_name = human_gene_names.group(1)
                return mouse_gene_name, human_gene_name
            except Exception as e:
                print(f'{human_gene_name_text}:{e}')
                return mouse_gene_name, 'error'
    else:
        return mouse_gene_name, ''


def request_mouse_gene_name(mouse_gene_name):
    with sem:
        try:
            url = base_url + f'?term={mouse_gene_name}'
            r = requests.get(url)
            r.encoding = 'utf-8'
            html = r.text
            return get_human_gene_name(mouse_gene_name, html)
        except Exception as e:
            print(f'{mouse_gene_name}:{e}')
            return mouse_gene_name, 'network error'


def get_mouse_human_gene_names(mouse_gene_names):
    mouse_human_gene_names = []
    threads = []
    for mouse_gene_name in mouse_gene_names:
        thread = threading.Thread(
            target=lambda q, arg1: q.put(request_mouse_gene_name(arg1)),
            args=(que, mouse_gene_name,),
            daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    while not que.empty():
        result = que.get()
        mouse_human_gene_names.append(result)
    return mouse_human_gene_names


@click.command()
@click.argument('input_file_path', type=click.Path(exists=True))
def main(input_file_path):
    input_dir = os.path.dirname(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    output_file_name = f'mouse-human.{input_file_name}'
    output_file_path = os.path.join(input_dir, output_file_name)
    with open(input_file_path, 'r') as f, open(output_file_path, 'w') as w:
        mouse_gene_names = [line.replace('\n', '') for line in f.readlines()]
        mouse_human_gene_names = get_mouse_human_gene_names(mouse_gene_names)
        w.writelines([f'{gene_names[0]},{gene_names[1]}\n' for gene_names in mouse_human_gene_names])


if __name__ == '__main__':
    """
    使用方法：python 本脚本路径 输入文件路径
    请注意：不需要输入任何参数
    """
    main()
