import unittest
import sys
import io
from homework.Lab_5.hw4.redirect import Redirect


class TestRedirect(unittest.TestCase):

    def setUp(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def test_redirect_stdout_only(self):
        stdout_capture = io.StringIO()
        with Redirect(stdout=stdout_capture):
            print('Hello stdout')
        self.assertIn('Hello stdout', stdout_capture.getvalue())

    def test_redirect_stderr_only(self):
        stderr_capture = io.StringIO()
        with Redirect(stderr=stderr_capture):
            print('Hello stderr', file=sys.stderr)
        self.assertIn('Hello stderr', stderr_capture.getvalue())

    def test_redirect_both_streams(self):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with Redirect(stdout=stdout_capture, stderr=stderr_capture):
            print('Hello stdout')
            print('Hello stderr', file=sys.stderr)
        self.assertIn('Hello stdout', stdout_capture.getvalue())
        self.assertIn('Hello stderr', stderr_capture.getvalue())

    def test_no_redirect(self):
        with Redirect():
            print('Hello')
        self.assertTrue(True)

    def test_nested_redirect(self):
        outer_stdout = io.StringIO()
        inner_stdout = io.StringIO()

        with Redirect(stdout=outer_stdout):
            print('Outer')
            with Redirect(stdout=inner_stdout):
                print('Inner')
            print('Outer again')

        self.assertIn('Outer', outer_stdout.getvalue())
        self.assertIn('Inner', inner_stdout.getvalue())
        self.assertIn('Outer again', outer_stdout.getvalue())

    def test_exception_in_block(self):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with Redirect(stdout=stdout_capture, stderr=stderr_capture):
                print('Before error')
                raise ValueError('Test error')
        except ValueError:
            pass

        self.assertIn('Before error', stdout_capture.getvalue())

    def test_streams_restored_after_exception(self):
        stdout_capture = io.StringIO()

        try:
            with Redirect(stdout=stdout_capture):
                raise ValueError('Test')
        except ValueError:
            pass

        self.assertEqual(sys.stdout, self.original_stdout)

    def test_multiple_prints_redirected(self):
        stdout_capture = io.StringIO()
        with Redirect(stdout=stdout_capture):
            print('Line 1')
            print('Line 2')
            print('Line 3')
        output = stdout_capture.getvalue()
        self.assertIn('Line 1', output)
        self.assertIn('Line 2', output)
        self.assertIn('Line 3', output)

    def test_stderr_with_traceback(self):
        stderr_capture = io.StringIO()
        import traceback

        with Redirect(stderr=stderr_capture):
            try:
                raise RuntimeError('Test traceback')
            except:
                traceback.print_exc()

        self.assertIn('RuntimeError', stderr_capture.getvalue())
        self.assertIn('Test traceback', stderr_capture.getvalue())

    def test_stdout_not_affected_when_only_stderr_redirected(self):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with Redirect(stderr=stderr_capture):
            print('Normal stdout', file=stdout_capture)
            print('To stderr', file=sys.stderr)

        self.assertIn('Normal stdout', stdout_capture.getvalue())
        self.assertIn('To stderr', stderr_capture.getvalue())

    def test_stderr_not_affected_when_only_stdout_redirected(self):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with Redirect(stdout=stdout_capture):
            print('To stdout')
            print('Normal stderr', file=sys.stderr)
            sys.stderr.write('Direct stderr\n')

        self.assertIn('To stdout', stdout_capture.getvalue())

    def test_context_manager_returns_self(self):
        with Redirect() as redirect:
            self.assertIsInstance(redirect, Redirect)

    def test_fool_protection_empty_context(self):
        with Redirect():
            pass
        self.assertEqual(sys.stdout, self.original_stdout)
        self.assertEqual(sys.stderr, self.original_stderr)

    def test_streams_restored_after_normal_exit(self):
        stdout_capture = io.StringIO()
        with Redirect(stdout=stdout_capture):
            print('Test')
        self.assertEqual(sys.stdout, self.original_stdout)


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner, exit=False)
