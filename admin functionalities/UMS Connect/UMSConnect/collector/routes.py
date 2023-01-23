from flask import (render_template, request, Blueprint, session)
from UMSConnect.models import Post, Comment
import joblib
import os

collector = Blueprint('collector', __name__)


@collector.route('/comments/<int:post_id>', methods=['GET','POST'])
def comments(post_id):
    post_title = ""
    comments = []
    post = Post.query.get(post_id)
    post_title = post.title

    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(post_id=post_id).paginate(page=page, per_page=5)
        # load the pre-trained model
    model = joblib.load(os.path.join(os.getcwd(), "UMSConnect", "collector", "SVMMODEL.joblib"))
        # classify the comments
    for comment in comments:
        prediction = model.predict([comment.text])
        comment.sentiment = prediction
    return render_template('comments.html', comments=comments, post_title=post_title, post_id=post_id)

