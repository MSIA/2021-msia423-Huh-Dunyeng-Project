# MSiA423 Template Repository

### Author: Dunyeng Huh
### QA: Dennis Zhao

## Charter

### Vision
- Reading is a splendid and traditional hobby that is slowly losing its place due to the blooming show industries and the success of video streaming platforms. However, the abundance of shows and movies might only be a factor why people are not reading books. While video streaming platforms have had enormous success due to their recommendation systems, we have not yet seen one for good reads! The goal of this application is to recommend books to its users, so that users can easily enjoy a good read and re-gain the habit of reading.  

### Mission
- Users will enter 2-3 books that they have enjoyed in the past. The recommendation system would output 2~3 books that will likely match the users' taste.
The main dataset comes from GoodReads(https://www.goodreads.com/list/show/1.Best_Books_Ever).

### Success criteria
- 1. Since we are working with unsupervised data and do not know how highly users will rate the book, the app will focus on 'Coverage' and 'Popularity' as the main criteria. We want the model to be able to cover 20% of the dataset to give a recommendation. Additionally, as high-rated books are more likely to be enjoyable to many, we want to calculate popularity by looking at the percentage of users who rate the item. 

- 2. Business Metric: The app will show users the name of the book and link to the site where the user can purchase the book. In the longrun, we would like to record the click-through rate of the link and sales conversion rate as well. 



..
=======
## Data Aquisition
The data can be downloaded via Kaggle's "goodreads books/author data" page. The data was gathered by webscraping goodreads website.
Proper citation and source of the data is added below. 
Ben Rosen (2019, January), goodreads books/author data, Version 1. Retrieved April 2nd, 2021 from https://www.kaggle.com/brosen255/goodreads-books.
https://www.kaggle.com/jealousleopard/goodreadsbooks


## Using the Application
1) User selects a book that he/she has enjoyed from a drop down menu 
2) Given the input, the book recommender model provides a recommendation to the user


<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Build the docker image 

Build the Docker Image before running all the functionalities within this app 

`docker build -t dhl454msia423 .`

### 2. Data ingestion and storage
To acquire the data (if applicable) and land it in S3, you can either 

1) directly download from https://www.goodreads.com/list/show/1.Best_Books_Ever   to your s3
2) use this line of code

`docker run -it     -e AWS_ACCESS_KEY_ID=KEY     -e AWS_SECRET_ACCESS_KEY=SECRET KEY     dhl454msia423 run.py s3 --download upload`


#### 3. Create the database 
To create the table in local SQLlite repo 

`docker run -it  dhl454msia423 run.py create_db`


#### 4. Database Insertion
To store the data inside S3 into a database of your choice using default settings, run the following code:

`docker run -it \
    -e MYSQL_HOST=url \
    -e MYSQL_PORT=3306 \
    -e MYSQL_USER=user \
    -e MYSQL_PASSWORD=psw \
    -e MYSQL_DATABASE=msia423_db \
    -e AWS_ACCESS_KEY_ID=keyid \
    -e AWS_SECRET_ACCESS_KEY=key \
    dhl454msia423 Create_database.py create_db`


### 5. Database operations
To create new users inside the database, run:

```SQL
CREATE USER 'msia423instructor'@'%' IDENTIFIED BY 'password';
```

### 6. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill dhl454msia423 
```


```
 
