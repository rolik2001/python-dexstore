import mock
import string
import unittest
import random
from pprint import pprint
from dexstore import DexStore
from dexstorebase.operationids import getOperationNameForId
from dexstore.amount import Amount
from dexstorebase.account import PrivateKey
from dexstore.instance import set_shared_dexstore_instance
from .fixtures import fixture_data, dexstore


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    def test_connect(self):
        dexstore.connect()

    def test_set_default_account(self):
        dexstore.set_default_account("init0")

    def test_info(self):
        info = dexstore.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'next_maintenance_time',
                    'recently_missed_count',
                    'time']:
            self.assertTrue(key in info)

    def test_finalizeOps(self):
        tx1 = dexstore.new_tx()
        tx2 = dexstore.new_tx()
        dexstore.transfer("init1", 1, "DST", append_to=tx1)
        dexstore.transfer("init1", 2, "DST", append_to=tx2)
        dexstore.transfer("init1", 3, "DST", append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    def test_transfer(self):
        tx = dexstore.transfer(
            "1.2.101", 1.33, "DST", memo="Foobar", account="init0")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "transfer"
        )
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertEqual(op["from"], "1.2.100")
        self.assertEqual(op["to"], "1.2.101")
        amount = Amount(op["amount"])
        self.assertEqual(float(amount), 1.33)

    def test_create_account(self):
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        tx = dexstore.create_account(
            name,
            registrar="init0",   # 1.2.100
            referrer="init1",    # 1.2.101
            referrer_percent=33,
            owner_key=format(key1.pubkey, "DST"),
            active_key=format(key2.pubkey, "DST"),
            memo_key=format(key3.pubkey, "DST"),
            additional_owner_keys=[format(key4.pubkey, "DST")],
            additional_active_keys=[format(key4.pubkey, "DST")],
            additional_owner_accounts=["committee-account"],  # 1.2.0
            additional_active_accounts=["committee-account"],
            proxy_account="init0",
            storekeys=False
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            format(key4.pubkey, "DST"),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key4.pubkey, "DST"),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            format(key4.pubkey, "DST"),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key4.pubkey, "DST"),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["options"]["voting_account"],
            "1.2.100")
        self.assertEqual(
            op["registrar"],
            "1.2.100")
        self.assertEqual(
            op["referrer"],
            "1.2.101")
        self.assertEqual(
            op["referrer_percent"],
            33 * 100)

    def test_weight_threshold(self):

        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['DST7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 3}  # threshold fine
        dexstore._test_weights_treshold(auth)
        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['DST7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 4}  # too high

        with self.assertRaises(ValueError):
            dexstore._test_weights_treshold(auth)

    def test_allow(self):
        tx = dexstore.allow(
            "DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
            weight=1,
            threshold=1,
            permission="owner"
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn("owner", op)
        self.assertIn(
            ["DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n", '1'],
            op["owner"]["key_auths"])
        self.assertEqual(op["owner"]["weight_threshold"], 1)

    def test_disallow(self):
        with self.assertRaisesRegex(ValueError, ".*Changes nothing.*"):
            dexstore.disallow(
                "DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
                weight=1,
                threshold=1,
                permission="owner"
            )
        with self.assertRaisesRegex(ValueError, "Cannot have threshold of 0"):
            dexstore.disallow(
                "DST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
                weight=1,
                threshold=1,
                permission="owner"
            )
        dexstore.disallow(
            "DST5i8bEmtnN4fP4jAsBe17z9CCuQcHLkRyTuRZXYZeN2kVCL1sXa",
            weight=1,
            threshold=1,
            permission="active"
        )

    def test_update_memo_key(self):
        tx = dexstore.update_memo_key("DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertEqual(
            op["new_options"]["memo_key"],
            "DST55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")

    def test_approvewitness(self):
        tx = dexstore.approvewitness("1.6.1")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "1:0",
            op["new_options"]["votes"])

    def test_approvecommittee(self):
        tx = dexstore.approvecommittee("1.5.0")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "0:11",
            op["new_options"]["votes"])
