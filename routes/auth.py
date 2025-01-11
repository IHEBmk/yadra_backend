from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from config import supabase
from schemas import RegisterSchema
from models import  User, authToken, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError
from functools import wraps



auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()

def validate_token():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"msg": "Missing token"}), 401
                
            token = token.split()[1]
            stored_token = authToken.query.filter_by(
                token=token,
                is_revoked=False
            ).first()
            
            if not stored_token or stored_token.expires_at < datetime.utcnow():
                return jsonify({"msg": "Invalid or expired token"}), 401
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@auth_blueprint.route('/register', methods=['POST'])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": {"code": "INVALID_INPUT", "message": "Invalid input", "details": err.messages}}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": {"code": "EMAIL_EXISTS", "message": "Email already registered", "details": {"field": "email"}}}), 400

    # response = supabase.auth.sign_up(email=data['email'], password=data['password'])
    # supabase_user_id = response['user']['id']
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        # supabase_id=supabase_user_id,
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        phone=data.get('phone'),
        role = data.get('role'),
        avatar = data.get('avatar'),
        created_at = datetime.now(),
        last_login = datetime.now(),
        state = 1
    )
    db.session.add(user)
    db.session.commit()


    return jsonify({
                       'msg':'user created successfully',
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
    # response = supabase.auth.sign_up(email=data['email'], password=data['password'])
    # supabase_user_id = response['user']['id']
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        # supabase_id=supabase_user_id,
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        phone=data.get('phone'),
        role = 2,
        avatar = data.get('avatar'),
        created_at = datetime.now(),
        last_login = datetime.now(),
        state = 1
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

def store_token(user_id, token, expires_delta):
    expires_at = datetime.now() + expires_delta
    new_token = authToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.session.add(new_token)
    db.session.commit()

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    db.session.commit()
    
    if user and bcrypt.check_password_hash(user.password, password):
        if user.state == 0 and user.is_hidden == False:
            expires_delta = timedelta(days=7)
            access_token = create_access_token(
                identity=user.id,
                expires_delta=expires_delta
            )
            
            store_token(user.id, access_token, expires_delta)
            
            user.last_login = datetime.now()
            db.session.commit()

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



@auth_blueprint.route('/logout', methods=['POST'])

@jwt_required()
@validate_token()
def logout():
    current_user_id = get_jwt_identity()
    token = request.headers.get('Authorization').split()[1]
    
    stored_token = authToken.query.filter_by(
        user_id=current_user_id,
        token=token,
        is_revoked=False
    ).first()
    
    if stored_token:
        stored_token.is_revoked = True
        db.session.commit()
        return jsonify({"msg": "Successfully logged out"}), 200
    
    return jsonify({"msg": "Token not found"}), 404







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
        user=User.query.filter_by(supabase_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        token=create_access_token(identity=user.id)
        return jsonify({"message": "OTP verified successfully",
                       'token': token,
                       'user':user.to_dict()
                           }), 200
        
    



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

@auth_blueprint.route('/verify-otp_email', methods=['GET'])
def verify_otp_email():
    data = request.args
    otp = data.get('acess_token')

    if  not otp:
        return jsonify({
            "msg":data,
            "error": "Phone number and OTP are required"}), 400

    try:
        otp=OTP.query.filter_by(otp=otp).first()
        if not otp:
            return jsonify({"error": "OTP not found"}), 404
        
        user=User.query.filter_by(email=otp.email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user.state=0
        db.session.commit()

        token=create_access_token(identity=user.id)
        return jsonify({"message": "OTP verified successfully",
                       'token': token,
                       'user':user.to_dict()
                           }), 200
        
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500