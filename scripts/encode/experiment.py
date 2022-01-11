# -*- encoding: utf-8 -*-
"""
@File Name      :   experiment.py    
@Create Time    :   2022/1/11 10:26
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
import threading
from queue import Queue
from urllib.parse import urlencode, unquote

from scripts.encode import base_url, base_search_url, base_bio_samples_url
from utils.excel import generate_xlsx_file
from utils.file import make_dir
from utils.http import session

thread_lock = threading.Lock()
que = Queue()
base_search_query = {
    # 基础参数，不知道干嘛的
    'type': ['Experiment'],
    'control_type!': ['*'],
    'status': ['released'],
    'perturbed': ['false'],
    # 查询内容
    'assay_title': ['polyA plus RNA-seq', 'total RNA-seq', 'RNA microarray'],
    # 暂时只查人类的
    'replicates.library.biosample.donor.organism.scientific_name': ['Homo sapiens'],
    # 总共查多少个
    'limit': 'all',
    # json格式返回
    'format': 'json',
}


def get_bio_sample_infos(query_dict):
    search_url = base_search_url + '?' + unquote(urlencode(query_dict, doseq=True))
    res = session.get(search_url)
    res.raise_for_status()
    result = res.json()
    bio_sample_infos = [{'bio_sample_id': item['accession'], 'cell_type': item['biosample_ontology']['term_name']} for
                        item in result['@graph']]
    return bio_sample_infos


class MyThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        # threading.Thread.__init__(self)
        super(MyThread, self).__init__()
        self.name = name
        self.target = target
        self.args = args
        self.result = self.target(*self.args)

    def get_result(self):
        return self.result or None


def get_bio_sample_file(bio_sample_id, cell_type):
    bio_sample_url = base_bio_samples_url + bio_sample_id + '/?format=json'
    res = session.get(bio_sample_url)
    res.raise_for_status()
    result = res.json()
    files = result['files']
    files_list = [{
        'bio_sample_id': bio_sample_id,
        'cell_type': cell_type,
        'file_id': file['accession'],
        'assembly': file['assembly'],
        'file_type': file['file_type'],
        'output_type': file['output_type'],
        'href': file['href'],
    } for file in files if file['output_category'] != 'raw data']
    has_hg38 = any([file['assembly'] == 'GRCh38' for file in files_list])
    if has_hg38:
        row = [list(file.values()) for file in files_list if file['assembly'] == 'GRCh38'
               and file['file_type'] == 'tsv' and file['output_type'] == 'gene quantifications']

    else:
        row = [list(file.values()) for file in files_list if file['assembly'] == 'hg19'
               and file['file_type'] == 'bed broadPeak' and file['output_type'] == 'filtered transcribed fragments']
    # download_links.extend(row)
    return row


def get_file_download_links(bio_sample_infos):
    """
    如果有h38，优先使用，否则使用h19
    h38: file_type:tsv output_type:gene quantifications
    h19: file_type:bed broadPeak output_type:filtered transcribed fragments
    """
    # 多线程写法
    download_links = []
    threads = []
    for bio_sample in bio_sample_infos:
        thread = threading.Thread(target=lambda q, arg1, arg2: q.put(get_bio_sample_file(arg1, arg2)),
                                  args=(que, bio_sample['bio_sample_id'], bio_sample['cell_type'],),
                                  daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    while not que.empty():
        download_links.extend(que.get())
    return download_links

    # 单线程写法，速度慢
    # download_links = []
    # count = 0
    # for bio_sample_id in bio_sample_ids:
    #     count += 1
    #     if count % 100 == 0:
    #         print(count)
    #     download_links.extend(get_bio_sample_file(bio_sample_id))
    # return download_links


def download_file(download_url, download_dir='./'):
    make_dir(download_dir)
    file_path = os.path.join(download_dir, download_url.split('/')[-1])
    res = session.get(download_url)
    res.raise_for_status()
    with open(file_path, 'wb') as f:
        # 一次性下载
        f.write(res.content)


def download_files(download_links, download_dir='./'):
    threads = []
    for download_link in download_links:
        download_url = base_url + download_link
        thread = threading.Thread(target=download_file, args=(download_url, download_dir))
        threads.append(thread)
    for thread in threads:
        thread.start()
    # 由于不需要获得任何结果，直接下载即可，所以就不join了


if __name__ == '__main__':
    """
    下载文件使用的是多线程，可以最大利用带宽，但是占用内存也非常大
    """
    # 获得信息和链接
    table_rows = get_file_download_links(get_bio_sample_infos(base_search_query))
    print('获得信息和下载链接成功')
    # 生成表格
    generate_xlsx_file('./download_links.xlsx', {
        'name': '下载链接',
        'data':
            [
                ['bio_sample_id', 'cell_type', 'file_id', 'assembly', 'file_type', 'output_type', 'download link'],
                *table_rows
            ]
    })
    print('生成表格成功，开始下载文件')
    # 下载文件
    download_files([row[-1] for row in table_rows], download_dir='./download_files/')
