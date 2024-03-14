from typing import (
    List,
    Optional,
)

import camelot
import numpy as np
import pandas as pd

__all__ = [
    "extract_table_from_pdf",
]


def extract_table_from_pdf(
        pdf_path,
        pages: str = "all",
        flavor: Optional[str] = "lattice",
        remove_headers: Optional[int] = 0,
) -> pd.DataFrame:
    # detects wrong column split (== only last column is empty)
    def only_last_is_empty(str_list: List[str]) -> bool:
        for i, s in enumerate(str_list):
            if i < len(str_list) - 1:
                if len(s) > 0:
                    continue

                else:
                    return False

            if len(s) == 0:
                return True

            else:
                return False

    # read pdf
    pages = camelot.read_pdf(pdf_path, pages=pages, flavor=flavor)
    # print(f"Successfully read {pdf_path} ({len(pages)} pages).")

    # generate raw table
    raw_table = []

    for page in pages:
        df = page.df

        df = df.replace("\n", "")
        df = df.replace(np.NaN, "")

        raw_table += df.values.tolist()

    # parse
    table = [raw_table[0]]

    for i in range(1, len(raw_table)):
        row = raw_table[i]

        # skip redundant rows (e.g., page headers)
        if row in table:
            continue

        # skip rows with wrongly split columns
        if only_last_is_empty(row):
            # table.append(row)
            continue

        # merge multiple lines
        if "" in row:
            table[-1] = [" ".join([v1, v2]) for v1, v2 in zip(table[-1], row)]

        else:
            table.append(row)

    # remove redundant spaces (e.g., "Main Track " -> "Main Track")
    for i, row in enumerate(table):
        table[i] = [" ".join(v.split()) for v in row]

    table = table[remove_headers:]
    table = pd.DataFrame(table[1:], columns=table[0])

    return table
