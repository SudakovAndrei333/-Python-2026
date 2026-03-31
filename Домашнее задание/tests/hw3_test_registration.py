import unittest
from homework.Lab_4.hw1_3.hw1_registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_email_valid(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered', response.get_data(as_text=True))

    def test_email_invalid_format(self):
        response = self.client.post('/registration', data={
            'email': 'invalid-email',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    def test_email_required(self):
        response = self.client.post('/registration', data={
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)

    def test_phone_valid(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)

    def test_phone_invalid_length(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '123',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)

    def test_phone_required(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)

    def test_name_valid(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test User',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)

    def test_name_required(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)

    def test_address_valid(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': '123 Main St',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)

    def test_address_required(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 400)

    def test_index_valid(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)

    def test_index_required(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address'
        })
        self.assertEqual(response.status_code, 400)

    def test_index_invalid_type(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': 'abc'
        })
        self.assertEqual(response.status_code, 400)

    def test_comment_optional(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456'
        })
        self.assertEqual(response.status_code, 200)

    def test_comment_with_value(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Test',
            'address': 'Test Address',
            'index': '123456',
            'comment': 'Some comment'
        })
        self.assertEqual(response.status_code, 200)

    def test_fool_protection_empty_data(self):
        response = self.client.post('/registration', data={})
        self.assertEqual(response.status_code, 400)

    def test_fool_protection_invalid_types(self):
        response = self.client.post('/registration', data={
            'email': 12345,
            'phone': 'not-a-number',
            'name': '',
            'address': '',
            'index': 'not-a-number'
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
