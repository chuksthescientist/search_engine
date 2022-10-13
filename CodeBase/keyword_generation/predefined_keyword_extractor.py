import pandas as pd
from nltk.corpus import stopwords
from ahocorapy.keywordtree import KeywordTree


def get_fixed_tree(File='../data/master keywords list.csv'):
    mesh_keywords = []
    keywords = pd.read_csv(File, names=['keyword'])['keyword'].to_list()
    kwtree = KeywordTree(case_insensitive=True)
    for kw in keywords:
        kwtree.add(kw)
    kwtree.finalize()
    return kwtree


def get_predefined_keywords(kwtree, textblob):
    stop_words = set(stopwords.words('english'))
    if textblob:
        textblob = textblob.replace('-', ' ')
        results = kwtree.search_all(textblob)
        keywords = []
        for res in results:
            if res is not None and res[0] not in stop_words:
                keywords.append(res[0].lower())
        return list(set(keywords))
    else:
        return []


if __name__ == "__main__":
    textblob = """Mechanistic models for ion-exchange chromatography of proteins are well-established and a broad consensus exists on most aspects of the detailed mathematical and physical description. A variety of specializations of these models can typically capture the general locations of elution peaks, but discrepancies are often observed in peak position and shape, especially if the column load level is in the non-linear range. These discrepancies may prevent the use of models for high-fidelity predictive applications such as process characterization and development of high-purity and -productivity process steps. Our objective is to develop a sufficiently robust mechanistic framework to make both conventional and anomalous phenomena more readily predictable using model parameters that can be evaluated based on independent measurements or well-accepted correlations. This work demonstrates the implementation of this approach for industry-relevant case studies using both a model protein, lysozyme, and biopharmaceutical product monoclonal antibodies, using cation-exchange resins with a variety of architectures (SP Sepharose FF, Fractogel EMD SO"""
    pkwtree = get_fixed_tree()
    print(get_predefined_keywords(pkwtree, textblob))
