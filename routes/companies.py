from datetime import datetime
from math import floor
from flask_bcrypt import Bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from config import supabase
from models import Branch, Company, Company_Users_visits, Company_register, Guest, Likes, Response, Review, User
from models import Company, db
import secrets
import string
import models







bcrypt = Bcrypt()
companies_blueprint = Blueprint('/companies', __name__)

@companies_blueprint.route('/verify', methods=['POST'])
@jwt_required()
def verify():
    account_id=get_jwt_identity()
    data=request.get_json()
    company_id=data.get('company_id')
    user=User.query.filter_by(id=account_id,role=1,is_hidden=False).first()
    company = Company.query.filter_by(id=company_id,is_hidden=False).first()
    if not user:
        return jsonify({"msg": "Aunothorized user"}), 404
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    company.verified=1
    db.session.commit()

    return jsonify({
        "msg": "verified company",
        "company_id": company.id,
        "verified": company.verified
    }), 200
    
    
    
    
    
@companies_blueprint.route('/unverify', methods=['POST'])
@jwt_required()
def uverify():
    account_id=get_jwt_identity()
    data=request.get_json()
    company_id=data.get('company_id')
    user=User.query.filter_by(id=account_id,role=1,is_hidden=False).first()
    company = Company.query.filter_by(id=company_id,is_hidden=False).first()
    if not user:
        return jsonify({"msg": "Aunothorized user"}), 404
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    company.verified=0
    db.session.commit()

    return jsonify({
        "msg": "unverified successfully",
        "company_id": company.id,
        "verified": company.verified
    }), 200















@companies_blueprint.route('/company_register/register', methods=['POST'])
@jwt_required()
def company_register():
    data = request.get_json()
    if not data:
         return jsonify({"msg": "no data"}), 401
    name = data.get('name')
    logo = data.get('logo')
    category = data.get('category')
    address = data.get('address')
    email = data.get('email')
    admin_email = data.get('admin_email')
    website = data.get('website')
    description = data.get('description')
    phone = data.get('phone')
    business_registration = data.get('business_registration')
    social_links = data.get('social_links')


    if not name or not category:
        return jsonify({"msg": "Missing name or category"}), 401

 
    if Company.query.filter_by(name=name,is_hidden=False).first() :
        return jsonify({"msg": "Name already exists"}), 401
    if Company.query.filter_by(email=email,is_hidden=False).first() :
        return jsonify({"msg": "Email already exists"}), 401
    if Company.query.filter_by(website=website,is_hidden=False).first() :
        return jsonify({"msg": "Website already exists"}), 401
    if Company.query.filter_by(social_links=social_links,is_hidden=False).first() :
        return jsonify({"msg": "Social Links already exists"}), 401

    company2 = Company_register(
        name,email,admin_email,phone,description,business_registration,social_links,website,logo,category,address
    )
    db.session.add(company2)
    db.session.commit()


    return jsonify({
        "company_id": company2.id,
    }), 201

@companies_blueprint.route('/get_company_register', methods=['GET'])
@jwt_required()
def get_company_register():
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,role=1,is_hidden=False).first()
    if user:
        companies = Company_register.query.all()
    
        companies_list = [company.to_dict() for company in companies]

        return jsonify({
        "companies": companies_list,
    }), 201
    else:
                return jsonify({
        "msg": "unauthorized",
    }), 401
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

