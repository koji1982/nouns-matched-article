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

def make_matched_rate_dict(base_nouns: str, id_nouns_dict: dict) -> dict:
    """id_nouns_dictのnounsに対して、base_nouns内の名詞と一致する
    名詞の割合を算出し、id:rateのdictの形で返す関数
    """
    #base_nounsが空の場合、
    #即ち、goodまたはuninterestedどちらかの評価が全くされていない場合は、
    #その評価の一致率を算出できないため空の辞書を返す
    if base_nouns == '':
        return {}
    #型チェックを行う
    #第一引数がstr,第二引数がdict{str:str}でない場合はErrorを送出する
    #また、どちらのstr(dict.keyは除く)もコンマ(,)で連結、成形されていることを前提とする
    if type(base_nouns) is not str:
        raise TypeError
    if ',' not in base_nouns:
        raise TypeError
    #strでないkeyが含まれている場合はerrorを送出
    if any(type(key) is not str for key in id_nouns_dict.keys()):
        raise TypeError
    #strでないvalueが含まれている場合はerrorを送出
    if any(type(val) is not str for val in id_nouns_dict.values()):
        raise TypeError
    #第二引数dictのvalueに','で繋がれていないstrが含まれる場合はerrorを送出
    if any(',' not in val for val in id_nouns_dict.values()):
        raise TypeError
    
    #dict{id:nouns}のそれぞれのrateを算出してdict{id:rate}を作成する
    url_rate_pairs = {}
    for article_id, article_nouns in id_nouns_dict.items():
        rate = get_duplicate_rate(base_nouns, article_nouns)
        url_rate_pairs[article_id] = str(rate)

    return url_rate_pairs

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