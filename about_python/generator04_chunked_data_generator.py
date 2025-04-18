#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 下午2:39

"""
# 练习：优化大数据生成过程
# 要求：
# - 使用生成器每次生成1000条用户数据
# - 将数据实时写入到CSV文件
# - 确保内存占用保持稳定
# 文件格式要求：
# name,address,phone
# 张三,北京市朝阳区,13800138000
"""
import csv
from faker import Faker
import sys
import time


def chunked_data_generator(chunk_size=1000, locale='zh_CN'):
    """
    分块生成用户数据的生成器
    :param chunk_size: 每批生成的数据量（默认1000条）
    :param locale: 数据语言设置
    """
    fake = Faker(locale)
    chunk = []

    while True:
        # 生成单条数据（内存友好）
        user = {
            'name': fake.name(),
            'address': fake.address().replace('\n', ' '),
            'phone': fake.phone_number()
        }
        chunk.append(user)

        # 达到分块大小时产出数据并清空临时存储
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []


def write_to_csv(filename, total_records, chunk_size=1000):
    """
    实时写入CSV文件的核心函数
    :param filename: 输出文件名
    :param total_records: 需要生成的总数据量
    :param chunk_size: 分块大小
    """
    # 初始化进度跟踪
    start_time = time.time()
    records_written = 0

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'address', 'phone'])
        writer.writeheader()

        # 创建分块生成器
        data_gen = chunked_data_generator(chunk_size)

        while records_written < total_records:
            chunk = next(data_gen) if total_records - records_written > chunk_size else next(data_gen)[
                                                                                        :total_records - records_written]
            writer.writerows(chunk)
            records_written += len(chunk)

            # 实时进度显示
            sys.stdout.write(f"\r已写入: {records_written}/{total_records} 条 "
                             f"耗时: {time.time() - start_time:.2f}秒 "
                             f"当前内存: {sys.getsizeof(chunk) / 1024:.2f}KB")
            sys.stdout.flush()

    print(f"\n完成！文件已保存至 {filename}")


if __name__ == "__main__":
    # 配置参数
    TARGET_RECORDS = 1_000_000  # 生成100万条数据
    CHUNK_SIZE = 1000  # 分块大小
    OUTPUT_FILE = 'users.csv'

    # 执行生成
    write_to_csv(OUTPUT_FILE, TARGET_RECORDS, CHUNK_SIZE)
