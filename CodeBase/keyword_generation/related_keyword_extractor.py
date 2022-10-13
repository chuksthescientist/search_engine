import sys, os
sys.path.insert(0, os.path.abspath('..'))
from pubmed_searcher import pubMedSearcherBio


def get_related_keywords(papers):
    keywords_related = {}
    for paper in papers:
        keywords_related[str(paper['pubmed_id'])] = paper['keywords']
    return keywords_related


if __name__ == "__main__":
    search_term = "affinity"
    articles = pubMedSearcherBio(search_term)
    print(get_related_keywords(articles))
