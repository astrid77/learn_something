#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/11 15:42

"""
  - 创建支持 `--env=prod` 的参数解析器
  - 练习：编写解析不同参数类型的脚本
"""
import argparse


def arg_parser():
    parser = argparse.ArgumentParser(prog='myprogram', description='这是一个示例程序')
    parser.add_argument('user', help='执行程序的用户')
    parser.add_argument('-cases', required=False, help='测试用例')
    parser.add_argument('--env',
                        choices=['test', 'prod', 'dev'],
                        default='test',
                        help='测试环境，默认test')
    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parser()
    print(args)
