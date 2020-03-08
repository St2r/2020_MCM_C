import pandas as pd
import split_words


def get_data(category: str):
    input_file_path = "../data/{0}.tsv".format(category)
    return pd.read_csv(input_file_path, sep='\t')


def select_verified_purchase(src: pd.DataFrame):
    l1 = src.shape[0]
    for i, x in src.iterrows():
        if not (x['verified_purchase'] == 'Y' or x['verified_purchase'] == 'y'):
            src.drop(i, inplace=True)
    l2 = src.shape[0]
    print('{0} reviews are deleted by select_verified_purchase'.format(l1 - l2))
    return src


def force_clean_same(src: pd.DataFrame):
    l1 = src.shape[0]
    src.drop_duplicates(subset=['review_headline', 'review_body'], inplace=True)
    l2 = src.shape[0]
    print("{0} reviews are deleted by force_clean_same".format(l1 - l2))
    return src


def compress_repeat_sentence(src: pd.DataFrame):
    for i, x in src.iterrows():
        review = x['review_body']
        src.loc[i, 'review_body'] = split_words.modify_review(review)
    return src


def clean_shout_review(src: pd.DataFrame):
    l1 = src.shape[0]
    for i, x in src.iterrows():
        if len(x['review_body']) < 15:
            src.drop(i, inplace=True)
    l2 = src.shape[0]
    print('{0} reviews are deleted by clean_shout_review'.format(l1 - l2))
    return src


def save_date(src: pd.DataFrame, category: str):
    output_file_path = "../data/save/{0}_cleaned.csv".format(category)
    src = pd.DataFrame(src[['star_rating', 'review_body', 'vine', 'helpful_votes']])
    src.to_csv(output_file_path, index=False)


category = 'microwave'
data = get_data(category)
# 筛选确认购买的
out = select_verified_purchase(data)
# 筛选完全相同的评论
out = force_clean_same(out)
# 单条评论去重
# out = compress_repeat_sentence(out)
# 筛选评论长度过短的
out = clean_shout_review(out)

save_date(out, 'microwave')
