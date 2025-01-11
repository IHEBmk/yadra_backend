from datetime import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Branch, Review, User
from models import Company, db
import models


response_blueprint = Blueprint('responses', __name__)

@response_blueprint.route('/get_responses', methods=['GET'])
def get_responses():
   responses = Response.query.filter_by(is_hidden = False)
    
   responses_list = [company.to_dict() for company in responses]

   return jsonify({
        "companies": responses_list,
    }), 201
   
   
   
   
@response_blueprint.route('/add_response', methods=['POST'])
@jwt_required()
def add_response():
    data = request.get_json()
    account_id=get_jwt_identity()
    description=data.get('description')
    review_id=data.get('review_id')
    user=User.query.filter_by(id=account_id).first()
    review=Review.query.filter_by(id=review_id).first()
    branch=Branch.query.filter_by(id=review.branch_id).first()
    if user:
        if (user.role==3 and user.company_id==branch.company_id)  or (user.role==4 and review.branch_id==user.branch_id) or(user.role==3 and review.company_id==user.company_id) or (user.role==2 and user.id == review.user_id):
            response=models.Response(review_id=review_id,description=description,user_id=account_id,created_at=datetime.now())
            db.session.add(response)
            db.session.commit()
            return jsonify({
            "msg": "Response added successfully",
            "response_id": response.id
        }), 201
        
            
        else:
            return  jsonify({
                    'msg':'User not authorized or review no longer exists'
                }),300 
        
    else:
        return  jsonify({
                    'msg':'User does not exist'
                }),300    
        
        
        
        
        




@response_blueprint.route('/delete_response', methods=['POST'])
@jwt_required()
def delete_response():
    data = request.get_json()
    account_id=get_jwt_identity()
    response_id=data.get('response_id')
    # account_id=data.get('account_id')
    user=User.query.filter_by(id=account_id).first()
    response=models.Response.query.filter_by(id=response_id).first()
    review=Review.query.filter_by(id=response.review_id).first()
    branch=Branch.query.filter_by(id=review.branch_id).first()
    if user and response:
        if (user.role==3 and user.company_id==branch.company_id)  or (user.role==4 and review.branch_id==user.branch_id):
            response.is_hidden = True
            db.session.commit()
            return jsonify({
            "msg": "Response deleted successfully",
        }), 201
            
        else:
            return  jsonify({
                    'msg':'User not authorized or review no longer exists'
                }),300 
        
    else:
        return  jsonify({
                    'msg':'User/response does not exist'
                }),300    