# 基础使用步骤

```python
# 1、导入模块
import argparse

# 2、创建解析器对象
parser = argparse.ArgumentParser(description="程序描述")

# 3、添加参数

# 3.1 位置参数
parser.add_argument("filename", help="输入文件名")

# 3.2 可选参数（以`-`或`--`开头）：
parser.add_argument("-v", "--verbose", action="store_true", help="启用详细模式")

# 4 解析参数
args = parser.parse_args()

# 5、使用参数
print(args.filename)
if args.verbose:
   print("详细模式已启用")
```

## 脚本示例

```python
# content of script.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="计算整数和")
    parser.add_argument("nums", nargs="+", type=int, help="参与计算的整数")
    parser.add_argument("-s", "--sum", action="store_true", help="求和（默认）")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    total = sum(args.nums)
    if args.verbose:
        print(f"输入数字: {args.nums}")
        print(f"总和: {total}")
    else:
        print(total)

if __name__ == "__main__":
    main()
```

使用方式：

```python
python script.py 1 2 3 -v  # 输出详细结果
python script.py 5 10      # 仅输出结果
```

# add_argument()

- name or flags - 一个名称或是由选项字符串组成的列表，例如 'foo' 或 '-f', '--foo'。
- action - 当参数在命令行中出现时使用的动作基本类型。
- nargs - 命令行参数应当消耗的数目。
- const - 被一些 action 和 nargs 选择所需求的常数。
- default - 当参数未在命令行中出现并且也不存在于命名空间对象时所产生的值。
- type - 命令行参数应当被转换成的类型。
- choices - 由允许作为参数的值组成的序列。
- required - 此命令行选项是否可省略 （仅选项可用）。
- help - 一个此选项作用的简单描述。
- metavar - 在使用方法消息中使用的参数值示例。
- dest - 被添加到 parse_args() 所返回对象上的属性名。
- deprecated - 参数的使用是否已被弃用。

## 常用的参数示例

```python
# 数据类型和默认值
parser.add_argument("--num", type=int, default=0, help="整数参数（默认0）")

# 必须的可选参数
parser.add_argument("--output", required=True, help="必须提供的输出路径")

# 互斥参数组
group = parser.add_mutually_exclusive_group()
group.add_argument("--option1", action="store_true")
group.add_argument("--option2", action="store_true")

# 多值参数
parser.add_argument("--files", nargs="+", help="多个文件名")

# 选择范围限制
parser.add_argument("--color", choices=["red", "green", "blue"], help="颜色选项")

# 自定义动作
parser.add_argument("--tag", action="append", help="添加标签")

# 自定义类型检查
def valid_file(filename):
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"文件不存在: {filename}")
    return filename

parser.add_argument("--config", type=valid_file, help="配置文件路径")
```

# 注意事项

1. **位置参数**：
   - 默认必须提供，除非设置`nargs="?"`和`default`。
   - 顺序敏感，需按定义顺序输入。

2. **可选参数**：
   - 使用`-`或`--`开头，可通过`dest`指定属性名。
   - 设置`required=True`可强制要求提供。

3. **类型与错误处理**：
   - `type`参数自动验证类型（如`int`、自定义函数）。
   - 无效输入会触发自动错误提示。

4. **帮助信息**：
   - 使用`help`参数描述用途，`-h/--help`自动生成帮助文档。

5. **默认值与常量**：
   - `default`设置未提供参数时的默认值。
   - `action="store_const"`配合`const`存储常量值。

6. **互斥参数**：
   - 使用`add_mutually_exclusive_group()`确保参数不冲突。

7. **错误处理**：
   ```python
   try:
       args = parser.parse_args()
   except argparse.ArgumentError as e:
       print(f"错误: {e}")
       sys.exit(1)
   ```
