from pprint import pprint
import MeCab

def extract_noun(text):
    """引数として受け取ったtextから名詞を取り出して、','で繋いだ
    一つのstrとして返す関数
    """
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

def sort_duplicated_nouns_list(base_nouns: str, url_nouns_dict: dict) -> list:
    """target_listの各文字列に対して、base_nouns内の名詞と一致する
    名詞の割合を算出して並べ替えたリストを返す関数
    """
    #型チェックを行う
    #第一引数がlist(str),第二引数がdict{str:str}でない場合はErrorを送出する
    #また、どちらのstr(dict.keyは除く)もコンマ(,)で連結、成形されていることを前提とする
    if type(base_nouns) is not str:
        raise TypeError
    if ',' not in base_nouns:
        raise TypeError
    #strでないkeyが含まれている場合はerrorを送出
    if any(type(key) is not str for key in url_nouns_dict.keys()):
        raise TypeError
    #strでないvalueが含まれている場合はerrorを送出
    if any(type(val) is not str for val in url_nouns_dict.values()):
        raise TypeError
    #第二引数dictのvalueに','で繋がれていないstrが含まれる場合はerrorを送出
    if any(',' not in val for val in url_nouns_dict.values()):
        raise TypeError
    
    #dict{url:nouns}のそれぞれのrateを算出してdict{url:rate}を作成する
    url_rate_pairs = {}
    for article_url, article_nouns in url_nouns_dict.items():
        rate = get_duplicate_rate(base_nouns, article_nouns)
        url_rate_pairs[article_url] = rate
    #rateの降順でソート
    url_rate_sorted = sorted(url_rate_pairs.items(), key=lambda pair: pair[1], reverse=True)
    
    
    for pair in url_rate_sorted:
        print(str(pair[0])+' 一致率:'+str(pair[1] * 100.0)+'%')
    #[(url, rate),
    # (url, rate),
    # (url, rate)]
    # の形のリストとして返す
    return url_rate_sorted

def get_duplicate_rate(source: str, target: str) -> float:
    """sourceを基準(1.0)として、targetにどれだけ一致する語句が入っているかを
    一致した語句数の割合で返す
    """
    split_sources = source.split(',')
    split_targets = target.split(',')
    duplicate_count = 0
    for source in split_sources:
        if source in split_targets:
            duplicate_count += 1
    
    return duplicate_count / len(split_sources)

import structlog

def callFunctionTest():
    logger = structlog.get_logger(__name__)
    logger.info("      Called from scraping/components/analysis.py    ")