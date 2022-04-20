from articles.nlp import make_matched_rate_dict
from articles.models import Article, Preference

def apply_choices(user):
    """ユーザーの評価をもとに一致率を算出しデータベースに格納する。"""
    
    user_preference = Preference.objects.get(user=user)
    #「いいね」「興味なし」と評価された記事のIDリストを取得する
    good_id_list = user_preference.get_good_list()
    uninterested_id_list = user_preference.get_uninterested_list()
    
    #記事に含まれる語句（名詞）を取り出し評価ごとに集める
    good_merged_nouns = make_merged_nouns_str(good_id_list)
    uninterested_merged_nouns = make_merged_nouns_str(uninterested_id_list)
    
    #算出対象となる側の記事（評価されていない記事）から
    #算出のために{ID:名詞}の辞書を作成する
    good_id_nouns_dict = make_id_nouns_dict(good_id_list, uninterested_id_list)
    uninterested_id_nouns_dict = make_id_nouns_dict(uninterested_id_list, good_id_list)

    #一致率を算出する。{記事ID:一致率}の形の辞書として受け取る
    good_id_rate_dict = make_matched_rate_dict(good_merged_nouns, good_id_nouns_dict)
    uninterested_id_rate_dict = make_matched_rate_dict(uninterested_merged_nouns,
                                                       uninterested_id_nouns_dict)
    
    #評価ごとの語句群と算出された語句の一致率を保存する。
    user_preference.good_nouns = good_merged_nouns
    user_preference.uninterested_nouns = uninterested_merged_nouns
    user_preference.set_recommended_id_rate_dict(good_id_rate_dict)
    user_preference.set_rejected_id_rate_dict(uninterested_id_rate_dict)
    user_preference.save()

def make_id_nouns_dict(article_id_list, rejected_id_list):
    """受け取った記事のIDリストから記事を取り出し、
    {ID:名詞}の辞書にして返す関数
    """
    #未評価の記事を取り出す。
    uneval_articles = [article for article in Article.objects.all() if str(article.id) not in article_id_list]
    uneval_articles = [article for article in uneval_articles if str(article.id) not in rejected_id_list]
    #{id:単語}のdictにして一致率を算出する
    id_nouns_dict = {}
    for article in uneval_articles:
        #未評価側も重複を失くすため、一度Setに変換した後でstrにつなぎ直す
        target_nouns = ','.join(set(article.noun.split(',')))
        id_nouns_dict[str(article.id)] = target_nouns
    return id_nouns_dict

def make_merged_nouns_str(article_id_list):
    """選択された記事の名詞を集め、重複無しつないでstr型で返す関数"""
    #評価がゼロの場合は空のstrを返して終了する
    if len(article_id_list) == 0:
        return ''
    #評価された全ての記事の名詞を一つのSetに集める
    merged_nouns = set()
    for article_id in article_id_list:
        nouns = Article.objects.get(id=article_id).noun
        nouns_set = set(nouns.split(','))
        merged_nouns = merged_nouns | nouns_set
    #集めた名詞をつなげてstrにして返す
    return ','.join(list(merged_nouns))