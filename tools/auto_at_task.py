# -*- encoding: utf-8 -*-
"""
@File Name      :   auto_at_task.py    
@Create Time    :   2022/5/13 22:15
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
@click.argument('input_dir_path', type=click.Path(exists=True))
@click.option('--minutes', '-m', default=15, help='minutes')
@click.option('--hours', '-h', default=0, help='hours')
@click.option('--days', '-d', default=0, help='days')
@click.option('--weeks', '-w', default=0, help='weeks')
@click.option('--months', '-M', default=0, help='months')
@click.option('--years', '-y', default=0, help='years')
def main(input_dir_path, minutes, hours, days, weeks, months, years):
    years = int(years)
    months = int(months) + years * 12
    weeks = int(weeks) + months * 4
    days = int(days) + weeks * 7
    hours = int(hours) + days * 24
    minutes = int(minutes) + hours * 60

    with open(os.path.join(input_dir_path, 'auto_at_task.sh'), 'w') as w:
        for index, file_path in enumerate([
            os.path.join(input_dir_path, file_name)
            for file_name in os.listdir(input_dir_path)
            if file_name.endswith('.sh') and 'at' not in file_name
        ]):
            w.write(f'at now + {minutes * index} minutes -f {file_path}\n')


if __name__ == '__main__':
    main()
