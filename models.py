from flask_sqlalchemy import SQLAlchemy
import uuid

from sqlalchemy import ForeignKey, Index

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'
    # supabase_id=db.Column(db.String(130), default=lambda: str(uuid.uuid4()))
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.Integer, ForeignKey('role.id'))              #1 for admin, 2 for user, 3 for company_admin, 4 for branch_admin
    company_id=db.Column(db.String(130), ForeignKey('company.id',ondelete='CASCADE'))
    branch_id = db.Column(db.String(130), ForeignKey('branch.id',ondelete='CASCADE'))
    created_at = db.Column(db.String(120),nullable=False)
    avatar = db.Column(db.String(120),nullable=False)
    last_login=db.Column(db.String(120),nullable=False)
    state = db.Column(db.Integer,nullable=False,default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "role": self.role,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "last_login": self.last_login,
            "state": self.state,
            "is_hidden": self.is_hidden
        }

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.String(130), primary_key=True,default =lambda: str(uuid.uuid4()))
    
    name = db.Column(db.String(32),unique=True,nullable=False)
    email = db.Column(db.String(132),unique=True,nullable=False)
    phone = db.Column(db.String(132),unique=True,nullable=True)
    description = db.Column(db.String(132),unique=True,nullable=False)
    website = db.Column(db.String(132),unique=True,nullable=False)
    business_registration = db.Column(db.String(132),unique=True,nullable=True)
    social_links = db.Column(db.String(132),unique=True,nullable=False)
    logo = db.Column(db.String(120),unique=True,nullable=False)
    category=db.Column(db.Integer,ForeignKey('category.id'))
    address = db.Column(db.String(120),nullable=False)
    created_at = db.Column(db.String(120),nullable=False)
    visits = db.Column(db.Integer, default=0) 
    verified = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)



    def __init__(
        self, name, email, phone=None, description=None, website=None,
        business_registration=None, social_links=None, logo=None,
        category=None, address=None, created_at=None, visits=0,
        verified=0, is_hidden=False
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.description = description
        self.website = website
        self.business_registration = business_registration
        self.social_links = social_links
        self.logo = logo
        self.category = category
        self.address = address
        self.created_at = created_at
        self.visits = visits
        self.verified = verified
        self.is_hidden = is_hidden
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "description": self.description,
            "website": self.website,
            "business_registration": self.business_registration,
            "social_links": self.social_links,
            "logo": self.logo,
            "category": self.category,
            "address": self.address,
            "created_at": self.created_at,
            "visits": self.visits,
            "verified": self.verified,
            "is_hidden": self.is_hidden
        }
class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.String(130), primary_key=True,default =lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(130),ForeignKey('company.id',ondelete='CASCADE'))
    name = db.Column(db.String(120),nullable=False,unique=True)
    email = db.Column(db.String(120),nullable=False)
    phone=db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    visits = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    



    def __init__(self, company_id, name, email, phone, address, visits=0, is_hidden=False):
        self.id = str(uuid.uuid4())
        self.company_id = company_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.visits = visits
        self.is_hidden = is_hidden

    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "visits": self.visits,
            "is_hidden": self.is_hidden,
        }
