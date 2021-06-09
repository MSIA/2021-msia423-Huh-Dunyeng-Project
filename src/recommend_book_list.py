import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def recommend_book_list(bookname, df4):
    """
    input: name of the book(str), cleaned dataframe from clean_data() function
    output: ordered df of 10 books that are similar to the input
    """

    book_trait = df4[bookname]
    logger.info("select a subset of dataset with the corresponding book name")
    book_like_bookname = df4.corrwith(book_trait)
    logger.info("calculate correlation with other books")

    ordered_list = pd.DataFrame(book_like_bookname, columns=['Correlation'])
    ordered_list.dropna(inplace=True)
    logger.info("make a ordered list based on the correlation, drop NA values")

    output_df = ordered_list.sort_values('Correlation', ascending=False)[1:11]
    logger.info("output 10 books with highest correlation score excluding the input itself")
    return output_df.reset_index()


if __name__ == '__main__':

    pass
