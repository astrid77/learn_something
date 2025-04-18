#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/4/12 下午1:37

"""
# 练习：使用Faker创建生成测试数据的生成器
# 要求：
# - 生成器每次yield一个包含姓名、地址、电话的字典
# - 使用中文数据（zh_CN）
# - 限制生成5条记录测试
# 示例输出：
# {'name': '王伟', 'address': '广东省深圳县', 'phone': '18956236745'}
"""
import faker


def get_test_data():
    fake = faker.Faker('zh_CN')
    for _ in range(5):
        yield {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number()
        }


test_data = get_test_data()
# for idx, record in enumerate(test_data, 1):
#     print(f'{idx}:{record}')
for record in test_data:
    print(record)
