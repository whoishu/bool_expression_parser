#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
布尔表达式解析器使用示例
"""

from bool_parser import BooleanExpression


def example_basic_operations():
    """基本操作示例"""
    print("=== 基本操作示例 ===")
    
    # 数字比较
    examples = [
        ("5 == 5", {}),
        ("10 > 5", {}),
        ("3.14 <= 4", {}),
        ("7 != 8", {})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:15} => {result}")


def example_variables():
    """变量使用示例"""
    print("\n=== 变量使用示例 ===")
    
    examples = [
        ("age >= 18", {"age": 25}),
        ("name == 'John'", {"name": "John"}),
        ("salary > 50000", {"salary": 75000}),
        ("is_active == True", {"is_active": True})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:20} 上下文{context} => {result}")


def example_arithmetic():
    """算术运算示例"""
    print("\n=== 算术运算示例 ===")
    
    examples = [
        ("3 + 2 == 5", {}),
        ("10 - 3 > 5", {}),
        ("4 * 5 == 20", {}),
        ("15 / 3 == 5", {}),
        ("salary + bonus > 60000", {"salary": 45000, "bonus": 18000})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:25} 上下文{context} => {result}")


def example_logical_operations():
    """逻辑运算示例"""
    print("\n=== 逻辑运算示例 ===")
    
    examples = [
        ("age >= 18 and score > 80", {"age": 22, "score": 95}),
        ("is_admin or is_moderator", {"is_admin": False, "is_moderator": True}),
        ("not is_banned", {"is_banned": False}),
        ("(age > 65 or years_service > 30) and is_eligible", 
         {"age": 45, "years_service": 35, "is_eligible": True})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:40} => {result}")
        print(f"    上下文: {context}")


def example_array_operations():
    """数组操作示例"""
    print("\n=== 数组操作示例 ===")
    
    examples = [
        ("scores[0] > 90", {"scores": [95, 87, 92]}),
        ("grades[1] == 'A'", {"grades": ["B", "A", "C"]}),
        ("matrix[0][1] == 5", {"matrix": [[1, 5], [3, 7]]}),
        ("3 in [1, 2, 3, 4]", {}),
        ("item in favorites", {"item": "apple", "favorites": ["apple", "banana"]})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:25} 上下文{context} => {result}")


def example_object_access():
    """对象属性访问示例"""
    print("\n=== 对象属性访问示例 ===")
    
    examples = [
        ("user[0].name == 'Alice'", 
         {"user": [{"name": "Alice", "age": 30}]}),
        ("product.price > 100", 
         {"product": {"name": "Laptop", "price": 1200}}),
        ("students[1].grades[0] >= 85", 
         {"students": [
             {"grades": [78, 82]}, 
             {"grades": [88, 91]}
         ]})
    ]
    
    for expr, context in examples:
        result = BooleanExpression(expr).evaluate(context)
        print(f"{expr:30} => {result}")
        print(f"    上下文: {context}")


def example_complex_expressions():
    """复杂表达式示例"""
    print("\n=== 复杂表达式示例 ===")
    
    # 电商折扣规则
    discount_rule = "(total_amount > 500 and is_vip) or (total_amount > 1000)"
    context1 = {"total_amount": 800, "is_vip": True}
    result1 = BooleanExpression(discount_rule).evaluate(context1)
    print(f"折扣规则: {discount_rule}")
    print(f"订单金额800，VIP用户 => 符合折扣条件: {result1}")
    
    context2 = {"total_amount": 1200, "is_vip": False}
    result2 = BooleanExpression(discount_rule).evaluate(context2)
    print(f"订单金额1200，普通用户 => 符合折扣条件: {result2}")
    
    # 员工绩效评估
    performance_rule = "sales_target_rate >= 1.0 and customer_satisfaction > 4.0 and not has_complaints"
    context3 = {"sales_target_rate": 1.2, "customer_satisfaction": 4.5, "has_complaints": False}
    result3 = BooleanExpression(performance_rule).evaluate(context3)
    print(f"\n绩效评估: {performance_rule}")
    print(f"销售达成率120%，客户满意度4.5，无投诉 => 通过评估: {result3}")


def example_string_operations():
    """字符串操作示例（需要修复Python3兼容性）"""
    print("\n=== 字符串操作示例 ===")
    print("注意: 这些功能在当前Python3环境中可能不工作，需要修复兼容性问题")
    
    examples = [
        ("name|upper == 'JOHN'", {"name": "john"}),
        ("email|lower", {"email": "USER@EXAMPLE.COM"}),
        ("text|split(',')", {"text": "apple,banana,orange"}),
        ("data|strip(' ')", {"data": "  hello world  "})
    ]
    
    for expr, context in examples:
        try:
            result = BooleanExpression(expr).evaluate(context)
            print(f"{expr:25} 上下文{context} => {result}")
        except Exception as e:
            print(f"{expr:25} => 错误: {e}")


if __name__ == "__main__":
    print("布尔表达式解析器功能演示")
    print("=" * 50)
    
    example_basic_operations()
    example_variables()
    example_arithmetic()
    example_logical_operations()
    example_array_operations()
    example_object_access()
    example_complex_expressions()
    example_string_operations()
    
    print("\n" + "=" * 50)
    print("演示完成！")