@companies_blueprint.route('/company_register/validate', methods=['POST'])
@jwt_required()
def company_register_validate():
    data = request.get_json()
    validated = data.get("validated")
    company_id = data.get("company_id")
    account_id=get_jwt_identity()
    user=User.query.filter_by(id=account_id,role=1,is_hidden=False).first()
    company = Company_register.query.filter_by(id = company_id,is_hidden=False).first()
    if user and company:
        if User.query.filter_by(email=company.admin_email,is_hidden=False).first():
            return jsonify({"msg": "Admin email already exists"}), 400
        if validated:
            company1=Company(name= company.name,email= company.email,phone= company.phone,website=company.website,description= company.description,social_links= company.social_links,business_registration= company.business_registration, logo=company.logo,avatar=company.avatar, category=company.category, address= company.address, created_at=datetime.now(),verified=0)
            db.session.add(company1)
            db.session.commit()
            company2 = Company.query.filter_by(name = company.name).first()
            admin_password = generate_password()
            db.session.add(User(email=company.admin_email, password=bcrypt.generate_password_hash(admin_password).decode('utf-8'), name = f"company.name admin", role = 3, company_id = company2.id,created_at=datetime.now(),last_login = datetime.now(),avatar=company.avatar,state=0) )
        company.is_hidden=True
        db.session.commit()
    
        if validated:
            return jsonify ({"msg": "company validated and admin account created", 
                             "company": {
                                 "id": company2.id,
                                 "account email": company.admin_email,
                                 "account_password": admin_password
                             }
                             }), 201
        else :
            return jsonify ({"msg": "Company registration rejected"}), 200
    else :
        if not company:
            return jsonify ({"msg": "Company not found"}), 402
        else:
            return jsonify ({"msg": "Not authorized"}), 402
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@companies_blueprint.route('/company/add_branch', methods=['POST'])
@jwt_required()
def add_branch():
    account_id=get_jwt_identity()

    user=User.query.filter_by(id=account_id,role=3,is_hidden=False,state=0).first()
    if user:
        data = request.get_json()
        name = data.get('name')
        account_email=data.get('account_email')
        category = data.get('category')
        address = data.get('address')
        email = data.get('email')
        phone = data.get('phone')
        company_id = user.company_id



        if not name or not category:
            return jsonify({"msg": "Missing name or category"}), 400
        company = Company.query.filter_by(id=company_id,is_hidden=False).first()
        if not company :
            return jsonify({"msg": "No company exists"}), 400
        branch = Branch.query.filter_by(name=name,is_hidden=False).first()

        if branch :
            return jsonify({"msg": "Name already exists"}), 400

        if User.query.filter_by(email=account_email,is_hidden=False).first():
            return jsonify({"msg": "Branch Admin email already exists"}), 400
            
        admin_password = generate_password()
        
        branch = Branch(
        name,company_id,email,email,address,phone)
        db.session.add(User(email=account_email, password=bcrypt.generate_password_hash(admin_password).decode('utf-8'), name = f"company.name admin", role = 4,company_id=company.id, branch_id = branch.id,created_at=datetime.now(),avatar=company.avatar,last_login = datetime.now(),state=0) )

        db.session.add(branch)
        db.session.commit()
        return jsonify({
        "msg": "Branch added successfully.",
        "branch_id": branch.id,
        "account_password":admin_password
    }), 201
    else:
        return jsonify({
        "msg": "unothorized user.",

    }), 301
        
        
    # name = data.get('name')
    # email = data.get('email')
    # phone = data.get('phone')
    # address = data.get('address')

    # if not name or not email or not phone or not address:
    #     return jsonify({"msg": "Missing required branch details."}), 400

    # company = Company.query.filter_by(id=company_id).first()
    # if not company:
    #     return jsonify({"msg": "Company not found."}), 404

    # if Branch.query.filter_by(name=name).first():
    #     return jsonify({"msg": "Branch name already exists."}), 400

    # branch = Branch(
    #     id=str(uuid.uuid4()),
    #     company=company_id,
    #     name=name,
    #     email=email,
    #     phone=phone,
    #     address=address
    # )

    # db.session.add(branch)
    # db.session.commit()

    # return jsonify({
    #     "msg": "Branch added successfully.",
    #     "branch_id": branch.id
    # }), 201































































@companies_blueprint.route('/edit_company/edit', methods=['POST'])
@jwt_required()
def edit_company():

            
        data = request.form.to_dict()
        account_id=get_jwt_identity()
        company_id=data.get('company_id')
        company=Company.query.filter_by(id=company_id,is_hidden=False).first()
        user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
        if user:
            if (user.role==3 or user.role==1) and company and company.id==user.company_id:
                if data.get('name'):
                    company.name= data.get('name')
                if data.get('description'):
                    company.description= data.get('description')
                if data.get('website'):
                    company.website= data.get('website')
                if data.get('social_links'):
                    company.social_links= data.get('social_links')
                if data.get('address'):
                    company.address= data.get('address')
                if data.get('email'):
                    company.email= data.get('email')
                if data.get('phone'):
                    company.phone= data.get('phone')
                if 'image'  in request.files:
                    file = request.files['image']
            
                    if file.filename == '':
                        return jsonify({"error": "No file selected"}), 400
                    file_name = f"images/{file.filename}"
                    files = supabase.storage.from_("Users").list(file_name)
                    if len(files) > 0:
                        public_url = supabase.storage.from_("Users").get_public_url(file_name)
                        company.logo = public_url
                        db.session.commit()
                        
                        return jsonify({
        "msg": 'company modified successfully',
"company": {
                            "id": company.id,
                            "name": company.name,
                            "email": company.email,
                            "phone": company.phone,
                            "logo": response
                        }
    }), 201 
                    image_data = file.read()
                    # Specify the file name you want to use in Supabase Storage
                    
                    # Upload the image to Supabase Storage
                    try:
                        response = supabase.storage.from_("company").upload(file_name, image_data)
                        public_url = supabase.storage.from_("company").get_public_url(file_name)
                        company.logo=public_url
                    except Exception as e:
                        return jsonify({
            "msg": str(e)}), 500
                db.session.commit()
                company=Company.query.filter_by(id=company_id,is_hidden=False).first()
                return jsonify({
                    "msg": 'company modified successfully',
                    "company": {
                        "id": company.id,
                        "name": company.name,
                        "email": company.email,
                        "phone": company.phone,
                        "logo": response
                    }
                }),
            else:
                if not company:
                    return jsonify({
            "msg":'Company doesn"t exist',

        }), 404   
                else: 
                    if not user:
                        return jsonify({
            "msg":'user doesn"t exist',

        }), 404 
                    else:
                    
                        return jsonify({
            "msg":'unothorised user',

        }), 404
        else:
                    
                        return jsonify({
            "msg":'no user',

        }), 404






