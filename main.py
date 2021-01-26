from app import db, create_app
import os

stage = os.getenv('STAGE')

app = create_app(stage)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(host=app.config['HOST'],
            port=app.config['PORT'], debug=app.config['DEBUG'],)
