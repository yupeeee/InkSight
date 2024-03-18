from typing import (
    Dict,
    List,
)

import nltk
import matplotlib.pyplot as plt
from multidict import MultiDict
from wordcloud import WordCloud

__all__ = [
    "generate_wordcloud",
]

nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("stopwords")
stopwords_list = nltk.corpus.stopwords.words("english")
stopwords_list += "-|&|:|vs".split("|")


def generate_frequency_dict(titles: List[str], ) -> Dict[str, int]:
    titles_joined = " ".join(" ".join(titles).split("."))
    fullTermsDict = MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for text in titles_joined.split(" "):
        if text in stopwords_list:
            continue

        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1

    for key in tmpDict:
        # noun check
        token = nltk.tokenize.word_tokenize(key)
        
        for i in nltk.pos_tag(token):
            if i[1].startswith("NN"):
                fullTermsDict.add(key, tmpDict[key])

    return fullTermsDict


def generate_wordcloud(
    titles: List[str],
    **kwargs,
) -> None:
    wc = WordCloud(
        **kwargs,
    )

    # generate word cloud
    wc.generate_from_frequencies(generate_frequency_dict(titles))

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
