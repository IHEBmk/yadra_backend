from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import  db
from routes.auth import auth_blueprint
from supabase import create_client, Client


from routes.companies import companies_blueprint
from routes.reviews import reviews_blueprint
from routes.categories import categories_blueprint
from routes.response import response_blueprint
from routes.analytics import analytics_blueprint
from routes.accounts import add_blueprint, edit_blueprint, user_blueprint
from waitress import serve

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['DEBUG'] = True
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


app.register_blueprint(analytics_blueprint, url_prefix='/api/analytics')
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(companies_blueprint, url_prefix='/api/companies')
app.register_blueprint(reviews_blueprint, url_prefix='/api/reviews')
app.register_blueprint(categories_blueprint, url_prefix='/api/categories')
app.register_blueprint(response_blueprint, url_prefix='/api/response')
app.register_blueprint(add_blueprint, url_prefix='/api/add')
app.register_blueprint(edit_blueprint, url_prefix='/api/edit')



@app.route("/")
def home():
    return "Yadra"

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
