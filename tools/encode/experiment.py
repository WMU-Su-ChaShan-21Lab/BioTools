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
from utils.file import make_dir,remove_file
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
# base_search_query = {
#     'type': ['Experiment'],
#     'status': ['released'],
#     'assay_title': ['polyA plus RNA-seq', 'total RNA-seq', 'RNA microarray'],
#     'replicates.library.biosample.donor.organism.scientific_name': ['Homo sapiens'],
#     'limit': 'all',
#     'format': ['json']
# }


def get_bio_sample_infos(query_dict):
    search_url = base_search_url + '?' + unquote(urlencode(query_dict, doseq=True))
    res = session.get(search_url)
    res.raise_for_status()
    result = res.json()
    bio_sample_infos = [{
        'bio_sample_id': item['accession'],
        'cell_type': item['biosample_ontology']['term_name'],
        'assay_title': item['assay_title'],
    } for item in result['@graph']]
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


def get_bio_sample_file(bio_sample_info):
    bio_sample_url = base_bio_samples_url + bio_sample_info['bio_sample_id'] + '/?format=json'
    res = session.get(bio_sample_url)
    res.raise_for_status()
    result = res.json()
    files = result['files']
    files_list = [{
        'bio_sample_id': bio_sample_info['bio_sample_id'],
        'cell_type': bio_sample_info['cell_type'],
        'assay_title': bio_sample_info['assay_title'],
        'file_id': file['accession'],
        'assembly': file['assembly'],
        'file_format': file['file_format'],
        'file_type': file['file_type'],
        'output_type': file['output_type'],
        'file_size':file.get('file_size', None),
        'md5sum':file['md5sum'],
        'href': file['href'],
    } for file in files if file['output_category'] != 'raw data']
    has_hg38 = any([file['assembly'] == 'GRCh38' for file in files_list])
    row = []
    if has_hg38:
        row = [list(file.values()) for file in files_list if file['assembly'] == 'GRCh38'
               and file['file_type'] == 'tsv' and file['output_type'] == 'gene quantifications'
               ]
    # 防止hg38中没有符合条件的，虽然可能性比较低
    if not row or not has_hg38:
        row = [list(file.values()) for file in files_list if file['assembly'] == 'hg19'
               # and 'bigBed' not in file['file_type']
               and ('bed' in file['file_type'] and 'bigBed' not in file['file_type'])
               # and (file['output_type'] == 'filtered transcribed fragments')
               ]
    # download_links.extend(row)
    return row


def get_file_infos(bio_sample_infos):
    """
    如果有h38，优先使用，否则使用h19
    h38: file_type:tsv output_type:gene quantifications
    h19: file_type:bed broadPeak output_type:filtered transcribed fragments
    """
    # 多线程写法
    file_infos = []
    threads = []
    for bio_sample_info in bio_sample_infos:
        thread = threading.Thread(target=lambda q, arg1: q.put(get_bio_sample_file(arg1)),
                                  args=(que, bio_sample_info,),
                                  daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    while not que.empty():
        file_infos.extend(que.get())
    return file_infos

    # 单线程写法，速度慢
    # download_links = []
    # count = 0
    # for bio_sample_id in bio_sample_ids:
    #     count += 1
    #     if count % 100 == 0:
    #         print(count)
    #     download_links.extend(get_bio_sample_file(bio_sample_id))
    # return download_links


def download_file(download_info, download_dir='./'):
    file_size,md5,download_link=download_info
    download_url=base_url + download_link
    make_dir(download_dir)
    file_path = os.path.join(download_dir, download_url.split('/')[-1])
    if os.path.exists(file_path):
        if file_size and os.path.getsize(file_path)==file_size:
            print(f'{file_path} 文件已经存在，跳过下载')
            return True
        else:
            remove_file(file_path)
    # print(file_path)
    res = session.get(download_url)
    res.raise_for_status()
    with open(file_path, 'wb') as f:
        # 一次性下载
        f.write(res.content)


def download_files(download_infos, download_dir='./'):
    threads = []
    for download_info in download_infos:
        thread = threading.Thread(target=download_file, args=(download_info, download_dir))
        threads.append(thread)
    for thread in threads:
        thread.start()
    # 由于不需要获得任何结果，直接下载即可，所以就不join了


if __name__ == '__main__':
    """
    本脚本是下载encode数据用的
    下载文件使用的是多线程，可以最大利用带宽，但是占用内存也非常大，如果内存不够很可能内存溢出
    """
    # 获得信息和链接
    file_info_rows = get_file_infos(get_bio_sample_infos(base_search_query))
    print('获得文件信息成功')
    # 生成表格
    generate_xlsx_file('./files_info.xlsx', {
        'name': '下载链接',
        'data':
            [
                ['bio_sample_id', 'cell_type', 'assay_title', 'file_id', 'assembly', 'file_format', 'file_type',
                 'output_type','file_size','md5sum','download link'],
                *file_info_rows
            ]
    })
    print('生成表格成功')
    # 下载文件
    download_files([row[-3:] for row in file_info_rows], download_dir='./download_files/')
    print('开始下载文件')
