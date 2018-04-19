# "Database code" for the DB Forum.
import psycopg2
import datetime

DBNAME = "news"


def get_article():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select title, count(*) as num from articles "
              "inner join log on concat('/article/', articles.slug) "
              "= log.path where log.status = '200 OK' group by "
              "articles.title order by num desc limit 3")
    posts = c.fetchall()
    db.close()
    return posts


def get_authors():
    """ Returns the the most popular article authors of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, count(*) as num from "
              "authors inner join articles on authors.id "
              "= articles.author inner join log on log.path "
              "like concat('%', articles.slug, '%') where "
              "log.status = '200 OK' group by authors.name "
              "order by num desc")
    author1 = c.fetchall()
    db.close()
    return author1


def get_errors():
    """Returns the day on which more than 1% of requests lead to errors."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select day, avg from (select day"
              ", round((sum(status)/(select count(*) from "
              "log where (time::date) = day) * 100), 2) as "
              "avg from (select (time::date) as day, count(*) "
              "as status from log where status like '%404%' "
              "group by day) as percent group by day order "
              "by avg desc) as result where avg >= 1")
    error = c.fetchall()
    db.close()
    return error
