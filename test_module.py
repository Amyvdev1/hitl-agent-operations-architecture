import unittest
from dataclasses import replace
from module import Approval, authorize, digest
class ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.args = dict(tenant="tenant-demo", task="task-demo", revision=1, arguments={"action":"preview"}, now=100, state="PENDING_APPROVAL")
        self.approval = Approval("tenant-demo", "task-demo", 1, digest(self.args["arguments"]), 200)
    def test_authorized(self):
        self.assertEqual(authorize(self.approval, **self.args), "APPROVED")
    def test_scope_and_mutation_fail_closed(self):
        for change in ({"tenant":"other"}, {"task":"other"}, {"revision":2}, {"arguments":{"action":"send"}}, {"now":200}, {"state":"APPROVED"}):
            with self.subTest(change=change), self.assertRaises(ValueError): authorize(self.approval, **{**self.args, **change})
    def test_machine_or_rejected_approval_denied(self):
        for change in ({"role":"agent"}, {"status":"REJECTED"}):
            with self.subTest(change=change), self.assertRaises(ValueError): authorize(replace(self.approval, **change), **self.args)
    def test_nonfinite_arguments_rejected(self):
        with self.assertRaises(ValueError): digest({"amount":float("nan")})
if __name__ == "__main__": unittest.main()
