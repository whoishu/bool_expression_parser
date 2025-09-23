# 布尔表达式解析器 (Bool Expression Parser)

一个功能强大的Python布尔表达式解析器，支持变量、算术运算、逻辑运算、字符串操作和数组访问。

## 项目概述

这个项目实现了一个灵活的布尔表达式解析和求值引擎，可以解析复杂的表达式字符串并在给定的上下文中计算结果。它使用PyParsing库构建语法解析器，支持多种数据类型和操作符。

## 核心功能特性

### 1. 数据类型支持
- **数字**: 整数和浮点数 (`5`, `3.14`, `-10`)
- **布尔值**: `True`, `False`
- **字符串**: 单引号或双引号字符串 (`'hello'`, `"world"`)
- **数组**: 支持常量数组 (`[1, 2, 3]`, `['a', 'b']`)

### 2. 比较操作符
- `==` 等于
- `!=` 不等于
- `<` 小于
- `>` 大于
- `<=` 小于等于
- `>=` 大于等于
- `in` 包含关系

### 3. 算术运算符
- `+` 加法
- `-` 减法
- `*` 乘法
- `/` 除法

### 4. 逻辑运算符
- `and` / `AND` 逻辑与
- `or` / `OR` 逻辑或
- `not` / `NOT` 逻辑非

### 5. 变量和数组访问
- **简单变量**: `name`, `age`
- **数组索引**: `scores[0]`, `matrix[1][2]`
- **对象属性**: `user.name`, `item[0].price`

### 6. 字符串修饰符
- `|upper` 转换为大写
- `|lower` 转换为小写
- `|split('delimiter')` 字符串分割
- `|strip('chars')` 去除指定字符

### 7. 优先级和括号
- 支持使用括号控制运算优先级
- 运算符优先级遵循数学规则

## 使用方法

### 基本用法

```python
from bool_parser import BooleanExpression

# 创建表达式对象
exp = BooleanExpression("5 > 3")

# 计算表达式结果
result = exp.evaluate()
print(result)  # True
```

### 使用变量

```python
# 带变量的表达式
exp = BooleanExpression("age >= 18 and score > 80")

# 提供变量上下文
context = {'age': 25, 'score': 95}
result = exp.evaluate(context)
print(result)  # True
```

### 复杂表达式示例

```python
# 算术运算
exp = BooleanExpression("(salary + bonus) * 0.8 > 50000")
result = exp.evaluate({'salary': 45000, 'bonus': 15000})

# 数组操作
exp = BooleanExpression("scores[0] > 90 and 'math' in subjects")
context = {
    'scores': [95, 87, 92],
    'subjects': ['math', 'science', 'english']
}
result = exp.evaluate(context)

# 字符串操作
exp = BooleanExpression("name|upper == 'JOHN'")
result = exp.evaluate({'name': 'john'})
```

## 安装要求

- Python 2.7+ 或 Python 3.x
- PyParsing 库

```bash
pip install pyparsing
```

## 项目结构

```
bool_expression_parser/
├── bool_parser.py          # 核心解析器实现
├── test_simple_bool.py     # 单元测试
└── README.md              # 项目文档
```

## 核心类说明

### BooleanExpression
主要的用户接口类，用于创建和计算表达式。

**方法**:
- `__init__(exp)`: 初始化表达式
- `evaluate(context=None)`: 计算表达式值

### Grammar  
语法定义类，使用PyParsing定义表达式的语法规则。

### BaseUnit及其子类
表达式元素的基类，包括：
- `Constant`: 常量值
- `Variable`: 变量引用
- `Array`: 数组字面量
- `Operator`: 二元操作符
- `NotOperator`: 逻辑非操作符
- `SplitModificator`: 字符串分割修饰符
- `StripModificator`: 字符串去空格修饰符
- `UpperModificator`: 大写转换修饰符
- `LowerModificator`: 小写转换修饰符

## 表达式语法

### 基本语法规则
- 变量名由字母、数字和下划线组成，首字符必须是字母或下划线
- 字符串用单引号或双引号包围
- 数组用方括号表示，元素用逗号分隔
- 使用空格分隔操作符和操作数

### 优先级规则（从高到低）
1. 括号 `()`
2. 数组访问 `[]`、属性访问 `.`
3. 字符串修饰符 `|`
4. 逻辑非 `not`
5. 乘除 `*` `/`
6. 加减 `+` `-`
7. 比较操作符 `==` `!=` `<` `>` `<=` `>=` `in`
8. 逻辑与 `and`
9. 逻辑或 `or`

## 使用场景

这个布尔表达式解析器适用于以下场景：

1. **规则引擎**: 配置驱动的业务规则判断
2. **数据过滤**: 根据表达式过滤数据集
3. **条件配置**: 在配置文件中定义复杂的条件逻辑
4. **模板系统**: 在模板中进行条件渲染
5. **工作流**: 定义工作流的条件分支

## 注意事项

- 项目最初为Python 2设计，在Python 3中运行可能需要一些兼容性调整
- 字符串修饰符功能在Python 3中可能需要修复`basestring`相关的问题
- 表达式解析是递归的，过于复杂的嵌套可能影响性能

## 贡献

欢迎提交问题报告和功能请求。如果你想贡献代码，请确保：
1. 编写相应的单元测试
2. 遵循现有的代码风格
3. 确保Python 2/3兼容性

## 作者

huxx <hzd0107@hotmail.com>
