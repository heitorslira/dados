from unittest import TestCase
from pathlib import Path
import csv
from src.ex1.ex1 import reconcile_accounts


class ReconciliarTest(TestCase):
    def setUp(self) -> None:
        path = Path(__file__).parent
        self.transactions1 = list(
            csv.reader(Path(path / "data" / "transactions1.csv").open())
        )
        self.transactions2 = list(
            csv.reader(Path(path / "data" / "transactions2.csv").open())
        )

        return super().setUp()

    def test_reconcile_accounts_return_two(self):
        out1, out2 = reconcile_accounts(self.transactions1, self.transactions2)
        self.assertIsNotNone(out1)
        self.assertIsNotNone(out2)

    def test_reconciliate_two_transactions(self):
        transaction1 = [["2024-10-10", "1", "2", "3", "4"]]
        transaction2 = [["2024-10-10", "1", "2", "3", "4"]]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")

    def test_reconciliate_two_transactions_missing(self):
        transaction1 = [["2024-10-10", "1", "2", "3", "4"]]
        transaction2 = [["2024-10-10", "1", "2", "3", "5"]]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "MISSING")
        self.assertEqual(out2[0][5], "MISSING")

    def test_reconciliate_can_handle_one_date_up_dif(self):
        transaction1 = [["2024-10-11", "1", "2", "3", "5"]]
        transaction2 = [["2024-10-10", "1", "2", "3", "5"]]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")

    def test_reconciliate_match_first_occurence(self):
        transaction1 = [["2024-10-11", "1", "2", "3", "5"]]
        transaction2 = [
            ["2024-10-10", "1", "2", "3", "5"],
            ["2024-10-11", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")
        self.assertEqual(out2[1][5], "MISSING")

    def test_reconciliate_match_two_occurances(self):
        transaction1 = [
            ["2024-10-11", "1", "2", "3", "5"],
            ["2024-10-11", "1", "2", "3", "5"],
        ]
        transaction2 = [
            ["2024-10-10", "1", "2", "3", "5"],
            ["2024-10-11", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out1[1][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")
        self.assertEqual(out2[1][5], "FOUND")

    def test_reconciliate_match_duplicate_transaction1(self):
        transaction1 = [
            ["2024-10-10", "1", "2", "3", "5"],
            ["2024-10-10", "1", "2", "3", "5"],
        ]
        transaction2 = [
            ["2024-10-10", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out1[1][5], "MISSING")
        self.assertEqual(out2[0][5], "FOUND")

    def test_reconciliate_match_duplicate_transaction2(self):
        transaction1 = [
            ["2024-10-10", "1", "2", "3", "5"],
        ]
        transaction2 = [
            ["2024-10-10", "1", "2", "3", "5"],
            ["2024-10-10", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")
        self.assertEqual(out2[1][5], "MISSING")

    def test_reconciliate_match_dif2(self):
        transaction1 = [
            ["2024-10-10", "1", "2", "3", "5"],
            ["2024-10-12", "1", "2", "3", "5"],
        ]
        transaction2 = [
            ["2024-10-11", "1", "2", "3", "5"],
            ["2024-10-11", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out1[1][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")
        self.assertEqual(out2[1][5], "FOUND")

    def test_reconciliate_match_dif_invertido(self):
        transaction1 = [
            ["2024-10-12", "1", "2", "3", "5"],
            ["2024-10-10", "1", "2", "3", "5"],
        ]
        transaction2 = [
            ["2024-10-11", "1", "2", "3", "5"],
            ["2024-10-11", "1", "2", "3", "5"],
        ]
        out1, out2 = reconcile_accounts(transaction1, transaction2)
        self.assertEqual(out1[0][5], "FOUND")
        self.assertEqual(out1[1][5], "FOUND")
        self.assertEqual(out2[0][5], "FOUND")
        self.assertEqual(out2[1][5], "FOUND")
