#!/usr/bin/env python3
#
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from newsdatadb import get_article, get_authors, get_errors

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
    <!DOCTYPE html>
    <html>
        <head>
            <title>DB Forum</title>
        </head>
        <body bgcolor="#E6E6FA">
            <h1 align="center">Results</h1>
            <!-- post content will go here -->
            <hr>
            %s
            <hr><br><br>
            %s
            <hr><br><br>
            %s
            <hr>
            </body>
    </html>

'''

Articles = '''\
    <li>%s - %s views</li>
    '''
Authors = '''\
    <li>%s - %s views</li>
    '''
Logs = '''\
    <li>%s - %s errors</li>
    '''


@app.route('/', methods=['GET'])
def main():
    '''Main page of the forum.'''
    articles = "".join(Articles % (title, num) for title, num in get_article())
    authors = "".join(Authors % (title, num) for title, num in get_authors())
    log = "".join(Logs % (date, result) for date, result in get_errors())
    html = HTML_WRAP % (articles, authors, log)
    return html


@app.route('/', methods=['POST'])
def post():
    '''New post submission.'''
    message = request.form['content']
    add_post(message)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
