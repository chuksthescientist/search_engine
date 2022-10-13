from Bio import Entrez
import datetime

def get_keywords_mesh(mesh):
    mesh_kewords_related = []
    for m in mesh:
        if 'DescriptorName' in m:
            mesh_kewords_related.append([str(m['DescriptorName']), m['DescriptorName'].attributes['UI']])
    return mesh_kewords_related


def get_authors(authors_list):
    authors = []
    for authr in authors_list:
        authors.append({
            'lastname': authr['LastName'] if 'LastName' in authr else None,
            'firstname': authr['ForeName'] if 'ForeName' in authr else None,
            'initials': authr['Initials'] if 'Initials' in authr else None,
            'affiliation': authr['AffiliationInfo'][0]['Affiliation'] if 'AffiliationInfo' in authr and 'Affiliation' in authr['AffiliationInfo'] else None,
        })
    return authors


def get_conclusion(abstract_texts):
    res = {}
    for text in abstract_texts:
        if 'Label' in text.attributes:
            if text.attributes['Label'] == "CONCLUSIONS":
                res = str(text)
    if type(res) == dict:
        res = None
    return res


def get_results(abstract_texts):
    res = {}
    for text in abstract_texts:
        if 'Label' in text.attributes:
            if text.attributes['Label'] == "RESULTS":
                res = str(text)
    if type(res) == dict:
        res = None
    return res


def get_methods(abstract_texts):
    res = {}
    for text in abstract_texts:
        if 'Label' in text.attributes:
            if text.attributes['Label'] == "METHODS":
                res = str(text)

    if type(res) == dict:
        res = None
    return res


def get_paper_structure(paper):
    return {
                u'pubmed_id': str(paper['MedlineCitation']['PMID']),
                u'title': str(paper['MedlineCitation']['Article']['ArticleTitle']) if 'Article' in paper['MedlineCitation'] and 'ArticleTitle' in paper['MedlineCitation']['Article'] else None,
                u'keywords': [str(word) for word in paper['MedlineCitation']['KeywordList'][0]] if 'KeywordList' in paper['MedlineCitation'] and len(paper['MedlineCitation']['KeywordList']) > 0 else [],
                u'journal': str(paper['MedlineCitation']['Article']['Journal']['Title']) if 'Article' in paper['MedlineCitation'] and 'Journal' in paper['MedlineCitation']['Article'] and 'Title' in paper['MedlineCitation']['Article']['Journal'] else None,
                u'abstract': str(paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]) if 'Article' in paper['MedlineCitation'] and 'Abstract' in paper['MedlineCitation']['Article'] and 'AbstractText' in paper['MedlineCitation']['Article']['Abstract'] and len(paper['MedlineCitation']['Article']['Abstract']['AbstractText']) > 0 else None,
                u'conclusions': get_conclusion(paper['MedlineCitation']['Article']['Abstract']['AbstractText']) if 'Article' in paper['MedlineCitation'] and 'Abstract' in paper['MedlineCitation']['Article'] and 'AbstractText' in paper['MedlineCitation']['Article']['Abstract'] else None,
                u'methods': get_methods(paper['MedlineCitation']['Article']['Abstract']['AbstractText']) if 'Article' in paper['MedlineCitation'] and 'Abstract' in paper['MedlineCitation']['Article'] and 'AbstractText' in paper['MedlineCitation']['Article']['Abstract'] else None,
                u'results': get_results(paper['MedlineCitation']['Article']['Abstract']['AbstractText']) if 'Article' in paper['MedlineCitation'] and 'Abstract' in paper['MedlineCitation']['Article'] and 'AbstractText' in  paper['MedlineCitation']['Article']['Abstract'] else None,
                u'copyrights': str(paper['MedlineCitation']['Article']['Abstract']['CopyrightInformation']) if 'Article' in paper['MedlineCitation'] and 'Abstract' in paper['MedlineCitation']['Article'] and 'CopyrightInformation' in paper['MedlineCitation']['Article']['Abstract'] else None,
                u'doi': str(paper['MedlineCitation']['Article']['ELocationID'][0]) if 'Article' in paper['MedlineCitation'] and 'ELocationID' in paper['MedlineCitation']['Article'] and len(paper['MedlineCitation']['Article']['ELocationID']) > 0 else None,
                u'publication_date': datetime.datetime.strptime(f"{paper['MedlineCitation']['Article']['ArticleDate'][0]['Year']}-{paper['MedlineCitation']['Article']['ArticleDate'][0]['Month']}-{paper['MedlineCitation']['Article']['ArticleDate'][0]['Day']}","%Y-%M-%d").date() if 'Article' in paper['MedlineCitation'] and 'ArticleDate' in paper['MedlineCitation']['Article'] and len(paper['MedlineCitation']['Article']['ArticleDate']) > 0 else None,
                u'authors': get_authors(paper['MedlineCitation']['Article']['AuthorList']) if 'Article' in paper['MedlineCitation'] and 'AuthorList' in paper['MedlineCitation']['Article'] else [],
                u'mesh_terms': get_keywords_mesh(paper['MedlineCitation']['MeshHeadingList']) if 'MeshHeadingList' in paper['MedlineCitation'] else []
            }


def pubMedSearcherBio(query, max_count=10):
    import datetime

    Entrez.email = 'myemail@ccc.com'

    handle = Entrez.esearch(db='pubmed',
                            retmode='xml',
                            term=query,
                            datetype='pdat',
                            retmax=max_count,
                            mindate='2010',
                            maxdate='2020')
    results = Entrez.read(handle)

    ids = ','.join(results['IdList'])

    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           sort='date',
                           id=ids)

    papers = Entrez.read(handle)

    articleInfo = []
    if 'PubmedArticle' in papers and len(papers['PubmedArticle']) > 0:
        for paper in papers['PubmedArticle']:
            articleInfo.append(get_paper_structure(paper))

    return articleInfo


if __name__ == "__main__":
    papers = pubMedSearcherBio("affinity", 10)
    print(papers)
