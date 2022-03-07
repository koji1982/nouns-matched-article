import re


def remove_csrf(html_source):
    """csrf部分を除去して返す関数"""
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_source)

# def load_template_tag(tag_str, context=None):
#     """テンプレートタグを読み出して返す関数"""
#     context = context or {}
#     context = Context(context)
#     return Template(tag_str).render(context)