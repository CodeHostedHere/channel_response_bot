
from flask import Flask
from extensions import database

flask_app = Flask(__name__)
database.init_app(flask_app)

db = database.get_db()

from slash_commands import slash_cmds_bp
from messages import messages_bp

flask_app.register_blueprint(slash_cmds_bp)
flask_app.register_blueprint(messages_bp)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)
    # Not working
    db.create_all()