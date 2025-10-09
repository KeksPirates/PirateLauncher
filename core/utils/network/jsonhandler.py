def split_data(data):
    json = json.loads(data)

    count = json["count"]
    posts = json["data"]
    query = json["query"]
    success = json["success"]

    return count, posts, query, success