@companies_blueprint.route('/edit_branch/edit', methods=['POST'])
@jwt_required()
def edit_branch():
    data = request.get_json()
    account_id=get_jwt_identity()
    branch_id=data.get('branch_id')
    branch=Branch.query.filter_by(id=branch_id,is_hidden=False).first()
    user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
    if not user:
                        return jsonify({
        "msg":"user doesn't exist",

    }), 404
    if (((user.role==3 and branch.company_id==user.company_id) or (user.role==4 and user.branch_id==branch_id)) or user.role==1) and branch:
        if data.get('name'):
            branch.name= data.get('name')
        if data.get('address'):
            branch.address= data.get('address')
        if data.get('email'):
            branch.email= data.get('email')
        if data.get('phone'):
            branch.phone= data.get('phone')

        db.session.commit()
        return jsonify({
        "msg": 'branch modified successfully',
    }), 201
    else:
        if not branch:
             return jsonify({
        "msg":'Company does not exist',

    }), 404   
        else: 
            if not user:
                 return jsonify({
        "msg":'user does not exist',

    }), 404 
            else:
                
                return jsonify({
        "msg":'unauthorised user',

    }), 404








@companies_blueprint.route('/get_branches', methods=['GET'])
def get_branches():
    # data = request.args.get()
    branches=Branch.query.filter_by(is_hidden=False)
    branches_list = [branch.to_dict() for branch in branches]

    return jsonify({
        "branches": branches_list,
    }), 201











@companies_blueprint.route('/get_branch', methods=['GET'])
@jwt_required()
def get_branch():

    account_id=get_jwt_identity()
    # account_id=request.args.get("account_id")
    branch_id=request.args.get('branch_id')
    user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
    guest = Guest.query.filter_by(id=account_id).first()
    company=Company.query.filter_by(id=branch.company_id,is_hidden=False).first()
    branch=Branch.query.filter_by(id=branch_id,is_hidden=False).first()
    user_id = user.id if user else None
    guest_id = guest.id if guest else None
    if branch:
        if user or guest:
            if user.role==2 or (user.company_id!= branch.company_id and user.role!=1) or guest:
                branch.visits+=1
                if not check_combination_exists(company.id, user_id, guest_id):
                    visit = Company_Users_visits(company_id=company.id,user_id=user_id,guest_id=guest_id)
                    db.session.add(visit)
                db.session.commit()
            elif user.state==1:
                return jsonify({"msg":"Banned user"})
        
        company=Company.query.filter_by(id=branch.company_id,is_hidden=False).first()
        logo=company.logo
        
        website=company.social_links
        category=company.category
        verified=company.verified
        ratings=get_branch_rating(branch)
        number_of_reviews,number_of_responses=get_branch_response_ratio(branch)
        avg_response_time=avg_branch_response_time(branch)
        return jsonify({
            'name':branch.name,
            'email':branch.email,
            'phone':branch.phone,
            'address':branch.address,
            'visits':branch.visits,
            'logo':logo,
            'website':website,
            'category':category,
            'verified':verified,
            'rating':ratings[0],
            'product_quality':ratings[1],
            'price':ratings[2],
            'delivery_speed':ratings[3],
            'ease_of_use':ratings[4],
            'customer_service':ratings[5],
            'repartition':ratings[6],
            'number_of_reviews':number_of_reviews,
            'number_of_responses':number_of_responses,
            'reviews_responses':get_branch_reviews(branch),
            'repartition':get_branch_rating(branch)[1],
            'avg_response_time':avg_response_time,
            
        }),201
    else:
        return jsonify({"msg":"no branch found"})
        
    
    
    
    
    
    
    

    
