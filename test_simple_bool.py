# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: huxx <hzd0107@hotmail.com>

import unittest

from bool_parser import *


class TestEqualsOperator(unittest.TestCase):
    # number constant equals operator
    def test_constant_number(self):
        exp = BooleanExpression("5==5")
        result = exp.evaluate()
        self.assertTrue(result)

        exp = BooleanExpression("5==6")
        result = exp.evaluate()
        self.assertFalse(result)

        exp = BooleanExpression("5.2 == 5.2")
        result = exp.evaluate()
        self.assertTrue(result)

        exp = BooleanExpression("5==5.0")
        result = exp.evaluate()
        self.assertTrue(result)

        exp = BooleanExpression("5.4==6.1")
        result = exp.evaluate()
        self.assertFalse(result)

    def test_boolean_constant(self):
        exp = BooleanExpression("True==True")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("False==True")
        self.assertFalse(exp.evaluate())

        exp = BooleanExpression("False==False")
        self.assertTrue(exp.evaluate())

    def test_string_constant(self):
        exp = BooleanExpression("'asd'=='asd'")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression('"as\\"d"=="as\\"d"')
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("\"asd\"==\"dsa\"")
        self.assertFalse(exp.evaluate())

    def test_variables(self):
        exp = BooleanExpression("one==two")
        self.assertTrue(exp.evaluate(dict(one=1, two=1)))

        exp = BooleanExpression("one==1")
        self.assertTrue(exp.evaluate(dict(one=1, two=1)))

    def test_array_item(self):
        exp = BooleanExpression("one[1] == 2")
        self.assertTrue(exp.evaluate(dict(one=[1, 2], two=1)))

    def test_double_array_item(self):
        exp = BooleanExpression("one[1][0] == 2")
        self.assertTrue(exp.evaluate(dict(one=[1, [2]], two=1)))

    def test_dot_item(self):
        exp = BooleanExpression("one[1].part == 2")
        self.assertTrue(exp.evaluate(dict(one=[1, dict(part=2)], two=1)))
        # a[0] == 1


class TestBooleanOperators(unittest.TestCase):
    def test_and(self):
        exp = BooleanExpression("1 == 1 == True")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("False")
        self.assertFalse(exp.evaluate())


class TestInOperator(unittest.TestCase):
    def test_in(self):
        exp = BooleanExpression("1 in v")
        self.assertTrue(exp.evaluate(dict(v=[1, 2])))

        exp = BooleanExpression("3 in v")
        self.assertFalse(exp.evaluate(dict(v=[1, 2])))


class TestInStringOperator(unittest.TestCase):
    def test_in_string(self):
        exp = BooleanExpression("1 in [1,2]")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("1 in [1]")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("3 in [1,2]")
        self.assertFalse(exp.evaluate())

        exp = BooleanExpression("3 in []")
        self.assertFalse(exp.evaluate())


class TestArithmeticOperators(unittest.TestCase):
    def test_plus(self):
        exp = BooleanExpression("3 == 1 + 2")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("1 + 2 == 3")
        self.assertTrue(exp.evaluate())

    def test_minus(self):
        exp = BooleanExpression("1 == 2 - 1")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("1 - 2 == - 1")
        self.assertTrue(exp.evaluate())

    def test_plus_minus_variable(self):
        exp = BooleanExpression("3 == one + two")
        self.assertTrue(exp.evaluate(dict(one=1, two=2)))

        exp = BooleanExpression("-1 == one + two")
        self.assertTrue(exp.evaluate(dict(one=1, two=-2)))

    def test_mul(self):
        exp = BooleanExpression("2 == 1 * 2")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("2 * - 2 == - 4")
        self.assertTrue(exp.evaluate())

    def test_div(self):
        exp = BooleanExpression("1 == 2 / 2")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("2 / - 2 == - 1")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("2 / 4 == 0.5")
        print "2 / 4 == 0.5", exp.evaluate()
        self.assertTrue(exp.evaluate())


class TestNotOperator(unittest.TestCase):
    def test_not_false(self):
        exp = BooleanExpression("not False")
        self.assertTrue(exp.evaluate())

    def abort_test_not_exp(self):
        exp = BooleanExpression("False AND False")
        self.assertTrue(exp.evaluate())

    def test_not_exp(self):
        exp = BooleanExpression("not a and b")
        self.assertFalse(exp.evaluate(dict(a=True, b=True)))

    def test_not_equal_priority(self):
        exp = BooleanExpression("a == 5 and not b")
        self.assertTrue(exp.evaluate(dict(a=5, b=False)))

        exp = BooleanExpression("not b and a == 5")
        self.assertTrue(exp.evaluate(dict(a=5, b=False)))

        exp = BooleanExpression("not a == 3 + 3 and b")
        self.assertTrue(exp.evaluate(dict(a=5, b=True)))


class TestBracketsPriority(unittest.TestCase):
    def test_parentesis(self):
        exp = BooleanExpression("4 + 4 / 2 == 6")
        self.assertTrue(exp.evaluate())

        exp = BooleanExpression("( 4 + 4 ) / 2 ")
        self.assertTrue(exp.evaluate() == 4)

        exp = BooleanExpression("6")
        self.assertTrue(exp.evaluate() == 6)


class TestStringModifiers(unittest.TestCase):
    def test_lower(self):
        exp = BooleanExpression("mystr|lower")
        self.assertTrue(exp.evaluate({'mystr': "STR"}) == "str")

    def test_upper(self):
        exp = BooleanExpression("mystr|upper")
        self.assertTrue(exp.evaluate(dict(mystr="str")) == "STR")

    def test_split(self):
        exp = BooleanExpression("mystr|split(',')")
        result = exp.evaluate(dict(mystr="a,b,c,d"))
        self.assertListEqual(result, ['a', 'b', 'c', 'd'])

    def test_strip(self):
        exp = BooleanExpression("mystr|strip('a')")
        self.assertTrue(exp.evaluate(dict(mystr="abba")) == "bb")

        exp = BooleanExpression("mystr|strip()")
        self.assertTrue(exp.evaluate(dict(mystr=" bb   ")) == "bb")


if __name__ == '__main__':
    unittest.main()
