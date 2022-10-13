#!/usr/bin/env python3
import click
import pprint
import json
from generate_keywords import get_new_keywords
from rank_papers import get_search_database
from keyword_generation.abstract_keyword_extractor import get_tree
from keyword_generation.predefined_keyword_extractor import get_fixed_tree
from utils.cache_query_articles import load_cache_articles
from rank_papers import get_ranked_papers
import pandas as pd
from tqdm import tqdm

paper_threshold = 50
keyword_threshold=0.10

pp = pprint.PrettyPrinter(indent=4)
print("--Loading requirements in memory and creating assets--")

kwtree = get_tree(dmeshFile='data/d2021.bin', qmeshFile='data/q2021.bin', cmeshFile='data/c2021.bin')
pkwtree = get_fixed_tree(File='data/master keywords list.csv')

with open('data/mesh_database.json', 'r') as f:
    mesh_database = json.load(f)

with open('data/train_dataset_mesh.json', 'r') as f:
    train_dataset_mesh = json.load(f)

with open('data/domain_mesh.json', 'r') as f:
    domain_mesh = json.load(f)


@click.command()
@click.option('--search_terms', default=None, help="Search Terms separated by ;")
@click.option('--generate_keywords', default=True, help="New keyword generation")
@click.option('--rank_papers', default=True, help="Article's ranking")
@click.option('--file_path', default=None, help="path of file to generate test data")
@click.option('--mode', default='train', help="Test if you want to search for new terms")
def cli(search_terms, generate_keywords, rank_papers, file_path, mode):
    print("--Running Query--")
    if search_terms == None and file_path != None:
        print("--Running On Test Data--")
        df_test = pd.read_csv(file_path)
        df_test = df_test[['Keywords (separated by ;)']]
        response_papers = []
        response_keywords = []
        print("--Fetching papers -> Ranking papers -> Generating keywords --")
        for search_term in tqdm(df_test['Keywords (separated by ;)'].to_list()):
            temp_papers = {'Keywords (separated by ;)': search_term}

            # get papers for the given keyword
            decoded_cache_articles = load_cache_articles(path='data/cache_articles.json')
            # rank papers
            ranked_papers, search_database = get_ranked_papers(search_term, 'test', train_dataset_mesh, domain_mesh,
                                                               decoded_cache_articles)
            ind = 1
            for rp in list(ranked_papers.keys()):
                if ind == 51:
                    break
                temp_papers.update({ind: rp})
                ind += 1
            response_papers.append(temp_papers)

            # generate new keywords for the given keyword
            new_keywords = get_new_keywords(search_term, kwtree, pkwtree, mesh_database, search_database,
                                            keyword_threshold=0.10, max_results=1000)
            keywords_generated = []
            for key in list(new_keywords.keys()):
                if key not in keywords_generated:
                    keywords_generated.append(key)
            response_keywords.append(",".join(keywords_generated))

        print(len(response_papers), len(response_keywords))
        df_papers = pd.DataFrame(response_papers[:50])
        df_keywords = pd.DataFrame(response_keywords)

        df_papers.to_csv('data/test_filled.csv', index=False)
        df_papers.to_csv('data/new_papers.csv', index=False)
        df_keywords.to_csv('data/generated_keywords.csv', header=False, index=False)

        print({"success": "Output Files are saved at 'data' folder in the root project directory!"})

    elif search_terms != None and file_path == None:
        print("--Running On Train or New Data--")
        if generate_keywords and rank_papers:
            # get papers for the given keyword
            print("--Fetching papers--")
            decoded_cache_articles = load_cache_articles(path='data/cache_articles.json')
            # rank papers
            print("--Ranking papers--")
            ranked_papers, search_database = get_ranked_papers(search_terms, mode, train_dataset_mesh, domain_mesh,
                                                               decoded_cache_articles)
            # generate new keywords for the given keyword
            print("--Generating keywords--")
            new_keywords = get_new_keywords(search_terms, kwtree, pkwtree, mesh_database, search_database,
                                            keyword_threshold=0.10, max_results=1000)

            top_ranked_paper = {}
            ind = 1
            for key, value in ranked_papers.items():
                top_ranked_paper[key] = value
                if ind == paper_threshold:
                    break
                ind += 1

            print({
                'ranked_papers': top_ranked_paper,
                'new_keywords': new_keywords
            })
        elif generate_keywords and not rank_papers:
            # generate new keywords for the given keyword
            print("--Generating keywords--")
            new_keywords = get_new_keywords(search_terms, kwtree, pkwtree, mesh_database, [],
                                            keyword_threshold=0.10, max_results=1000)
            print({
                'ranked_papers': [],
                'new_keywords': new_keywords
            })

        elif not generate_keywords and rank_papers:
            # get papers for the given keyword
            print("--Fetching papers--")
            decoded_cache_articles = load_cache_articles(path='data/cache_articles.json')
            # rank papers
            print("--Ranking papers--")
            ranked_papers, search_database = get_ranked_papers(search_terms, mode, train_dataset_mesh, domain_mesh,
                                                               decoded_cache_articles)

            top_ranked_paper = {}
            ind = 1
            for key, value in ranked_papers.items():
                top_ranked_paper[key] = value
                if ind == paper_threshold:
                    break
                ind += 1

            print({
                'ranked_papers': top_ranked_paper,
                'new_keywords': []
            })
    else:
        print('incorrect arguments')


if __name__ == '__main__':
    cli()
