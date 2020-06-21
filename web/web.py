import flask
from common import db

from common.db import (articles, users)


DB_DSN = "dbname=artsql"
app = flask.Flask(__name__)
connection = db.create_connection(DB_DSN)


@app.route("/articles")
def show_all_articles():
    all_articles = articles.get_articles(connection)
    all_users = users.get_all_users(connection)
    return flask.render_template('form.html',
                                 articles=all_articles,
                                 users=all_users)


@app.route("/map-user-post", methods=['POST'])
def map_user_to_articles_post():
    user_id = flask.request.form.get("user_id")
    article_id = flask.request.form.get("article_id")
    # args = flask.request.args
    # user_id = args["user_id"]
    # article_id = args["article_id"]
    mapped = users.assign_user_to_article(
        connection,
        user_id,
        article_id
    )
    return flask.jsonify(mapped)


if __name__ == "__main__":
    app.run(use_reloader=1)
