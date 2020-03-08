from textblob import TextBlob
import pandas as pd


def get_data(category: str):
    data_path = '../data/save/{0}_cleaned.tsv'.format(category)
    return pd.read_csv(data_path, sep='\t')


def get_sentiment(review:str):
    blob = TextBlob(review)
    return blob.sentiment.polarity,blob.sentiment.subjectivity


def save_date(src:pd.DataFrame,category):
    output_file_path = "../data/save/blob_mark/{0}_marked.csv".format(category)
    src = pd.DataFrame(src[['star_rating', 'review_body', 'vine']])
    src.to_csv(output_file_path, index=False)
