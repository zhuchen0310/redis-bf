#! /usr/bin/python
# -*- coding:utf-8 -*-
# @zhuchen    : 2020/8/5 14:48
import sys
from os import path
from ctypes import c_char_p, CDLL, c_long, c_double

try:
    here = path.abspath(path.dirname(__file__))
    if sys.platform == "darwin":
        so_file_name = "bfmac"
    else:
        so_file_name = "bflinux"
    lib = CDLL(f'{here}/{so_file_name}.so')
except Exception as e:
    print(e)
    raise BaseException("请指定 apollo config 路径")


class RedisBF:

    def __init__(self, bf_type: str="", expected_number: int=10000, fp_rate: float=0.1):
        """
        :param bf_type: 布隆过滤器 类型, 实例化使用
        :param expected_number: 用于计算bit数组长度 math.ceil(float(expected_number) * math.log(1/fp_rate) / math.log(2) / math.log(2))
        :param fp_rate: 用于计算哈希函数个数 math.ceil(math.log2(1 / fp_rate))
        """
        self.type = bf_type if bf_type else f"{expected_number}-{fp_rate}"
        self.expected_number = expected_number
        self.fp_rate = fp_rate

    def add_items(self, bf_name: str, items: list):
        """
        添加 元素到bf中
        :param bf_name: name1, 在redis中格式为bf:name1
        :param items: [1,2,3,4]
        """
        if not items:
            return
        if not isinstance(items[0], str):
            items_str = ','.join(map(str, items))
        else:
            items_str = ','.join(items)
        lib.AddVideos(
            c_char_p(bf_name.encode()),
            c_char_p(items_str.encode()),
            c_long(self.expected_number),
            c_double(self.fp_rate)
        )

    def filter_items(self, bf_name: str, items: list):
        """
        过滤掉已存在的元素
        :param bf_name: name1, 在redis中格式为bf:name1
        :param items: [1,2,3,4]
        return ['1', '2']
        """
        if not items:
            return
        if not isinstance(items[0], str):
            items_str = ','.join(map(str, items))
        else:
            items_str = ','.join(items)
        lib.FilterVideos.restype = c_char_p
        ret_str = lib.FilterVideos(c_char_p(bf_name.encode()), c_char_p(items_str.encode()))
        ret_items = ret_str.decode().split(",")
        return ret_items
