import unittest
from homework.Lab_5.hw3.block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):

    def test_error_is_ignored(self):
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)

    def test_error_is_propagated(self):
        err_types = {TypeError}
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(err_types):
                a = 1 / 0

    def test_inner_block_propagates_outer_ignores(self):
        outer_err_types = {TypeError}
        inner_err_types = {ZeroDivisionError}
        try:
            with BlockErrors(outer_err_types):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except:
            self.fail()

    def test_child_errors_are_ignored(self):
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'
        self.assertTrue(True)

    def test_no_error_occurs(self):
        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            a = 1 + 1
        self.assertEqual(a, 2)

    def test_multiple_error_types_ignored(self):
        err_types = {ZeroDivisionError, TypeError, ValueError}
        with BlockErrors(err_types):
            a = 1 / 0
        with BlockErrors(err_types):
            b = 1 + '0'
        with BlockErrors(err_types):
            c = int('abc')
        self.assertTrue(True)

    def test_unexpected_error_propagated(self):
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 + '0'

    def test_nested_blocks_different_errors(self):
        outer_errors = {ValueError}
        inner_errors = {ZeroDivisionError}
        try:
            with BlockErrors(outer_errors):
                with BlockErrors(inner_errors):
                    x = 1 / 0
                y = int('abc')
        except:
            self.fail()

    def test_empty_error_collection(self):
        err_types = set()
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(err_types):
                a = 1 / 0

    def test_exception_hierarchy(self):
        err_types = {ArithmeticError}
        with BlockErrors(err_types):
            a = 1 / 0
        with BlockErrors(err_types):
            b = 1 + 1j
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
