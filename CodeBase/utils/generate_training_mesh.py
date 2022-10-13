import sys, os

sys.path.insert(0, os.path.abspath('..'))
import json
from cache_query_articles import load_cache_articles
import pandas as pd


def related_keywords_mesh(papers):
    mesh_kewords_related = {}
    for paper in papers:
        if paper['mesh_terms']:
            mesh_kewords_related[paper['doi']] = paper['mesh_terms']
        else:
            mesh_kewords_related[paper['doi']] = paper['keywords']
    return mesh_kewords_related


if __name__ == "__main__":

    # custom Decoder
    decoded_cache_articles = load_cache_articles()
    File = '../data/train.csv'
    df_train = pd.read_csv(File)
    df_train = df_train[['Keywords (separated by ;)', 'doi']]

    train_dataset = {}
    for ind, row in df_train.iterrows():
        for key in row['Keywords (separated by ;)'].split(';'):
            if key in train_dataset:
                train_dataset[key].append(row['doi'])
            else:
                train_dataset[key] = [row['doi']]

    train_papers = []
    for key, value in train_dataset.items():
        if key in decoded_cache_articles:
            articles = decoded_cache_articles[key]
            for art in articles:
                if art['doi'] and (art['doi'] in value):
                    train_papers.append(art)

    with open('../data/mesh_database.json', 'r') as f:
        mesh_database = json.load(f)

    mesh_keywrds_extracted = related_keywords_mesh(train_papers)

    reverse_train = {}
    for key, value in train_dataset.items():
        for val in value:
            if val in reverse_train:
                reverse_train[val].append(key)
            else:
                reverse_train[val] = [key]

    ranking_schema = {}
    for key, value in mesh_keywrds_extracted.items():
        values = [val[0] for val in value]
        for keywrd in reverse_train[key]:
            if keywrd in ranking_schema:
                ranking_schema[keywrd].extend(values)
            else:
                ranking_schema[keywrd] = values
        ranking_schema[keywrd] = list(set(ranking_schema[keywrd]))
    # print(len(ranking_schema),ranking_schema.keys())

    with open('../data/train_dataset_mesh.json', 'w') as f:
        json.dump(ranking_schema, f)