@companies_blueprint.route('/get_company', methods=['GET'])
@jwt_required()
def get_company():
    # account_id=request.args.get("account_id")
    account_id=get_jwt_identity()
    company_id=request.args.get("company_id")
    user=User.query.filter_by(id=account_id,is_hidden=False).first()
    guest = Guest.query.filter_by(id=account_id).first()
    company=Company.query.filter_by(id=company_id,is_hidden=False).first()
    user_id = user.id if user else None
    guest_id = guest.id if guest else None
    if company:
        if user or guest:
            if user.role==2 or (user.company_id!= company.id and user.role!=1) or guest:
                company.visits+=1
                if not check_combination_exists(company.id, user_id, guest_id):
                    visit = Company_Users_visits(company_id=company.id,user_id=user_id,guest_id=guest_id)
                    db.session.add(visit)
                db.session.commit()

        rating=get_company_rating(company)
        number_of_reviews,number_of_responses=get_company_response_ratio(company)
        avg_response_time=avg_company_response_time(company)
        return jsonify({
            'name':company.name,
            'email':company.email,
            'description': company.description,
            'phone':company.phone,
            'address':company.address,
            'visits':company.visits,
            'logo':company.logo,
            'website':company.website,
            'category':company.category,
            'verified':company.verified,
            'rating':rating,
            'number_of_reviews':number_of_reviews,
            'number_of_responses':number_of_responses,
            'avg_response_time':avg_response_time,
            'social_links':company.social_links,
        }),200

    else:
        return jsonify({"msg":"no company found"})
    
    
    
@companies_blueprint.route('/get_company_reviews', methods=['GET'])
@jwt_required()
def get_company_reviews():
    company_id=request.args.get("company_id")
    company=Company.query.filter_by(id=company_id,is_hidden=False).first()
    if company:
        return jsonify({'reviews':get_company_reviews(company),
        }),200
    else:
        return jsonify({"msg":"no company found"}), 404
    
    
    
    
    
    
    
@companies_blueprint.route('/get_companies', methods=['GET'])
def get_companies():
    companies=Company.query.filter_by(is_hidden=False).all()
    if companies:
    
        companies_list=[company.to_dict() for company in companies]
        for company in companies_list:
            company['rating']=get_branches(company)[1]


        return jsonify({
            'companies':companies_list,        
        }),201
        
        
        
@companies_blueprint.route('/get_company_branches', methods=['GET'])
def get_company_branches():
    company_id=request.args.get("company_id")
    company=Company.query.filter_by(id=company_id,is_hidden=False).first()
    if not company:
        return jsonify({'message':'company not found'}),404
    
    branches=get_branches(company)
    
    return jsonify({'branches':branches}),200
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@companies_blueprint.route('/company/delete_company', methods=['POST'])
@jwt_required()
def delete_company():
    account_id=get_jwt_identity()

    user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
    if user and (user.role==3 or user.role==1):
        data = request.get_json()
        company_id = data.get('company_id')
        company=Company.query.filter_by(id=company_id,is_hidden=False).first()
        if company:
            company.is_hidden=True
            db.session.commit()
            return jsonify({'message':'branch deleted'}),200
        else:
            return jsonify({'message':'branch not found'}),404
    else:
        return jsonify({'message':'user not found'}),404  
    
    
    
    
    
    
    
    
    
@companies_blueprint.route('/company/delete_branch', methods=['POST'])
@jwt_required()
def delete_branch():
    account_id=get_jwt_identity()

    user=User.query.filter_by(id=account_id,is_hidden=False,state=0).first()
    if user and (user.role==3 or user.role==1):
        data = request.get_json()
        branch_id = data.get('branch_id')
        branch=Branch.query.filter_by(id=branch_id,is_hidden=False).first()
        if branch:
            branch.is_hidden=True
            db.session.commit()
            return jsonify({'message':'branch deleted'}),200
        else:
            return jsonify({'message':'branch not found'}),404
    else:
        return jsonify({'message':'user not found'}),404
    
    
    