class Company_register(db.Model):
    __tablename__ = 'company_register'

    id = db.Column(db.String(130), primary_key=True,default =lambda: str(uuid.uuid4()))
    name = db.Column(db.String(32),unique=True,nullable=False)
    email = db.Column(db.String(132),unique=True,nullable=False)
    admin_email = db.Column(db.String(132),unique=True,nullable=False)
    phone = db.Column(db.String(132),unique=True,nullable=True)
    description = db.Column(db.String(132),unique=True,nullable=False)
    website = db.Column(db.String(132),unique=True,nullable=False)
    business_registration = db.Column(db.String(132),unique=True,nullable=True)
    social_links = db.Column(db.String(132),unique=True,nullable=False)
    logo = db.Column(db.String(500),unique=True,nullable=False)
    category=db.Column(db.Integer,ForeignKey('category.id'))
    address = db.Column(db.String(120),nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.String(120),nullable=False)



    def __init__(self, name,email,admin_email,phone,description,business_registration,social_links,website,logo,category,address):
        self.name = name
        self.admin_email=admin_email
        self.email=email
        self.phone=phone
        self.description=description
        self.website=website
        self.business_registration=business_registration
        self.social_links=social_links
        self.logo=logo
        self.category=category
        self.address = address

    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "admin_email": self.admin_email,
            "phone": self.phone,
            "description": self.description,
            "website": self.website,
            "business_registration": self.business_registration,
            "social_links": self.social_links,
            "logo": self.logo,
            "category": self.category,
            "address": self.address,
            "is_hidden": self.is_hidden,
            "created_at": self.created_at
        }

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key = True, autoincrement = 'auto')
    name = db.Column(db.String(120),nullable=False,unique=True)

    def __init__(self, name):
        self.name = name
    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }

class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key = True, autoincrement = 'auto')
    name = db.Column(db.String(120),nullable=False,unique=True)

    def __init__(self, name):
        self.name = name
        
    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }
        
        
        

        
        
        
        
        
        
        
        
        
        
class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(130),ForeignKey('users.id'))
    company_id = db.Column(db.String(130),ForeignKey('company.id',ondelete='CASCADE'))
    branch_id = db.Column(db.String(130),ForeignKey('branch.id',ondelete='CASCADE'))
    title = db.Column(db.String(120))
    description = db.Column(db.String(120))
    rating = db.Column(db.Float, nullable=False)
    product_quality = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    delivery_speed = db.Column(db.Float, nullable=False)
    ease_of_use = db.Column(db.Float, nullable=False)
    customer_service = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String(120),nullable=False)
    tags = db.Column(db.String(120),nullable=False)
    is_anonymous = db.Column(db.Boolean, default = False)
    is_hidden = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "title": self.title,
            "description": self.description,
            "rating": self.rating,
            "product_quality": self.product_quality,
            "price": self.price,
            "delivery_speed": self.delivery_speed,
            "ease_of_use": self.ease_of_use,
            "customer_service": self.customer_service,
            "created_at": self.created_at,
            "tags": self.tags,
            "is_anonymous": self.is_anonymous,
            "is_hidden": self.is_hidden
        }
    
    
    
class Flagged(db.Model):
    __tablename__ = 'flagged'
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id= db.Column(db.String(130),ForeignKey('review.id',ondelete='CASCADE'))
    description= db.Column(db.String(120))
    user_id= db.Column(db.String(130),ForeignKey('users.id'))
    flagged_at = db.Column(db.String(120),nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            'user_id': self.user_id,
            'description': self.description,
            'flagged_at': self.flagged_at
        }
    

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id= db.Column(db.String(130),ForeignKey('review.id'))
    description= db.Column(db.String(120))
    user_id= db.Column(db.String(130),ForeignKey('users.id'))
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.String(120),nullable=False)
    
    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "review_id": self.review_id,
            "description": self.description,
            "user_id": self.user_id,
            "is_hidden": self.is_hidden,
            "created_at": self.created_at
        }

class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id= db.Column(db.String(130),ForeignKey('review.id',ondelete='CASCADE'))
    user_id= db.Column(db.String(130),ForeignKey('users.id',ondelete='CASCADE'))
    
    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "review_id": self.review_id,
            "user_id": self.user_id
        }
class Guest(db.Model):
    __tablename__ = 'guest'
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))

    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id
        }
        
        
class Company_Users_visits(db.Model):
    __tablename__ = 'company_users'
    id = db.Column(db.String(130), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(130),ForeignKey('company.id',ondelete='CASCADE'))
    user_id = db.Column(db.String(130),ForeignKey('users.id',ondelete='CASCADE'))
    guest_id = db.Column(db.String(130),ForeignKey('guest.id',ondelete='CASCADE'))

    
    def to_dict(self):
        """Converts the model's attributes to a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "user_id": self.user_id,
            "guest_id": self.guest_id
        }