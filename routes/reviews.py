from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from models import Branch, Company, Flagged, Guest, User, db, Review, Likes
from datetime import datetime
import uuid
import logging
import models
from routes.companies import get_company_rating
from schemas import ReviewSchema, validate_media_files

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

reviews_blueprint = Blueprint('reviews', __name__)

@reviews_blueprint.route('/submit', methods=['POST'])
@jwt_required()
def submit_review():
    user_id = get_jwt_identity()
    json_data = request.get_json()  
    logger.info(f"Received form data: {json_data}")
    schema = ReviewSchema()
    try:
        validated_data = schema.load(json_data)
    except ValidationError as err:
        return jsonify({"msg": "Validation failed", "errors": err.messages}), 400

    

    print(validated_data)
    branch_id = validated_data["branch_id"]
    company_id = validated_data["company_id"]
    branch = Branch.query.filter_by(id=str(branch_id)).first()
    company=Company.query.filter_by(id=str(company_id)).first()
    if not branch and not company:
        return jsonify({"msg": "Entity not found"}), 404

    

    
    review = Review(
        id=str(uuid.uuid4()),
        user_id=user_id,
        company_id=company_id,
        branch_id=branch_id, 
        description=validated_data["content"],
        rating=validated_data["rating"]["general_rating"],
        product_quality=validated_data["rating"]["product_quality"],
        price=validated_data["rating"]["price"],
        delivery_speed=validated_data["rating"]["delivery_speed"],
        ease_of_use=validated_data["rating"]["ease_of_use"],
        customer_service=validated_data["rating"]["customer_service"],
        created_at=datetime.now(),
        is_anonymous=validated_data["is_anonymous"],
        tags=",".join(validated_data.get("tags", [])),
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({
        "review_id": review.id,
        "status": "published",
    }), 201



@reviews_blueprint.route('/flag', methods=['POST'])
@jwt_required()
def flag_review():
    current_user_id = get_jwt_identity()
    user= User.query.filter_by(id= current_user_id).first()
    role = user.role
    
    if (role !=2):
        data = request.get_json()
        review_id = data.get('review_id')
        description = data.get('description')

        if not review_id or not description or len(description) < 10 or len(description) > 500:
            return jsonify({"message": "Invalid review ID or description is too short."}), 400

        review = Review.query.filter_by(id=review_id, is_hidden=False).first()
        if not review:
            return jsonify({"message": "Review not found."}), 404
        branch = Branch.query.filter_by(id = review.branch_id).first()
        company_id = Company.query.filter_by(id = branch.company_id).first().id
        if user.company_id != company_id and role!=1:
            return jsonify({"message": "You are not authorized to flag this review."}), 403

        
        existing_flag = Flagged.query.filter_by(review_id=review_id, user_id=current_user_id).first()
        if existing_flag:
            return jsonify({"message": "You have already flagged this review."}), 400

        flagged = Flagged(
            review_id=review_id,
            description=description,
            user_id=current_user_id,
            flagged_at=datetime.now()
        )

        db.session.add(flagged)
        db.session.commit()

        return jsonify({
            "message": "Review flagged successfully",
            "flag_id": flagged.id,
            "flagged_at": flagged.flagged_at
        }), 201
    else :
        return jsonify({"message": "You don't have the right to flag this review"}), 403



@reviews_blueprint.route('/get_flagged', methods=['GET'])
@jwt_required()
def get_flagged_reviews():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    if user.role != 1:
        return jsonify({"message": "Admin access required."}), 403

    flagged_reviews = Flagged.query.filter_by(is_hidden=False).all()

    flagged_reviews_list = [flagged.to_dict() for flagged in flagged_reviews]

    return jsonify({
        "flagged_reviews": flagged_reviews_list
    }), 200



@reviews_blueprint.route('/flag/validate', methods=['POST'])
@jwt_required()
def validate_flagged_review():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    
    if not user or user.role != 1:
        return jsonify({"message": "Admin access required."}), 403

    data = request.get_json()
    flag_id = data.get('flag_id')
    validated = data.get('validated')

    if not flag_id or validated not in [True, False]:
        return jsonify({"message": "Invalid request."}), 400

    flag = Flagged.query.filter_by(id=flag_id).first()
    if not flag:
        return jsonify({"message": "Flag not found."}), 404

    flag.is_hidden=True
    db.session.commit()

    if validated:
        review = Review.query.filter_by(id=flag.review_id).first()
        if review:
            review.is_hidden = True

    db.session.commit()

    return jsonify({
        "message": f"Flag validation {'approved and review deleted' if validated else 'rejected'} successfully.",
        "flag_id": flag.id,
        "validated": validated
    }), 200



@reviews_blueprint.route('/toggle_like', methods=['POST'])
@jwt_required()
def like_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    review_id = data.get('review_id')

    if not review_id:
        return jsonify({"message": "Review ID is required."}), 400

    review = Review.query.filter_by(id=review_id, is_hidden = False).first()
    if not review:
        return jsonify({"message": "Review not found."}), 404

    existing_like = Likes.query.filter_by(review_id=review_id, user_id=user_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({
            "message": "Like removed successfully",
            "review_id": review_id,
            "user_id": user_id
        }), 200

    like = Likes(
        review_id=review_id,
        user_id=user_id
    )
    db.session.add(like)
    db.session.commit()

    return jsonify({
        "message": "Review liked successfully",
        "review_id": review_id,
        "user_id": user_id
    }), 201

@reviews_blueprint.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    review_id = data.get('review_id')

    if not review_id:
        return jsonify({"message": "Review ID is required."}), 400

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return jsonify({"message": "Review not found."}), 404

    if review.user_id != user_id and User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "You are not authorized to delete this review."}), 403

    review.is_hidden = True
    responses =  models.Response.query.filter_by(review_id = review.id)
    for response in responses:
        response.is_hidden = True
    db.session.commit()

    return jsonify({
        "message": "Review deleted successfully",
        "review_id": review.id
    }), 200


@reviews_blueprint.route('/likes_status', methods=['GET'])
@jwt_required()
def get_likes_status():
    user_id = get_jwt_identity()
    data = request.get_json()
    review_id = data['review_id'] 

    if not review_id:
        return jsonify({"message": "Review ID is required."}), 400

   
    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return jsonify({"message": "Review not found."}), 404

    likes_count = Likes.query.filter_by(review_id=review_id).count()

    user_liked = Likes.query.filter_by(review_id=review_id, user_id=user_id).first()

    return jsonify({
        "likes_count": likes_count,
        "user_liked": True if user_liked else False
    }), 200


    

@reviews_blueprint.route('/recent', methods=['GET'])
@jwt_required()
def get_recent():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        user=Guest.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404
        reviews=Review.query.filter_by(is_hidden=False,user_id=user.id).order_by(Review.created_at.desc()).limit(3).all()
        return jsonify({"reviews": reviews}), 200
    else:
        reviews=Review.query.filter_by(user_id=user.id,is_hidden=False).order_by(Review.created_at.desc()).limit(3).all()
        
        reviews=[review.to_dict() for review in reviews]
        for review in reviews:
            company=Company.query.filter_by(id=review['company_id']).first()
            review['company_rating']=get_company_rating(company)
            review['company_name']=company.name
            review['company_logo']=company.logo
        return jsonify({"reviews": reviews}), 200
    
    
    
    
    
    
    
    
    
    