@companies_blueprint.route('/company/get_companies_by_category', methods=['GET'])
# @jwt_required()
def get_companies_by_category():
    # account_id=get_jwt_identity()

        category_id = request.args.get('category_id')
        companies=Company.query.filter_by(category_id=category_id,is_hidden=False).all()
        companies=[company.to_dict() for company in companies]
        return jsonify({'companies':companies}),200

    
    
    
@companies_blueprint.route('/company/search_companies', methods=['GET'])
# @jwt_required()
def search_companies():
    search_name=request.args.get('search_name')
    if not search_name:
        return jsonify({'message':'no search name'}),400
    search_name=search_name.strip()
    companies=Company.query.filter(Company.name.like('%'+search_name+'%')).all()
    company_list=[]
    for company in companies:
        if company.is_hidden:
            continue
        company_list.append(company.to_dict())

    return jsonify({'companies':[company.to_dict() for company in companies]}),200
    
    

@companies_blueprint.route('/company/get_suggestions',methods=['POST'])
def get_suggestions():
    company_id = request.get_json().get('company_id')
    suggestions = get_company_suggestions(company_id)
    companies = Company.query.filter(Company.id.in_(suggestions)).all()
    companies = [{'id':company.id,'name':company.name, 'logo':company.logo, 'rating':company.rating} for company in companies]
    return jsonify({'companies':companies}),200


def get_company_suggestions(company_id):
    company_visits = Company_Users_visits.query.filter_by(company_id=company_id).all()
    suggestions = {}
    for visit in company_visits:
        if visit.guest_id:
            if visit.company_id not in suggestions:
                suggestions[company_id] = 1
            else :
                suggestions[company_id] += 1
        elif visit.user_id:
            if visit.company_id not in suggestions:
                suggestions[company_id] = 1
            else :
                suggestions[company_id] += 1
    sorted_suggestions = sorted(suggestions.items(), key=lambda item: item[1], reverse=True)

    return sorted_suggestions[:3]
    
    
    
    
    
    
    
    
    
    
    
    
    
