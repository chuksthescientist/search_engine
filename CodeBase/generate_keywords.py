import json
from pubmed_searcher import pubMedSearcherBio
from keyword_generation.abstract_keyword_extractor import get_abstract_keywords, get_tree
from keyword_generation.related_keyword_extractor import get_related_keywords
from keyword_generation.predefined_keyword_extractor import get_predefined_keywords, get_fixed_tree
from keyword_generation.expanded_keyword_extractor import paper_keywords_mesh, get_expanded_keywords


def get_new_keywords(search_term, kwtree, pkwtree, mesh_database, search_database, keyword_threshold=0.10,
                     max_results=100):
    if search_database:
        articles = search_database
    else:
        query = get_query(search_term)
        articles = pubMedSearcherBio(query, max_results)

    abstract_keywords = {}
    for paper in articles:
        abstract_keywords[str(paper['pubmed_id'])] = get_abstract_keywords(kwtree, paper['abstract'])
        abstract_keywords[str(paper['pubmed_id'])].extend(get_abstract_keywords(kwtree, paper['title']))
        abstract_keywords[str(paper['pubmed_id'])] = list(set(abstract_keywords[str(paper['pubmed_id'])]))

    related_keywords = get_related_keywords(articles)

    predefined_keywords = {}
    for paper in articles:
        predefined_keywords[str(paper['pubmed_id'])] = get_predefined_keywords(pkwtree, paper['abstract'])
        predefined_keywords[str(paper['pubmed_id'])].extend(get_predefined_keywords(pkwtree, paper['title']))
        predefined_keywords[str(paper['pubmed_id'])] = list(set(predefined_keywords[str(paper['pubmed_id'])]))

    mesh_keywrds_extracted = paper_keywords_mesh(articles)
    expanded_keywords = get_expanded_keywords(mesh_database, mesh_keywrds_extracted)

    extracted_keywords_list = {}
    for key in abstract_keywords.keys():
        extracted_keywords_list[key] = abstract_keywords[key]
        extracted_keywords_list[key].extend(related_keywords[key])
        extracted_keywords_list[key].extend(predefined_keywords[key])
        extracted_keywords_list[key].extend(expanded_keywords[key]) if key in expanded_keywords else \
            extracted_keywords_list[key].extend([])

    all_keywords = []
    for key, value in extracted_keywords_list.items():
        all_keywords.extend(value)

    from collections import Counter
    freq_keywords = Counter(all_keywords)
    ranked_keywords = dict(sorted(freq_keywords.items(), key=lambda item: item[1], reverse=True))

    keywords_scores = {}
    for key, value in ranked_keywords.items():
        if value / len(abstract_keywords) > keyword_threshold:
            keywords_scores[key] = value / len(abstract_keywords)

    return keywords_scores


def get_query(search_term):
    search_term = search_term.rstrip(';')

    if ';' in search_term:
        search_term = search_term.split(";")

        query = ""
        for i in range(len(search_term) - 1):
            query += f"({search_term[i]}) AND "
        query = query + f"({search_term[i + 1]})"
    else:
        query = search_term

    return query


if __name__ == "__main__":
    kwtree = get_tree(dmeshFile='data/d2021.bin', qmeshFile='data/q2021.bin', cmeshFile='data/c2021.bin', )
    pkwtree = get_fixed_tree(File='data/master keywords list.csv')

    with open('data/mesh_database.json', 'r') as f:
        mesh_database = json.load(f)
    search_term = "affinity"
    query = get_query(search_term)

    new_keywords = get_new_keywords(query, kwtree, pkwtree, mesh_database, [], max_results=10)
    print(new_keywords)
