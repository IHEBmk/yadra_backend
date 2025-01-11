from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from config import supabase
from models import Branch, Company, Guest, User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required



add_blueprint = Blueprint('add', __name__)
bcrypt = Bcrypt()

@add_blueprint.route('/company', methods=['POST'])
@jwt_required()
def add_company_account():
    data = request.get_json()
    account_id=get_jwt_identity()
    user=User.query.filter(or_(User.role==1, User.role == 3),User.id==account_id).first()
    
    company=Company.query.filter_by(id=data.get('company_id'),is_hidden=False).first()
    
    if user and company:
        if user.company_id != company.id and user.role != 1:
            return jsonify({
            "msg":'unauthorized',

            }), 404
        
        hashed_password= bcrypt.generate_password_hash(data['password']).decode('utf-8'),


        user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            phone=data.get('phone'),
            role = 3,
            avatar = data.get('avatar'),
            created_at = datetime.now(),
            company_id=data.get('company_id'),
            last_login = datetime.now(),
            state = 0
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

        return jsonify({
        "user_id": user.id,
        "token": token,
        "expires_in": 3600
    }), 201
    else:
        if not user:
            
            return jsonify({
        "msg":'unauthorized',

    }), 404
        else:
            return jsonify({
        "msg":'Company doesn"t exist',

    }), 404
            
            
            
            
            
            
    
    
    
    
    
    
    





@add_blueprint.route('/branch', methods=['POST'])
@jwt_required()
def add_branch_account():
    data = request.get_json()
    account_id=get_jwt_identity()
    user=User.query.filter(or_(User.role == 3, User.role == 4, User.role == 1),User.id==account_id).first()
    branch=Branch.query.filter_by(id=data.get('branch_id'),is_hidden=False).first()

    if user and branch:
        if user.role !=1 and user.company_id != branch.company_id:
            return jsonify({
            "msg":'unauthorized',

            }), 404
        hashed_password= bcrypt.generate_password_hash(data['password']).decode('utf-8'),


        user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            phone=data.get('phone'),
            role = 4,
            avatar = data.get('avatar'),
            created_at = datetime.now(),
            company_id = branch.company_id,
            branch_id=data.get('branch_id'),
            last_login = datetime.now(),
            state = 0
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

        return jsonify({
        "user_id": user.id,
        "token": token,
        "expires_in": 3600
    }), 201
    else:
        if not user:
            
            return jsonify({
        "msg":'unauthorized',

    }), 404
        else:
            return jsonify({
        "msg":'Branch does not exist',

    }), 404
        
        
        
        
edit_blueprint = Blueprint('edit_account', __name__)
        
        
        







@edit_blueprint.route('/ban', methods=['POST'])
@jwt_required()
def ban():
    data = request.get_json()
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,role=1).first()
    if user:
        user2=User.query.filter_by(id=data.get('user_id')).first()
        if user2:
            user2.state=1
            db.session.commit()
            return jsonify({
        "msg": 'user banned successfully',
    }), 201
    else:
        return jsonify({
        "msg":'user doesn"t exist',

    }), 404



@edit_blueprint.route('/unban', methods=['POST'])
@jwt_required
def unban():
    data = request.get_json()
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,role=1).first()
    if user:
        user2=User.query.filter_by(id=data.get('user_id')).first()
        if user2:
            user2.state=0
            db.session.commit()
            return jsonify({
        "msg": 'user unbanned successfully',
    }), 201
    else:
        return jsonify({
        "msg":'user does not exist',

    }), 404
        
        
        
        




@edit_blueprint.route('/getbanned', methods=['GET'])
@jwt_required()
def get_ban():
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,role=1).first()
    if user:
        user2=User.query.filter_by(state=1,is_hidden=False)
        
        if user2:
            user_list=[user1.to_dict() for user1 in user2]
            return jsonify({
        "users": user_list,
    }), 201
    else:
        return jsonify({
        "msg":'user doesn"t exist',

    }), 404






@edit_blueprint.route('/account', methods=['POST'])
@jwt_required()
def edit_account():


        data = request.form.to_dict()
        account_id=get_jwt_identity()
        user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
        if user:
            if data.get('name'):
                user.name= data.get('name')
            if data.get('password'):
                print(data.get('current_password'))
                print(data.get('password'))
                current_password = data.get('current_password')
                if bcrypt.check_password_hash(user.password, current_password):
                    user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
                else:
                    return jsonify({"error": "Current password is incorrect"}), 400
            if data.get('email'):
                user.email= data.get('email')
            if data.get('phone'):
                user.phone= data.get('phone')
            if 'image'  in request.files:
                file = request.files['image']
    
                if file.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                file_name = f"images/{file.filename}"
                temp=f"{file.filename}"
                files = supabase.storage.from_("Users").list('images/')

                file_exists = any(file['name'] == temp for file in files)
                if file_exists:
                    public_url = supabase.storage.from_("Users").get_public_url(file_name)
                    user.avatar = public_url
                    db.session.commit()
                    return jsonify({
        "msg": 'user modified successfully',
"user": {
                "phone": user.phone,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "avatar": public_url
            }
    }), 200


                image_data = file.read()
                try:
                    response = supabase.storage.from_("Users").upload(file_name, image_data)
                    if not response:
                        return jsonify({"error": "Error uploading file"}), 500

                    public_url = supabase.storage.from_("Users").get_public_url(file_name)
                    user.avatar= public_url
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            db.session.commit()
            
            return jsonify({
        "msg": 'user modified successfully',
"user": {
                "phone": user.phone,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "avatar": public_url
            }
    }), 201 
           

        else:
                return jsonify({
        "msg":'user doesn"t exist',

    }), 404









user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id,is_hidden=False,state=0).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "role": user.role,
        "company_id": user.company_id,
        "branch_id": user.branch_id,
        "created_at": user.created_at,
        "avatar": user.avatar,
        "state": user.state,
        "last_login": user.last_login,
    }), 200

@add_blueprint.route('/add_guest', methods=['POST'])
def register():
    

    guest = Guest(
    )
    db.session.add(guest)
    db.session.commit()

    token = create_access_token(identity=guest.id, expires_delta=timedelta(days=365))

    return jsonify({
        "user_id": guest.id,
        "token": token,
    }), 201
    
    
@user_blueprint.route('/user_name_avatar', methods=['GET'])
@jwt_required()
def get_user_name__avatar():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id,is_hidden=False,state=0).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "name": user.name,
        "avatar": user.avatar
    }), 200