# -*- encoding: utf-8 -*-
"""
@File Name      :   add_rows.py    
@Create Time    :   2022/5/6 15:03
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
import time
from itertools import islice

import click

add_text = """##contig=<ID=M,length=16571>
##contig=<ID=1,length=249250621>
##contig=<ID=2,length=243199373>
##contig=<ID=3,length=198022430>
##contig=<ID=4,length=191154276>
##contig=<ID=5,length=180915260>
##contig=<ID=6,length=171115067>
##contig=<ID=7,length=159138663>
##contig=<ID=8,length=146364022>
##contig=<ID=9,length=141213431>
##contig=<ID=10,length=135534747>
##contig=<ID=11,length=135006516>
##contig=<ID=12,length=133851895>
##contig=<ID=13,length=115169878>
##contig=<ID=14,length=107349540>
##contig=<ID=15,length=102531392>
##contig=<ID=16,length=90354753>
##contig=<ID=17,length=81195210>
##contig=<ID=18,length=78077248>
##contig=<ID=19,length=59128983>
##contig=<ID=20,length=63025520>
##contig=<ID=21,length=48129895>
##contig=<ID=22,length=51304566>
##contig=<ID=X,length=155270560>
##contig=<ID=Y,length=59373566>
##contig=<ID=1_gl000191_random,length=106433>
##contig=<ID=1_gl000192_random,length=547496>
##contig=<ID=4_gl000193_random,length=189789>
##contig=<ID=4_gl000194_random,length=191469>
##contig=<ID=7_gl000195_random,length=182896>
##contig=<ID=8_gl000196_random,length=38914>
##contig=<ID=8_gl000197_random,length=37175>
##contig=<ID=9_gl000198_random,length=90085>
##contig=<ID=9_gl000199_random,length=169874>
##contig=<ID=9_gl000200_random,length=187035>
##contig=<ID=9_gl000201_random,length=36148>
##contig=<ID=11_gl000202_random,length=40103>
##contig=<ID=17_gl000203_random,length=37498>
##contig=<ID=17_gl000204_random,length=81310>
##contig=<ID=17_gl000205_random,length=174588>
##contig=<ID=17_gl000206_random,length=41001>
##contig=<ID=18_gl000207_random,length=4262>
##contig=<ID=19_gl000208_random,length=92689>
##contig=<ID=19_gl000209_random,length=159169>
##contig=<ID=21_gl000210_random,length=27682>
##contig=<ID=Un_gl000211,length=166566>
##contig=<ID=Un_gl000212,length=186858>
##contig=<ID=Un_gl000213,length=164239>
##contig=<ID=Un_gl000214,length=137718>
##contig=<ID=Un_gl000215,length=172545>
##contig=<ID=Un_gl000216,length=172294>
##contig=<ID=Un_gl000217,length=172149>
##contig=<ID=Un_gl000218,length=161147>
##contig=<ID=Un_gl000219,length=179198>
##contig=<ID=Un_gl000220,length=161802>
##contig=<ID=Un_gl000221,length=155397>
##contig=<ID=Un_gl000222,length=186861>
##contig=<ID=Un_gl000223,length=180455>
##contig=<ID=Un_gl000224,length=179693>
##contig=<ID=Un_gl000225,length=211173>
##contig=<ID=Un_gl000226,length=15008>
##contig=<ID=Un_gl000227,length=128374>
##contig=<ID=Un_gl000228,length=129120>
##contig=<ID=Un_gl000229,length=19913>
##contig=<ID=Un_gl000230,length=43691>
##contig=<ID=Un_gl000231,length=27386>
##contig=<ID=Un_gl000232,length=40652>
##contig=<ID=Un_gl000233,length=45941>
##contig=<ID=Un_gl000234,length=40531>
##contig=<ID=Un_gl000235,length=34474>
##contig=<ID=Un_gl000236,length=41934>
##contig=<ID=Un_gl000237,length=45867>
##contig=<ID=Un_gl000238,length=39939>
##contig=<ID=Un_gl000239,length=33824>
##contig=<ID=Un_gl000240,length=41933>
##contig=<ID=Un_gl000241,length=42152>
##contig=<ID=Un_gl000242,length=43523>
##contig=<ID=Un_gl000243,length=43341>
##contig=<ID=Un_gl000244,length=39929>
##contig=<ID=Un_gl000245,length=36651>
##contig=<ID=Un_gl000246,length=38154>
##contig=<ID=Un_gl000247,length=36422>
##contig=<ID=Un_gl000248,length=39786>
##contig=<ID=Un_gl000249,length=38502>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
"""


@click.command()
@click.option('--input_dir', '-i', type=str, required=True, help='Input dir')
@click.option(
    '--output_dir', '-o', type=str, default='',
    help='Output directory path, according to input files to generate files.')
def main(input_dir, output_dir):
    start = time.perf_counter()
    if not output_dir:
        output_dir = os.path.join(input_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    file_paths = [file_path for file_path in os.listdir(input_dir) if file_path.endswith('.gz')]
    for file_path in file_paths:
        print('handling ' + file_path)
        with gzip.open(os.path.join(input_dir, file_path), 'rt') as input_file, \
                gzip.open(os.path.join(output_dir, file_path), 'wt') as output_file:
            stop = False
            inserted = False
            while not stop:
                lines = list(islice(input_file, 100000))
                if not lines:
                    stop = True
                else:
                    if not inserted:
                        for i in range(len(lines)):
                            if '##FILTER=<ID=INFO0.95,Description="IMPUTE2 style imputation information score < 0.95">' in \
                                    lines[i] and '##contig=<ID=10,length=2147483647>' in lines[i + 1]:
                                lines = lines[:i + 1] + [row + '\n' for row in add_text.split('\n')] + lines[i + 2:]
                                inserted = True
                                break
                    output_file.writelines(lines)
        print(f'{time.perf_counter() - start}')


if __name__ == '__main__':
    main()
