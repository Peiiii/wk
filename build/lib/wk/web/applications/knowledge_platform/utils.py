import jieba
from wk import string_utils as TU
def get_keywords(text):
    keywords = list(jieba.cut_for_search(text))
    keywords = list(filter(lambda word: TU.is_all_chinese(word) or TU.is_all_alphabet_or_digit(word), keywords))
    keywords = list(set(keywords))
    return keywords