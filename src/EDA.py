import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_data(file="data/good_reads_final.csv"):
    try:
        df1 = pd.read_csv(file)
        logger.info("read df")
    except FileNotFoundError:
        df1 = pd.read_csv("/usr/src/"+file)
    return df1


def clean_data(df1):
    # Data Cleansing

    df1 = df1.replace(r'\n', '', regex=True)
    logger.info("get rid of '\n' in the title")

    df1['book_title'] = df1['book_title'].str.strip()
    logger.info("get rid of space in the title")

    genre1 = df1.genre_1.value_counts().reset_index()
    popular_genre1 = [i for i in genre1['index'].head(40)]
    logger.info("Limit the number of Genres to consider to 40.")

    df2 = df1[['book_title', 'author_average_rating', 'num_ratings', 'num_reviews', 'book_average_rating', 'genre_1']]
    df2['genre_1'] = df2.genre_1.apply(lambda x: x if x in popular_genre1 else 'other')
    df3 = pd.get_dummies(df2, columns=['genre_1'], drop_first=True)
    logger.info("Build and add a dummy column for the categorical column:'Genre'")

    df3['num_ratings'] = (df3['num_ratings'] - df3['num_ratings'].min()) / (
            df3['num_ratings'].max() - df3['num_ratings'].min())
    df3['num_reviews'] = (df3['num_reviews'] - df3['num_reviews'].min()) / (
            df3['num_reviews'].max() - df3['num_reviews'].min())
    df3['author_average_rating'] = (df3['author_average_rating'] - df3['author_average_rating'].min()) / (
            df3['author_average_rating'].max() - df3['author_average_rating'].min())
    df3['book_average_rating'] = (df3['book_average_rating'] - df3['book_average_rating'].min()) / (
            df3['book_average_rating'].max() - df3['book_average_rating'].min())
    logger.info("Normalization")

    df4 = df3.pivot_table(columns='book_title')
    logger.info("return pivoted data")
    return df4



if __name__ == '__main__':
    pass
