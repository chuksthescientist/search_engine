import sys, os
sys.path.insert(0, os.path.abspath('..'))
import pandas as pd
import json
from pubmed_searcher import pubMedSearcherBio
from tqdm import tqdm
import time


def get_revelant_mesh(mesh_kewords_related):
    from collections import Counter
    all_mesh_words = []
    for mesh in mesh_kewords_related:
        all_mesh_words.append(mesh[0])
    return list(dict(sorted(Counter(all_mesh_words).items(), key=lambda item: item[1], reverse=True)).keys())[:50]


def related_keywords_mesh(papers):
    mesh_kewords_related = []
    for paper in papers:
        mesh_kewords_related.extend(paper['mesh_terms'])
    mesh_kewords_related = get_revelant_mesh(mesh_kewords_related)
    return mesh_kewords_related


def get_domain_mesh(keywords):
    domain_mesh = {}
    for key in tqdm(keywords):
        try:
            papers = pubMedSearcherBio(f"{key}", 10000)
            mesh_extracted = related_keywords_mesh(papers)
            domain_mesh[key] = mesh_extracted
            time.sleep(20)
        except Exception as e:
            print(str(e))
            print(key)
        domain_mesh[key] = []
    return domain_mesh


def keywords_mesh(papers):
    mesh_kewords_related = []
    for paper in papers:
        mesh_kewords_related.extend(paper['mesh_terms'])

    all_mesh_words = []
    for mesh in mesh_kewords_related:
        all_mesh_words.append(mesh[0])

    return all_mesh_words


def get_train_mesh(train_dataset):
    train_mesh = {}
    for key, values in train_dataset.items():
        train_mesh[key] = []
        for value in values:
            papers = pubMedSearcherBio(f"{value}", 1)
            mesh_extracted = keywords_mesh(papers)
            train_mesh[key].extend(mesh_extracted)
        train_mesh[key] = list(set(train_mesh[key]))
    return train_mesh


if __name__ == "__main__":
    File = '../data/master keywords list.csv'
    keywords = pd.read_csv(File, names=['keyword'])['keyword'].to_list()

    File = '../data/train.csv'
    df_train = pd.read_csv(File)
    df_train = df_train[['Keywords (separated by ;)', 'doi']]

    domain_mesh = get_domain_mesh(keywords)

    train_dataset = {}
    for ind, row in df_train.iterrows():
        for key in row['Keywords (separated by ;)'].split(';'):
            if key in train_dataset:
                train_dataset[key].append(row['doi'])
            else:
                train_dataset[key] = [row['doi']]

    train_mesh = get_train_mesh(train_dataset)

    # replace or add train mesh into domain terms
    for key, value in train_mesh.items():
        for val in value:
            if val not in domain_mesh:
                domain_mesh[key].append(val)

    # save domain mesh
    with open('../data/domain_mesh.json', 'w') as f:
        json.dump(domain_mesh, f)
