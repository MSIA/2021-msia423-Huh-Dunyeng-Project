import argparse
import os
from src import to_s3, EDA, Create_database
import logging

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('book-recommender-pipeline')

from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')
    logger.info("Add parsers for both creating a database and adding songs to it")

    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")
    sb_create.add_argument("--tablename", default="df4",
                           help="Name")
    logger.info("Create sub-parser creating database")

    sb_ingest = subparsers.add_parser("s3", description="upload or download data to database")
    sb_ingest.add_argument("--filename", default="df", help="filename to be inserted into s3")
    sb_ingest.add_argument("--bucket_name", default="2021-msia423-huh-dunyeng", help="bucket name in s3")

    sb_ingest.add_argument("--download", default="download", help="download")
    sb_ingest = subparsers.add_parser("s3_download", description="Add data to database")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/bookshelf.db',
                           help="SQLAlchemy connection URI for database")
    logger.info("Create sub-parser ingesting new data")

    print(os.getcwd())
    df1 = EDA.get_data()

    logger.info("Read Data")
    args = parser.parse_args()
    sp_used = args.subparser_name
    df4 = EDA.clean_data(df1)
    logger.info("Outputs a clean data after preprocessing")

    if sp_used == 'create_db':
        Create_database.create_db(args.engine_string)
    elif sp_used == 's3':
        if args.download == 'download':
            df2 = to_s3.download_s3(args.filename, args.bucket_name)
            logger.info("if given the condition download, download from s3")
        else:
            to_s3.upload_s3(df1, args.filename, args.bucket_name)
            logger.info("if not, upload to s3")
    else:
        parser.print_help()
