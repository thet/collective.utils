# -*- coding: utf-8 -*-
from collective.sync.testing import COLLECTIVE_UTILS_INTEGRATION_TESTING
import unittest2 as unittest


class TestSetup(unittest.TestCase):
    layer = COLLECTIVE_UTILS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_true(self):
        """Dummy test.
        """
        self.assertTrue(True)