def generate_password(length=12):
    """Generates a secure random password with at least one uppercase, lowercase, digit, and special character."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    # Define character pools
    uppercase = string.ascii_uppercase  # A-Z
    lowercase = string.ascii_lowercase  # a-z
    digits = string.digits              # 0-9
    special_chars = "!@#$%^&*()-_=+"

    # Ensure the password contains at least one of each required type
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(special_chars),
    ]

    # Fill the rest of the password length with a mix of all character types
    all_chars = uppercase + lowercase + digits + special_chars
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    # Shuffle the password to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    return ''.join(password)





def get_branches(company):
    if isinstance(company, dict):
        branches=Branch.query.filter_by(company_id=company['id'],is_hidden=False)
    else:
        branches=Branch.query.filter_by(company_id=company.id,is_hidden=False)

    branches_list=[branch.to_dict() for branch in branches]
    rate=0
    count=0
    for branch in branches_list:
        rating =get_branch_rating(branch)
        count+=1
        rate+=rating[0]
        branch['rating']=rating[0]
    if count>0:
        rate/=count
    return branches_list,rate

def get_company_rating(company):
    reviews=Review.query.filter_by(company_id=company.id, is_hidden = False).all()
    rate=0
    count=0
    for review in reviews:
        rate+=review.rate
        count+=1
    if count>0:
        rate/=count
    return rate
    
    
    
    
def get_branch_reviews(branch):
    reviews=Review.query.filter_by(branch_id=branch.id, is_hidden = False).all()
    reviews_list=[review.to_dict() for review in reviews]
    for review in reviews_list:
        review['responses']=get_review_responses(review)
        review["likes"], review["user_liked"] = get_review_likes(review) 
        review["user_name"], review["user_avatar"] = get_review_user_information(review)
        review['status']=[]
        if review["is_anonymous"]:
            review['user_name']='Anonymous'
            review['user_avatar']=None
        if len(review['responses'])>0:
            review['status'].append('Company replied')
    return reviews_list


def get_company_reviews(company):
    reviews=Review.query.filter_by(company_id=company.id, is_hidden = False).all()
    reviews_list=[review.to_dict() for review in reviews]
    for review in reviews_list:
        review['responses']=get_review_responses(review)
        review["likes"], review["user_liked"] = get_review_likes(review) 
        review["user_name"], review["user_avatar"] = get_review_user_information(review)
        review['status']=[]
        if review["is_anonymous"]:
            review['user_name']='Anonymous'
            review['user_avatar']=None
        if len(review['responses'])>0:
            review['status'].append('Company replied')
    return reviews_list

def get_review_user_information(review):
    user = User.query.filter_by(id=review["user_id"]).first()
    return user.name, user.avatar


def get_review_likes(review):
    likes_count = Likes.query.filter_by(review_id=review["id"]).count()
    user_liked = Likes.query.filter_by(review_id=review["id"], user_id=get_jwt_identity()).first()
    return likes_count, True if user_liked else False

def get_review_responses(review):
    if isinstance(review,dict):
        
        responses=models.Response.query.filter_by(review_id=review['id'],is_hidden=False).all()
    else:
        responses=models.Response.query.filter_by(review_id=review["id"],is_hidden=False).all()

    # responses_list=[response.to_dict() for response in responses]
    return responses
    
    
def get_branch_rating(branch):
    if isinstance(branch,dict):
        
        reviews=Review.query.filter_by(branch_id=branch['id'], is_hidden=False).all()
    else:
        reviews=Review.query.filter_by(branch_id=branch.id, is_hidden= False).all()
    repartition=[0,0,0,0,0,0]
    product_quality=0
    price=0
    delivery_speed=0
    ease_of_use=0
    customer_service=0
    rating=0
    count=0
    for review in reviews:
        
        count+=1
        if  not review.rating:
           continue 
        print( review.rating)
        product_quality+=review.product_quality
        price+=review.price
        delivery_speed+=review.delivery_speed
        ease_of_use+=review.ease_of_use
        customer_service+=review.customer_service
        rating+=review.rating
        repartition[floor(review.rating)]+=1
    
    
    if count>0:
        rating=rating/count
        for i in range(len(repartition)):
            repartition[i]/=count 
    
    return [rating,product_quality,price,delivery_speed,ease_of_use,customer_service,repartition]












def get_company_response_ratio(company):
        reviews =Review.query.filter_by(company_id=company.id,is_hidden=False).all()
        number_of_reviews=len(reviews)
        number_of_responses=0
        for review in reviews:
            response=Response.query.filter_by(review_id=review.id).count()
            number_of_responses+=response
        
        return number_of_reviews,number_of_responses
        


def get_branch_response_ratio(branch):
        branch_id = branch.id
        branch=Company.query.filter_by(id=branch_id).first()
        if not branch:
            return jsonify({'message':'company not found'}),404
        reviews =Review.query.filter_by(company_id=branch_id).all()
        number_of_reviews=len(reviews)
        number_of_responses=0
        for review in reviews:
            response=Response.query.filter_by(review_id=review.id).count()
            number_of_responses+=response
        
        return number_of_reviews,number_of_responses
        


def avg_company_response_time(company):
        review_response=[]
        reviews =Review.query.filter_by(company_id=company.id).all()
        for review in reviews:
            response=Response.query.filter_by(review_id=review.id).first()
            if response:
                review_response.append([review.created_at,response.created_at])
        avg_response_time=0
        if not len(review_response):
            return 0
        for i in range(len(review_response)):
            #convert string to datetime
            
            review_date=datetime.strptime(review_response[i][0], "%Y-%m-%d %H:%M:%S.%f")
            response_date=datetime.strptime(review_response[i][1], "%Y-%m-%d %H:%M:%S.%f")
            avg_response_time+=((response_date-review_date).total_seconds()/3600)
        avg_response_time/=len(review_response)
        return avg_response_time
        
        
        
def avg_branch_response_time(branch):
        review_response=[]
        reviews =Review.query.filter_by(company_id=branch.id).all()
        for review in reviews:
            response=Response.query.filter_by(review_id=review.id).first()
            if response:
                review_response.append([review.created_at,response.created_at])
        avg_response_time=0
        for i in range(len(review_response)):
            
            review_date=datetime.strptime(review_response[i][0], "%Y-%m-%d %H:%M:%S.%f")
            response_date=datetime.strptime(review_response[i][1], "%Y-%m-%d %H:%M:%S.%f")
            avg_response_time+=((response_date-review_date).total_seconds()/3600)
        avg_response_time/=len(review_response)
        return avg_response_time

def check_combination_exists(company_id, user_id, guest_id):
    exists = db.session.query(
        db.session.query(Company_Users_visits)
        .filter_by(company_id=company_id, user_id=user_id, guest_id=guest_id)
        .exists()
    ).scalar()
    return exists


# def get_company_suggestions(company_id):
#     company_visits = Company_Users_visits.query.filter_by(company_id=company_id).all()
#     suggestions = {}
#     for visit in company_visits:
#         if visit.guest_id:
#             if visit.company_id not in suggestions:
