# -*- encoding: utf-8 -*-
"""
@File Name      :   delete.py    
@Create Time    :   2022/5/11 16:58
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

import click


@click.command()
@click.argument('dir_path', type=click.Path(exists=True))
def main(dir_path):
    file_paths = [os.path.join(dir_path, dir_name, dir_name + 'filter.txt.gz') for dir_name in os.listdir(dir_path)]
    for file_path in file_paths:
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    main()
