from flask import (render_template, request, Blueprint)
from flaskblog.models import Post, Comment
import joblib
import os

collector = Blueprint('collector', __name__)

@collector.route('/comments', methods=['GET','POST'])
def comments():
    post_title = ""
    comments = []
    if request.method == 'POST':
        post_id = request.form['post_id']
        post = Post.query.get(post_id)
        post_title = post.title
        comments = Comment.query.filter_by(post_id=post_id).all()
        # load the pre-trained model
        model = joblib.load(os.path.join(os.getcwd(), "flaskblog", "collector", "SVMMODEL.joblib"))
        # classify the comments
        for comment in comments:
            prediction = model.predict([comment.text])
            comment.sentiment = prediction
    return render_template('comments.html', comments=comments, post_title=post_title)
