from datetime import datetime, timedelta
from enum import Flag
from flask import Blueprint, request, jsonify
from routes.companies import get_branches
from schemas import RegisterSchema
from sqlalchemy import extract, func
from models import Branch, Category, Company, Company_register, Flagged, Response, Review, User, Visit, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import  get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError



analytics_blueprint = Blueprint('analytics', __name__)
bcrypt = Bcrypt()

@analytics_blueprint.route('/charts/get_categories_distribution', methods=['GET'])
@jwt_required()
def categories_distribution():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    distribution=[]
    categories=Category.query.all()
    for i  in  range(len(categories)):
        distribution.append({})
        distribution[i]['name']=categories[i].name
        distribution[i]['distribution']=len(Company.query.filter_by(category=categories[i].id).all())
        
    return jsonify({"message": "succesfully calculated ",
                    "data":distribution}), 200
    
    
    
@analytics_blueprint.route('/blocks/get_num_of_inactive_branches', methods=['GET'])
@jwt_required()
def get_num_of_inactive_branches():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user.role==1:
        return jsonify({"message": "Unauthorized User"}), 404
    branches = Branch.query.filter_by(is_hidden=False).all()
    branch_ids = [branch.id for branch in branches]
    inactive_branches = 0
    for branch_id in branch_ids:
        admins = User.query.filter_by(role=3, branch_id=branch_id).all()
        for admin in admins:
            last_login = datetime.strptime(admin.last_login, '%Y-%m-%d %H:%M:%S') 
            one_month_ago = datetime.now() - timedelta(days=30)
            if last_login < one_month_ago:
                continue
        inactive_branches += 1
    return jsonify({"message": "succesfully calculated ",
                    "number of inactive branches": inactive_branches}), 200
    
    
@analytics_blueprint.route('/charts/get_companies_distribution', methods=['GET'])
@jwt_required()
def companies_distribution():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    distribution=[{'accepted':0,'pending':0,'rejected':0}]
    total_number=len(Company_register.query.all())
    companies=len(Company.query.filter_by(is_hidden=False).all())
    pending=len(Company_register.query.filter_by(is_hidden=False).all())
    rejected_companies=len(Company_register.query.filter_by(is_hidden=True).all())-companies
    return jsonify({"message": "succesfully calculated ",
                    "accepted":companies,
                    "pending":pending,
                    "rejected":rejected_companies}), 200
    
    
    
    
    
    
    
    




@analytics_blueprint.route('/charts/get_reviews_distribution', methods=['GET'])
@jwt_required()
def reviews_distribution():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    distribution={}
    
    companies=Company.query.filter_by(is_hidden=False)
    for company in companies:
        distribution[company.name]=0
    reviews=Review.query.filter_by(is_hidden=False)
    for review  in  reviews:
        branch=Branch.query.filter_by(id=review.branch_id).first()
        company=Company.query.filter_by(id=branch.company_id).first()
        distribution[company.name]+=1

            
        
    return jsonify({"message": "succesfully calculated ",
                    "data":distribution}), 200
        
    
    
@analytics_blueprint.route('/blocks/get_num_users', methods=['GET'])
@jwt_required()
def get_num_users():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    number_of_users=len(User.query.filter_by(role=2,is_hidden=False,state=0).all())
    return jsonify({"message": "succesfully calculated ",
                    "number of users":number_of_users}), 200
    
    
    
    
    
    
    
    
    
@analytics_blueprint.route('/blocks/get_num_companies', methods=['GET'])
@jwt_required()
def get_num_companies():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Unauthorized User"}), 404
    
    number_of_companies=len(Company.query.filter_by(is_hidden=False).all())
    return jsonify({"message": "succesfully calculated ",
                    "number of companies":number_of_companies}), 200
    
    
    
    
    
    
    
    
    
    
    
    
    
@analytics_blueprint.route('/blocks/get_num_of_active_users', methods=['GET'])
@jwt_required()
def get_num_of_active_users():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    users=User.query.filter_by(is_hidden=False).all()
    number_of_active_users=0
    today=datetime.now()
    print (today)
    for user in users:
        last_login=datetime.strptime(user.last_login,'%Y-%m-%d %H:%M:%S.%f') 
        if today - last_login <= timedelta(days=1):
            number_of_active_users+=1
    return jsonify({"message": "succesfully calculated ",
                    "number_of_new_users":number_of_active_users}), 200
    
    
    
    
    
    
    
    




