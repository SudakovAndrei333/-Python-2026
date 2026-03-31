import unittest
from homework.Lab_3.hw2.decrypt import decrypt


class TestDecryptBase(unittest.TestCase):
    def assert_decrypts_to(self, encrypted: str, expected: str):
        result = decrypt(encrypted)
        self.assertEqual(
            result, expected,
            f'"{encrypted}" → ожидалось "{expected}", получено "{result}"'
        )


class TestDecryptSingleDot(unittest.TestCase):
    def test_trailing_single_dot(self):
        self.assertEqual(decrypt('абра-кадабра.'), 'абра-кадабра')

    def test_single_dot_only(self):
        self.assertEqual(decrypt('.'), '')

    def test_single_dot_in_middle(self):
        cases = [
            ('а.бра', 'абра'),
            ('1.2.3', '123'),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)


class TestDecryptDoubleDot(unittest.TestCase):
    def test_double_dot_removes_char(self):
        cases = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('1..2.3', '23'),
            ('ab..c', 'ac'),
            ('x..', ''),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot_on_empty(self):
        cases = [
            ('..', ''),
            ('....', ''),
            ('a......', ''),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)


class TestDecryptMixedDots(unittest.TestCase):
    def test_triple_dot(self):
        cases = [
            ('абрау...-кадабра', 'абра-кадабра'),
            ('abc...d', 'abd'),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_four_dots(self):
        cases = [
            ('абра--..кадабра', 'абра-кадабра'),
            ('abcd....', 'ab'),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_many_dots_empty_result(self):
        cases = [
            ('абра........', ''),
            ('1.......................', ''),
        ]
        for encrypted, expected in cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_dots_with_letter_at_end(self):
        self.assertEqual(decrypt('абр......a.'), 'a')

class TestDecryptAllTaskExamples(unittest.TestCase):
    def test_all_examples_from_task(self):
        examples = [
            ('абра-кадабра.', 'абра-кадабра'),
            ('абраа..-кадабра', 'абра-кадабра'),
            (' абраа..-.кадабра', ' абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', ''),
        ]
        for encrypted, expected in examples:
            with self.subTest(encrypted=encrypted, expected=expected):
                result = decrypt(encrypted)
                self.assertEqual(
                    result, expected,
                    f'Failed: "{encrypted}" > expected "{expected}", got "{result}"'
                )


if __name__ == '__main__':
    unittest.main(verbosity=2)