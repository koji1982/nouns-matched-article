import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from articles.models import Article, Preference

#https://www.ranks.nl/stopwords/japaneseより
STOP_WORDS_JP = [
    'これ','それ','あれ','この','その','あの','ここ','そこ','あそこ',
    'こちら','どこ','だれ','なに','なん','何','私','貴方',	'貴方',
    '我々','私達','あの人','あのかた','彼女','彼','です','あります',
    'おります','います','は','が','の','に','を','で','え','から',
    'まで','より','も','どの','と','し','それで','しかし', 'こと', 'もの'
]

def compute_tfidf_cos_similarity(user):
    """全記事内の各単語のTF-IDF値を求め、「利用者が評価した記事のTF-IDF vector」に対する
    各記事のTF-IDF vectorのコサイン類似度を算出し、コサイン類似度が高い記事を
    推奨候補・除外候補として保存する。
    """    
    user_preference = Preference.objects.get(user=user)
    #全記事の中での各単語のTF-IDFを求める
    corpus_all_articles = []
    all_articles = Article.objects.all()
    tfidf_id_list = []
    for article in all_articles:
        corpus_all_articles.append(article.noun.replace(',',' '))
        tfidf_id_list.append(article.id)
    tfidf_vectorizer = TfidfVectorizer(stop_words=STOP_WORDS_JP)
    tfidf_val_csr_mat = tfidf_vectorizer.fit_transform(corpus_all_articles)
    #「いいね」「興味なし」と評価された記事のIDリストを取得し、
    #それぞれの評価ごとに統合されたTF-IDF vectorを作成する
    good_id_list = user_preference.get_good_list()
    uninterested_id_list = user_preference.get_uninterested_list()
    ordered_vocabulary = tfidf_vectorizer.get_feature_names_out()
    good_vector, good_word_tfidf_dict = make_merged_vector_and_dict(tfidf_val_csr_mat,
                                                                    tfidf_id_list,
                                                                    good_id_list,
                                                                    ordered_vocabulary)
    uninterested_vector, uninterested_word_tfidf_dict = make_merged_vector_and_dict(
                                                                      tfidf_val_csr_mat,
                                                                      tfidf_id_list,
                                                                      uninterested_id_list,
                                                                      ordered_vocabulary)
    #未評価の記事（推奨、除外を判断する対象となる記事）のIDを取り出し
    #各記事のTF-IDF vectorを作成する
    uneval_articles = [article for article in Article.objects.all() if str(article.id) not in good_id_list]
    uneval_article_id_list = [article.id for article in uneval_articles if str(article.id) not in uninterested_id_list]

    uneval_id_vector_dict = make_id_vector_dict(tfidf_val_csr_mat,
                                                tfidf_id_list,
                                                uneval_article_id_list)
    #cos類似度を計算し辞書{記事ID: cos類似度}の形で受け取る
    good_id_cos_sim_dict = calc_cosine_similarity(good_vector,
                                                  uneval_id_vector_dict)
    uninterested_id_cos_sim_dict = calc_cosine_similarity(uninterested_vector,
                                                          uneval_id_vector_dict)

    #結果を保存する
    word_idf_dict = make_word_idf_dict(tfidf_vectorizer.get_feature_names_out(),
                                       tfidf_vectorizer.idf_)
    # print(word_idf_dict)
    print(len(good_id_list))
    print(len(good_word_tfidf_dict))
    print(good_word_tfidf_dict)
    user_preference.set_good_noun_tfidf_dict(good_word_tfidf_dict)
    user_preference.set_uninterested_noun_tfidf_dict(uninterested_word_tfidf_dict)
    user_preference.set_recommended_id_rate_dict(good_id_cos_sim_dict)
    user_preference.set_rejected_id_rate_dict(uninterested_id_cos_sim_dict)
    user_preference.set_word_idf_dict(word_idf_dict)
    user_preference.save()

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

def get_cosine_similarity(fitted_vectorizer, base_corpus, target_corpus):
    """
    """
    base_vector = fitted_vectorizer.transform(base_corpus)
    target_vector = fitted_vectorizer.transform(target_corpus)
    return cosine_similarity(base_vector.toarray(), target_vector.toarray())

def make_id_vector_dict(tfidf_val_csr_mat, tfidf_whole_id_list, target_id_list):
    """target_id_list内のIDのIF-IDF値から一つずつvectorに作成してvectorのlistとして返す"""
    id_vectors_dict = {}
    for target_id in target_id_list:
        id_index = tfidf_whole_id_list.index(int(target_id))
        start_indptr = tfidf_val_csr_mat.indptr[id_index]
        end_indptr = tfidf_val_csr_mat.indptr[id_index + 1]
        vector = [0.0] * tfidf_val_csr_mat.shape[1]
        vector_indices = tfidf_val_csr_mat.indices[start_indptr:end_indptr]
        vector_data = tfidf_val_csr_mat.data[start_indptr:end_indptr]
        for index, data in zip(vector_indices, vector_data):
            vector[index] = data
        id_vectors_dict[target_id] = vector
    return id_vectors_dict

def make_merged_vector_and_dict(tfidf_val_csr_mat, tfidf_whole_id_list, target_id_list, vocabulary):
    """target_id_list内のIDのIF-IDF値を取り出して一つのvectorに統合して返す"""
    vector_list = []
    word_tfidf_dict = {}
    vector = [0.0] * tfidf_val_csr_mat.shape[1]
    for target_id in target_id_list:
        id_index = tfidf_whole_id_list.index(int(target_id))
        start_indptr = tfidf_val_csr_mat.indptr[id_index]
        end_indptr = tfidf_val_csr_mat.indptr[id_index + 1]
        vector_indices = tfidf_val_csr_mat.indices[start_indptr:end_indptr]
        vector_data = tfidf_val_csr_mat.data[start_indptr:end_indptr]
        for index, data in zip(vector_indices, vector_data):
            vector[index] = data
            word_tfidf_dict[vocabulary[index]] = str(data)
    #要素(vector)一つだけのリストを作成する
    vector_list.append(vector)
    return vector_list, word_tfidf_dict

def calc_cosine_similarity(base_vector, target_id_vector_dict):
    id_result_dict = {}
    for id, target_vector in target_id_vector_dict.items():
        cos_similarity = cosine_similarity(base_vector, [target_vector])
        id_result_dict[str(id)] = str(cos_similarity[0][0])
    return id_result_dict

def make_word_idf_dict(ordered_word_list, ordered_idf_list):
    word_idf_dict = {}
    for word, idf in zip(ordered_word_list, ordered_idf_list):
        word_idf_dict[word] = str(idf)
    return word_idf_dict
