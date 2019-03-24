import time
import unittest
from dexstore import DexStore, exceptions
from dexstore.instance import set_shared_dexstore_instance
from dexstore.blockchainobject import ObjectCache


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dst = DexStore(
            nobroadcast=True,
        )
        set_shared_dexstore_instance(self.dst)

    def test_cache(self):
        cache = ObjectCache(default_expiration=1)
        self.assertEqual(str(cache), "ObjectCache(n=0, default_expiration=1)")

        # Data
        cache["foo"] = "bar"
        self.assertIn("foo", cache)
        self.assertEqual(cache["foo"], "bar")
        self.assertEqual(cache.get("foo", "New"), "bar")

        # Expiration
        time.sleep(2)
        self.assertNotIn("foo", cache)

        # Get
        self.assertEqual(cache.get("foo", "New"), "New")
