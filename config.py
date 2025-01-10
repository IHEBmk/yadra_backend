
import os

from supabase import Client, create_client
url = "https://llywvssiygqpkshmhrts.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxseXd2c3NpeWdxcGtzaG1ocnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0MzYwNTgsImV4cCI6MjA1MjAxMjA1OH0.A5Eid8ku2YhGQGG4IfBjhF-RZ3JMX1SuHFXhp6FU3fY"
supabase: Client = create_client(url, key)
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://avnadmin:AVNS_YTTEqwkucVTUn0CXMz5@mysql-fb3fc04-yadra.k.aivencloud.com:10371/yadra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')