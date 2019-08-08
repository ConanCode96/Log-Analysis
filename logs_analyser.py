#!/usr/bin/env python3


import psycopg2


def ask_database(req):
    try:
        connection = psycopg2.connect(database="news")
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute(req)
    res = cursor.fetchall()
    connection.close()
    return res


fetch_articles = """select articles.title, count(*) as counter
            from log, articles
            where articles.slug = substr(log.path, 10)
            group by articles.title
            order by counter desc
            limit 3;"""


fetch_authors = """select authors.name, count(*) as counter
            from articles, authors, log
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            and authors.id = articles.author
            group by authors.name
            order by counter desc;
            """

fetch_failureRate = """select time, failRate
            from rate
            where failRate > 1;
            """


def first_question():
    res = ask_database(fetch_articles)

    print("\n\t" + "Top 3 articles of all time" + "\n")

    for title, freq in res:
        print("\"{}\" -- {} views".format(title, freq))


def second_question():
    res = ask_database(fetch_authors)

    print("\n\t" + "Top authors of all time" + "\n")

    for name, freq in res:
        print("{} -- {} views".format(name, freq))


def thrid_question():
    res = ask_database(fetch_failureRate)

    print("\n\t" + "Days with more than one percentage of bad requests" + "\n")

    for day, rate in res:
        print("""{0:%B %d, %Y}
            -- {1:.2f} % errors""".format(day, rate))


if __name__ == '__main__':
    first_question()
    second_question()
    thrid_question()
