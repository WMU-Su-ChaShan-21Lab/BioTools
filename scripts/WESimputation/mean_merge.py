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

import os
from collections import defaultdict

import click


@click.command()
@click.argument('input_dir_path', type=click.Path(exists=True))
def main(input_dir_path):
    file_names = [file_name for file_name in os.listdir(input_dir_path) if file_name.endswith('.mean.txt.gz')]
    file_names.sort()
    chr_file_names = defaultdict(list)
    for file_name in file_names:
        chr_file_names[file_name.split('.')[0].split('-')[0]].append(file_name)
    for chr_name, file_names in chr_file_names.items():
        with open(os.path.join(input_dir_path, chr_name + '.mean.txt.gz'), 'w') as w:
            for file_name in file_names:
                with open(os.path.join(input_dir_path, file_name)) as f:
                    w.write(f.read())


if __name__ == '__main__':
    main()