@analytics_blueprint.route('/blocks/get_num_new_users', methods=['GET'])
@jwt_required()
def get_num_new_users():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Unauthorized User"}), 404
    
    users=User.query.all()
    number_of_new_users=0
    today=datetime.now()
    print (today)
    for user in users:
        created_at=datetime.strptime(user.created_at,'%Y-%m-%d %H:%M:%S.%f')
        if created_at.day==today.day and created_at.month==today.month and created_at.year==today.year:
            number_of_new_users+=1
    return jsonify({"message": "succesfully calculated ",
                    "number_of_new_users":number_of_new_users}), 200
    
    
    
    
    
    
    
    
    
    
    
    
@analytics_blueprint.route('/blocks/churn_rate', methods=['GET'])
@jwt_required()
def churn_rate():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Unauthorized User"}), 404
    
    users=User.query.filter_by(state=0)
    churn_rate=0
    today=datetime.now()
    for user in users:
        last_login=datetime.strptime(user.last_login,'%Y-%m-%d %H:%M:%S.%f')
        if today - last_login > timedelta(days=31):
            churn_rate+=1
    churn_rate/=len(users)
    return jsonify({"message": "succesfully calculated ",
                    "churn_rate":churn_rate*100}), 200
    
    
    
    
    
    
    

@analytics_blueprint.route('/blocks/get_num_branches', methods=['GET'])
@jwt_required()
def get_num_branches():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    num_branches=len(Branch.query.filter_by(is_hidden=False).all())
    return jsonify({"message": "succesfully calculated ",
                    "number of branches":num_branches}), 200    
    
    
    
    
@analytics_blueprint.route('/blocks/get_num_reviews', methods=['GET'])
@jwt_required()
def get_num_reviews():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    number_of_reviews=len(Review.query.all())
    return jsonify({"message": "succesfully calculated ",
                    "number of reviews":number_of_reviews}), 200
    


    

    
@analytics_blueprint.route('/blocks/get_average_rating', methods=['GET'])
@jwt_required()
def get_average_rating():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    reviews=Review.query.filter_by(is_hidden=False).all()
    avg_rating=0
    for review in reviews:
        avg_rating+=review.rating
    avg_rating/=len(reviews)
    return jsonify({"message": "succesfully calculated ",
                    "avg_rating":avg_rating}), 200
    
    
    




@analytics_blueprint.route('/blocks/num_flagged', methods=['GET'])
@jwt_required()
def num_flagged():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    
    flagged=len(Flagged.query.all())
    
    return jsonify({"message": "succesfully calculated ",
                    "Num_of_flagged":flagged}), 200
    
    
    
    

    
    
    
    
    
@analytics_blueprint.route('/blocks/reviews_for_company', methods=['GET'])
@jwt_required()
def reviews_for_company():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==3:
        return jsonify({"message": "Aunothorized User"}), 404
    
    company=Company.query.filter_by(id=user.company_id).first()
    branches=Branch.query.filter_by(company_id=company.id).all()
    reviews=[]
    for branch in branches:
        reviews.extend(Review.query.filter_by(branch_id=branch.id,is_hidden=False).all())
        
    
    num_reviews=len(reviews)
    
    return jsonify({"message": "succesfully calculated ",
                    "Num_of_reviews":num_reviews}), 200
    
    
    
    
    
    
    
    
    
    
    
    
    
@analytics_blueprint.route('/blocks/avg_rating_for_company', methods=['GET'])
@jwt_required()
def avg_rating_for_company():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==3:
        return jsonify({"message": "Aunothorized User"}), 404
    
    company=Company.query.filter_by(id=user.company_id).first()
    branches=Branch.query.filter_by(company_id=company.id).all()
    reviews=[]
    for branch in branches:
        reviews.extend(Review.query.filter_by(branch_id=branch.id,is_hidden=False).all())
        
    avg_rating=0
    for review in reviews:
        avg_rating+=review.rating
    num_reviews=len(reviews)
    
    avg_rating/=num_reviews
    return jsonify({"message": "succesfully calculated ",
                    "Avg_rating":avg_rating}), 200
    
    
    
    
    
    
    

    
    
    
    
    
    
    


