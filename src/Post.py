class Post:

    def __init__(self, post_id, title, content):
        self.id = post_id #ID of the post
        self.title = title #title of the post
        self.content = content #content of the post
        self.comments = [] #instance variable to store the comments of each post object. 

