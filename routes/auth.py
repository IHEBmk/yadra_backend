from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from config import supabase
from schemas import RegisterSchema
from models import  User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError



auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": {"code": "INVALID_INPUT", "message": "Invalid input", "details": err.messages}}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": {"code": "EMAIL_EXISTS", "message": "Email already registered", "details": {"field": "email"}}}), 400

    response = supabase.auth.sign_up(email=data['email'], password=data['password'])
    supabase_user_id = response['user']['id']
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        supabase_id=supabase_user_id,
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        phone=data.get('phone'),
        role = data.get('role'),
        avatar = data.get('avatar'),
        created_at = datetime.now(),
        last_login = datetime.now(),
        state = 0
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))

    return jsonify({
                            "user": {
                "phone": user.phone,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "avatar": user.avatar
            },
        "token": token
    }), 201

@auth_blueprint.route('/register_user', methods=['POST'])
def register_user():
    schema = RegisterSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": {"code": "INVALID_INPUT", "message": "Invalid input", "details": err.messages}}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": {"code": "EMAIL_EXISTS", "message": "Email already registered", "details": {"field": "email"}}}), 400
    response = supabase.auth.sign_up(email=data['email'], password=data['password'])
    supabase_user_id = response['user']['id']
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        supabase_id=supabase_user_id,
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        phone=data.get('phone'),
        role = 2,
        avatar = data.get('avatar'),
        created_at = datetime.now(),
        last_login = datetime.now(),
        state = 0
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))

    return jsonify({
        "token": token,
                    "user": {
                "phone": user.phone,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "avatar": user.avatar
            }
    }), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('remember_me', False)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    response = supabase.auth.sign_in(email=email, password=password)
    supabase_user_id = response['user']['id']
    user = User.query.filter_by(email=email,supabase_id=supabase_user_id,is_hidden=False).first()
    db.session.commit()
    if user and bcrypt.check_password_hash(user.password, password):
        if user.state==0 and user.is_hidden==False:
            
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=7)  
            )
            user.last_login=datetime.now()

            return jsonify({
            "token": access_token,
            "user": {
                "phone": user.phone,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "avatar": user.avatar
            }
        }), 200
        else:
            return jsonify({"msg": "user is banned"}), 401

    return jsonify({"msg": "Invalid email or password"}), 401







@auth_blueprint.route('/send-otp_phone', methods=['POST'])
def send_otp_phone():
    data = request.json
    phone = data.get('phone')

    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    try:
        # Send OTP using Supabase
        response = supabase.auth.sign_in_with_otp(phone=phone)
        return jsonify({"message": "OTP sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_blueprint.route('/send-otp_email', methods=['POST'])
def send_otp_email():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "email  is required"}), 400

    try:
        # Send OTP using Supabase
        response = supabase.auth.sign_in_with_otp(email=email)
        return jsonify({"message": "OTP sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@auth_blueprint.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone = data.get('phone')
    otp = data.get('otp')

    if not phone or not otp:
        return jsonify({"error": "Phone number and OTP are required"}), 400

    try:
        # Verify OTP using Supabase
        response = supabase.auth.verify_otp(phone=phone, token=otp)
        user_id = response['user']['id']

        # Check if the user exists in the MySQL database
        mysql_user = User.query.filter_by(phone=phone).first()
        if not mysql_user:
            # Create a new user in MySQL if not exists
            new_user = User(phone=phone, supabase_id=user_id)
            db.session.add(new_user)
            db.session.commit()

        # Generate JWT or session for your app
        token = create_access_token(identity=mysql_user.id if mysql_user else new_user.id)

        return jsonify({"message": "OTP verified successfully", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
    
    
    
    
    
    
    
    
    
@auth_blueprint.route('/Delete', methods=['POST'])
@jwt_required()
def Delete():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_hidden = True
        db.session.commit()
        return jsonify({"msg": "user is hidden"}), 200
    return jsonify({"msg": "user not found"}), 404
    