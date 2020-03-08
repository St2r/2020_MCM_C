import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import split_words

input_file_path = "data/microwave.tsv"
review_pos_path = "data/save/microwave_pos_review.txt"
review_neg_path = "data/save/microwave_neg_review.txt"


def drop_useless(src: pd.DataFrame):
    useless_columns = ['marketplace', 'customer_id', 'product_id', 'product_title', 'product_category']
    src.drop(columns=useless_columns, inplace=True)


def format_headline(s: str):
    comma = {'.', ',', '?', '!'}
    if not s[-1] in comma:
        s += '.'
    s += ' '
    return s


def select_neg_review():
    data_neg = data[(data['star_rating'] == 1)|(data['star_rating'] == 2)]
    review_neg = data_neg['review_headline'].apply(format_headline) + data_neg['review_body']
    review_neg = review_neg.apply(split_words.split_review)
    review_neg = pd.DataFrame(review_neg)

    for i, w in review_neg.iterrows():
        if w[0] == '':
            review_neg.drop(i, inplace=True)
    review_neg.to_csv(review_neg_path, index=False, header=False, encoding='utf-8')


def select_pos_review():
    data_pos = data[(data['star_rating'] == 5)|(data['star_rating'] == 4)]
    review_pos = data_pos['review_headline'].apply(format_headline) + data_pos['review_body']
    review_pos = review_pos.apply(split_words.split_review)
    review_pos = pd.DataFrame(review_pos)

    for i, w in review_pos.iterrows():
        if w[0] == '':
            review_pos.drop(i, inplace=True)
    review_pos.to_csv(review_pos_path, index=False, header=False, encoding='utf-8')


if __name__ == '__main__':
    data = pd.read_csv(input_file_path, sep='\t')
    drop_useless(data)
    select_neg_review()
    select_pos_review()

