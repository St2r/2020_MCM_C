import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
from bs4 import BeautifulSoup

porter_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stopWords = set(nltk.corpus.stopwords.words('english'))
stopWords.add(("'s", "'re", "...", ",", ".", "!", "?", "n't", "'t", "'ll", "'ve"))


def word_generator(tagged_words: list):
    for word, tag in tagged_words:
        if tag.startswith('NN'):
            yield lemmatizer.lemmatize(word, pos='n')
        elif tag.startswith('VB'):
            yield lemmatizer.lemmatize(word, pos='v')
        elif tag.startswith('JJ'):
            yield lemmatizer.lemmatize(word, pos='a')
        elif tag.startswith('R'):
            yield lemmatizer.lemmatize(word, pos='r')
        else:
            yield word


def modify_sentence(sentence: str) -> list:
    sentence = delete_last_punctuation(sentence).lower()
    modified_words = list()
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
    words = word_generator(tagged_words)
    # print(tagged_words)
    temp = ''
    for w in words:
        # 去除连续重复项
        # 停用词过滤 ->
        if w not in stopWords and w != temp:
            modified_words.append(w)
            temp = w
    return modified_words


def delete_last_punctuation(s: str):
    p = {',', '.', '!', '?', '"'}
    while s != '' and s[-1] in p:
        s = s[:-1]
    return s


def sentence_contained(sen1: list, sen2: list) -> bool:
    unique_sen1 = 0
    common = 0
    for i in sen1:
        if i in sen2:
            common += 1
        else:
            unique_sen1 += 1
    if unique_sen1 == 0:
        return True
    return False


def modify_review(review: str) -> str:
    l1 = len(review)
    # sentences = re.split(pattern=r'\. |\? |! |, ', string=review)
    sentences = nltk.sent_tokenize(review)
    words = list()
    for sentence in sentences:
        words.append(modify_sentence(sentence))
    modified_sentences = list()
    for i in range(len(words)):
        not_contained = True
        for j in range(i + 1, len(words)):
            if sentence_contained(words[i], words[j]):
                not_contained = False
                break
        if not_contained:
            modified_sentences.append(' '.join(words[i]) + '.')
    out = ' '.join(modified_sentences)
    if l1 - len(out) > 20:
        print('???')
    return out


def split_review(review: str) -> str:
    review = BeautifulSoup(review).get_text()
    sentences = re.split(pattern=r'\. |\? |! |, ', string=review)
    words = list()
    for sentence in sentences:
        words.append(modify_sentence(sentence))
    modified_sentences = list()
    for i in range(len(words)):
        not_contained = True
        for j in range(i + 1, len(words)):
            if sentence_contained(words[i], words[j]):
                not_contained = False
                break
        if not_contained:
            modified_sentences.append(' '.join(words[i]))
    out = ' '.join(modified_sentences)
    return out


m = modify_sentence("""She was told apples are bad""")
