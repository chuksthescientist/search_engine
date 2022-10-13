import sys, os
sys.path.insert(0, os.path.abspath('..'))
import json
from pubmed_searcher import pubMedSearcherBio


def paper_keywords_mesh(papers):
    mesh_keywrds_extracted = {}
    for paper in papers:
        mesh_keywrds_extracted[paper['pubmed_id']] = paper['mesh_terms']
    return mesh_keywrds_extracted


def get_expanded_keywords(mesh_database, mesh_keywrds_extracted):
    expanded_keywords = {}
    for pmid, keywords in mesh_keywrds_extracted.items():
        expanded_keywords[pmid] = []
        for keyword in keywords:
            if keyword[0] in mesh_database.keys():
                for key, value in mesh_database[keyword[0]].items():
                    if key in ['subheads', 'subheads_synonyms', 'synonyms', 'cross_reference', 'pharmalogical_actions',
                               'synonym_combination'] and value:
                        expanded_keywords[pmid].extend(value)
        expanded_keywords[pmid] = list(set(expanded_keywords[pmid]))
    return expanded_keywords


if __name__ == "__main__":
    articles = pubMedSearcherBio("affinity", 10)
    with open('../data/mesh_database.json', 'r') as f:
        mesh_database = json.load(f)
    mesh_keywrds_extracted = paper_keywords_mesh(articles)
    print(get_expanded_keywords(mesh_database, mesh_keywrds_extracted))
