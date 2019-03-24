import unittest
from pprint import pprint
from dexstore import DexStore
from dexstorebase.operationids import getOperationNameForId
from dexstore.instance import set_shared_dexstore_instance
from .fixtures import fixture_data, dexstore


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    def test_finalizeOps_proposal(self):
        # proposal = dexstore.new_proposal(dexstore.tx())
        proposal = dexstore.proposal()
        dexstore.transfer("init1", 1, "DST", append_to=proposal)
        tx = dexstore.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_proposal2(self):
        proposal = dexstore.new_proposal()
        # proposal = dexstore.proposal()
        dexstore.transfer("init1", 1, "DST", append_to=proposal)
        tx = dexstore.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_combined_proposal(self):
        parent = dexstore.new_tx()
        proposal = dexstore.new_proposal(parent)
        dexstore.transfer("init1", 1, "DST", append_to=proposal)
        dexstore.transfer("init1", 1, "DST", append_to=parent)
        tx = parent.json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 2)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        self.assertEqual(
            getOperationNameForId(ops[1][0]),
            "transfer")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_changeproposer_new(self):
        proposal = dexstore.proposal(proposer="init5")
        dexstore.transfer("init1", 1, "DST", append_to=proposal)
        tx = dexstore.tx().json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.90747")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    """
    def test_finalizeOps_changeproposer_legacy(self):
        dexstore.proposer = "init5"
        tx = dexstore.transfer("init1", 1, "DST")
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.11")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")
    """

    def test_new_proposals(self):
        p1 = dexstore.new_proposal()
        p2 = dexstore.new_proposal()
        self.assertIsNotNone(id(p1), id(p2))

    def test_new_txs(self):
        p1 = dexstore.new_tx()
        p2 = dexstore.new_tx()
        self.assertIsNotNone(id(p1), id(p2))
