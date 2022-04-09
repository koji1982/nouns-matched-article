from django import template
from articles.nlp import make_matched_rate_dict
from articles.models import Article, Preference

register = template.Library()

@register.filter(name='apply_choices')
def apply_choices(request):
    """評価した記事に含まれる単語(名詞)をまとめて、
    その単語群と他の記事内の単語がどれだけ一致するかを算出して保存する関数
    """
    print('test 1')
    #good評価の単語を集める
    # good_id_list = Article.objects.all().filter(evaluation=Article.EVAL_GOOD)
    preference_query = Preference.objects.filter(username=request.user)
    #該当するユーザーが存在しない場合は空のリストを返す
    if preference_query.count() == 0:
        return
    user_preference = preference_query[0]
    print('test 2')

    good_id_list = user_preference.get_good_list()
    uninterested_id_list = user_preference.get_uninterested_list()

    good_merged_nouns = make_merged_nouns_str(good_id_list)
    uninterested_merged_nouns = make_merged_nouns_str(uninterested_id_list)
    print('test 3')
    good_id_nouns_dict = make_id_nouns_dict(good_id_list, uninterested_id_list)
    uninterested_id_nouns_dict = make_id_nouns_dict(uninterested_id_list, good_id_list)
    #一致率を算出する。{記事ID:一致率}の形の辞書として受け取る
    good_id_rate_dict = make_matched_rate_dict(good_merged_nouns, good_id_nouns_dict)
    uninterested_id_rate_dict = make_matched_rate_dict(uninterested_merged_nouns, uninterested_id_nouns_dict)

    user_preference.good_nouns = good_merged_nouns
    user_preference.uninterested_nouns = uninterested_merged_nouns
    user_preference.save_recommended_id_rate_dict(good_id_rate_dict)
    user_preference.save_rejected_id_rate_dict(uninterested_id_rate_dict)
    user_preference.save()
    print(user_preference.username)
    print(user_preference.recommended_id_rate_pair)

def make_id_nouns_dict(article_id_list, rejected_id_list):
    """"""
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
    """選択された記事の名詞(重複無し)を集めてstr型につないで返す関数"""
    #評価がゼロの場合は空リストと空辞書を返して終了する
    if len(article_id_list) == 0:
        return []
    #評価された全ての記事の名詞を一つのSetに集める
    merged_nouns = set()
    for article_id in article_id_list:
        nouns = Article.objects.get(id=article_id).noun
        nouns_set = set(nouns.split(','))
        merged_nouns = merged_nouns | nouns_set
    #集めた名詞をつなげてstrにして返す
    return ','.join(list(merged_nouns))