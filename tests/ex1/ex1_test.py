import csv
from pathlib import Path
from unittest import TestCase
from src.ex1.ex1 import reconcile_accounts


class ReconciliateTest(TestCase):
    def settup(self):
        path = Path(__file__).parent.parent.parent / "src" / "ex1" / 'data'
        self.transactions1 = list(csv.reader(Path(path / "data" / "transactions1.csv").open()))
        self.transactions2 = list(csv.reader(Path(path / "data" / "transactions2.csv").open()))
        
        
    def test_return_unstack(self):
        out1,out2 = reconcile_accounts(self.transactions1, self.transactions2)
        
        