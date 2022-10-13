## [Soro Journal Search Engine PoC Codebase Development Challenge](https://www.topcoder.com/challenges/d23f152d-160d-459d-a9c7-b95e02161675)
- The objective is to implement a journal search engine using NLP techniques to handle one data source only, PubMed Central. Your journal search engine should be able to conduct keyword search using PubMed API/DB 


## Tech Stack
- [Anaconda Python3](https://www.anaconda.com/distribution/)


## Deploying Solution
```CMD
conda create -n solo python==3.7.0 -y
conda activate solo
cd path/to/solution directory/ eg.,(cd  D:\topcoder\Soro Journal Search Engine PoC Codebase Development Challenge\CodeBase\requirements.txt)
pip install -r requirements.txt
```
```python
# open python console -> simply type python in the conda prompt
import nltk
nltk.download('stopwords')
nltk.download('punkt')
# exit() -> to get out of the console
```

## Solution Run Conda CMD
### testing the tool with the test data to generate required files for the challenge
```CMD
python cli.py --file_path=data\test_blank.csv --mode=test
```
###  testing the tool with known keywords already cached, this will also work for non cached keywords but will take longer to get results
#### generating both keywords and ranked papers for a given search term
```CMD
python cli.py --search_terms="affinity" --generate_keywords=True --rank_papers=True --mode=train
```
#### generating keywords for a given search term
```CMD
python cli.py --search_terms="affinity;Protein A;electrophoresis" --generate_keywords=True --rank_papers=False --mode=train
```
#### generating ranked papers for a given search term
```CMD
python cli.py --search_terms="affinity;Protein A;electrophoresis" --generate_keywords=False --rank_papers=True --mode=train
```
#### search keywords and rank articles for a new keyword not present in either train or test
```CMD
python cli.py --search_terms="Fever" --generate_keywords=True --rank_papers=True --mode=train
```

## NOTE 
- All the keywords from the master csv has been cached for faster processing of results
- Every Run takes 1 min in the beginning to load and create required dependency files for processing
- New keywords can be searched using mode train, but will only look for direct relations when searching pubmed and will take time.
- It's recommended to run caching for new keywords so that all direct and related papers based on keywords from various sources can be included to enrich the papers fetching.
- The Generated files for testing can be found in the directory 'data' as well as 'test generated files'

## DIRECTORY STRUCTURE
  - data - Contains all the data sources and metadata created for the process with the test data required for the challenge
  - keyword_generation - Contains all files related to extracting keywords from the papers
  - utils - Contains all files needed to create required metadata and dependency files for processing.
  - cli.py - To run the solution can be directly used in any backend API development in either Django or Flask
  - generate_keywords.py - To generate any keywords present in the articles
  - pubmed_searcher.py - The actual fetcher that fetches relevant articles from pubmed API and create a python object to be consumed by downstream processes.
  - rank_papers.py - The ranker logic file that take a list of articles and ranks them.

## Idea Document
- An idea.pdf is provided that explains my approach along with additional information on all the files in the submission.
