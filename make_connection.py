import os
import sqlalchemy
# the engine_string format
#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}"
conn_type = "mysql+pymysql"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("DATABASE_NAME")
engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"
# print(engine_string)  # Enable this line if you need to debug, but use caution as it prints your password
engine = sqlalchemy.create_engine(engine_string)


conn = mysql.connector(connect(host="msia423-db.cmkqywpn0cl9.us-east-1.rds.amazonaws.com"))