@analytics_blueprint.route('/blocks/review_trends', methods=['GET'])
@jwt_required()
def review_trends():
    user_id = get_jwt_identity()
    filter_by=request.get_json().get('filter')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.role==3:
        return jsonify({"message": "Aunothorized User"}), 404
    today=datetime.now()
    reviews=Review.query.all() 
    num_of_reviews=0
    if filter_by=='daily' or  filter_by==None:
        for review in reviews:
            review_date=datetime.strptime(review.created_at,'%Y-%m-%d %H:%M:%S.%f')
            if review_date.day==today.day and review_date.month==today.month and review_date.year==today.year:
                num_of_reviews+=1
        return jsonify({"message": "succesfully calculated ",
                        "num_of_reviews":num_of_reviews}), 200
        
    elif filter_by=='weekly':
        for review in reviews:
            review_date=datetime.strptime(review.created_at,'%Y-%m-%d %H:%M:%S')
            if today - review_date <= timedelta(weeks=1):
                    num_of_reviews+=1
        return jsonify({"message": "succesfully calculated ",
                        "num_of_reviews":num_of_reviews}), 200
    elif filter_by=='monthly':
        for review in reviews:
            review_date=datetime.strptime(review.created_at,'%Y-%m-%d %H:%M:%S')
            if today - review_date <= timedelta(days=30):
                num_of_reviews+=1
        return jsonify({"message": "succesfully calculated ",
                        "num_of_reviews":num_of_reviews}), 200

            
            
            

