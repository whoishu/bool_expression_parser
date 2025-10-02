# API 参考文档

## 核心类

### BooleanExpression

主要的用户接口类，用于创建和计算布尔表达式。

#### 构造函数

```python
BooleanExpression(exp)
```

**参数:**
- `exp` (str): 要解析的表达式字符串

**示例:**
```python
expr = BooleanExpression("age > 18")
```

#### 方法

##### evaluate(context=None)

计算表达式的值。

**参数:**
- `context` (dict, optional): 变量上下文字典，默认为空字典

**返回:**
- 表达式的计算结果，类型取决于表达式

**示例:**
```python
# 无变量表达式
result = BooleanExpression("5 > 3").evaluate()  # True

# 带变量表达式
result = BooleanExpression("age >= 18").evaluate({'age': 25})  # True
```

## 支持的表达式语法

### 字面量

#### 数字
- 整数: `123`, `-45`
- 浮点数: `3.14`, `-2.5`

#### 布尔值
- `True`
- `False`

#### 字符串
- 单引号: `'hello'`
- 双引号: `"world"`
- 转义字符: `"He said \"Hello\""`

#### 数组
- 数字数组: `[1, 2, 3]`
- 字符串数组: `['a', 'b', 'c']`
- 混合数组: `[1, 'hello', True]`
- 空数组: `[]`

### 变量

#### 简单变量
```
name
age
is_active
```

#### 数组访问
```
scores[0]          # 访问第一个元素
matrix[1][2]       # 多维数组访问
```

#### 对象属性访问
```
user.name          # 访问对象属性
items[0].price     # 数组元素的属性
```

### 操作符

#### 比较操作符
- `==` : 等于
- `!=` : 不等于
- `<` : 小于
- `>` : 大于
- `<=` : 小于等于
- `>=` : 大于等于
- `in` : 包含关系

#### 算术操作符
- `+` : 加法
- `-` : 减法
- `*` : 乘法
- `/` : 除法

#### 逻辑操作符
- `and` / `AND` : 逻辑与
- `or` / `OR` : 逻辑或
- `not` / `NOT` : 逻辑非

### 字符串修饰符

**注意**: 这些功能在Python 3中可能需要兼容性修复。

#### upper
```python
"name|upper"  # 将字符串转为大写
```

#### lower
```python
"name|lower"  # 将字符串转为小写
```

#### split
```python
"text|split(',')"    # 使用逗号分割字符串
"text|split(' ')"    # 使用空格分割字符串
```

#### strip
```python
"text|strip()"       # 去除首尾空白字符
"text|strip('x')"    # 去除首尾的特定字符
```

### 优先级

表达式的运算优先级从高到低：

1. 括号 `()`
2. 数组访问 `[]`、对象属性访问 `.`
3. 字符串修饰符 `|`
4. 逻辑非 `not`
5. 乘除 `*` `/`
6. 加减 `+` `-`
7. 比较操作符 `==` `!=` `<` `>` `<=` `>=` `in`
8. 逻辑与 `and`
9. 逻辑或 `or`

### 表达式示例

```python
# 简单比较
"5 > 3"

# 变量使用
"age >= 18"

# 算术运算
"salary + bonus > 50000"

# 数组操作
"scores[0] > 90"
"'math' in subjects"

# 对象访问
"user.age > 21"
"products[0].price < 100"

# 逻辑运算
"age > 18 and score > 80"
"is_admin or is_moderator"
"not is_banned"

# 复杂表达式
"(total > 500 and is_vip) or total > 1000"

# 字符串操作（需要兼容性修复）
"name|upper == 'JOHN'"
"email|split('@')[1] == 'company.com'"
```

## 错误处理

表达式解析和求值过程中可能出现的异常：

### ParseException
当表达式语法错误时抛出。

```python
try:
    expr = BooleanExpression("5 ==")  # 语法错误
    result = expr.evaluate()
except ParseException as e:
    print(f"语法错误: {e}")
```

### KeyError
当访问不存在的变量或属性时抛出。

```python
try:
    expr = BooleanExpression("unknown_var > 5")
    result = expr.evaluate({})  # unknown_var 不存在
except KeyError as e:
    print(f"变量不存在: {e}")
```

### ValueError
当操作数类型不匹配时抛出。

```python
try:
    expr = BooleanExpression("5 + 'hello'")  # 类型不匹配
    result = expr.evaluate()
except ValueError as e:
    print(f"类型错误: {e}")
```

## 最佳实践

1. **变量命名**: 使用有意义的变量名，遵循Python命名约定
2. **类型一致性**: 确保操作数类型匹配
3. **上下文完整性**: 提供表达式中用到的所有变量
4. **表达式复杂度**: 避免过于复杂的嵌套表达式
5. **错误处理**: 适当处理可能的异常情况