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
    dir_names = os.listdir(dir_path)
    file_names = [os.path.join(dir_path, dir_name, dir_name + '.sortedfilter.txt.gz') for dir_name in dir_names]
    for file_name in file_names:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(file_name)


if __name__ == '__main__':
    main()
