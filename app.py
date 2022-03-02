from enum import unique
from flask import Flask,  request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from flask.views import MethodView
from datetime import datetime
from app import errors
import jsonschema



app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def home():
    return "Hello, flask!"

def check_health():
    return jsonify({
        "status": "ok"
        })


class BaseModel():
    @classmethod
    def id(cls, object_id):
        object = cls.query.get(object_id)
        if object:
            return object
        else:
            raise errors.CantFindIt

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.NoLuck
    
    def adds(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.NoLuck


class UserModelAd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    text =  db.Column(db.Text, index=True, nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_of_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ads', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.dtext,
            'created_at': self.date_of_creation,
        }


class ViewForAdds(MethodView):

    def get(self, ad_id):
        add = UserModelAd.by_id(ad_id)
        return jsonify(add.to_dict())

    def post(self):
        add = UserModelAd(**request.json)
        add.add()
        return jsonify(add.to_dict())

    def delete(self, ad_id):
        add = UserModelAd.by_id(ad_id)
        add.delete()
        return jsonify({'message': f'Ad was deleted'})


app.add_url_rule('/', view_func=home, methods=['GET'])
app.add_url_rule('/check_health', view_func=check_health, methods=['GET'])

app.add_url_rule('/ads/', view_func=ViewForAdds.as_view('ads_create'), methods=['POST', ])
app.add_url_rule('/ads/<int:ad_id>', view_func=ViewForAdds.as_view('ads_get'), methods=['GET', ])
app.add_url_rule('/ads/<int:ad_id>', view_func=ViewForAdds.as_view('ads_delete'), methods=['DELETE', ])


#if __name__ == '__main__':
#    db.create_all()
#    app.run(debug=True)