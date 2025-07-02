from app import app
from models import db, Newsletter

with app.app_context():
    Newsletter.query.delete()

    n1 = Newsletter(title="Newsletter 1", body="This is the first newsletter.")
    n2 = Newsletter(title="Newsletter 2", body="This is the second newsletter.")
    n3 = Newsletter(title="Newsletter 3", body="This is the third newsletter.")

    db.session.add_all([n1, n2, n3])
    db.session.commit()

    print(" Seeded newsletters!")
