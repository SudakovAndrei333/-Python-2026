import unittest
from freezegun import freeze_time
from homework.Lab_3.hw1.hello_word_with_name import app

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()
        self.name = 'Тест'
        self.base_url_path = '/hello-world/'

    @freeze_time('2026-03-23')  # понедельник
    def test_monday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошего понедельника!', response.data.decode())

    @freeze_time('2026-03-24')  # вторник
    def test_tuesday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошего вторника!', response.data.decode())

    @freeze_time('2026-03-25')  # среда
    def test_wednesday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошей среды!', response.data.decode())

    @freeze_time('2026-03-26')  # четверг
    def test_thursday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошего четверга!', response.data.decode())

    @freeze_time('2026-03-27')  # пятница
    def test_friday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошей пятницы!', response.data.decode())

    @freeze_time('2026-03-28')  # суббота
    def test_saturday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошей субботы!', response.data.decode())

    @freeze_time('2026-03-29')  # воскресенье
    def test_sunday(self):
        response = self.client.get(self.base_url_path + self.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Тест. Хорошего воскресенья!', response.data.decode())

    @freeze_time('2026-03-25')  # среда
    def test_any_name(self):
        name = 'Анна'
        response = self.client.get(self.base_url_path + name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Привет, {name}. Хорошей среды!', response.data.decode())

    @freeze_time('2026-03-25')  # среда
    def test_username_contains_wish(self):
        name = 'Хорошей среды'
        response = self.client.get(f'/hello-world/{name}')
        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn(f'Привет, {name}. Хорошей среды!', response.data.decode())

if __name__ == '__main__':
    unittest.main()