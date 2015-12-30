# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013, 2015 ppzuche Inc.
# Author: huxx <hzd0107@hotmail.com>
from __future__ import division

import operator

from pyparsing import *

operator_map = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '-': operator.sub,
    '+': operator.add,
    '*': operator.mul,
    '/': lambda a, b: a / b,
    '%': operator.mod,
    'and': operator.and_,
    'or': operator.or_,
    'AND': operator.and_,
    'OR': operator.or_,
    'in': lambda a, b: a in b
}


def convert_boolean(s, l, tokens):
    """
    parse action for bool constant, convert first token into boolean value
    :param tokens:
    :return: True or False
    :rtype: bool
    """
    if tokens[0] == 'True':
        return True
    elif tokens[0] == 'False':
        return False


def convert_expression(s, l, t):
    """
    convert expression into Operator instance or single expression
    :param t: expression, for example: (1,'<',2)
    :type t: list or tuple
    :return: Operator instance or a single value
    """
    if len(t) == 1:
        return t[0]
    elif len(t) == 3:
        return Operator(t[1], t[0], t[2])
    else:
        raise Exception(t)


def convert_not_expression(s, l, t):
    """
    not expression converter
    :param t:
    :return:
    """
    if len(t) == 1:
        return t
    if len(t) == 2 and t[0].lower() == 'not':
        return NotOperator(t[1])
    else:
        raise Exception()


def convert_upper_lower(s, l, tokens):
    """
    parse action for 'upper' and 'lower'
    :param s: useless
    :param l: useless
    :param tokens: list or tuple
    :return:
    """
    if len(tokens) == 2 and isinstance(tokens[1], basestring):
        if tokens[1].lower() == 'upper':
            return UpperModificator(tokens[0])
        elif tokens[1].lower() == 'lower':
            return LowerModificator(tokens[0])
    else:
        raise Exception(tokens)


def convert_split_strip(s, l, tokens):
    """
    parse action for 'split' and 'strip'
    :param s:
    :param l:
    :param tokens:
    :return:
    """
    if not len(tokens) in [2, 3]:
        raise Exception(tokens)
    arg = ' '
    if len(tokens) == 3:
        arg = tokens[2]
    if tokens[1] == 'split':
        return SplitModificator(tokens[0], arg)
    elif tokens[1] == 'strip':
        return StripModificator(tokens[0], arg)


class BaseUnit(object):
    """
    base class
    """

    def get_value(self, context):
        pass


class Constant(BaseUnit):
    def __init__(self, constant):
        self.constant = constant

    def get_value(self, context):
        return self.constant


class Variable(BaseUnit):
    """
    parse action for variable
    """

    def __init__(self, tokens):
        self.parts = tokens

    def get_value(self, context):
        result = context
        for part in self.parts:
            result = result[part]
        return result


class Array(BaseUnit):
    """
    parse action for array
    """

    def __init__(self, tokens):
        self.parts = tokens

    def get_value(self, context):
        result = []
        for part in self.parts:
            result.append(part.get_value(context))
        return result


class SplitModificator(BaseUnit):
    def __init__(self, value, argument):
        self.value = value
        self.argument = argument

    def get_value(self, context):
        string = self.value.get_value(context)
        if isinstance(string, (str, unicode)) and isinstance(self.argument, (str, unicode)):
            return string.split(self.argument)
        else:
            raise ValueError('value and arguments for split must be strings!')


class StripModificator(BaseUnit):
    def __init__(self, value, argument):
        self.value = value
        self.argument = argument

    def get_value(self, context):
        string = self.value.get_value(context)
        if isinstance(string, (str, unicode)) and isinstance(self.argument, (str, unicode)):
            return string.strip(self.argument)
        else:
            raise ValueError('value and arguments for strip must be strings!')


class UpperModificator(BaseUnit):
    def __init__(self, value):
        self.value = value

    def get_value(self, context):
        string = self.value.get_value(context)
        if isinstance(string, basestring):
            return string.upper()
        else:
            raise ValueError('value must be strings!')


class LowerModificator(BaseUnit):
    def __init__(self, value):
        self.value = value

    def get_value(self, context):
        string = self.value.get_value(context)
        if isinstance(string, basestring):
            return string.lower()
        else:
            raise ValueError('value must be strings!')


class NotOperator(BaseUnit):
    """
    operator for 'not'
    """

    def __init__(self, operand):
        """

        :param operand:
        :return:
        """
        self.operand = operand

    def get_value(self, context):
        """

        :param context:
        :return:
        """
        return not self.operand.get_value(context)


