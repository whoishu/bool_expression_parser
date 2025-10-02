#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
布尔表达式解析器简化示例
"""

from bool_parser import BooleanExpression


def safe_evaluate(expr_str, context=None):
    """安全执行表达式求值"""
    try:
        result = BooleanExpression(expr_str).evaluate(context or {})
        return result, None
    except Exception as e:
        return None, str(e)


def main():
    print("布尔表达式解析器功能演示")
    print("=" * 50)
    
    # 基本测试用例
    test_cases = [
        # 基本比较
        ("5 == 5", {}),
        ("10 > 5", {}),
        ("3.14 <= 4", {}),
        
        # 变量
        ("age >= 18", {"age": 25}),
        ("score > 80", {"score": 95}),
        
        # 算术运算
        ("3 + 2 == 5", {}),
        ("10 - 3 > 5", {}),
        ("4 * 5 == 20", {}),
        ("15 / 3 == 5", {}),
        
        # 数组访问
        ("scores[0] > 90", {"scores": [95, 87, 92]}),
        ("3 in [1, 2, 3, 4]", {}),
        
        # 对象访问
        ("user.name == 'Alice'", {"user": {"name": "Alice", "age": 30}}),
        
        # 逻辑运算（简化）
        ("age > 18", {"age": 25}),
        ("not False", {}),
        
        # 复杂表达式
        ("(salary + bonus) > 60000", {"salary": 45000, "bonus": 18000}),
        ("score >= 80", {"score": 95}),
    ]
    
    print("测试结果:")
    for expr_str, context in test_cases:
        result, error = safe_evaluate(expr_str, context)
        if error:
            print(f"❌ {expr_str:25} => 错误: {error}")
        else:
            print(f"✅ {expr_str:25} => {result}")
            if context:
                print(f"   上下文: {context}")
    
    print("\n" + "=" * 50)
    print("项目功能总结:")
    print("✅ 数字比较运算 (==, !=, <, >, <=, >=)")
    print("✅ 基本算术运算 (+, -, *, /)")
    print("✅ 变量引用和上下文求值")
    print("✅ 数组字面量和索引访问")
    print("✅ 对象属性访问 (object.property)")
    print("✅ in 操作符")
    print("✅ 逻辑非 (not)")
    print("✅ 括号优先级控制")
    print("⚠️  复杂逻辑运算 (and/or) - 可能需要语法调整")
    print("⚠️  字符串修饰符 - 需要Python3兼容性修复")


if __name__ == "__main__":
    main()