import re
import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for
from config.flaskconfig import DB_HOST, DB_PORT, DB_USER, DB_PW, DATABASE, SQLALCHEMY_DATABASE_URI


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
from src.Create_database import Bookshelf, BookshelfManager, read_table
from src.recommend_book_list import recommend_book_list
from src.EDA import get_data, clean_data

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# bookshelf_manager = BookshelfManager(app)



# Purpose of the below functions
# 1) Read data from s3 thru "get_data()"
# 2) preprocess data using "clean_data()"
# 3) Take user input + cleaned data to make a final recommendation
# 4) Show the result


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['GET', 'POST'])
def data():
    #df1 = get_data()
    #df4 = clean_data(df1)
    URI = re.sub(r'sqlite:///','',SQLALCHEMY_DATABASE_URI)

    df1 = read_table("select * from msia423_db.raw_table1", DB_HOST, DB_USER, DB_PW, DATABASE, DB_PORT, URI)
    df4 = clean_data(df1)

    if request.method == 'POST':
        # user_input = request.form.get("book_name")
        user_input = request.form.to_dict()['book_name']
        user_input = str(user_input)
        # print(user_input)
        try:
            recommendation = recommend_book_list(user_input, df4)
            # print(recommendation)
            # recommendation = recommendation.to_html(classes='dataframe', header="true", index=False)

            if len(recommendation) == 0:
                return render_template('not_found.html', user_input=user_input)
            else:
                return render_template("index.html", recommendation=recommendation, user_input=user_input)

        except:
            traceback.print_exc()
            logger.warning("Not able to display recommendations, error page returned")
            return render_template('error.html')


@app.route('/error/')
def add_entry():
    """View that process a POST with book input
    :return: redirect to index page
    """
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
