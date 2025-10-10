import json

def split_data(data):
    p_json = json.loads(data)

    count = p_json["count"]
    posts = p_json["data"]
    query = p_json["query"]
    success = p_json["success"]

    return count, posts, query, success

def format_data(data):
    post_titles = [post["title"] for post in data]
    post_links = [post["url"] for post in data]

    return post_titles, post_links



# https://open.spotify.com/track/70vjXI7oBou5buTtgiJeRW?si=25640cc4243c4bf3
