from argparse import Namespace
import pandas as pd
import requests

__all__ = [
    "load_data",
]

url = "https://iclr.cc/static/virtual/data/iclr-{year}-orals-posters.json"


def load_data(
    args: Namespace,
) -> pd.DataFrame:
    assert args.c == "iclr"

    response = requests.get(url.format(year=args.y))
    response.raise_for_status()

    data_dict = response.json()["results"]
    data_dict = pd.DataFrame(data_dict).to_dict()

    data_df = {
        "id": [],
        "title": [],
        "authors": [],
    }

    for id, title, authors in zip(
        data_dict["id"].values(),
        data_dict["name"].values(),
        data_dict["authors"].values(),
    ):
        data_df["id"].append(int(id))
        data_df["title"].append(str(title))
        data_df["authors"].append(
            ", ".join([author["fullname"] for author in authors]))

    data_df = pd.DataFrame(data_df)

    return data_df
