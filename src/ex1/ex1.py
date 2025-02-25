import datetime as dt
from collections import defaultdict
from typing import List

TDataType = List[List[str]]
LAGS = 1


def reconcile_accounts(transaction1: TDataType, transaction2: TDataType) -> TDataType:
    hash_map2 = defaultdict(lambda: [])

    for idx2, row2 in enumerate(transaction2):
        key = "-".join(row2[1:])
        hash_map2[key].append(idx2)

    matched_indexes = {}

    for idx1, row1 in enumerate(transaction1):
        key = "-".join(row1[1:])
        if key in hash_map2:
            for tr2_index in hash_map2[key]:
                date_tr1 = dt.datetime.strptime(row1[0], "%Y-%m-%d")
                dates_tr2 = [
                    dt.datetime.strptime(transaction2[tr2_index][0], "%Y-%m-%d")
                    + dt.timedelta(lag)
                    for lag in range(-LAGS, LAGS + 1)
                ]

                for date_tr2 in dates_tr2:
                    if (
                        date_tr1 == date_tr2
                        and tr2_index not in matched_indexes.values()
                    ):
                        prev_match = matched_indexes.get(idx1)
                        if prev_match is not None:
                            prev_found_date = dt.datetime.strptime(
                                transaction2[prev_match][0], "%Y-%m-%d"
                            )
                            if prev_found_date <= date_tr1:
                                continue

                        matched_indexes[idx1] = tr2_index
                        # found_tr1_indexes.add(idx1)
                        # found_tr2_indexes.add(tr2_index)
                        break

    for idx, row in enumerate(transaction1):
        if idx in matched_indexes.keys():
            row.append("FOUND")
        else:
            row.append("MISSING")

    for idx, row in enumerate(transaction2):
        if idx in matched_indexes.values():
            row.append("FOUND")
        else:
            row.append("MISSING")

    return transaction1, transaction2


def main():
    from pprint import pprint
    from pathlib import Path
    import csv
    
    path = Path(__file__).parent
    transactions1 = list(csv.reader(Path(path / "data" / "transactions1.csv").open()))
    transactions2 = list(csv.reader(Path(path / "data" / "transactions2.csv").open()))
    out1, out2 = reconcile_accounts(transactions1, transactions2)
    
    pprint(out1)
    print()
    pprint(out2)
    
if __name__ == "__main__":
    main()
    