import unittest

from tests.unittest_fw_reference.home.login_test import LoginTests
from tests.unittest_fw_reference.welcome.welcome_test import WelcomeTest


login = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
welcome = unittest.TestLoader().loadTestsFromTestCase(WelcomeTest)

welcome_page_loaded_properly = unittest.TestSuite([login, welcome])

unittest.TextTestRunner(verbosity=2).run(welcome_page_loaded_properly)
