import unittest
from datetime import datetime
from unittest.mock import patch
from homework.Lab_3.hw4.person import Person


class TestPersonInit(unittest.TestCase):
    def test_init_with_required_args(self):
        p = Person('Анна', 1990)
        self.assertEqual(p.name, 'Анна')
        self.assertEqual(p.yob, 1990)
        self.assertEqual(p.address, '')

    def test_init_with_all_args(self):
        p = Person('Борис', 1985, 'г. Москва, ул. Ленина, 10')
        self.assertEqual(p.name, 'Борис')
        self.assertEqual(p.yob, 1985)
        self.assertEqual(p.address, 'г. Москва, ул. Ленина, 10')


class TestPersonGetAge(unittest.TestCase):
    @patch('Lab_3.hw4.person.datetime.datetime')
    def test_get_age_calculation(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 6, 15)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        p = Person('Тест', 2000)
        self.assertEqual(p.get_age(), 24)  # 2024 - 2000

    @patch('Lab_3.hw4.person.datetime.datetime')
    def test_get_age_newborn(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        p = Person('Младенец', 2024)
        self.assertEqual(p.get_age(), 0)

    @patch('Lab_3.hw4.person.datetime.datetime')
    def test_get_age_future_birth_raises_no_error(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        p = Person('Из будущего', 2030)
        self.assertEqual(p.get_age(), -6)


class TestPersonGetName(unittest.TestCase):

    def test_get_name_returns_correct_value(self):
        p = Person('Дмитрий', 1978)
        self.assertEqual(p.get_name(), 'Дмитрий')

    def test_get_name_after_set_name(self):
        p = Person('Старое', 1990)
        p.set_name('Новое')
        self.assertEqual(p.get_name(), 'Новое')

    def test_get_name_with_unicode(self):
        p = Person('🎉 Праздник 🎊', 2000)
        self.assertEqual(p.get_name(), '🎉 Праздник 🎊')


class TestPersonSetName(unittest.TestCase):

    def test_set_name_changes_value(self):
        p = Person('Иван', 1980)
        p.set_name('Пётр')
        self.assertEqual(p.name, 'Пётр')
        self.assertEqual(p.get_name(), 'Пётр')

    def test_set_name_accepts_empty_string(self):
        p = Person('Непустое', 1995)
        p.set_name('')
        self.assertEqual(p.name, '')

    def test_set_name_idempotent(self):
        p = Person('A', 2000)
        p.set_name('B')
        p.set_name('C')
        p.set_name('D')
        self.assertEqual(p.get_name(), 'D')


class TestPersonGetAddress(unittest.TestCase):
    def test_get_address_default_empty(self):
        p = Person('Тест', 2000)
        self.assertEqual(p.get_address(), '')

    def test_get_address_returns_set_value(self):
        p = Person('Тест', 2000, 'ул. Примерная, 1')
        self.assertEqual(p.get_address(), 'ул. Примерная, 1')

    def test_get_address_after_set_address(self):
        p = Person('Тест', 2000)
        p.set_address('Новый адрес')
        self.assertEqual(p.get_address(), 'Новый адрес')


class TestPersonSetAddress(unittest.TestCase):
    def test_set_address_changes_value(self):
        p = Person('Тест', 2000, 'Старый адрес')
        p.set_address('Новый адрес')
        self.assertEqual(p.address, 'Новый адрес')

    def test_set_address_can_clear(self):
        p = Person('Тест', 2000, 'Был адрес')
        p.set_address('')
        self.assertEqual(p.address, '')

    def test_set_address_with_special_chars(self):
        addr = 'г. Санкт-Петербург, пр. Невский, д. 28, кв. 15'
        p = Person('Тест', 2000)
        p.set_address(addr)
        self.assertEqual(p.get_address(), addr)


class TestPersonIsHomeless(unittest.TestCase):
    def test_is_homeless_when_address_empty(self):
        p = Person('Бездомный', 1990, '')
        self.assertTrue(p.is_homeless())

    def test_is_homeless_when_address_not_set(self):
        p = Person('Без адреса', 1985)
        self.assertTrue(p.is_homeless())

    def test_is_homeless_false_when_address_set(self):
        p = Person('Домосед', 2000, 'Дом, милый дом')
        self.assertFalse(p.is_homeless())

    def test_is_homeless_after_clearing_address(self):
        p = Person('Тест', 2000, 'Есть адрес')
        self.assertFalse(p.is_homeless())
        p.set_address('')
        self.assertTrue(p.is_homeless())


class TestPersonIntegration(unittest.TestCase):
    @patch('Lab_3.hw4.person.datetime.datetime')
    def test_full_workflow(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        p = Person('Алексей', 1992, 'г. Казань')
        self.assertEqual(p.get_age(), 32)
        self.assertFalse(p.is_homeless())

        p.set_name('Алекс')
        p.set_address('')

        self.assertEqual(p.get_name(), 'Алекс')
        self.assertTrue(p.is_homeless())
        self.assertEqual(p.get_age(), 32)


if __name__ == '__main__':
    unittest.main(verbosity=2)
