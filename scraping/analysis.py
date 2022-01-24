from pprint import pprint
import MeCab
from scraping.database import ArticleDB

def extract_noun(text):
    tagger = MeCab.Tagger()
    parsed_article = tagger.parse(text)
    split_words = parsed_article.split('\n')
    split_words = split_words[:-2]
    nouns = []
    for split_word in split_words:
        word_attrib = split_word.split(',')
        word, classify = word_attrib[0].split('\t')
        if (classify == '名詞') & ('数' not in word_attrib[1:]):
            nouns.append(word)
    connected_nouns = ','.join(nouns)
    return connected_nouns

def get_duplicate_rate_list(source):
    all_nouns = ArticleDB.getAllNoun()
    url_rate_pairs = {}
    for article_nouns in all_nouns:
        rate = get_duplicate_rate(source, article_nouns[1])
        url_rate_pairs[article_nouns[0]] = rate

    u_r_sorted = sorted(url_rate_pairs.items(), key=lambda pair: pair[1], reverse=True)
    # print(u_r_sorted)
    for pair in u_r_sorted:
        print(str(pair[0])+' 一致率:'+str(pair[1] * 100.0)+'%')

def get_duplicate_rate(source, target):
    split_sources = source.split(',')
    split_targets = target.split(',')
    duplicate_count = 0
    for source in split_sources:
        if source in split_targets:
            duplicate_count += 1
    
    # print('test')
    # print(split_sources)
    # print(split_targets)
    # print('source count '+str(duplicate_count))
    # print('source_length '+str(len(split_sources)))
    # print(duplicate_count / len(split_sources))
    # denom = len(split_sources) if len(split_sources) < len(split_targets) else len(split_targets)
    # print(duplicate_count / denom)
    # print(denom)
    return duplicate_count / len(split_sources)

import structlog

def callFunctionTest():
    logger = structlog.get_logger(__name__)
    logger.info("      Called from scraping/components/analysis.py    ")