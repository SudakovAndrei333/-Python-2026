import unittest
from homework.Lab_5.hw2.remote_execution import app


class TestRemoteExecution(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_valid_code_execution(self):
        response = self.client.post('/run_code', data={
            'code': "print('Hello World')",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello World', response.get_data(as_text=True))

    def test_valid_code_with_calculation(self):
        response = self.client.post('/run_code', data={
            'code': "print(2 + 2)",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('4', response.get_data(as_text=True))

    def test_valid_code_with_semicolon(self):
        response = self.client.post('/run_code', data={
            'code': "import time; time.sleep(1); print('Done')",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Done', response.get_data(as_text=True))

    def test_timeout_less_than_execution_time(self):
        slow_code = "import time; time.sleep(10); print('Done')"
        response = self.client.post('/run_code', data={
            'code': slow_code,
            'timeout': '2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('timeout', response.get_data(as_text=True).lower())

    def test_timeout_exactly_30_seconds(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')",
            'timeout': '30'
        })
        self.assertEqual(response.status_code, 200)

    def test_timeout_exceeds_30_seconds(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')",
            'timeout': '31'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    def test_timeout_zero(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')",
            'timeout': '0'
        })
        self.assertEqual(response.status_code, 400)

    def test_timeout_negative(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')",
            'timeout': '-5'
        })
        self.assertEqual(response.status_code, 400)

    def test_code_required(self):
        response = self.client.post('/run_code', data={
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    def test_timeout_required(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')"
        })
        self.assertEqual(response.status_code, 400)

    def test_code_empty_string(self):
        response = self.client.post('/run_code', data={
            'code': '',
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)

    def test_unsafe_input_pipe(self):
        response = self.client.post('/run_code', data={
            'code': "print() | cat /etc/passwd",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Небезопасные символы', response.get_data(as_text=True))

    def test_unsafe_input_ampersand(self):
        response = self.client.post('/run_code', data={
            'code': "print() & rm -rf /",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)

    def test_unsafe_input_backticks(self):
        response = self.client.post('/run_code', data={
            'code': "print(`whoami`)",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)

    def test_unsafe_input_dollar(self):
        response = self.client.post('/run_code', data={
            'code': "print($HOME)",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)

    def test_unsafe_input_newline(self):
        response = self.client.post('/run_code', data={
            'code': "print()\nimport os",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 400)

    def test_fool_protection_invalid_timeout_type(self):
        response = self.client.post('/run_code', data={
            'code': "print('OK')",
            'timeout': 'not-a-number'
        })
        self.assertEqual(response.status_code, 400)

    def test_fool_protection_empty_data(self):
        response = self.client.post('/run_code', data={})
        self.assertEqual(response.status_code, 400)

    def test_code_with_syntax_error(self):
        response = self.client.post('/run_code', data={
            'code': "print(invalid_syntax",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', response.get_data(as_text=True))

    def test_code_no_output(self):
        response = self.client.post('/run_code', data={
            'code': "x = 1 + 1",
            'timeout': '5'
        })
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)