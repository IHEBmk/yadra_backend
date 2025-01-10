from datetime import datetime
import uuid
import bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Branch, Category, Company, Company_register, User
from models import Company, db
import secrets
import string


categories_blueprint = Blueprint('categories', __name__)

@categories_blueprint.route('/get_categories', methods=['GET'])
def get_categories():
   categories = Category.query.all()
   categories_list = [category.to_dict() for category in categories]

   return jsonify({
        "companies": categories_list,
    }), 201
   
   
   
   
@categories_blueprint.route('/add_category', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    name = data.get('name')
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,is_hidden=False).first()
    if user:
        if user.role==1:
            category=Category.query.filter_by(name=name).first()
            if category:
                return  jsonify({
                    'msg':'category already exists'
                }),300
            else:
                category=Category(name=name)
                db.session.add(category)
                db.session.commit()
            
        else:
            return  jsonify({
                    'msg':'User not authorized'
                }),300 
        
    else:
        return  jsonify({
                    'msg':'User does not exist'
                }),300    