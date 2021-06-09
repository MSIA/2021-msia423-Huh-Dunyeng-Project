import pandas as pd
import logging
from botocore.exceptions import ParamValidationError, ClientError

logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def upload_s3(df, filename, bucket_name="2021-msia423-huh-dunyeng"):
    """ Save dataframe to S3
    Arg: Dataframe(df), filename(str), bucket_name(str)

    """
    try:
        df.to_csv('s3://{0}/{1}'.format(bucket_name,filename), index=False)
        logger.info("upload dataframe to s3")
    except (ClientError, ParamValidationError):
        logger.error("ClientError or ParamValidationError occured")


def download_s3(filename,bucket_name="2021-msia423-huh-dunyeng"):
    """ Download dataframe from S3
    Arg: filename(str), bucket_name(str)

    """
    try:
        downloaded_df = pd.read_csv('s3://{0}/{1}'.format(bucket_name,filename))
        logger.info("download dataframe from s3")
        return downloaded_df
    except (ClientError, ParamValidationError):
        logger.error("ClientError or ParamValidationError occured")


if __name__ == '__main__':
    # test
    pass