#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : day0412_data_generator_gb.py
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 下午3:31

"""
# 终极练习：生成1GB测试数据文件
# 要求：
# - 使用生成器保持内存占用<50MB
# - 数据包含姓名/地址/电话
# - 输出到data.csv文件
# - 显示实时进度（已生成数据量）
# 提示：
# 1. 计算单条记录的大致字节数
# 2. 根据目标大小计算需要生成的总条数
# 3. 使用with语句管理文件写入
"""

import csv
import os
import sys
import time
import psutil
from faker import Faker


class DataGenerator:
    def __init__(self, target_gb=1, memory_limit=1):
        self.fake = Faker('zh_CN')
        self.target_bytes = target_gb * 1024 ** 2 * 10
        # self.target_bytes = target_gb * 1024 ** 3
        self.memory_limit = memory_limit * 1024 ** 2  # 转换为字节
        self.batch_size = 1000  # 初始批次大小
        self.sample_size = 1000  # 样本数量
        self.memory_used_already = psutil.virtual_memory().used  # 初始内存使用字节数

        # 预计算单条记录大小
        self.record_template = self._create_record_template()
        self.avg_record_size = self._calculate_record_size()

    def _create_record_template(self):
        """创建具有代表性的记录模板"""
        return (
            "张三",  # 中文姓名基准长度
            "中国北京市朝阳区建国路100号",  # 典型地址长度
            "13800138000"  # 标准电话格式
        )

    def _calculate_record_size(self):
        """精确计算单条记录的平均字节数"""
        sample_records = [self._generate_record() for _ in range(self.sample_size)]
        total_size = 0

        with open(".temp_sample.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'address', 'phone'])

            for record in sample_records:
                line = ','.join(record)
                total_size += len(line.encode('utf-8')) + 1  # +1 for newline

        os.remove(".temp_sample.csv")
        return total_size / self.sample_size

    def _generate_record(self):
        """生成单条记录的优化版本"""
        return (
            self.fake.name(),
            self.fake.address().strip().replace('\n', ' '),
            self.fake.phone_number()
        )

    def _adjust_batch_size(self):
        """动态调整批次大小保持内存安全"""
        mem = psutil.virtual_memory()
        used_percent = mem.used / self.memory_limit

        if used_percent > 0.8:  # 内存使用超过80%
            self.batch_size = max(100, int(self.batch_size * 0.7))
        elif used_percent < 0.5:  # 内存充裕时适当增加
            self.batch_size = min(10000, int(self.batch_size * 1.2))

    def _show_progress(self, start_time, written_bytes):
        """显示进度和资源使用情况"""
        elapsed = time.time() - start_time
        percent = written_bytes / self.target_bytes * 100
        speed = written_bytes / (1024 ** 2) / elapsed if elapsed > 0 else 0

        mem = psutil.virtual_memory()
        if mem.used > self.memory_used_already:
            mem_usage = (mem.used - self.memory_used_already) / (1024 ** 2)
        else:
            # 这种情况可能是其他消耗内存程序释放了，暂时不作处理
            mem_usage = -(self.memory_used_already - mem.used) / (1024 ** 2)

        print(f"\r进度: {percent:.2f}% | "
              f"已写入: {written_bytes / (1024 ** 3):.2f}GB | "
              f"速度: {speed:.2f}MB/s | "
              f"内存使用: {mem_usage:.2f}MB | "
              f"批次大小: {self.batch_size}  ", end='')

    def generate(self, filename):
        start_time = time.time()
        estimated_records = int(self.target_bytes / self.avg_record_size)

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\')
            writer.writerow(['name', 'address', 'phone'])
            f.flush()  # 立即写入表头

            written_bytes = f.tell()
            records_generated = 0

            while written_bytes < self.target_bytes:
                # 生成批次数据
                chunk = []
                for _ in range(self.batch_size):
                    chunk.append(self._generate_record())
                    records_generated += 1

                # 写入并刷新
                writer.writerows(chunk)
                f.flush()  # 关键：立即释放内存

                # 更新写入量
                written_bytes = f.tell()

                # 显示进度
                self._show_progress(start_time, written_bytes)

                # 动态调整批次
                self._adjust_batch_size()

                # 精确终止控制
                remaining_bytes = self.target_bytes - written_bytes
                if remaining_bytes < self.avg_record_size * 2:
                    self.batch_size = 1
                elif remaining_bytes < self.avg_record_size * 100:
                    self.batch_size = 10

                # 最终检查
                if written_bytes >= self.target_bytes:
                    break

        # 不能截断，要确保内容完整
        # 最终文件截断（确保精确大小）
        # with open(filename, 'r+', encoding='utf-8') as f:
        #     f.seek(self.target_bytes)
        #     f.truncate()

        print(f"\n生成完成！最终文件大小: {os.path.getsize(filename) / (1024 ** 3):.2f}GB")


if __name__ == "__main__":
    generator = DataGenerator(target_gb=1, memory_limit=50)
    generator.generate("1gb_data.csv")
