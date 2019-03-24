# -*- coding: utf-8 -*-
import unittest
from dexstore import DexStore
from dexstore.asset import Asset
from dexstore.instance import set_shared_dexstore_instance, SharedInstance
from dexstore.blockchainobject import BlockchainObject

import logging

log = logging.getLogger()


class Testcases(unittest.TestCase):
    def test_dst1dst2(self):
        b1 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)

        b2 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        b1 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)
        set_shared_dexstore_instance(b1)
        test = Asset("1.3.0", blockchain_instance=b1)
        # Needed to clear cache
        test.refresh()

        b2 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)
        set_shared_dexstore_instance(b2)
        dst = Asset("1.3.0", blockchain_instance=b2)
        # Needed to clear cache
        dst.refresh()

        self.assertEqual(test["symbol"], "TEST")
        self.assertEqual(dst["symbol"], "DST")
        
    def test_default_connection2(self):
        b1 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)
        test = Asset("1.3.0", blockchain_instance=b1)
        test.refresh()

        b2 = DexStore("ws://127.0.0.1:7738", nobroadcast=True)
        dst = Asset("1.3.0", blockchain_instance=b2)
        dst.refresh()

        self.assertEqual(test["symbol"], "TEST")
        self.assertEqual(dst["symbol"], "DST")
