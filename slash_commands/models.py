from extensions import database
from flask import current_app
db = database.get_db()

class Rule(db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(15))
    rule_type = db.Column(db.String(10))
    trigger = db.Column(db.Text())
    message = db.Column(db.Text())
    team_domain = db.Column(db.String(50))
    team_id = db.Column(db.String(50))


    def __repr__(self):
        return f' "{self.message} to {self.trigger} in {self.channel_id} within {self.team_domain}">'

# Also not working
db.create_all(app=current_app)
db.session.commit()