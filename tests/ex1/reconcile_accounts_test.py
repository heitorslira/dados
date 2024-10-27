from unittest import TestCase
from pathlib import Path
import csv
from src.ex1.ex1 import reconcile_accounts

class ReconciliarTest(TestCase):
    
    def setUp(self) -> None:
        path = Path(__file__).parent
        self.transactions1 = list(csv.reader(Path(path / "data" / "transactions1.csv").open()))
        self.transactions2 = list(csv.reader(Path(path / "data" / "transactions2.csv").open()))

        return super().setUp()
    
    def test_reconcile_accounts(self):
        
        out1, out2 = reconcile_accounts(self.transactions1, self.transactions2)
        
        self.assertTrue(True)