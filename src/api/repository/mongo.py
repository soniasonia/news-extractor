def save_articles(mongo, data):
    mongo.db.articles.insert(data)
