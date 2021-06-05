import pandas as pd


def recommend_book_list(bookname, df4):
    """
    input: name of the book(str)
    output: ordered df of 10 books that are similar to the input
    """

    book_trait = df4[bookname]
    book_like_bookname = df4.corrwith(book_trait)

    ordered_list = pd.DataFrame(book_like_bookname, columns=['Correlation'])
    ordered_list.dropna(inplace=True)
    # corr_temp.head()
    output_df = ordered_list.sort_values('Correlation', ascending=False)[1:11]
    return output_df.reset_index()


if __name__ == '__main__':

    pass
