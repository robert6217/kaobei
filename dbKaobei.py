from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://jsqtlknuyihbuh:064c73f01072edf9414df18dd4ea7814f9d290d55355a31a8b792f630296fcf7@ec2-54-235-206-118.compute-1.amazonaws.com:5432/d9mb5esa80jgth'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class KaobeiID(db.Model):
    __tablename__ = 'KaobeiID'

    ID = db.Column(db.Integer, primary_key=True)
    FansPageID = db.Column(db.String(100), unique=True, nullable=False)
    KaobeiName = db.Column(db.String(64), nullable=False)
    KaobeiPicture = db.Column(db.String(50), nullable=False)

    def __init__(self, FansPageID, KaobeiName, KaobeiPicture):
        self.FansPageID = FansPageID
        self.KaobeiName = KaobeiName
        self.KaobeiPicture = KaobeiPicture

class KaobeiData(db.Model):
    __tablename__ = 'KaobeiData'

    ID = db.Column(db.Integer, primary_key=True)
    PageID = db.Column(db.String(100), db.ForeignKey('KaobeiID.FansPageID'), nullable=False, )
    PostID = db.Column(db.String(200), nullable=False)
    PostTime = db.Column(db.DateTime, nullable=False)
    PostMessage = db.Column(db.String(10000))
    PostLink = db.Column(db.String(50))
    PostLike = db.Column(db.Integer, nullable=False)
    PostComment = db.Column(db.Integer, nullable=False)
    PostShare = db.Column(db.Integer, nullable=False)

    def __init__(self, PageID, PostID, PostMessage, PostLink, PostTime, PostLike, PostComment, PostShare):
        self.PageID = PageID
        self.PostID = PostID
        self.PostTime = PostTime
        self.PostMessage = PostMessage
        self.PostLink = PostLink
        self.PostLike = PostLike
        self.PostComment = PostComment
        self.PostShare = PostShare

    page = db.relationship('KaobeiID',backref=db.backref('pages'))
if __name__ == '__main__':
    manager.run()