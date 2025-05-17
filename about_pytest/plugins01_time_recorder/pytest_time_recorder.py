#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Astrid Wang
# @GitHub : https://github.com/astrid77/
# @Date : 2025/5/17 16:31

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # 获取所有测试用例的执行报告
    reports = []
    for status in ('passed', 'failed', 'skipped'):
        reports.extend(terminalreporter.stats.get(status, []))

    # 提取用例名称及执行时间
    durations = []
    for report in reports:
        if report.when == 'call':  # 仅统计测试执行阶段（排除 setup/teardown）
            duration = getattr(report, 'duration', 0)
            durations.append((report.nodeid, duration))

    if not durations:
        return

    # 按执行时间排序
    sorted_durations = sorted(durations, key=lambda x: x[1], reverse=True)
    total_duration = sum(d[1] for d in sorted_durations)

    # 输出到终端
    terminalreporter.write_sep('=', "用例执行时间统计")
    terminalreporter.line(f"总耗时: {total_duration:.2f}s")
    terminalreporter.line("\n最慢的5个用例:")

    max_len = max(len(name) for name, _ in sorted_durations[:5])
    for name, duration in sorted_durations[:5]:
        terminalreporter.line(f"{name:{max_len}} : {duration:.2f}s")
