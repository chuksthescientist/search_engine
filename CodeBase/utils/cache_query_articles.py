import sys, os

sys.path.insert(0, os.path.abspath('..'))
from tqdm import tqdm
import datetime
from json import JSONEncoder
import json
import dateutil.parser
from pubmed_searcher import pubMedSearcherBio


def extract_articles_cache(search_term, domain_mesh):
    docs = []
    try:
        papers = pubMedSearcherBio(f"{search_term}", 1500)
        docs.extend(papers)
    except Exception as e:
        print(str(e))
        print("Error :", search_term)

    for key in tqdm(domain_mesh[search_term]):
        try:
            papers = pubMedSearcherBio(f"{search_term} AND {key}", 50)
            docs.extend(papers)
        except Exception as e:
            print(str(e))
            print("Error :", f"{search_term} AND {key}")

    return docs


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def DecodeDateTime(Dict):
    # custom Decoder
    if 'publication_date' in Dict and Dict["publication_date"] != None:
        Dict["publication_date"] = dateutil.parser.parse(Dict["publication_date"])
        return Dict
    else:
        return Dict


def load_cache_articles(path='../data/cache_articles.json'):
    # use of object_hook
    with open(path, 'r') as f:
        decoded_cache_articles = json.load(f, object_hook=DecodeDateTime)
    # print(len(decoded_cache_articles))

    return decoded_cache_articles


if __name__ == "__main__":
    print("caching artciles")
    with open('../data/domain_mesh.json', 'r') as f:
        domain_mesh = json.load(f)

    cache_articles = {}
    for key in domain_mesh.keys():
        cache_articles[key] = extract_articles_cache(key, domain_mesh)

    with open('../data/cache_articles.json', 'w') as f:
        json.dump(cache_articles, f, indent=4, cls=DateTimeEncoder)

    print("articles cached!")
