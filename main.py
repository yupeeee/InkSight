import argparse
import matplotlib.pyplot as plt
import numpy as np

import utils

plt.rcParams.update({'font.size': 15})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", type=str, required=True, help="conference name")
    parser.add_argument("--y", type=int, required=True, help="conference year")
    args = parser.parse_args()

    data = getattr(utils, args.c).load_data(args)

    ids = data["id"]
    titles = data["title"]
    authors = data["authors"]

    count = len(ids)
    print(f"Number of papers accepted: {count}")

    # generate histogram (Paper ID)
    plt.hist(x=ids, bins=np.linspace(0, max(ids), 100), histtype="bar")
    plt.title(f"{args.c}-{args.y}")
    plt.xlabel("Paper ID")
    plt.ylabel("#Accepted Papers")
    plt.show()

    # generate wordcloud
    utils.generate_wordcloud(
        titles,
        width=1920,
        height=1080,
        max_words=1000,
        min_font_size=5,
        background_color="white",
    )
