# -*- encoding: utf-8 -*-
"""
@File Name      :   group.py    
@Create Time    :   2022/3/23 14:53
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

import click
import pandas as pd


@click.command()
@click.option('--input_file_path', '-i', type=str, required=True, help='input file path')
@click.option('--output_file_path', '-o', type=str, required=True, help='output file path')
def myopia_grouping(input_file_path='./温医大结果导出—sum.xlsx', output_file_path='./分组.xlsx'):
    # 读取Excel文件
    input_file = pd.read_excel(input_file_path, sheet_name=None)
    # 读取所有的sheet到一个列表
    dfs = [sheet_df for sheet_df in input_file.values()]
    # 合并所有sheet
    df = pd.concat(dfs, axis=0)
    # 先筛选出备注有信息的行
    remarks_df = df.loc[df['备注'].notnull()]
    # 再筛选出备注没有信息的行
    df = df.loc[df['备注'].isnull()]
    # 筛选出有一些没测到数据的行
    empty_df = df.loc[(df['右球镜s'].isnull()) & (df['左球镜s'].isnull())]
    # 最后得到可以筛选的数据
    df = df.loc[(df['右球镜s'].notnull()) & (df['左球镜s'].notnull())]
    # 筛选高度近视的行
    high_myopia_df = df.loc[(df['右球镜s'] <= -6) | (df['左球镜s'] <= -6)].copy()
    # 在原来的数据中剔除这些筛选出来的数据
    df = df.append(high_myopia_df).drop_duplicates(keep=False)
    high_myopia_df.loc[:, ['分组']] = '高度近视（HM）'
    # 这不能大于小于连写，必须分开
    myopia_df = df.loc[((-6 < df['右球镜s']) & (df['右球镜s'] <= -3)) | ((-6 < df['左球镜s']) & (df['左球镜s'] <= -3))].copy()
    normal_df = df.append(myopia_df).drop_duplicates(keep=False)
    myopia_df.loc[:, ['分组']] = '近视（Myopia）'
    # 筛选完近视的剩下就都是正常的
    # normal_df = df.loc[(df['右球镜s'] > -3) | (df['左球镜s'] > -3)].copy()
    normal_df.loc[:, ['分组']] = '正常'

    # 合并分组数据
    # 眼轴长度
    eye_axis_df = pd.concat([
        high_myopia_df[['学籍号', '右眼眼轴长度(AL)', '左眼眼轴长度(AL)', '分组']],
        myopia_df[['学籍号', '右眼眼轴长度(AL)', '左眼眼轴长度(AL)', '分组']],
        normal_df[['学籍号', '右眼眼轴长度(AL)', '左眼眼轴长度(AL)', '分组']]
    ], axis=0).rename(columns={'右眼眼轴长度(AL)': '右眼眼轴长度(RAL)', '左眼眼轴长度(AL)': '左眼眼轴长度(LAL)'})
    # 角膜曲率
    cornea_curvature_df = pd.concat([
        high_myopia_df[['学籍号', '右眼角膜曲率(K2)', '左眼角膜曲率(K2)', '分组']],
        myopia_df[['学籍号', '右眼角膜曲率(K2)', '左眼角膜曲率(K2)', '分组']],
        normal_df[['学籍号', '右眼角膜曲率(K2)', '左眼角膜曲率(K2)', '分组']]
    ], axis=0).rename(columns={'右眼角膜曲率(K2)': '右眼角膜曲率(RK2)', '左眼角膜曲率(K2)': '左眼角膜曲率(LK2)'})
    # 眼压
    intraocular_tension_df = pd.concat([
        high_myopia_df[['学籍号', '右眼眼压', '左眼眼压', '分组']],
        myopia_df[['学籍号', '右眼眼压', '左眼眼压', '分组']],
        normal_df[['学籍号', '右眼眼压', '左眼眼压', '分组']]
    ], axis=0)

    # 输出结果文件
    output_file = pd.ExcelWriter(output_file_path)
    eye_axis_df.to_excel(output_file, sheet_name='眼轴长度', index=False)
    cornea_curvature_df.to_excel(output_file, sheet_name='角膜曲率', index=False)
    intraocular_tension_df.to_excel(output_file, sheet_name='眼压', index=False)
    empty_df.to_excel(output_file, sheet_name='空数据', index=False)
    remarks_df.to_excel(output_file, sheet_name='有备注', index=False)
    output_file.save()


if __name__ == '__main__':
    """
    本脚本在python3.8环境下测试通过，预计Python3.6版本以上都不会出现问题
    注意：本脚本需要安装click包
    帮助：python3 group.py --help
    """
    myopia_grouping()
