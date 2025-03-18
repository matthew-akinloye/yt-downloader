# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ewrfsder43344rf')  # Fallback to a default value
    
    # Debug Mode
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Convert to boolean
    
    # Database Configuration (Pooled Connection - Recommended for most uses)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://default:XHEYSl5Cax7e@ep-aged-meadow-a42wsudx-pooler.us-east-1.aws.neon.tech/verceldb?sslmode=require')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False