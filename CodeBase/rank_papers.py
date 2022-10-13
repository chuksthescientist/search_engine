import json
from collections import Counter
from utils.cache_query_articles import load_cache_articles
from pubmed_searcher import pubMedSearcherBio

def filter_papers(papers):
    mesh_kewords_related = {}
    filtered_database = {}
    for paper in papers:
        mesh_kewords_related[paper['title']] = paper['mesh_terms']
        filtered_database[paper['title']] = paper
    return mesh_kewords_related, filtered_database


def get_global_domain_mesh(train_dataset_mesh):
    train_keywords = list(train_dataset_mesh.keys())
    global_domain_mesh = []
    for keyword in train_keywords:
        for key in train_dataset_mesh[keyword]:
            if key not in global_domain_mesh:
                global_domain_mesh.append(key)
    return global_domain_mesh


def get_search_database(search_term, decoded_cache_articles):
    searchterms = search_term.split(";")
    search_database = []

    for st in searchterms:
        if st in decoded_cache_articles:
            search_database.extend(decoded_cache_articles[st])
        else:
            articles = pubMedSearcherBio(st, 2000)
            search_database.extend(articles)
    return searchterms, search_database


def get_rank_vector(mode, searchterms, train_dataset_mesh, global_domain_mesh, domain_mesh):
    if mode == "train":
        new_search_vector = []
        for st in searchterms:
            if st in train_dataset_mesh:
                for wrd in train_dataset_mesh[st]:
                    if wrd not in new_search_vector:
                        new_search_vector.append(wrd)
        if len(new_search_vector) == 0:
            new_search_vector = global_domain_mesh
    else:
        new_search_vector = global_domain_mesh
        for st in searchterms:
            if st in domain_mesh:
                for wrd in domain_mesh[st]:
                    if wrd not in new_search_vector:
                        new_search_vector.append(wrd)
    return new_search_vector


def return_ranked_papers(target_mesh, papers_extracted):
    rank = {}
    for key, value in papers_extracted.items():
        count = 0
        for val in value:
            if val[0] in target_mesh:
                count += 1
        rank[key] = count / len(target_mesh)

    return dict(sorted(Counter(rank).items(), key=lambda item: item[1], reverse=True))


def get_ranked_papers(search_term, mode, train_dataset_mesh, domain_mesh, decoded_cache_articles):
    global_domain_mesh = get_global_domain_mesh(train_dataset_mesh)

    searchterms, search_database = get_search_database(search_term, decoded_cache_articles)

    papers_extracted, filtered_database = filter_papers(search_database)

    target_vector = get_rank_vector(mode, searchterms, train_dataset_mesh, global_domain_mesh, domain_mesh)

    ranked_papers = return_ranked_papers(target_vector, papers_extracted)

    filtered_database = [value for key, value in filtered_database.items()]

    return ranked_papers, filtered_database


if __name__ == "__main__":
    search_term = "Protein A"
    mode = "train"

    with open('data/train_dataset_mesh.json', 'r') as f:
        train_dataset_mesh = json.load(f)

    with open('data/domain_mesh.json', 'r') as f:
        domain_mesh = json.load(f)

    decoded_cache_articles = load_cache_articles(path='data/cache_articles.json')

    print(get_ranked_papers(search_term, mode, train_dataset_mesh, domain_mesh, decoded_cache_articles))
