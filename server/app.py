#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Root index route
class Index(Resource):
    def get(self):
        return make_response({"index": "Welcome to the Newsletter RESTful API"}, 200)

api.add_resource(Index, '/')

# Collection route: /newsletters
class Newsletters(Resource):
    def get(self):
        all_newsletters = Newsletter.query.all()
        response = [n.to_dict() for n in all_newsletters]
        return make_response(response, 200)

    def post(self):
        new_newsletter = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        db.session.add(new_newsletter)
        db.session.commit()
        return make_response(new_newsletter.to_dict(), 201)

api.add_resource(Newsletters, '/newsletters')

# Item route: /newsletters/<id>
class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        return make_response(record.to_dict(), 200)

    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])
        db.session.add(record)
        db.session.commit()
        return make_response(record.to_dict(), 200)

    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        db.session.delete(record)
        db.session.commit()
        return make_response({"message": "record successfully deleted"}, 200)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
