# -*- encoding: utf-8 -*-
"""
@File Name      :   dicts.py    
@Create Time    :   2022/1/11 21:30
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

from collections import Counter


def union_dict_use_counter(dict1, dict2):
    """
    字典合并，相同key值相加，但是在循环里尽量不要直接调用此方法，应该创建一个Counter对象之后不断调用
    """
    return Counter(dict1) + Counter(dict2)


def union_dict_use_set(*objs):
    """
    同上，使用集合，速度更快，但最终输出会无序
    """
    _keys = set(sum([list(obj.keys()) for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key, 0) for obj in objs])
    return _total


def union_dict_use_for(result,append):
    """
    for循环速度最快，注意本函数无返回值，
    """
    for key, value in append.items():
        if result.get(key,None):
            result[key] += value
        else:
            result[key] = value
    return result