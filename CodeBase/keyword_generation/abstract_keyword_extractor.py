from nltk.corpus import stopwords
import re
from ahocorapy.keywordtree import KeywordTree


def get_tree(dmeshFile='../data/d2021.bin', qmeshFile='../data/q2021.bin', cmeshFile='../data/c2021.bin'):
    mesh_keywords = []

    # descriptors
    with open(dmeshFile, mode='rb') as file:
        dmesh = file.readlines()
    for line in dmesh:
        meshTerm = re.search(b'MH = (.+)$', line)
        if meshTerm:
            term = meshTerm.group(1)
            mesh_keywords.append(term.decode('utf-8'))

    # qualifiers
    with open(qmeshFile, mode='rb') as file:
        qmesh = file.readlines()
    for line in qmesh:
        meshTerm = re.search(b'SH = (.+)$', line)
        if meshTerm:
            term = meshTerm.group(1)
            mesh_keywords.append(term.decode('utf-8'))

    # Supplementary Records
    with open(cmeshFile, mode='rb') as file:
        cmesh = file.readlines()
    for line in cmesh:
        meshTerm = re.search(b'NM = (.+)$', line)
        if meshTerm:
            term = meshTerm.group(1)
            mesh_keywords.append(term.decode('utf-8'))

    kwtree = KeywordTree(case_insensitive=True)
    for kw in mesh_keywords:
        kwtree.add(kw)
    kwtree.finalize()
    return kwtree


def get_abstract_keywords(kwtree, textblob):
    stop_words = set(stopwords.words('english'))
    if textblob:
        results = kwtree.search_all(textblob)
        keywords = []
        for res in results:
            if res is not None and res[0] not in stop_words:
                keywords.append(res[0])
        return list(set(keywords))
    else:
        return []


if __name__ == "__main__":
    textblob = """Many recombinant proteins are products of great value in biomedical and industrial fields. The use of solubility and affinity tags are commonly used to increase yields and facilitate the purification process. However, it is of paramount importance in several applications to remove the fusion tag from the final product. In this regard, the Tobacco Etch Virus protease (TEV) is one of the most widely used for tag removal. The presence in the TEV of the same tag to be removed facilitates the separation of TEV and the tag from the cleaved recombinant protein in a single purification step. We generated a double-tagged (StrepTagII and HisTag) TEV variant with reported mutations that improve the activity, the expression yield in E.coli, and that decrease the auto-proteolysis. This TEV can be easily purified by two consecutive affinity chromatography steps with high yields and purity. The cleavage reaction can be done to almost completeness in as fast as 15\u202fmin at room temperature and the removal of the protease and tags is performed in a single purification step, independent of the previous presence of a StrepTagII or a HisTag on the target."""
    kwtree = get_tree()
    keywords = get_abstract_keywords(kwtree, textblob)
    print(keywords)
