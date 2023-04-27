import pytest

def run_tests():
    pytest.main(['test-home-page.py', 'test-login.py', 'test-navbar.py', 'test-register.py'])


if __name__ == '__main__':
    run_tests()
