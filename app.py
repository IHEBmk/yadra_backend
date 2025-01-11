import random
import secrets
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
import requests
from models import  OTP, db
from routes.auth import auth_blueprint

from supabase import create_client, Client
TEST_IP = "8.8.8.8"  
USE_TEST_IP = False   # Set to True to use test IP

def get_public_ip():
    if USE_TEST_IP:
        return TEST_IP
        
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except Exception as e:
        return None

from routes.companies import companies_blueprint
from routes.reviews import reviews_blueprint
from routes.categories import categories_blueprint
from routes.response import response_blueprint
from routes.analytics import analytics_blueprint
from routes.accounts import add_blueprint, edit_blueprint, user_blueprint
from waitress import serve
from flask_mail import Mail



app = Flask(__name__)
app.config.from_object('config.Config')
app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 587  # Use the correct port
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mekidecheiheb900@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'azdm xlzf ddgl vcch'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'mekidecheiheb900@gmail.com'  # Default sender email

mail = Mail(app)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 587  # Use the correct port
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mekidecheiheb900@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'azdm xlzf ddgl vcch'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'mekidecheiheb900@gmail.com'  # Default sender email

mail = Mail(app)

app.register_blueprint(analytics_blueprint, url_prefix='/api/analytics')
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(companies_blueprint, url_prefix='/api/companies')
app.register_blueprint(reviews_blueprint, url_prefix='/api/reviews')
app.register_blueprint(categories_blueprint, url_prefix='/api/categories')
app.register_blueprint(response_blueprint, url_prefix='/api/response')
app.register_blueprint(add_blueprint, url_prefix='/api/add')
app.register_blueprint(edit_blueprint, url_prefix='/api/edit')

@app.route('/send-otp_email', methods=['POST'])
def send_confirmation_code():
    data = request.get_json()

    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Generate a 6-digit confirmation code
    confirmation_code = str(random.randint(100000, 999999))

    # Create the email content
    msg = Message('Your Confirmation Code', recipients=[email])
    msg.body = f"Your confirmation code is: {confirmation_code}"

    try:
        # Send the email
        new_otp=OTP(otp=confirmation_code,email=email)
        db.session.add(new_otp)
        db.session.commit()
        mail.send(msg)
        # Store the code in the session or database to verify later (this is just an example)
        # Example: store the code in some temporary storage like a session or DB
        # session['confirmation_code'] = confirmation_code

        return jsonify({"message": "Confirmation code sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-location')
def get_location():
    try:
        client_ip = get_public_ip()
        
        if not client_ip:
            return jsonify({
                'error': 'Could not determine public IP',
                'details': 'Failed to lookup public IP address'
            }), 500

        response = requests.get(f'http://ip-api.com/json/{client_ip}')
        data = response.json()
        
        if data['status'] == 'success':
            location_data = {
                'ip': client_ip,
                'country': {
                    'name': data['country'],
                    'iso_code': data['countryCode']
                },
                'city': {
                    'name': data['city'],
                    'region': data['regionName'],
                    'region_code': data['region']
                },
                'location': {
                    'latitude': data['lat'],
                    'longitude': data['lon']
                },
                'timezone': data['timezone'],
                'isp': data['isp'],
                'org': data['org']
            }
            return jsonify(location_data)
        else:
            return jsonify({
                'error': 'Location lookup failed',
                'details': data.get('message', 'Unknown error'),
                'ip': client_ip
            }), 404

    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'details': str(e)
        }), 500

@app.route("/")
def home():
    return "Yadra"

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