class Operator(BaseUnit):
    def __init__(self, op, left, right):
        """
        binary operators and evaluation
        :param op: operator ,such as '+','-','>' etc.
        :type op: str
        :param left: single value or Operator instance
        :param right:
        :return:
        """
        self.left = left
        self.right = right
        self.operator = op

    def get_value(self, context):
        left_value = self.left.get_value(context)
        right_value = self.right.get_value(context)
        if self.operator in ('+', '-', '*', '/', '%'):
            if not isinstance(left_value, (int, float)) or not isinstance(right_value, (int, float)):
                raise ValueError('both arguments for %s must be numeric' % self.operator)
        if self.operator not in operator_map:
            raise ValueError('unsupported operator: %s' % self.operator)
        operator_func = operator_map.get(self.operator)
        return operator_func(left_value, right_value)


class Grammar(object):
    # number constants
    plus_minus = Literal('+') | Literal('-')
    point = Literal('.')
    dot = Literal('.').suppress()
    bar = Literal('|').suppress()
    comma = Literal(',').suppress()
    l_array = Literal('[').suppress()
    r_array = Literal(']').suppress()
    l_bracket = Literal('(').suppress()
    r_bracket = Literal(')').suppress()

    string_lower = Literal('lower')
    string_upper = Literal('upper')
    string_split = Literal('split')
    string_strip = Literal('strip')

    integer = Optional(plus_minus) + Word(nums)
    integer.setParseAction(lambda s, l, t: int(''.join(t)))

    floatnumber = Combine(integer + point + Word(nums))
    floatnumber.setParseAction(lambda s, l, t: float(t[0]))

    number = floatnumber | integer

    # boolean constants
    boolean = Literal('True') | Literal('False')
    boolean.setParseAction(convert_boolean)

    # string constants
    string = dblQuotedString | quotedString
    string.setParseAction(removeQuotes)

    array_of_numbers = Literal('[')
    array_of_strings = Literal('[')

    constant = number | boolean | string
    constant.setParseAction(lambda s, l, t: Constant(t[0]))

    # array
    empty_array = l_array + r_array
    array = empty_array | (l_array + OneOrMore(constant + ZeroOrMore(comma)) + r_array)
    array.setParseAction(lambda s, l, t: Array(t))

    # variable name
    name = Word(alphas + "_", alphanums + "_")

    # array_access
    array_access = name + OneOrMore(
        l_array + integer + r_array)

    # variable atom TODO: find better expression
    variable_atom = array_access | name

    variable = variable_atom + ZeroOrMore(
        dot + variable_atom)
    variable.leaveWhitespace()
    variable.setParseAction(lambda s, l, t: Variable(t))

    upper_lower_exp = (string | variable) + bar + (string_lower | string_upper)
    upper_lower_exp.addParseAction(convert_upper_lower)

    split_strip_exp = (string | variable) + bar + (string_split | string_strip) + l_bracket + Optional(
        string) + r_bracket
    split_strip_exp.addParseAction(convert_split_strip)

    operand = split_strip_exp | upper_lower_exp | constant | variable | array

    prio_expression = Forward()
    atom_expression = operand | prio_expression

    operator = oneOf("* /")
    muldiv_exp = Forward()
    muldiv_exp << atom_expression + Optional(operator + muldiv_exp)
    muldiv_exp.addParseAction(convert_expression)

    operator = oneOf("+ -")
    addsub_exp = Forward()
    addsub_exp << muldiv_exp + Optional(operator + addsub_exp)
    addsub_exp.addParseAction(convert_expression)

    operator = oneOf("!= == < > <= >= in")
    comparsion_exp = Forward()
    comparsion_exp << addsub_exp + Optional(operator + comparsion_exp)
    comparsion_exp.addParseAction(convert_expression)

    operator = oneOf("not NOT")
    not_exp = Forward()
    not_exp << Optional(operator) + comparsion_exp
    not_exp.addParseAction(convert_not_expression)

    operator = oneOf("and or AND OR")
    expression = Forward()
    expression << not_exp + Optional(operator + expression)

    prio_expression << l_bracket + expression + r_bracket
    prio_expression.addParseAction(convert_expression)

    final_expression = expression | prio_expression + StringEnd()

    def parse(self, expr):
        result = self.final_expression.parseString(expr)
        return result[0]


class BooleanExpression(object):
    grammar = Grammar()  # grammar for logic expression

    def __init__(self, exp):
        """

        :param exp:
        :type exp: str
        :return:
        """
        self.expression = exp
        self.expression_root = self.grammar.parse(self.expression)
        self.context = {}

    def evaluate(self, context=None):
        if not context:
            context = {}
        value = self.expression_root.get_value(context)
        return value
