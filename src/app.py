import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

#global dictionary for storing posts:
posts = {}

comments = {}




@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here


#route number 1: here's a POST method to post a post. 
@app.route("/post", methods = ['POST'])
#input is a json that represents the "title" and contents of post.
def create_post():
    body = json.loads(request.data)

    title = body.get("title")
    link = body.get("link")
    username = body.get("username")

    if title == None or link == None or username == None:
        return json.dumps({"error": "You need to enter every field."}), 400
    
    #if the user enters all info, then increment the id, and create a var "new_post", add new_post to posts[] 
    new_id = len(posts)+1
    new_post = {"id": new_id, "upvotes": 1, "title": title, "link": link, "username": username}
    posts[new_id] = new_post

    return json.dumps(new_post), 201


#route number 2: here's a route to return all posts. basically we are returning all posts stored in the dictionary. 
@app.route("/api/posts/", methods = ['GET'])
def get_posts():
    all_posts = {"posts" : list(posts.values())}
    return json.dumps(all_posts), 200


#route number 3: get a specific post. 
@app.route("/api/posts/<int:user_id>/", methods = ['GET'])
def get_specific_post(user_id):

    retrievedPost = posts.get(user_id)

    #and if no post is found:
    if retrievedPost is None:
        return json.dumps({"error": "Oh, that post doesn't exist."}), 404
    
    return json.dumps(retrievedPost), 200

    


#route number 4: delete a specific post. 
@app.route("/api/posts/<int:user_id>/", methods = ['DELETE'])
def delete_specific_post(user_id):
    removed_post = posts.pop(user_id, None)
    if removed_post is None:
        return json.dumps({"error": "Oh, that post can't be found."}), 404
    
    return json.dumps(removed_post), 200


#route number 5: post a comment for a specific post. 
@app.route("/api/posts/<int:post_id>/comments/", methods = ['POST'])
def post_a_comment(post_id):
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")

    if text == None:
        return json.dumps({"error": "You need to enter something for the comment."}), 400
    if username == None:
        return json.dumps({"error": "We cannot process the username."}), 400
    #comments is a dictionary within the posts dictionary. 

    #if the user enters all info, then increment the id, check if that post exists first. 
    if posts[post_id] is None:
        return json.dumps({"error": "Seems that post does not exist. Try another post!"}), 400
    
    #if the post exists, we need to check if that respective posts comments exist. 
    if comments.get(post_id) == None: 
        #create an empty list for comments[key]
        comments[post_id] = []


    #now append a comment to comments[post_id]
    new_comment_id = len(comments[post_id]) + 1
    new_comment = {"id": new_comment_id, "upvotes": 1, "text": text, "username": username}
    comments[post_id].append(new_comment)
        
    return json.dumps(new_comment), 201


#route number 6: get a specific comment. 
@app.route("/api/posts/<int:user_id>/", methods = ['GET'])
def get_specific_comment(user_id):


    retrievedComment = comments.get(user_id)

    if retrievedComment is None:
        return json.dumps({"error": "Oh, that post doesn't exist."}), 404
    

    return json.dumps(retrievedComment), 200

    


#route number 7: edit a comment
@app.route("/api/posts/<int:pid>/comments/<int:cid>/", methods=['POST'])
def update_comment(pid, cid):


    #check if the post exists. 
    if pid not in posts:
        return json.dumps({"error": "Post not found."}), 404
    
    #check if comments exist for the post. 
    if cid not in comments or len(comments[pid]) < cid:
        return json.dumps({"error": "Comment not found."}), 404
    
    #get the comment body from the request.
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "You need to provide new text for the comment."}), 400
    
    comments[pid][cid - 1]["text"] = text  # Adjust for zero-based index

    return json.dumps(comments[pid][cid - 1]), 200

    

    
    
    
    

     
    





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
