# -*- encoding: utf-8 -*-
"""
@File Name      :   merge.py    
@Create Time    :   2022/5/8 17:32
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

import gzip
import os
from collections import defaultdict

import click


@click.command()
@click.argument('input_dir_path', type=click.Path(exists=True))
@click.option('--size', '-s', type=int, help='Size')
def main(input_dir_path, size=10000000):
    file_names = [
        file_name for file_name in os.listdir(input_dir_path)
        if file_name.endswith('.statistics.txt.gz') and 'all' not in file_name
    ]
    file_names.sort()
    chr_file_names = defaultdict(list)
    for file_name in file_names:
        loci = file_name.split('.')[0]
        chromosome, start, end = loci.split('-')
        if int(end) - int(start) == size:
            chr_file_names[chromosome].append(file_name)
    with gzip.open(os.path.join(input_dir_path, 'all.statistics.txt.gz'), 'wt') as all_writer:
        for chromosome, file_names in chr_file_names.items():
            with gzip.open(os.path.join(input_dir_path, chromosome + '.statistics.txt.gz'), 'wt') as w:
                for file_name in file_names:
                    with gzip.open(os.path.join(input_dir_path, file_name), 'rt') as f:
                        head = f.readline()
                        content = f.read()
                        w.write(content)
                        all_writer.write(content)


if __name__ == '__main__':
    main()
