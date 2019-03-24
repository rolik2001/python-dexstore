# -*- coding: utf-8 -*-
import unittest
from dexstore.blockchainobject import Object
from .fixtures import fixture_data, dexstore


class Testcases(unittest.TestCase):
    def setUp(self):
        fixture_data()

    def test_object(self):
        Object("2.1.0")
