import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def upload_s3(df, filename, bucket_name="2021-msia423-huh-dunyeng"):

    df.to_csv('s3://{0}/raw/{1}'.format(bucket_name,filename))
    logger.info("upload dataframe")

def download_s3(filename,bucket_name="2021-msia423-huh-dunyeng"):

    downloaded_df = pd.read_csv('s3://{0}/raw/{1}'.format(bucket_name,filename))
    logger.info("download dataframe")
    return downloaded_df


if __name__ == '__main__':
    # test
    pass