@analytics_blueprint.route('/charts/users_over_time', methods=['POST'])
@jwt_required()
def get_users_over_time():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body is required"}), 400

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    group_by = data.get('group_by', 'day') 

    if not start_date or not end_date:
        return jsonify({"message": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    if group_by not in ['day', 'month', 'year']:
        return jsonify({"message": "Invalid group_by value. Use 'day', 'month', or 'year'"}), 400

    if group_by == 'day':
        time_format = func.date(User.created_at)  
    elif group_by == 'month':
        time_format = func.date_format(User.created_at, '%Y-%m')  
    elif group_by == 'year':
        time_format = func.year(User.created_at)  

    results = db.session.query(
        time_format.label('time_period'),
        func.count(User.id).label('user_count')
    ).filter(
        func.date(User.created_at) >= start_date,
        func.date(User.created_at) <= end_date
    ).group_by(time_format).order_by(time_format).all()

    if group_by == 'day':
        format_str = '%Y-%m-%d'
    elif group_by == 'month':
        format_str = '%Y-%m'
    elif group_by == 'year':
        format_str = '%Y'

    data = [
        {"time_period": row.time_period.strftime(format_str) if isinstance(row.time_period, datetime) else row.time_period, 
         "user_count": row.user_count}
        for row in results
    ]

    return jsonify(data), 200


@analytics_blueprint.route('/charts/reviews_over_time', methods=['POST'], endpoint='reviews_over_time')
@jwt_required()
def get_review_count():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body is required"}), 400

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    branch_id = data.get('branch_id')
    group_by = data.get('group_by', 'day')  

    if not start_date or not end_date:
        return jsonify({"message": "start_date and end_date are required."}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    if group_by not in ['day', 'month', 'year']:
        return jsonify({"message": "Invalid group_by value. Use 'day', 'month', or 'year'."}), 400

    if group_by == 'day':
        time_format = func.date(Review.created_at)
    elif group_by == 'month':
        time_format = func.date_format(Review.created_at, '%Y-%m')  
    elif group_by == 'year':
        time_format = func.year(Review.created_at)

    reviews = db.session.query(
        time_format.label('time_period'),
        func.count(Review.id).label('review_count')
    ).filter(
        Review.branch_id == branch_id,
        func.date(Review.created_at) >= start_date,
        func.date(Review.created_at) <= end_date
    ).group_by(time_format).order_by(time_format).all()
    

    response = [
        {
            "time_period": str(row.time_period),
            "review_count": row.review_count
        }
        for row in reviews
    ]

    return jsonify(response), 200

@analytics_blueprint.route('/charts/nb_reviews_per_company', methods=['GET'])
@jwt_required()
def nb_reviews_per_company():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403
    companies = Company.query.filter_by(is_hidden=False).all()
    nb_reviews_per_company = {}
    for company in companies:
        nb_reviews_per_company[company.id] = db.session.query(func.count(Review.id)).filter(Review.company_id == company.id).scalar() + get_branches(company)[1]
    sorted_reviews = sorted(nb_reviews_per_company.items(), key=lambda item: item[1], reverse=True)

    return jsonify([{"company" :company_id, "number_of_reviews": nb_reviews_per_company[company_id]} for company_id, _ in sorted_reviews[:5]]),200



@analytics_blueprint.route('/blocks/user_growth', methods=['GET'], endpoint='user_growth')
@jwt_required
def user_growth():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    current_month = datetime.now().month

    current_month_users = db.session.query(func.count(User.id)).filter(
        extract('month', User.created_at) == current_month
    ).scalar()

    previous_month_users = db.session.query(func.count(User.id)).filter(
        extract('month', User.created_at) == current_month - 1
    ).scalar()

    if previous_month_users == 0:
        growth_percentage = 0 if current_month_users == 0 else 100
    else:
        growth_percentage = ((current_month_users - previous_month_users) / previous_month_users) * 100

    return jsonify({
        "current_month_users": current_month_users,
        "previous_month_users": previous_month_users,
        "growth_percentage": growth_percentage
    }), 200

@analytics_blueprint.route('/blocks/company_response_avg', methods=['GET'], endpoint = "company_response_avg")
@jwt_required
def company_response_avg():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    company_id = data['company_id']
    company = Company.query.filter_by(id=company_id).first()
    if not company:
        return jsonify({"message": "Company not found"}), 404

    total_reviews = db.session.query(func.count(Review.id)).join(
        Branch, Review.branch_id == Branch.id).filter(
        Branch.company_id == company_id
    ).scalar()

    responded_reviews = db.session.query(func.count(Review.id)).join(
        Response, Response.review_id == Review.id).join(
        Branch, Review.branch_id == Branch.id).filter(
        Branch.company_id == company_id
    ).distinct().scalar()

    if total_reviews == 0:
        return jsonify({"message": "No reviews for this company"}), 404

    return jsonify({
        "company_id": company.id,
        "company_name": company.name,
        "total_reviews": total_reviews,
        "responded_reviews": responded_reviews
    }), 200
    
    
    
    
    
    
    
    
    
    
@analytics_blueprint.route('/blocks/company_response_rate', methods=['GET'], endpoint = "company_response_rate")
@jwt_required
def company_response_rate():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    company_id = data['company_id']
    company = Company.query.filter_by(id=company_id).first()
    if not company:
        return jsonify({"message": "Company not found"}), 404

    reviews_with_responses = db.session.query(
        Review.id,
        Review.created_at.label('review_created_at'),
        Response.created_at.label('response_created_at')
    ).join(
        Response, Response.review_id == Review.id
    ).join(
        Branch, Review.branch_id == Branch.id
    ).filter(
        Branch.company_id == company_id
    ).all()

    total_reviews = len(reviews_with_responses)

    if total_reviews == 0:
        return jsonify({"message": "No reviews with responses for this company"}), 404


    total_response_time = 0
    for review in reviews_with_responses:
        review_time = datetime.strptime(review.review_created_at, '%Y-%m-%d %H:%M:%S.%f')
        response_time = datetime.strptime(review.response_created_at, '%Y-%m-%d %H:%M:%S.%f')
        response_time_diff = (response_time - review_time).total_seconds()
        total_response_time += response_time_diff

    avg_response_time = total_response_time / total_reviews if total_reviews > 0 else 0
    avg_response_time_minutes = avg_response_time / 60 

    return jsonify({
        "company_id": company.id,
        "company_name": company.name,
        "total_reviews": total_reviews,
        "average_response_time_minutes": avg_response_time_minutes
    }), 200

@analytics_blueprint.route('/charts/get_number_of_companies', methods=['GET'])
@jwt_required()
def get_number_of_companies():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user.role==1:
        return jsonify({"message": "Aunothorized User"}), 404
    companies=Company.query.all()
    number_of_companies=len(companies)
    return jsonify({"message": "succesfully calculated ",
                    "number of companies":number_of_companies}), 200

@analytics_blueprint.route('increment_visit_count', methods=['POST'])
@jwt_required()
def increment_visit_count():
    Visit.increment_visit_count()
    return jsonify({"message": "visit count incremented"}), 200


@analytics_blueprint.route('/charts/visits_over_time', methods=['POST'])
@jwt_required()
def get_visits_over_time():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body is required"}), 400

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    group_by = data.get('group_by', 'day') 

    if not start_date or not end_date:
        return jsonify({"message": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    if group_by not in ['day', 'month', 'year']:
        return jsonify({"message": "Invalid group_by value. Use 'day', 'month', or 'year'"}), 400

    if group_by == 'day':
        time_format = func.date(Visit.interval_start)
        format_str = '%Y-%m-%d'
    elif group_by == 'month':
        time_format = func.date_format(Visit.interval_start, '%Y-%m')  
        format_str = '%Y-%m'
    elif group_by == 'year':
        time_format = func.year(Visit.interval_start)  
        format_str = '%Y'

    results = db.session.query(
        time_format.label('time_period'),
        func.sum(Visit.visit_count).label('visit_count')
    ).filter(
        func.date(Visit.interval_start) >= start_date,
        func.date(Visit.interval_start) <= end_date
    ).group_by(time_format).order_by(time_format).all()

    data = [
        {
            "time_period": row.time_period.strftime(format_str) if isinstance(row.time_period, datetime) else row.time_period,
            "visit_count": row.visit_count
        }
        for row in results
    ]

    return jsonify(data), 200


@analytics_blueprint.route('/charts/companies_over_time', methods=['POST'])
@jwt_required()
def get_companies_over_time():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body is required"}), 400

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    group_by = data.get('group_by', 'day') 

    if not start_date or not end_date:
        return jsonify({"message": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    if group_by not in ['day', 'month', 'year']:
        return jsonify({"message": "Invalid group_by value. Use 'day', 'month', or 'year'"}), 400

    if group_by == 'day':
        time_format = func.date(Company.created_at) 
        format_str = '%Y-%m-%d'
    elif group_by == 'month':
        time_format = func.date_format(Company.created_at, '%Y-%m')
        format_str = '%Y-%m'
    elif group_by == 'year':
        time_format = func.year(Company.created_at) 
        format_str = '%Y'

    results = db.session.query(
        time_format.label('time_period'),
        func.count(Company.id).label('company_count')
    ).filter(
        func.date(Company.created_at) >= start_date,
        func.date(Company.created_at) <= end_date
    ).group_by(time_format).order_by(time_format).all()

    data = [
        {
            "time_period": row.time_period.strftime(format_str) if isinstance(row.time_period, datetime) else row.time_period,
            "company_count": row.company_count
        }
        for row in results
    ]

    return jsonify(data), 200

@analytics_blueprint.route('/charts/visits_heatmap', methods=['GET'])
@jwt_required()
def get_visits_heatmap():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    results = db.session.query(
        Visit.interval_start.label('interval_start'),
        Visit.interval_end.label('interval_end'),
        func.sum(Visit.visit_count).label('total_visits')
    ).filter(
        Visit.interval_start >= start_date,
        Visit.interval_end <= end_date
    ).group_by(Visit.interval_start, Visit.interval_end).order_by(Visit.interval_start).all()

    data = [
        {
            "interval_start": row.interval_start.strftime('%Y-%m-%d %H:%M:%S'),
            "interval_end": row.interval_end.strftime('%Y-%m-%d %H:%M:%S'),
            "total_visits": row.total_visits
        }
        for row in results
    ]

    return jsonify(data), 200

@analytics_blueprint.route('/get_reviews', methods=['POST'])
@jwt_required()
def get_reviews():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403
    data = request.get_json()
    company_id = data.get('company_id')
    company_branches = Branch.query.filter_by(company_id=company_id).all()
    reviews = Review.query.filter_by(company_id=company_id).all()
    for branch in company_branches:
        reviews.extend(Review.query.filter_by(branch_id=branch.id).all())
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify({"reviews": reviews_list}), 200

@analytics_blueprint.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    if User.query.filter_by(id=user_id).first().role != 1:
        return jsonify({"message": "Admin role required"}), 403
    users = User.query.filter_by(is_hidden=False).all()
    users_list = [user.to_dict() for user in users]
    data = [
        {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "last_login": user["last_login"],
            "state": user["state"],
            "nb_reviews": get_nb_users_reviews(user["id"])
        }
        for user in users_list
    ]

    return jsonify(data), 200

def get_nb_users_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return len(reviews)