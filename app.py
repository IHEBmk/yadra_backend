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
@app.route('/api/get_recomendation' , methods=['POST'])
def Get_recomendations():
    data=request.form
    speciality=data['speciality']
    moyenne=calculate_moyenne(speciality,data)
    if speciality=='' or speciality==None or speciality=='N00':
        return jsonify({'error':'Please enter a speciality'})
    cluster=Find_cluster(speciality,data)
    Recomendations=Recomendations(speciality,moyenne,cluster)
    return jsonify({'Recomendations':Recomendations})
        
        

def calculate_moyenne(speciality,data):
    coeficients=[]
    if speciality=='N00':
        return -1
    elif speciality=='N01':
        coeficients=[6,3,3,4,2,2,6]
    elif speciality=='N02':
        coeficients=[5,5,5,3,2,4,2,2]
    elif speciality=='N03':
        coeficients=[3,2,2,2,2,5,6,5,2]
    elif speciality=='N04':
        coeficients=[3,2,2,2,2,7,2,6,2]
    elif speciality=='N05':
        coeficients=[2,2,2,2,2,6,7,2]
    elif speciality=='N06':
        coeficients=[3,2,2,4,2,5,2,5,6,2]
    if 'sport_mark' in data.keys():
        coeficients.append(1)
    
        
    moyenne=0
    i=0
    for subject in data.keys():
        if subject=='amazigh_mark':
            continue 
        if i>len(coeficients)-1:
            break
        if subject=='speciality':
            continue
        
        if data[subject]==None:
            return -1
        moyenne+=data['subject']*coeficients[i]
        i+=1
    sum_of_coeficients=sum(coeficients)
    if sum_of_coeficients==0:
        return -1
    moyenne=moyenne/sum_of_coeficients
    return moyenne



def Find_cluster(speciality,data):
    
    if speciality=="N04":
        try:
            with open("orientation_mapping_maths.json", "r") as json_file:
                json_data = json.load(json_file)
            cluster_centroids = np.array(json_data["centroids"])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print("Error: Unable to load centroids from orientation_mapping_maths.json")
            cluster_centroids = np.array([])
        weights = {
    'ANGLAIS': 4,
    'FRANÇAIS': 4,
    'LITTERATURE_ARABE': 9,
    'MATHEMATIQUE': 49,
    'PHYSIQUE': 36,
    'SNV': 4,
    'HISTOIRE_GEOGRAPHIE': 4,
    'SCIENCE ISLAMIQUE': 4,
    'PHILOSOPHIE': 4,
    'E.P.S': 0.0001,
    'LANGUE_AMAZIGH': 0.0001
}
    
    new_record = {
    'ANGLAIS': data['Anglais'],
    'FRANÇAIS': data['Français'],
    'LITTERATURE_ARABE': data['Arabe'],
    'MATHEMATIQUE': data['Mathématiques'],
    'PHYSIQUE': data['Physique'],
    'SNV': data['Science'],
    'HISTOIRE_GEOGRAPHIE': data['Histoire Géographie'],
    'SCIENCE_ISLAMIQUE': data['Education Islamique'],
    'PHILOSOPHIE': data['Philosophie'],
    'LANGUE_AMAZIGH': 0
}
    if 'spoort_mark' in data.keys():
        new_record['E.P.S'] = data['sport_mark']

# Apply the same weights to the new record
    for subject, weight in weights.items():
        if subject in new_record:
            new_record[subject] = new_record[subject] * weight

    # Convert new record to a DataFrame (same structure as original data)
    new_record_df = pd.DataFrame([new_record])

    if cluster_centroids.size > 0:
        # Calculate distances from the new record to each centroid
        distances = euclidean_distances(new_record_df, cluster_centroids)

        # Find the closest cluster (the one with the minimum distance)
        closest_cluster = np.argmin(distances)
        print(f"The new record is assigned to cluster: {closest_cluster}")
    else:
        print("No centroids available to assign a cluster.")
    
    
    
    
def Recomendations(speciality,moyenne,cluster):
    Recomendations=[]
    try:
            with open("specialities__univ_map.json", "r") as json_file:
                json_data = json.load(json_file)
            Etablissements=json_data[speciality]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print("Error: Unable to load Fillieres from specialities__univ_map.json")
    try:
            with open("orientation_mapping_maths.json", "r") as json_file:
                json_data = json.load(json_file)
            cluster=json_data[cluster]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):             
            print("Error: Unable to load centroids from orientation_mapping_maths.json")  
    for Suggestion in cluster:
        if len(Recomendations)>=5:
            break
        if Suggestion[0][1] in Etablissements.keys() and Suggestion[0][0] in Etablissements[Suggestion[0][1]] and moyenne>=Suggestion[3]:
            Recomendations.append(Suggestion)
    return Recomendations

@app.route("/")
def home():
    return "Yadra"

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
