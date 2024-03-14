import argparse

import config
from utils import extract_table_from_pdf


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", type=str, required=True)
    args = parser.parse_args()

    table = extract_table_from_pdf(**getattr(config, args.conference))

    print(table)
